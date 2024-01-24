# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
# Sample code to demonstrate GET object with presigned URL

import requests    # To install: pip install requests
from s3PresignedURLs import create_presigned_url

# Target bucket and object (key) specified here
# Define the target bucket and prefix
target_bucket = "kfukaya-tagging"
target_bucket = "kfukaya-wasabi-doc"
target_file = "data/test.txt" 
target_file = "material.pptx" 

print(target_bucket)
print(target_file)

url = create_presigned_url(target_bucket, target_file)

if url is not None:
    response = requests.get(url)
    print(f"Generated Presigned URL for GET Object ({target_file}) is [{url}]")
    
    print(url)
