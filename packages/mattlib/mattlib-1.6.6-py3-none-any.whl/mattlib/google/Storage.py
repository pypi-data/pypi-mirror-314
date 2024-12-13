from google.cloud import storage

def get_type(filename):
    filetype = filename.split('.')[1]
    if filetype == 'json':
        return 'application/json'
    if filetype == 'txt':
        return 'text/plain'
    if filetype=='csv':
        return 'text/csv'

# 	retirado de: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-code-sample
def upload_blob_from_memory(bucket_name, contents, destination_blob_name):
    storage_client = storage.Client\
        .from_service_account_json('service_account.json')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    content_type = get_type(destination_blob_name)
    blob.upload_from_string(contents, content_type=content_type)
