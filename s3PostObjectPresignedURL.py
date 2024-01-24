# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
# Sample code to demonstrate GET object with presigned URL

import requests    # To install: pip install requests
import logging
from s3PresignedURLs import create_presigned_url, create_presigned_post

# Target bucket and object (key) specified here
# Define the target bucket and prefix
target_bucket = "kfukaya-wasabi-doc"
target_file = "data/test.txt" 

print(target_bucket)
print(target_file)

# Generate a presigned S3 POST URL
object_name = target_file
response = create_presigned_post(target_bucket, object_name)
if response is None:
    exit(1)

print(f"Presigned URL: {response['url']}")
print(f"Presigned fields: {response['fields']}")

# Demonstrate how another Python program can use the presigned URL to upload a file
with open(object_name, 'rb') as f:
    files = {'file': (object_name, f)}
    http_response = requests.post(response['url'], data=response['fields'], files=files)

# If successful, returns HTTP status code 204
logging.info(f'File upload HTTP status code: {http_response.status_code}')
print(f'File upload HTTP status code: {http_response.status_code}')
