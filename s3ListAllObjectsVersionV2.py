import boto3
from botocore.exceptions import ClientError

# Use the following code to connect using Wasabi profile from .aws/credentials file

# Define the target bucket and prefix
#target_bucket = "kfukaya-with-versioning-and-object-lock"
# target_bucket = "kfukaya-bucket-object-lock"
target_bucket = "centr-source-bucket"
#target_bucket = "kfukaya-null-bucket"
target_prefix = ""

# define function to list object's version
"""
list_all_objects_version(bucket_name, prefix_name)
args:
    bucket_name: name of the target bucket
    prefix_name: name of the prefix (aka folder path)
return:
    Response Structure (type List)
    [ { 'Versions': [ {'Key': "key name", 
                      'VersionId': "Version ID of an object" }, {} ... ],
        ''DeleteMarkers' : [],
       },
      { 'Versions': [ {'Key': "key name", 
                      'VersionId': "Version ID of an object" }, {} ... ],
        ''DeleteMarkers' : [],
       },
       ...
     ]
reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_object_versions.html#
"""
def list_all_objects_version(bucket_name, prefix_name):
    session = boto3.session.Session(profile_name="wasabi")
    
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key
    # region = 'ap-northeast
    region = 'ap-southeast-2'
    endpoint_url = 'https://s3.' + region + '.wasabisys.com'

    s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

    result = {}
    repeatCall = True # When True, the list_object_versions is to be called
    key = ""
    version_id = ""
    all_versions_list = []

    while repeatCall:
        try:
            result = s3.list_object_versions(
                Bucket=bucket_name,
                KeyMarker=key,
                VersionIdMarker=version_id, 
                Prefix=prefix_name
            )
            # print(f"result type (after function call): {type(result)}")
            # print(f"result : {result}")

            # print(f"IsTruncated: {result['IsTruncated']}")
            # print(f"KeyMarker: {result['KeyMarker']}")
            # print(f"VersionIdMarker: {result['VersionIdMarker']}")

            # Append version dict to List
            all_versions_list.append(result)
            
            repeatCall =  result['IsTruncated']
            if repeatCall:
                key = result['NextKeyMarker']
                version_id = result['NextVersionIdMarker']
                # print(f"NextKeyMarker: {result['NextKeyMarker']}")
                # print(f"NextVersionIdMarker: {result['NextVersionIdMarker']}")

            # print(f"repeatCall: {repeatCall}")
            
        except ClientError as e:
            raise Exception("boto3 client error in list_all_objects_version function: " + e.__str__())
        except Exception as e:
            raise Exception("Unexpected error in list_all_objects_version function of s3 helper: " + e.__str__())
    
    return all_versions_list


def process_obj_dict(d):
    print("Key name: " + d['Key'])
    print("Version Id: " + d['VersionId'])
    # print("Last Modified: " + str(d['LastModified']))
    # print("Latest version: " + str(d['IsLatest']))
    # print("*****************************")  

#     
def show_versions(only_latest_flag):
    #-----------------------------------------------------------
    # Now call the defined function with the specified bucket and prefix
    #-----------------------------------------------------------
    # target_bucket : global variable
    # target_prefix : global variable
    all_versions_dict = list_all_objects_version(target_bucket, target_prefix)

    #only_latest_flag = False
    # only_latest_flag = True
    # print(f" Return list: {all_versions_dict}")

    for version_dict in all_versions_dict:
        try:
            versions = version_dict['Versions']
            # print(f"{versions}")
            for v in versions:
                #print(v)
                #print(type(v))
                if only_latest_flag:
                    if v['IsLatest']:
                        process_obj_dict(v)
                else:
                    process_obj_dict(v)
            try:
                deletes = version_dict['DeleteMarkers']
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

def main():
    # List all versions
    # Parameter: 
    #   True: Show Latest version only
    #   False: Show all versions
    show_versions(False)

if __name__ == "__main__":
    main()

