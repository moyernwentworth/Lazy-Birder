from google.cloud import storage


def uploadPic(pic,location):

	client = storage.Client.from_service_account_json(json_credentials_path='/home/pi/scripts/pas/creds.json')
    # get bucket 
	bucket = client.get_bucket('bucket name')
	# blob = random type; this case a pic
	object_name_in_gcs_bucket = bucket.blob(pic)
	# Name of the object in local file system
	object_name_in_gcs_bucket.upload_from_filename(location)

	
