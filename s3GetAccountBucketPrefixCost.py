# Get Cost of the storage targettings the objects filtered by bucket name and prefix
# This should help calculate the total cost of the storage within a "folder" 
# or based on wild card "target_prefix*"

# PYTHON EXECUTION
# When executing the source code with python command,
# parameters can be specified:
# parameter 1: bucket name
# parameter 2: prefix

import boto3
import datetime

DEFAULT_REGION = 'us-east-1' #ALWAYS
TARGET_PROFILE = "wasabi"
TARGET_REGION = "ap-northeast-1"

def getS3Client(profileName: str) -> boto3.client:
    # Use the following code to connect using Wasabi profile from .aws/credentials file
    # session = boto3.Session(profile_name="wasabi")
    if profileName == None:
        profileName = "default"
        
    session = boto3.Session(profile_name=profileName)
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key
    region = TARGET_REGION
    endpoint_url = 'https://s3.' + region + '.wasabisys.com'
    # endpoint_url = 'https://s3.wasabisys.com'

    print(region)
    print(endpoint_url)
    #print(aws_access_key_id)
    #print(aws_secret_access_key)

    s3Client = boto3.client('s3',
                    region_name = region,
                    endpoint_url=endpoint_url,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)

    return s3Client

def getS3ClientFromBucket(profileName: str, bucket_name: str):

    # Optin s3 client (set per each bucket)
    optin_s3 = None

    # get s3 client and credentials
    s3Client = getS3Client(profileName)
    session = boto3.Session(profile_name=profileName)
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key

    location = s3Client.get_bucket_location(Bucket=bucket_name)
    
    if location['LocationConstraint'] is not None:
        bucket_region = location['LocationConstraint']
        # create s3 client with the optin region
        endpoint_url = 'https://s3.' + bucket_region + '.wasabisys.com'
        # endpoint_url = 'https://s3.wasabisys.com'
        optin_s3 = boto3.client('s3',
                region_name = bucket_region,
                endpoint_url=endpoint_url,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key)
    else:
        bucket_region = DEFAULT_REGION
        endpoint_url = 'https://s3.' + bucket_region + '.wasabisys.com'
        # endpoint_url = 'https://s3.wasabisys.com'
        optin_s3 = boto3.client('s3',
                region_name = bucket_region,
                endpoint_url=endpoint_url,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key)
        
    print(f"Bucket location: {bucket_region}") 
    return optin_s3

def convert_bytes(byte_size):
    kb_size = byte_size / 1024
    mb_size = kb_size / 1024
    gb_size = mb_size / 1024
    tb_size = gb_size / 1024
    
    return kb_size, mb_size, gb_size, tb_size

def show_size(total_objects_size):
    # get size per unit
    kb, mb, gb, tb = convert_bytes(total_objects_size)

    if tb > 1.0:
        print(f"******** Account Total Consumed Size: {round(tb,4)} TB")
        # print(f"******** Bucket Consumed Total Size: {tb} TB")
    elif gb > 1.0:
        print(f"******** Account Total Consumed Size: {round(gb,4)} GB")
        # print(f"******** Bucket Consumed Total Size: {gb} GB")
    elif mb > 1.0:
        print(f"******** Account Total Consumed Size: {round(mb,4)} MB")
        # print(f"******** Bucket Consumed Total Size: {mb} MB")
    elif kb > 1.0:
        print(f"******** Account Total Consumed Size: {round(kb,4)} KB")
        # print(f"******** Bucket Consumed Total Size: {kb} KB")
    print(f"******** Account Total Consumed Size: {total_objects_size} bytes")

def calculate_cost(total_objects_size, price_per_tb):
    # get size per unit
    kb, mb, gb, tb = convert_bytes(total_objects_size)

    # RCS price $6.99 for TB
    print(f"******** Storage Size: {round(tb,6)} TB")
    print(f"******** Storage Size: {total_objects_size} bytes")
    print(f"******** Storage Cost: {round(tb*price_per_tb,4)} USD")

# Get the account total bucket storage utilization
# with prefix filtering support
# bucket_name: the name of the bucket
# target_prefix: the prefix to be used to filter
def get_acct_bucket_cost(bucket_name, target_prefix):

    # Bucket Consumed object total size
    total_objects_size = 0
    profile = TARGET_PROFILE

    # Get s3 client with the profile specified
    s3 = getS3Client(profile)
    
    print(f'Bucket name: {bucket_name}') 

    # Get s3 client from the bucket (with optin supported)
    optin_s3 = getS3ClientFromBucket(profile, bucket_name)
    
    objects = optin_s3.list_objects_v2(Bucket=bucket_name)
    
    # check whether the bucket is empty or not
    try:
        dict_objects = objects['Contents']
    except KeyError:
        print('No object found... the target bucket is empty!!!')
        return

    for obj in dict_objects:
        key_name = obj['Key']

        if not key_name.startswith(target_prefix):
            print(f"-- skipping {key_name}")
            continue

        print(f"-- {key_name}")

        lastModified = obj['LastModified'].strftime('%A, %B %d, %Y %I:%M %p')
        # print(f"------ {lastModified}")
    
        # sum up the object size that is violating the Bucket Consumed policy
        total_objects_size = total_objects_size + int(obj['Size'])

    print(f"... Target Bucket: {bucket_name}")
    print(f"... Target Prefilx: {target_prefix}")
    print(f"... Total Consumed Size: {total_objects_size} ")

    # Show the storage size 
    # show_size(total_objects_size)

    # RCS price $6.99
    calculate_cost(total_objects_size, 6.99)

# main function
# python3 <*.py> bucket_name prefix
# bucket_name: the name of the target bucket
# prefix: the prefix of the object to be filtered
def main():

    # Specify the default targets    
    # default_target_bucket = "a-cloudnas-bucket-backup"
    default_target_bucket = "kfukaya-bucket-tokyo"
    # default_target_prefix = "shi"
    # default_target_prefix = "ginza/"
    default_target_prefix = "shinagawa/"
    
    import sys

    # Get command-line arguments
    target_bucket = sys.argv[1] if len(sys.argv) > 1 else default_target_bucket
    target_prefix = sys.argv[2] if len(sys.argv) > 2 else default_target_prefix

    get_acct_bucket_cost(target_bucket, target_prefix)

# Executed when called directly
if __name__ == "__main__":
    print(f"Account Bucket Total Consumed Cost (Delete not included) calculation started...")

    # execute main
    main()

    print(f"Account Bucket Total Consumed Cost (Delete not included) calculation completed.")
