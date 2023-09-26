# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/select_object_content.html
# https://docs.google.com/spreadsheets/d/1eepIWOHicQsLyZsb0mSXGPTXDp3vlql-aGuy1AWJED0/edit#gid=863195591
# https://aws.amazon.com/jp/blogs/storage/querying-data-without-servers-or-databases-using-amazon-s3-select/

#***************************************************************
# IMPORTANT
#***************************************************************
# S3 SELECT IS NOT SUPPORTED BY WASABI AS OF 9/26/2023
#***************************************************************

import boto3

# Define the target bucket and prefix
#target_bucket = "kfukaya-with-versioning-and-object-lock"
target_bucket = "kfukaya-bucket-object-lock"
#target_bucket = "kfukaya-null-bucket"
target_prefix = "data"
#target_file = "airportCodes.csv"
target_file = "sample_data.csv"
target_key = target_prefix + '/' + target_file
#target_key = target_file

print(target_bucket)
print(target_key)

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

#s3 = boto3.client('s3')
s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

r = s3.select_object_content(
        Bucket=target_bucket,
        Key=target_key,
        ExpressionType='SQL',
        Expression="select * from s3object s where s.\"Name\" = 'Jane'",
        InputSerialization = {'CSV': {"FileHeaderInfo": "Use"}, 'CompressionType': 'NONE'},
        OutputSerialization = {'CSV': {}},
)
        #Expression="select * from s3object s where s.\"Country (Name)\" like '%United States%'",
        #Expression="select * from s3object s where s.\"Country\" like '%USA%'",

print(type(r))
print(r)
print(type(r['Payload']))
print(r['Payload'])

print("Payload reading ...")

file_found_flag = False

for event in r['Payload']:

    print(type(event))
    print(event)
    
    if 'Records' in event:
        records = event['Records']['Payload'].decode('utf-8')
        print(records)
    elif 'Stats' in event:
        statsDetails = event['Stats']['Details']
        print("Stats details bytesScanned: ")
        print(statsDetails['BytesScanned'])
        print("Stats details bytesProcessed: ")
        print(statsDetails['BytesProcessed'])
    elif 'End' in event:
        file_found_flag = True

if file_found_flag:
    print("File found and processed.")
else:
    print("File " + target_key + " not found in the bucket!!!!")
    
print("Payload reading completed!")