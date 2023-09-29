import boto3
from botocore.exceptions import ClientError

# Use the following code to connect using Wasabi profile from .aws/credentials file

# Define the target bucket and prefix
#target_bucket = "kfukaya-with-versioning-and-object-lock"
target_bucket = "kfukaya-bucket-object-lock"
#target_bucket = "kfukaya-null-bucket"
target_prefix = ""

# define function to list object's version
"""
list_all_objects_version(bucket_name, prefix_name)
args:
    bucket_name: name of the target bucket
    prefix_name: name of the prefix (aka folder path)
return:
    Response Structure (type dict)
    { 'Versions' : [ {'Key': "key name", 
                      'VersionId': "Version ID of an object" }, 
                      ...
                    ], ...
     }
reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_object_versions.html#
"""
def list_all_objects_version(bucket_name, prefix_name):
    session = boto3.session.Session(profile_name="wasabi")
    
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key
    region = 'ap-northeast-1'
    endpoint_url = 'https://s3.' + region + '.wasabisys.com'

    s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

    result = {}
    try:
        result = s3.list_object_versions(Bucket=bucket_name, Prefix=prefix_name)
    except ClientError as e:
        raise Exception("boto3 client error in list_all_objects_version function: " + e.__str__())
    except Exception as e:
        raise Exception("Unexpected error in list_all_objects_version function of s3 helper: " + e.__str__())
    return result

def process_obj_dict(d):
    print("Key name: " + d['Key'])
    print("Version Id: " + d['VersionId'])
    print("Last Modified: " + str(d['LastModified']))
    print("Latest version: " + str(d['IsLatest']))
    print("*****************************")  
    

#-----------------------------------------------------------
# Now call the defined function with the specified bucket and prefix
#-----------------------------------------------------------
objs_dict = list_all_objects_version(target_bucket, target_prefix)

#only_latest_flag = False
only_latest_flag = True
try:
    versions = objs_dict['Versions']
    #print(versions)
    print("[Versions]")
    for v in versions:
        #print(v)
        #print(type(v))
        if only_latest_flag:
            if v['IsLatest']:
                process_obj_dict(v)
        else:
            process_obj_dict(v)
    try:
        deletes = objs_dict['DeleteMarkers']
        #print(deletes)
        print("[DeleteMarkers]")
        
        for d in deletes:
            #print(d)
            #print(type(d))
            if only_latest_flag:
                if d['IsLatest']:
                    process_obj_dict(d)
            else:
                process_obj_dict(d)
    except KeyError:
        print('No delete marker found.')
except KeyError:
    print('No object found... the target bucket is empty!!!')

print("End of the execution.") 
