# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/list_virtual_mfa_devices.html

import boto3

# Define the parameters
assignStatus = 'Any'
#assignStatus = 'Assigned'
#assignStatus = 'Unassigned'

session = boto3.Session(profile_name="wasabi")
credentials = session.get_credentials()
aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key
region = 'ap-northeast-1'
#endpoint_url = 'https://s3.' + region + '.wasabisys.com'
endpoint_url = 'https://sts.' + region + '.wasabisys.com'

print(region)
print(endpoint_url)
#print(aws_access_key_id)
#print(aws_secret_access_key)

# IAM service used
s3 = boto3.client('iam',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

r = s3.list_virtual_mfa_devices(
  AssignmentStatus=assignStatus
)

print(r)
print(type(r))

print('------------------')
print('VirtualMFADevices:')
print(r['VirtualMFADevices'])
print('------------------')

print('Listing all Virtual MFA Devices linked to a user ....')
for mfaDevice in r['VirtualMFADevices']:
    if mfaDevice.get('User'):
      print(f'Virutal MFA Device S/N: {mfaDevice["SerialNumber"]}') 
#      print(f"Virutal MFA Device's User: {mfaDevice['User']}") 
      print(f"Virutal MFA Device's User Name: {mfaDevice['User']['UserName']}") 
      print(f"Virutal MFA Device's User ID: {mfaDevice['User']['UserId']}") 
      print(f"Virutal MFA Device's User ARN: {mfaDevice['User']['Arn']}") 
