# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/get_session_token.html#
# EndPoint URL is with sts.wasabisys.com (sts.<<region>>.wasabisys.com)
# Japanese only
# https://zenn.dev/sugikeitter/articles/how-to-use-boto3-various-settings

import boto3

# Define the parameters
durationSeconds=3600
sessionName='kfukaya'

#'arn:aws:iam::100000222373:role/S3FullAccessRole'
assumeRoleARN='arn:aws:iam::100000222373:role/S3FullAccessRole'

print(durationSeconds)
print(assumeRoleARN)

session = boto3.Session(profile_name="normal")
credentials = session.get_credentials()
aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key
region = 'ap-northeast-1'
#endpoint_url = 'https://s3.' + region + '.wasabisys.com'

# STS is a global service and should not be directly using the regional endopoint
endpoint_url = 'https://sts.' + region + '.wasabisys.com'
#endpoint_url = 'https://sts.wasabisys.com'

print(region)
print(endpoint_url)
#print(aws_access_key_id)
#print(aws_secret_access_key)

sts_client = boto3.client('sts',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

sessionPolicy = '{"Version": "2012-10-17","Statement": [{"Effect": "Allow","Action": "s3:*","Resource": "*"}]}'

temp_creds = sts_client.assume_role(
    RoleArn=assumeRoleARN, # IAM Role ARN
    # Session ID (Anything unique to distingush the session)
    RoleSessionName=f'RoleSession-{region}-{sessionName}',
    # session Policy JSON
    Policy=sessionPolicy, 
    DurationSeconds=durationSeconds # Duration in seconds
)

# Create tempporary session with the temporary credentials generated with STS
s3 = boto3.client(
    's3',
    aws_access_key_id=temp_creds.get('Credentials').get('AccessKeyId'),
    aws_secret_access_key=temp_creds.get('Credentials').get('SecretAccessKey'),
    aws_session_token=temp_creds.get('Credentials').get('SessionToken')
)

#-----------------------------------------
print("Temporary session created....")

# List buckets
r = s3.list_buckets()

print(type(r))
print(r)


