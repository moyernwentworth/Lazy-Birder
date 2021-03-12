import os
import cv2
import numpy as np
from google.cloud import storage
from tempfile import NamedTemporaryFile
def reformat_image(event, context):
    file = event
    client = storage.Client()
    source_bucket = client.get_bucket(file['bucket'])
    source_blob = source_bucket.get_blob(file['name'])
    image = np.asarray(bytearray(source_blob.download_as_string()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
    scale_percent = 50  # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    with NamedTemporaryFile() as temp:
        # Extract name to the temp file
        temp_file = "".join([str(temp.name), file['name']+'-temp'])
        # Save image to temp file
        cv2.imwrite(temp_file, resized)
        # Uploading the temp image file to the bucket
    
    # check if upload is complete; if not error
    stats = uploadPic(file['name'], temp_file)
    if stats == True:
        delete_pic(file['bucket'], file['name'])
    else: 
        sys.exit('Upload Error: did not delete')

def uploadPic(pic,location):

        client = storage.Client.from_service_account_json('-----contact me-----')
        
        bucket = client.get_bucket(-----contact me-----')

        object_name_in_gcs_bucket = bucket.blob(pic)
        # object original location 
        object_name_in_gcs_bucket.upload_from_filename(location)
        #gets upload status returns it 
        stats = storage.Blob(bucket=bucket, name=pic).exists()
        return stats
        

def delete_pic(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

    print("Birdy {} deleted.".format(blob_name))
