# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/upload_file.html 

import boto3

# Define the target bucket and prefix
target_bucket = "kfukaya-tagging"
# target_file = "data/sample_data.csv"
target_file = "data/sample_data.txt"

print(target_bucket)
print(target_file)

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


# upload an object (.data/sample_data.csv)
r = s3.upload_file(
    target_file,
    target_bucket,
    target_file,
)

print(r)

print(type(r))
