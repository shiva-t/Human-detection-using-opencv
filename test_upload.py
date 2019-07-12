from google.cloud import storage

def uploadFile(file):
 storage_client = storage.Client()
 bucket = storage_client.get_bucket('video-surv.appspot.com')
 blob = bucket.blob(file)
 blob.upload_from_filename(file)
#print('File {} uploaded to {}'.format(file,file))
