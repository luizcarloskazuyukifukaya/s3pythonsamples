# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/get_object_attributes.html#

import boto3

# Define the target bucket and prefix
target_bucket = "kfukaya-tagging"
# target_file = "test.txt"
target_file = "data/sample_data.txt"

# downloaded_file name
saved_file = 'data/downloaded_file.txt'

print(target_bucket)
print(target_file)

session = boto3.Session(profile_name="wasabi")
credentials = session.get_credentials()
aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key
region = 'ap-northeast-1'
endpoint_url = 'https://s3.' + region + '.wasabisys.com'

print(region)
print(endpoint_url)
#print(aws_access_key_id)
#print(aws_secret_access_key)

s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

r = s3.get_object(
    Bucket=target_bucket,
    Key=target_file,
)
print('Object downloaded successfully.') 
print(type(r))
print(r)

print('------------------')
print(r['ResponseMetadata'])
print('------------------')
print(r['Metadata'])
print('------------------')
print(r['ETag'])
print('------------------')
print(r['VersionId'])


# Now get a range (part) of the Object
# Specify the byte range you want to download (e.g., bytes 0-999)
# 10 bytes only 
range_header = 'bytes=2-15' 
 
# Download the specific range of bytes from the object 
r = s3.get_object(
        Bucket=target_bucket,
        Key=target_file,
        Range=range_header
) 
print('Object downloaded (partially) successfully.') 
print(type(r))
print(r)

print('------------------')
print(r['ResponseMetadata'])
print('------------------')
print(r['Metadata'])
print('------------------')
print(r['ETag'])
print('------------------')
print(r['VersionId'])

# Save the downloaded object to a file 
with open(saved_file, 'wb') as f: 
    f.write(r['Body'].read()) 

print(f'File saved successfully. Name: {saved_file}') 