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

CATEGORIES = [
              'BLACK-CAPPED_CHICKADEE', 'NORTHERN_CARDINAL', 'CROW', 'AMERICAN_GOLDFINCH',
              'BALTIMORE_ORIOLE', 'CHIPPING_SPARROW', 'COMMON_GRACKLE', 'COMMON_STARLING',
              'DARK-EYED_JUNCO', 'DOWNY_WOODPECKER', 'EASTERN_BLUEBIRD', 'GRAY_CATBIRD',
              'HOUSE_FINCH', 'HOUSE_SPARROW', 'MOURNING_DOVE', 'NORTHERN_FLICKER', 
              'PURPLE_FINCH', 'RED-HEADED_WOODPECKER', 'RED-WINGED_BLACKBIRD', 'TITMOUSE'       
]

def prepare(file1):
  IMG_SIZE = 224
  new_array = cv2.resize(file1, (IMG_SIZE, IMG_SIZE))
  return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

def predict(pic,bucket):
    client = storage.Client.from_service_account_json('keys.json')

    source_blob = bucket.get_blob(pic)
    image1 = np.asarray(bytearray(source_blob.download_as_string()), dtype="uint8")
    img = cv2.imdecode(image1, cv2.IMREAD_GRAYSCALE)


    PROJECT_NAME = 'name'
    CREDENTIALS = 'keys.json'
    MODEL_PATH = 'path to h5'

    FS = gcsfs.GCSFileSystem(project=PROJECT_NAME,token=CREDENTIALS)
    # going to use authenticated open path in storage to access h5 file
    # very complicated, have to access specific way; if you dont get it dont touch it
    with FS.open(MODEL_PATH, mode='rb') as model_file:
        model_gcs = h5py.File(model_file, mode='r')
        myModel = load_model(model_gcs)
        prepared = prepare(img)
        prediction = myModel.predict([prepared])
        print(pic)
        listy = []
        prediction1 = str(prediction).split(" ")
        for i in range(len(prediction1)):
            x = str(prediction1[i]).replace("[","").replace("]","").replace("\n", "")
            listy.append((x))
        listx = [round(float(item)) for item in listy if len(item) > 1]
        #print(listx)
        max_value = max(listx)
        #print (max_value)
        max_index = listx.index(max_value)
        #print (max_value)
        results = CATEGORIES[max_index]
        print (results) 
        return (results)  
    return 0

def uploadPic(pic, location, cat):

        # Setting credentials using the downloaded JSON file
        client = storage.Client.from_service_account_json('keys.json')

        # Creating bucket object
        bucket = client.get_bucket('processed bucket name')

        # add ~ to make nameing convention easier to follow
        picMod = str(cat) + "~" + pic

        # Name of the object to be stored in the bucket
        object_name_in_gcs_bucket = bucket.blob(picMod)

        source_bucket = location
        source_blob = source_bucket.get_blob(pic)
        image = np.asarray(bytearray(source_blob.download_as_string()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)

        with NamedTemporaryFile() as temp:
            # Extract name to the temp file
            temp_file = "".join([str(temp.name), picMod])
            # Save image to temp file
            cv2.imwrite(temp_file, image)
            # Uploading the temp image file to the bucket


        # Name of the object in local file system
        object_name_in_gcs_bucket.upload_from_filename(temp_file)
        stats = storage.Blob(bucket=bucket, name=picMod).exists()
        return stats
        

def delete_pic(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    # removes blob from original bucket
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

    print("Bird image {} deleted.".format(blob_name))


def main_start(event, context):
    file = event    
    client = storage.Client()
    source_bucket = client.get_bucket(file['bucket'])
    source_blob = source_bucket.get_blob(file['name'])

    cat = predict(file['name'],source_bucket)

    stats = uploadPic(file['name'],source_bucket, cat )
    if stats == True:
        delete_pic(file['bucket'], file['name'])
    else: 
        sys.exit('Upload Error: did not delete')
