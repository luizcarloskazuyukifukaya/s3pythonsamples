# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
# Sample code to demonstrate GET object with presigned URL

import requests    # To install: pip install requests
from s3PresignedURLs import create_presigned_url

# local expiration value (if not expecified, the default is defined in the s3PresignedURLs.py)
EXPIRATION_VALUE=31536000 # seconds (365 days) (SigV2)

# Target bucket and object (key) specified here
# Define the target bucket and prefix
target_bucket = "kfukaya-tagging"
target_bucket = "kfukaya-wasabi-doc"
target_file = "data/test.txt" 
target_file = "material.pptx" 

print(f"Target bucket: {target_bucket}")
print(f"Target file: {target_file}")
print(f"Expiration: {EXPIRATION_VALUE} secs")

url = create_presigned_url(target_bucket, target_file, EXPIRATION_VALUE)

if url is not None:
    response = requests.get(url)
    print(f"Generated Presigned URL for GET Object ({target_file}) is [{url}]")
    
    print(url)
