# AWS S3 boto3 reference
# Sample code to demonstrate PUT bucket (create new bucket)

import requests    # To install: pip install requests
import logging

# Bucket related
from s3Bucket import create_bucket, list_buckets, delete_bucket

# Bucket policy related
from s3Bucket import set_bucket_policy, get_bucket_policy, delete_bucket_policy

# Target bucket and object (key) specified here
# Define the target bucket and prefix
target_bucket = "kfukaya-tagging"
target_folder = "folder/"
target_file = target_folder + "test.txt" 

print(target_bucket)
print(target_folder)
print(target_file)

# Create a bucket
# region for TOKYO (ap-northeast-1)
if create_bucket(target_bucket, 'ap-northeast-1'):
    # success
    logging.info(f'Bucket: {target_bucket}')
    print(f'Bucket: {target_bucket}')
else:
    # failed
    logging.info(f'Bucket: {target_bucket} creation failed')
    print(f'Bucket: {target_bucket} creation failed')
