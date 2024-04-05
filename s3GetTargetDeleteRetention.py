import boto3
import datetime

JST = datetime.timezone(datetime.timedelta(hours=9), "JST")
# https://qiita.com/nagataaaas/items/1582cebb51962f9a80e9

def calculate_time_difference(object_timestamp_obj, origin_timestamp_obj):
    # calculate the time differences in hours with the current time (given as a parameter also)
    # object_timestamp_obj: the datetime of the target object
    # origin_timestamp_obj: the point of time (usually calculated from the current time)
    # Note: The both input should be in datetime object
    
    # If need to convert from string format 'YYYY-MM-DD HH:MM:SS'
    # object_timestamp_obj = datetime.strptime(object_timestamp, '%Y-%m-%d %H:%M:%S')
    
    # Get the current time
    current_time = origin_timestamp_obj
    
    # TypeError: can't subtract offset-naive and offset-aware datetimes
    
    # Calculate the difference in time
    time_difference = current_time - object_timestamp_obj
    # print(f">>>>>>>> Delta time (type): {type(time_difference)}")
    # print(f">>>>>>>> Delta time: {time_difference}")

    # Convert the time difference to hours
    difference_in_hours = time_difference.total_seconds() / 3600
    
    return difference_in_hours

def check_delete_retention_violation(obj, delete_retention_days, target_datetime):
    # Check whether the given object (boto3 object format) violate the delete retention policy or not
    # obj: the target object (boto3 s3 object)
    # delete_retention_days: 30 days or 90 days expected
    # target_datetime: the current time (datetime)
    # (note) This value will be used to check if the target object violate the delete retention policy or not
    # [RETURN]
    # True: when violates
    # False: when does not violate
        
    # Calculate the difference in time
    time_difference_in_hours = calculate_time_difference(
        obj['LastModified'],
        target_datetime)
    
    target_delete_retention_in_hours = delete_retention_days * 24

    if time_difference_in_hours < target_delete_retention_in_hours:
        # When less than the target_delete_retention_in_hours
        # VIOLATE: True
        return True
    else:
        # When greater or equal to the target_delete_retention_in_hours
        # NO VIOLATION: False
        return False

def convert_bytes(byte_size):
    kb_size = byte_size / 1024
    mb_size = kb_size / 1024
    gb_size = mb_size / 1024
    tb_size = gb_size / 1024
    
    return kb_size, mb_size, gb_size, tb_size

# main function
def main():
    # Delete Retention object total size
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

    # Get the current time
    # Against this time the delta time will be calculated to determine the delete retention violation
    current_time = datetime.datetime.now(JST)
    current_time_str = current_time.strftime('%A, %B %d, %Y %I:%M %p')
    print(f"[Current date and time] : {current_time_str}")

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
            print('No object found... the target bucket is empty!!!')
            continue

        # Delete retention: 30 days (RCS, used this time)
        # Delete retention: 90 days (PayGO)
        retention_days = 30

        #print(type(objects['Contents']))
        for obj in dict_objects:
            # print(f"-- {obj['Key']}")
            lastModified = obj['LastModified'].strftime('%A, %B %d, %Y %I:%M %p')
            # print(f"------ {lastModified}")
        
            # check delete retention violation
            delete_retention_check = check_delete_retention_violation(obj, retention_days, current_time)
            if delete_retention_check is True:
                print(f"Object Key name: {obj['Key']}")
                print(f"Object Last Modified Time: {lastModified} [violating {retention_days} days]")
                print(f"Object Size: {obj['Size']} ")
                
                # sum up the object size that is violating the delete retention policy
                total_objects_size = total_objects_size + int(obj['Size'])
                print(f"... Accumulated Total Size: {total_objects_size} ")

    # Show results
    print(f"******** Calculated based on Date: {current_time_str} ")

    kb,mb,gb,tb = convert_bytes(total_objects_size)
    if tb > 1.0:
        print(f"******** Delete Retention Total Size: {round(tb,4)} TB")
        # print(f"******** Delete Retention Total Size: {tb} TB")
    elif gb > 1.0:
        print(f"******** Delete Retention Total Size: {round(gb,4)} GB")
        # print(f"******** Delete Retention Total Size: {gb} GB")
    elif mb > 1.0:
        print(f"******** Delete Retention Total Size: {round(mb,4)} MB")
        # print(f"******** Delete Retention Total Size: {mb} MB")
    elif kb > 1.0:
        print(f"******** Delete Retention Total Size: {round(kb,4)} KB")
        # print(f"******** Delete Retention Total Size: {kb} KB")

    print(f"******** Delete Retention Total Size: {total_objects_size} bytes")

# Executed when called directly
if __name__ == "__main__":
    print(f"Delete Retention check started...")

    # execute main
    main()

    print(f"Delete Retention check completed.")
