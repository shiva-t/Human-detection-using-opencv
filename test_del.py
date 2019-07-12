from google.cloud import storage

storage_client = storage.Client()
bucket = storage_client.get_bucket('shetty_buck')
bucket.delete()
print('File {} uploaded to {}'.format('shetty_buck'))

