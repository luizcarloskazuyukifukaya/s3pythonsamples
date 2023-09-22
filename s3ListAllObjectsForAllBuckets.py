import boto3

# Use the following code to connect using Wasabi profile from .aws/credentials file

# session = boto3.Session(profile_name="wasabi")
session = boto3.Session(profile_name="wasabi")
credentials = session.get_credentials()
aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key
region = 'ap-northeast-1'
endpoint_url = 'https://s3.' + region + '.wasabisys.com'

print(region)
print(endpoint_url)
print(aws_access_key_id)
print(aws_secret_access_key)

s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

# List buckets
response = s3.list_buckets()
# Output the bucket names
print('Listing all objects within a existing bucket ....')
for bucket in response['Buckets']:
    # print(f'  {bucket["Name"]}')
    print('Bucket name: ' + bucket["Name"]) 
    
    objects = s3.list_objects_v2(Bucket=bucket["Name"])
    #print(objects['Name']) 
    #print(type(objects))
    
    # check whether the bucket is empty or not
    try:
        dict_objects = objects['Contents']
    except KeyError:
        print('No object found... the target bucket is empty!!!')
        continue

    #print(type(objects['Contents']))

    for obj in dict_objects:
        print('-- ' + obj['Key'])