import boto3
import sys

# define global variables
DEFAULT_REGION = 'us-east-1' #ALWAYS
default_target_region = 'ap-southeast-2'
default_target_bucket = "centr-source-bucket"
default_timestamp_flag = "false"
default_prefix = ""
default_verbose = "false"
default_price_per_1tb = 6.99

# Get command-line arguments
target_bucket = sys.argv[1] if len(sys.argv) > 1 else default_target_bucket
target_region = sys.argv[2] if len(sys.argv) > 2 else default_target_region
timestamp_flag = sys.argv[3] if len(sys.argv) > 3 else default_timestamp_flag
target_prefix = sys.argv[4] if len(sys.argv) > 4 else default_prefix

# print(f"Input target_price: {type(sys.argv[5])}")

target_price = float(sys.argv[5]) if len(sys.argv) > 5 else default_price_per_1tb
# print(f"target_price: {type(target_price)}")

target_verbose = sys.argv[6] if len(sys.argv) > 6 else default_verbose

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
        print(f"Total Size: {round(tb,4)} TB")
        # print(f"Total Size: {tb} TB")
    elif gb > 1.0:
        print(f"Total Size: {round(gb,4)} GB")
        # print(f"Total Size: {gb} GB")
    elif mb > 1.0:
        print(f"Total Size: {round(mb,4)} MB")
        # print(f"Total Size: {mb} MB")
    elif kb > 1.0:
        print(f"Total Size: {round(kb,4)} KB")
        # print(f"Total Size: {kb} KB")
    print(f"Total Size: {total_objects_size} bytes")

def calculate_cost(total_objects_size, price_per_tb):
    # get size per unit
    kb, mb, gb, tb = convert_bytes(total_objects_size)

    # RCS price $6.99 for TB
    # print(f"Storage Size: {round(tb,4)} TB")
    # print(f"Storage Cost Type: {type(round(tb,4))}")
    print(f"Storage Price per TB: {price_per_tb}")
    print(f"Storage Price: {round(tb*price_per_tb,4)} USD")

def search_targets_and_calculate_cost():
    # Use the following code to connect using Wasabi profile from .aws/credentials file

    # session = boto3.Session(profile_name="wasabi")
    session = boto3.Session(profile_name="wasabi")
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key

    endpoint_url = 'https://s3.' + target_region + '.wasabisys.com'
    # endpoint_url = 'https://s3.wasabisys.com'

    # print(target_region)
    # print(endpoint_url)
    #print(aws_access_key_id)
    #print(aws_secret_access_key)

    s3 = boto3.client('s3',
                    endpoint_url=endpoint_url,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)

    bucket_name = target_bucket
    print(f'Bucket name: {bucket_name}') 

    # Optin s3 client (set per each bucket)
    optin_s3 = None

    location = s3.get_bucket_location(Bucket=bucket_name)

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
        
    # print(f"Bucket location: {bucket_region}") 

    # This is limited to 1000
    # objects = optin_s3.list_objects_v2(Bucket=bucket_name)
    # #print(objects['Name']) 
    # #print(type(objects))

    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket_name, Prefix="")

    counts = 0
    total_size = 0
    for page in pages:
        # check whether the bucket is empty or not
        try:
            dict_objects = page['Contents']
            for obj in dict_objects:
                key_name = obj['Key']
                
                # filter Key with prefix
                if not key_name.startswith(target_prefix):
                    if target_verbose == "true":
                        print(f"-- skipping {key_name}")
                    continue
                
                lastModified = obj['LastModified'].strftime('%A, %B %d, %Y %I:%M %p')
                if timestamp_flag == "true":
                    print(f'{obj["Key"]}, {obj["Size"]}, "{lastModified}"')
                else:
                    print(f'{obj["Key"]}, obj["Size"]')

                # print(f"Size: {obj["Size"]}")
                total_size = total_size + obj['Size']                
                counts = counts + 1
        except KeyError:
            print('No object found... the target bucket is empty!!!')

    print(f"Target Bucket: {bucket_name}")
    print(f"Target Prefilx: {target_prefix}")

    print(f"Total objects {counts}")

    # show total size
    show_size(total_size)

        # Storage price per TB is passed
    calculate_cost(total_size, target_price)


def main():
    # Get all targets and calculate the cost (USD)
    search_targets_and_calculate_cost()

if __name__ == "__main__":
    main()
