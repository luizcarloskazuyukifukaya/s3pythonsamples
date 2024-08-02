# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/list_users.html

import boto3

session = boto3.Session(profile_name="wasabi")
credentials = session.get_credentials()
aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key

region = 'ap-northeast-1'
endpoint_url = 'https://iam.' + region + '.wasabisys.com'

print(region)
print(endpoint_url)
#print(aws_access_key_id)
#print(aws_secret_access_key)

s3 = boto3.client('iam',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

# r = s3.list_users()
paginator = s3.get_paginator('list_users')
response_iterator = paginator.paginate()
accounts=[]
for page in response_iterator:
    for user in page['Users']:
        accounts.append(user['UserName'])
        # print(f"User name is {user['UserName']}")

for account in accounts:
  print(account)
