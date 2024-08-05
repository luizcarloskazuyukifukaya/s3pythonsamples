# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/upload_file.html 

import boto3
from datetime import datetime

# Print time stamp
def show_current_time():
    now = datetime.now() # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    print("date and time:", date_time)

def upload_data(bucket):

    print(bucket)

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

    for i in range(50):
        target_directory = "./data"
        key_name = f"dummy-{i+1}.data"
        target_file = f"{target_directory}/{key_name}"

        print(f"Uploading {target_file} ...")
        
        # upload an object (.data/sample_data.csv)
        r = s3.upload_file(
            target_file,
            bucket,
            key_name,
        )

    print(r)

    print(type(r))

def main():
    # Define the target bucket and prefix
    target_bucket = "restec-bucket-tokyo"
    # target_bucket = "restec-bucket-frankfurt"
    # target_bucket = "restec-bucket-oregon"

    # show time before upload
    show_current_time()

    upload_data(target_bucket)

    # show time after upload
    show_current_time()

if __name__ == '__main__':
    main()