import boto3
import datetime

JST = datetime.timezone(datetime.timedelta(hours=9), "JST")
# https://qiita.com/nagataaaas/items/1582cebb51962f9a80e9

def convert_bytes(byte_size):
    kb_size = byte_size / 1024
    mb_size = kb_size / 1024
    gb_size = mb_size / 1024
    tb_size = gb_size / 1024
    
    return kb_size, mb_size, gb_size, tb_size

# main function
def main():
    # Bucket Consumed object total size
    total_objects_size = 0

    # Use the following code to connect using Wasabi profile from .aws/credentials file
    # session = boto3.Session(profile_name="wasabi")
    session = boto3.Session(profile_name="wasabi")
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key
    DEFAULT_REGION = 'us-east-1' #ALWAYS
    region = 'ap-northeast-1'
    endpoint_url = 'https://s3.' + region + '.wasabisys.com'
    # endpoint_url = 'https://s3.wasabisys.com'

    print(region)
    print(endpoint_url)
    #print(aws_access_key_id)
    #print(aws_secret_access_key)

    s3 = boto3.client('s3',
                    region_name = region,
                    endpoint_url=endpoint_url,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)

    # List buckets
    response = s3.list_buckets()
    # Output the bucket names
    print('Listing all objects within a existing bucket ....')

    for bucket in response['Buckets']:
        bucket_name = bucket["Name"]
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
            
        print(f"Bucket location: {bucket_region}") 

        objects = optin_s3.list_objects_v2(Bucket=bucket["Name"])
        #print(objects['Name']) 
        #print(type(objects))
        
        # check whether the bucket is empty or not
        try:
            dict_objects = objects['Contents']
        except KeyError:
            # print('No object found... the target bucket is empty!!!')
            continue

        #print(type(objects['Contents']))
        for obj in dict_objects:
            # print(f"-- {obj['Key']}")
            lastModified = obj['LastModified'].strftime('%A, %B %d, %Y %I:%M %p')
            # print(f"------ {lastModified}")
        
            # sum up the object size that is violating the Bucket Consumed policy
            total_objects_size = total_objects_size + int(obj['Size'])

        print(f"... Bucket's Total Consumed Size: {total_objects_size} ")

    kb,mb,gb,tb = convert_bytes(total_objects_size)
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

# Executed when called directly
if __name__ == "__main__":
    print(f"Account Total Consumed Size calculation started...")

    # execute main
    main()

    print(f"Account Total Consumed Size calculation completed.")
