# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/delete_user.html

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


# Specify the user name to be deleted
UserName = "new-user"

s3 = boto3.client('iam',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

# Check whether the user already exist
user_exists = False
# List all users
r = s3.list_users()
for user in r["Users"]:
  if user["UserName"] == UserName:
    print(f'{UserName} already exist!')
    user_exists = True
    
if user_exists:
  # Use does exist, so let us delete it
  # Delete the user now
  r = s3.delete_user(
      UserName=UserName
  )

  print(type(r))
  print(r)

  print(f"{UserName} deleted.")
else:
  print(f"{UserName} does not exist. Operation cancelled.")


