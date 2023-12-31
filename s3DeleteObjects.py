# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/delete_objects.html# 

import boto3

# Define the target bucket and prefix
target_bucket = "kfukaya-tagging"
target_files = [{ 'Key': 'test3.txt' }, {'Key': 'test2.txt'}]

print(target_bucket)
print(target_files)

session = boto3.Session(profile_name="wasabi")
credentials = session.get_credentials()
aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key
region = 'ap-northeast-1'
endpoint_url = 'https://s3.' + region + '.wasabisys.com'

print(region)
print(endpoint_url)
#print(aws_access_key_id)
#print(aws_secret_access_key)

s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

r = s3.delete_objects(
    Bucket=target_bucket,
    Delete={
        'Objects': target_files,
        },
    BypassGovernanceRetention=True,
)

print(type(r))
print(r)