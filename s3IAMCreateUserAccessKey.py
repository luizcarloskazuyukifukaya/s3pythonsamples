# AWS S3 boto3 reference
# for AccessKey creation (implemented in this sample)
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/create_access_key.html
# for AccessKey deletion
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/delete_access_key.html

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
    # Create the Access and Secret Key now
    r = s3.create_access_key(
        UserName=TargetUserName
    )

    print(type(r))
    print(r)
    
    print(f"AccessKeyId: {r['AccessKey']['AccessKeyId']}")
    print(f"SecretAccessKey: {r['AccessKey']['SecretAccessKey']}")
else:
    print(f"{TargetUserName} does not exist. Operation cancelled.")


