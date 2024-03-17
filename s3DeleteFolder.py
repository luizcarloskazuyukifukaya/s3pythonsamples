# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/delete_object.html#
# NOTE:
# This is the basically the same as s3DeleteObject.py as a folder is still an S3 Object with Prefix only

import boto3

# Define the target bucket and prefix
target_bucket = "kfukaya-tagging"
#target_folder = "data/"
target_folder = "othernewdata/"
target_file = target_folder + "sample_data.csv"

print(target_bucket)
print(target_folder)
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

# check whether the folder already exist or not
r = s3.list_objects(Bucket=target_bucket, Prefix=target_folder)

# for debugging purpose only
print(r)

if not "Contents" in r:
    # Folder does not exist yet when the "Contents" element does not exist
    # 
    
    print(type(r))
    print(r)

    print(f"{target_folder} does not exist in {target_bucket}. Operation cancelled.")

else:
    
    # Check if the folder is empty or not
    
    dict_objects = r['Contents']
    #print(type(r['Contents']))

    print(len(dict_objects))
    
    if len(dict_objects) > 1:
        print("More than one Object exist already!!! Operation cancelled.")

        for obj in dict_objects:
            print('-- ' + obj['Key'])    
    else:  
        r = s3.delete_object(
            Bucket=target_bucket,
            Key=target_folder, #folder only
        )
        
        print(type(r))
        print(r)
        print(f"{target_folder} is deleted from {target_bucket}.")



