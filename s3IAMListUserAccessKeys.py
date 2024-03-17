# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/list_access_keys.html

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


# Specify the user name so the access key and secret key are created
TargetUserName = "new-user"

s3 = boto3.client('iam',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

# Check whether the user already exist
user_exists = False
# List all users
r = s3.list_users()
for user in r["Users"]:
  if user["UserName"] == TargetUserName:
    print(f'{TargetUserName} already exist!')
    user_exists = True
    
if user_exists:
    # List the Access Keys now
    r = s3.list_access_keys(
        UserName=TargetUserName
#        Marker='string',
#        MaxItems=123
    )
    print(type(r))
    print(r)
    
    for accessKeyMetadata in r['AccessKeyMetadata']:
        print(f"AccessKeyId: {accessKeyMetadata['AccessKeyId']}")
        print(f"AccessKeyId: {accessKeyMetadata['Status']}")
else:
    print(f"{TargetUserName} does not exist. Operation cancelled.")


