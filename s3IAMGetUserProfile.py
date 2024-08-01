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

try:
  s3 = boto3.client('iam',
                    endpoint_url=endpoint_url,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)

  print(s3)

  # r = s3.get_login_profile(
  #     UserName='kfukaya-normal',
  # )
  r = s3.get_instance_profile(
      InstanceProfileName="S3FullAccessRole",
  )
  print(type(r))
  print(r)

except s3.exceptions.NoSuchEntityException:
  print('No such entity!')

except s3.exceptions.ServiceFailureException:
  print('Service Failure !')

except s3.exceptions.ClientError:
  print('Client Error !')

