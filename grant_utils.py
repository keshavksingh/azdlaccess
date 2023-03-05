import json
import os
# define a dictionary to store: 
# 1.) SPN (UserName)
# 2.) "Assetname" (Unique ADLS Path with AKA Name)
# 3.) its respective "ADLS Gen2 Path"
# 4.) Permission to the Path "Read/Write"
#data = {"spn1": [{"assetname":["ADLS2","read"]},{"assetname2":["ADLS3","write"]}]}
"""
UserName= "SPN1"
AssetName= "sales_raw"
ADLSPath="https://cseoedlppeadlsg2wus201.blob.core.windows.net/cseo/dev/users/kesin/stream/sales_raw"
Permission="write"
"""

class grantauthorization:
    def __init__(self,UserName,AssetName,ADLSPath,Permission):
        self.UserName = UserName
        self.AssetName = AssetName
        self.ADLSPath = ADLSPath
        self.Permission = Permission
        
    def grantpermission(self):

        data = {self.UserName:[{self.AssetName:[self.ADLSPath,self.Permission]}]}
        filename = "auth_data.json"

        # check if the file already exists
        fd=0
        if os.path.isfile(filename):
            with open(filename, "r") as f:
                existing_data = json.load(f)
                for U,V in existing_data.items():
                    if self.UserName==U:
                        for Assets in V:
                            for Asset,AssetVal in Assets.items():
                                if self.AssetName==Asset:
                                    Assets[Asset]=[self.ADLSPath,self.Permission]
                                    fd=1
                        if fd==0:
                            existing_data[U].append({self.AssetName:[self.ADLSPath,self.Permission]})
                            fd=2
                if fd==0:
                    existing_data[self.UserName]=[{self.AssetName:[self.ADLSPath,self.Permission]}]
        else:
            existing_data = data

        # write the updated data to the file
        with open(filename, "w") as f:
            json.dump(existing_data, f)
        return
class searchasset:
    def __init__(self,UserName,AssetName):
        self.UserName = UserName
        self.Assetname = AssetName

    def searchassetinfile(self):
        filename = "auth_data.json"
        if os.path.isfile(filename):
            with open(filename, "r") as f:
                existing_data = json.load(f)
                for U,V in existing_data.items():
                    if self.UserName==U:
                        for Assets in V:
                            for Asset,AssetVal in Assets.items():
                                if self.Assetname==Asset:
                                    print("Asset Found!")
                                    ADLS_URI,Permission=Assets[Asset][0],Assets[Asset][1]
                                    return ADLS_URI,Permission

