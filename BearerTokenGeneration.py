import requests,os 
from dotenv import load_dotenv
load_dotenv() 

tenant_id = os.environ.get('AZURE_TENANT_ID')
client_id = os.environ.get('AZURE_CLIENT_ID')
client_secret = os.environ.get('AZURE_CLIENT_SECRET')
resource = 'https://graph.microsoft.com'

# request an access token from Azure AD
auth_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/token'
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'resource': resource
}
response = requests.post(auth_url, data=data)

# parse the response and extract the access token
access_token = response.json()['access_token']
print(access_token)

# use the access token to make API requests
headers = {'Authorization': f'Bearer {access_token}'}
api_url = 'https://graph.microsoft.com/v1.0/me'
response = requests.get(api_url, headers=headers)
