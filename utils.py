from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.storage.filedatalake import DataLakeServiceClient
from datetime import datetime, timedelta

import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import generate_file_system_sas, generate_directory_sas
from azure.storage.blob import BlobServiceClient, UserDelegationKey



load_dotenv()


class authorize:

    def __init__(self,tenant_id,client_id,client_secret,subscription_id):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.subscription_id = subscription_id

    def isServicePrincipalValid(self):
        credentials = ClientSecretCredential(
                        tenant_id=self.tenant_id,
                        client_id=self.client_id,
                        client_secret=self.client_secret
                    )
        resource_client = ResourceManagementClient(
                        credential=credentials,
                        subscription_id=self.subscription_id
                    )
        try:
            resource_client.providers.get('Microsoft.Compute')
            #print("Service principal is valid")
            return True
        except:
            #print("Service principal is not valid")
            return False  

class datalakedirectory_sas:
    def __init__(self,adlsuri,tenant_id,client_id,client_secret,storagekey,subscription_id,permission):
        self.adlsuri=adlsuri
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.storagekey = storagekey
        self.subscription_id = subscription_id
        self.permission = permission

    def generate_datalake_credentials(self):
        ath = authorize(self.tenant_id,self.client_id,self.client_secret,self.subscription_id)
        if ath.isServicePrincipalValid():
            credentials = ClientSecretCredential(
                                tenant_id=self.tenant_id,
                                client_id=self.client_id,
                                client_secret=self.client_secret
                            )
            return credentials

    def adls_uri_exists(self)->bool:
        account_url, file_path = self.adlsuri.split('/', 3)[-2:]
        container,filepath = file_path.split('/',1)[-2:]
        account_name= account_url.split('.',1)[0]

        service_client = DataLakeServiceClient(account_url=f"https://{account_name}.dfs.core.windows.net", credential=self.generate_datalake_credentials())
        # Check if the path exists
        path_exists = False
        try:
            if service_client.get_file_system_client(container).get_directory_client(filepath)._get_path_properties:
                path_exists = True
                return path_exists
        except:
            return path_exists
    
    def genrate_datalakedirectory_sas(self):
        if self.adls_uri_exists():
            account_url, file_path = self.adlsuri.split('/', 3)[-2:]
            file_system,path = file_path.split('/',1)[-2:]
            account_name= account_url.split('.',1)[0]
            
            if self.permission=="read":
                permissions = "rle"
            elif self.permission=="write":
                permissions="racwdlmeop"

            start = datetime.utcnow() - timedelta(minutes=15)
            expiry=datetime.utcnow() + timedelta(minutes=10)

            ACCOUNT_KEY = self.storagekey
            credentials = self.generate_datalake_credentials()

            blob_service_client = BlobServiceClient(
                account_url=f"https://{account_name}.blob.core.windows.net",
                credential=credentials
            )

            user_delegation_key = blob_service_client.get_user_delegation_key(
                key_start_time=start,
                key_expiry_time=expiry
            )

            sas_token = generate_directory_sas(
                account_name=account_name,
                file_system_name=file_system,
                directory_name=path,
                permission=permissions,
                start=start,
                expiry=expiry,
                credential=ACCOUNT_KEY,#user_delegation_key,
                recursive=True
            )

            DataLake_Service_Client = DataLakeServiceClient(account_url=f"https://{account_name}.dfs.core.windows.net", credential=credentials)
            file_system_client = DataLake_Service_Client.get_file_system_client(file_system)
            directory_client = file_system_client.get_directory_client(path)

            print(f"{directory_client.url}?{sas_token}")

            return(account_name,"abfss://"+file_system+"@"+account_name+".dfs.core.windows.net/"+path,sas_token)


   

 
