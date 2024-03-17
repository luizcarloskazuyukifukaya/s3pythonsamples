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
target_bucket = "kfukaya-tagging"
target_folder = "folder/"
target_file = target_folder + "test.txt" 

print(target_bucket)
print(target_folder)
print(target_file)

# Sample of bucket policy in dict
# The bucket policy should be customized to meet your needs
# Ideally should be provided as a file
bucket_policy = {
    'Version': '2012-10-17',
    'Statement': [
        {
            'Sid': 'BucketPolicyAddedByS3Boto3',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': ['s3:GetObject'],
            'Resource': f'arn:aws:s3:::{target_bucket}/*'
        }    
    ]
}

## Tips
# Bucket Policy in JSON (dict)
# import json
# bucket_policy = json.loads(str_bucket_policy) #string to JSON dict:
# str_bucket_policy = json.dumps(bucket_policy) #JSON dict to string: 


# Set bucket policy
# bucket policy is expected to be JSON dict (NOT string)
set_bucket_policy(target_bucket, bucket_policy)

# If successful, returns HTTP status code 204
logging.info(f'Bucket Policy: {bucket_policy}')
print(f'Bucket Policy: {bucket_policy}')