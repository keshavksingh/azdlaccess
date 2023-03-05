# Import Uvicorn & the necessary modules from FastAPI
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
# Import other necessary packages
from dotenv import load_dotenv
import os,json
from grant_utils import grantauthorization,searchasset
from utils import authorize,datalakedirectory_sas

# Load the environment variables from the .env file into the application
load_dotenv() 

# Initialize the FastAPI application
app = FastAPI()
@app.post("/requestaccess")
async def requestaccess(UserName: str, AssetName: str, ADLSPath: str, Permission: str):
    ga = grantauthorization(UserName,AssetName,ADLSPath,Permission).grantpermission()
    return ("Access Successfully Granted!")

@app.post("/getJITaccess")
async def getjitaccess(UserName: str,AssetName:str):
    ADLS_URI,Permission = searchasset(UserName,AssetName).searchassetinfile()
    adlsuri = ADLS_URI
    platform_subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID')
    platform_tenant_id = os.environ.get('AZURE_TENANT_ID')
    platform_client_id = os.environ.get('AZURE_CLIENT_ID')
    platform_client_secret = os.environ.get('AZURE_CLIENT_SECRET')
    storagekey = os.environ.get('ACCOUNT_KEY')
    dlobj = datalakedirectory_sas(adlsuri,platform_tenant_id,platform_client_id,platform_client_secret,storagekey,platform_subscription_id,Permission)
    account_name,adls_uri,sas_token = dlobj.genrate_datalakedirectory_sas()
    data={
        "account_name":account_name,
        "adls_uri":adls_uri,
        "sas_token":sas_token
    }
    json_data  = json.dumps(data)
    return(json_data)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)