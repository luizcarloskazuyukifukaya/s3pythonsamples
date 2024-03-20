# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/get_session_token.html#
# EndPoint URL is with sts.wasabisys.com (sts.<<region>>.wasabisys.com)

import boto3

# Define the parameters
durationSeconds=3600

print(durationSeconds)

session = boto3.Session(profile_name="wasabi")
credentials = session.get_credentials()
aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key
region = 'ap-northeast-1'
#endpoint_url = 'https://s3.' + region + '.wasabisys.com'

# STS is a global service and should not be directly using the regional endopoint
#endpoint_url = 'https://sts.' + region + '.wasabisys.com'
endpoint_url = 'https://sts.wasabisys.com'

print(region)
print(endpoint_url)
#print(aws_access_key_id)
#print(aws_secret_access_key)

s3 = boto3.client('sts',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

r = s3.get_session_token(
  DurationSeconds=durationSeconds
)

print(r)
print(type(r))

print('------------------')
print('Credentials:')
print(r['Credentials'])
print('------------------')
print('ResponseMetadata:')
print(r['ResponseMetadata'])
print('------------------')

cred=r['Credentials']
print('AccessKeyId:')
print(cred['AccessKeyId'])
print('SecretAccessKey:')
print(cred['SecretAccessKey'])
print('Expiration:')
print(cred['Expiration'])
print('SessionToken:')
print(cred['SessionToken'])
print('------------------')

