# AWS S3 boto3 reference
# Sample code to demonstrate PUT bucket policy

import requests    # To install: pip install requests
import logging

# Bucket related
from s3Bucket import create_bucket, list_buckets, delete_bucket

# Bucket policy related
from s3Bucket import set_bucket_policy, get_bucket_policy, delete_bucket_policy

# Target bucket and object (key) specified here
# Define the target bucket and prefix
#target_bucket = "kfukaya-tagging"
target_bucket = "kfukaya-wasabi-us-east-1"

print(target_bucket)


## Tips
# Bucket Policy in JSON (dict)
# import json
# bucket_policy = json.loads(str_bucket_policy) #string to JSON dict:
# str_bucket_policy = json.dumps(bucket_policy) #JSON dict to string: 


# Get bucket policy
# bucket policy is expected to be JSON dict (NOT string)
bucket_policy = get_bucket_policy(target_bucket)

# If successful, returns HTTP status code 204
logging.info(f'Bucket Policy: {bucket_policy}')
print(f'Bucket Policy: {bucket_policy}')