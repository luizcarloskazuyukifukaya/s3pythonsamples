# AWS S3 boto3 reference
# Sample code to demonstrate PUT Object Lock bucket (create new Object Lock bucket)

import requests    # To install: pip install requests
import logging

# Object Lock Bucket related
from s3Bucket import create_object_lock_bucket, delete_bucket
    
def main():
    # Target bucket specified here
    target_bucket = "kfukaya-object-lock-bucket-python"
    target_region = "ap-northeast-1"
    print(target_bucket)
    print(target_region)

    # Create a bucket
    # region for TOKYO (ap-northeast-1)
    if create_object_lock_bucket(target_bucket, target_region):
        # success
        logging.info(f'Object Lock Bucket: {target_bucket}')
        print(f'Object Lock Bucket: {target_bucket}')

        # # delete bucket
        # delete_bucket(target_bucket)    
    else:
        # failed
        logging.info(f'Object Lock Bucket: {target_bucket} creation failed')
        print(f'Object Lock Bucket: {target_bucket} creation failed')

if __name__ == "__main__":
    main()
