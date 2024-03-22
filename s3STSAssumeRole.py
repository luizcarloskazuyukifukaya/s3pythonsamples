# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/get_session_token.html#
# EndPoint URL is with sts.wasabisys.com (sts.<<region>>.wasabisys.com)
# Japanese only
# https://zenn.dev/sugikeitter/articles/how-to-use-boto3-various-settings
#
# Example of policy to assign to a user who can assume role
# Policy (JSON) allowing any instance to perform sts:AssumeRole
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Principal": {
#         "AWS": "*"
#       },
#       "Action": "sts:AssumeRole"
#     }
#   ]
# }

# Example of role with policy named "WasabiFullAccess"
# Role ARN 'arn:aws:iam::100000222373:role/S3FullAccessRole'
# JSON of WasabiFullAccess policy
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Action": "s3:*",
#       "Resource": "*"
#     },
#     {
#       "Effect": "Allow",
#       "Action": [
#         "iam:*",
#         "sts:*"
#       ],
#       "Resource": "arn:aws:iam::${aws:accountid}:user/${aws:username}"
#     }
#   ]
# }

# *******************************************************
# IMPORTANT THIS IS A EXAMPLE FOR WASABI Connection
# *******************************************************
import boto3

# Define the parameters
durationSeconds=3600
sessionName='kfukayaWASABI'

#'arn:aws:iam::100000222373:role/S3FullAccessRole'
assumeRoleARN='arn:aws:iam::100000222373:role/S3FullAccessRole'
# arn:aws:iam::295267756805:role/AWSAssumeRoleS3FullAccess
#assumeRoleARN='arn:aws:iam::295267756805:role/AWSAssumeRoleS3FullAccess'

print(durationSeconds)
print(assumeRoleARN)

session = boto3.Session(profile_name="normal")
#session = boto3.Session(profile_name="normalAWS")
# The IAM user associated with the profile specified should have the sts:AssumeRole policy at least
credentials = session.get_credentials()
aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key

# Get the region name from the session
# region = session.region_name
region = 'ap-northeast-1'
#endpoint_url = 'https://s3.' + region + '.wasabisys.com'

# Get the S3 endpoint URL from the session
# s3_endpoint_url = session.get_config_variable('s3')['endpoint_url']
# print(f"The S3 endpoint URL specified in the AWS CLI profile is: {s3_endpoint_url}")

# STS is a global service and should not be directly using the regional endopoint
sts_endpoint_url = 'https://sts.' + region + '.wasabisys.com'
#sts_endpoint_url = 'https://sts.' + region + '.amazonaws.com'
#sts_endpoint_url = 'https://sts.wasabisys.com'
#sts_endpoint_url = 'https://sts.amazonaws.com'

# S3 endopoint
endpoint_url = 'https://s3.' + region + '.wasabisys.com'
#endpoint_url = 'https://s3.' + region + '.amazonaws.com'
#endpoint_url = 'https://s3.wasabisys.com'
#endpoint_url = 'https://s3.amazonaws.com'

print(region)
print(endpoint_url)
#print(aws_access_key_id)
#print(aws_secret_access_key)

sts_client = boto3.client('sts',
                  endpoint_url=sts_endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)


# The session policy specified here
sessionPolicy = '{"Version": "2012-10-17","Statement": [{"Effect": "Allow","Action": "s3:*","Resource": "*"}]}'

temp_creds = sts_client.assume_role(
    RoleArn=assumeRoleARN, # IAM Role ARN
    # Session ID (Anything unique to distinguish the session)
    RoleSessionName=f'RoleSession-{region}-{sessionName}',
    # session Policy JSON
    Policy=sessionPolicy, 
    DurationSeconds=durationSeconds # Duration in seconds
)

#print(temp_creds)
#print(type(temp_creds))

r=temp_creds
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
print(f"Size: {len(cred['SessionToken'])}")
print('------------------')

# Create tempporary session with the temporary credentials generated with STS
s3 = boto3.client(
    's3',
#    region_name=region,
    endpoint_url=endpoint_url,
    aws_access_key_id=temp_creds.get('Credentials').get('AccessKeyId'),
    aws_secret_access_key=temp_creds.get('Credentials').get('SecretAccessKey'),
    aws_session_token=temp_creds.get('Credentials').get('SessionToken')
)

#-----------------------------------------
print("Temporary session created....")

# Create bucket
#bucket_name = f'AWS-bucket-xyz-20240321-{sessionName}'
bucket_name = f'awsbucketnamekfukaya20240321'
print("Creating bucket....")
print(f'Bucket Name: {bucket_name}')

r = s3.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={
        'LocationConstraint': region,
        # 'Location': {
        #     'Type': 'AvailabilityZone',
        #     'Name': 'string'
        # },
        # 'Bucket': {
        #     'DataRedundancy': 'SingleAvailabilityZone',
        #     'Type': 'Directory'
        # }
    },    
)
# print(type(r))
# print(r)

# print('------------------')
# print('ResponseMetadata:')
# print(r['ResponseMetadata'])
print('------------------')
print('HTTPHeaders:')
print(r['ResponseMetadata']['HTTPHeaders'])
print('------------------')

# List buckets
print("Listing bucket....")
r = s3.list_buckets()
# print(type(r))
# print(r)

# print('------------------')
# print('ResponseMetadata:')
# print(r['ResponseMetadata'])
# print('------------------')
# print('HTTPHeaders:')
# print(r['ResponseMetadata']['HTTPHeaders'])
# print('------------------')
# print('Buckets:')
# print(r['Buckets'])
# print('------------------')

# Output the bucket names
print('Existing buckets:')
for bucket in r['Buckets']:
    print(f'  {bucket["Name"]}')


print("Deleting bucket....")
print(f'Bucket Name: {bucket_name}')
r = s3.delete_bucket(Bucket=bucket_name)
# print(type(r))
# print(r)

print('------------------')
print('ResponseMetadata:')
print(r['ResponseMetadata'])
print('------------------')
# print('HTTPHeaders:')
# print(r['ResponseMetadata']['HTTPHeaders'])
# print('------------------')

print("Done.")