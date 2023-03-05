import pyspark
from pyspark.sql import SparkSession
class sparkread:
    def __init__(self,operation):
        self.operation="azuredlaccess"
    def loaduri(self,url,username,assetname):
        import requests, json
        if self.operation=="azuredlaccess":
            data = {
                    "UserName": username,
                    "AssetName": assetname
                    }

            response = requests.post(url, params=data)
            data = response.json()
            data = json.loads(data)
            account_name,adls_uri,sas_token=data['account_name'],data['adls_uri'],data['sas_token']
            spark.conf.set("fs.azure.account.auth.type."+account_name+".dfs.core.windows.net", "SAS")
            spark.conf.set("fs.azure.sas.token.provider.type."+account_name+".dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.sas.FixedSASTokenProvider")
            spark.conf.set("fs.azure.sas.fixed.token."+account_name+".dfs.core.windows.net", sas_token)
            df = spark.read.format('delta').load(adls_uri)
            return df