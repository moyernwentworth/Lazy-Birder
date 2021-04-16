import os
import cv2
import numpy as np
from google.cloud import storage
from tempfile import NamedTemporaryFile
import h5py
import gcsfs
from tensorflow import keras
from PIL import Image
from keras.models import load_model
from yolo import yolo_act

def uploadPic(pic, location):
        # Setting credentials using the downloaded JSON file
        client = storage.Client.from_service_account_json('keys.json')

        bucket = client.get_bucket('pre-process-birds-bucket')

        # Name of the object to be stored in the bucket
        object_name_in_gcs_bucket = bucket.blob(pic)


        source_bucket = location
        source_blob = source_bucket.get_blob(pic)
        image = np.asarray(bytearray(source_blob.download_as_string()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)

        with NamedTemporaryFile() as temp:
            # Extract name to the temp file
            temp_file = "".join([str(temp.name), pic])
            # Save image to temp file
            cv2.imwrite(temp_file, image)
            bird = yolo_act(temp_file, 'gs:path/path/yolo-coco')
            cv2.imwrite(temp_file, bird)
            #creates new file to upload from csv img info returned by yolo


        # Name of the object in local file system
        object_name_in_gcs_bucket.upload_from_filename(temp_file)
        stats = storage.Blob(bucket=bucket, name=pic).exists()
        return stats
        

def delete_pic(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

    print("Bird image {} deleted.".format(blob_name))


def main_start(event, context):
    file = event    
    client = storage.Client()
    source_bucket = client.get_bucket(file['bucket'])
    source_blob = source_bucket.get_blob(file['name'])


    stats = uploadPic(file['name'],source_bucket)

    if stats == True:
        delete_pic(file['bucket'], file['name'])
    else: 
        sys.exit('Upload Error: did not delete')
