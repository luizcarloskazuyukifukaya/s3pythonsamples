# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/select_object_content.html

import boto3

# session = boto3.Session(profile_name="wasabi")
session = boto3.Session(profile_name="wasabi")
credentials = session.get_credentials()
aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key
region = 'ap-northeast-1'
endpoint_url = 'https://s3.' + region + '.wasabisys.com'

print(region)
print(endpoint_url)
print(aws_access_key_id)
print(aws_secret_access_key)

#s3 = boto3.client('s3')
s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

# Retrieve the list of existing buckets
r = s3.list_buckets()

# Output the bucket names
#print('Existing buckets:')
#for bucket in r['Buckets']:
#    print(f'  {bucket["Name"]}')

#print(type(r))
#print(r)
#print(type(r['ResponseMetadata']))
#print(r['ResponseMetadata'])

print('Wasabi Object Storage Server version: ' + (r['ResponseMetadata']['HTTPHeaders']['server']))
print('Current Date: ' + (r['ResponseMetadata']['HTTPHeaders']['date']))
