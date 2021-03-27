from django.test import TestCase

from google.cloud import storage
import sys
import pymysql
import os
import datetime


year = yearlst[0]
monthlst=["Mar","Apr","May"]
month = monthlst[0]
daylst = datetime.datetime.today().day
# TODO: might need to add padding for # days
day = str(daylst)+"_"

def downloadPics():
    client = storage.Client.from_service_account_json(json_credentials_path=r'windows path to key')
    
    # get bucket 
    bucket = client.get_bucket('bucket')
    
    # For more detail check out blob api guide and storage guide: 
    # https://googleapis.dev/python/storage/latest/client.html 
    # https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/storage/cloud-client/storage_download_file.py
 
    destination_file_name = 'local-dest' 
    blobs = bucket.list_blobs()
    
    # Checks that month/day/year are current
    for blob in blobs:
        if blob.name[0]+blob.name[1] == year:
            if blob.name[2]+blob.name[3]+blob.name[4] == month:
                if blob.name[5]+blob.name[6]+blob.name[7] == day:
                    # changes spaceing for local save
                    filename = blob.name.replace(':', '-')
                    # checks local path, if that blob isnt there, download and print name
                    if os.path.exists(destination_file_name + filename) == False:
                        print (blob.name)
                        blob.download_to_filename(destination_file_name + filename)  # Download
    


def main():
    print("start")
    downloadPics()

if __name__ == "__main__":
    main()