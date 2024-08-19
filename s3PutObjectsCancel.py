# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/put_object.html

import boto3

def create_keys(bucket):

    target_bucket = bucket
    print(target_bucket)
    # fix object file as a template
    target_file = "data/object.txt"
    # target number of objects to be created
    max_keys = 10
    target_key_base = "dummy-key"
        
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

    for i in range(max_keys):

        key_name = f"{target_key_base}{i+1}.data"

        # upload an object (.data/sample_data.csv)
        r = s3.put_object(
            Body=target_file,
            Bucket=target_bucket,
            Key=key_name,
            # ServerSideEncryption='AES256',
            # StorageClass='STANDARD_IA',
        )

        # print(r)
        print(f"{i}: {key_name} key created on {target_bucket}.")

def delete_keys(bucket):

    target_bucket = bucket
    print(target_bucket)
    # fix object file as a template
    target_file = "data/object.txt"
    # target number of objects to be created
    max_keys = 10
    target_key_base = "dummy-key"
        
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

    for i in range(max_keys):

        key_name = f"{target_key_base}{i+1}.data"

        # delete an object
        r = s3.delete_object(
            Bucket=target_bucket,
            Key=key_name,
        )

        # print(r)
        print(f"{i}: {key_name} key deleted from {target_bucket}.")


def main():
    # Define the target bucket and prefix
    target_bucket = "kfukaya-put-objects"

    # create_keys(target_bucket)
    delete_keys(target_bucket)


if __name__ == '__main__':
    main()