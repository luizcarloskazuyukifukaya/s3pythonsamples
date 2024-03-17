# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/create_user.html

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


# Specify the user name to be created
NewUserName = "new-user"

s3 = boto3.client('iam',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

# Check whether the user already exist
no_user_creation = True
# List all users
r = s3.list_users()
for user in r["Users"]:
  if user["UserName"] == NewUserName:
    print(f'{NewUserName} already exist!')
    no_user_creation = False
    
if no_user_creation:
  # Create new user now
  r = s3.create_user(
  #    Path='string',
      UserName=NewUserName,
  #    PermissionsBoundary='string',
      Tags=[
          {
              'Key': 'UserName',
              'Value': f'{NewUserName}'
          },
      ]
  )

  print(type(r))
  print(r)


