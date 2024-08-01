# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/delete_bucket.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-bucket-policies.html

import logging
import boto3
from botocore.exceptions import ClientError

import json

# define the default region as a global variable
# DEFAULT_REGION = 'ap-northeast-1'
DEFAULT_REGION = 'us-east-1'
DEFAULT_S3_DOMAIN = '.wasabisys.com'
# DEFAULT_PROFILE = 'wasabi'
DEFAULT_PROFILE = 'NVirginia1'

# Create an S3 bucket
def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Wasabi URL
    session = boto3.Session(profile_name=DEFAULT_PROFILE)
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key
    
    # Check if the region parameter is specified
    if region is None:
        region = DEFAULT_REGION
    
    endpoint_url = 'https://s3.' + region + DEFAULT_S3_DOMAIN

    print(region)
    print(endpoint_url)
    #print(aws_access_key_id)
    #print(aws_secret_access_key)

    s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

    # Create bucket
    try:
        if region is None:
            s3.create_bucket(Bucket=bucket_name)
        else:
            location = {'LocationConstraint': region}
            s3.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        print(e)
        return False
    return True

# List existing buckets
def list_buckets():
    """List existing bucket for the account

    :return: List of buckets
    """

    # Wasabi URL
    session = boto3.Session(profile_name=DEFAULT_PROFILE)
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key

    # region
    region = DEFAULT_REGION
    
    endpoint_url = 'https://s3.' + region + DEFAULT_S3_DOMAIN

    print(DEFAULT_PROFILE)
    print(region)
    print(endpoint_url)
    print(aws_access_key_id)
    print(aws_secret_access_key)

    s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)
    
    # Retrieve the list of existing buckets
    response = s3.list_buckets()

    # Output the bucket names
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')
    
    return response['Buckets']

# Delete existing bucket
def delete_bucket(bucket_name):
    """Delete existing bucket for the account

    :return: None
    """

    # Wasabi URL
    session = boto3.Session(profile_name=DEFAULT_PROFILE)
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key

    # region
    region = DEFAULT_REGION
    
    endpoint_url = 'https://s3.' + region + DEFAULT_S3_DOMAIN

    print(region)
    print(endpoint_url)
    #print(aws_access_key_id)
    #print(aws_secret_access_key)

    s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)
    
    # Retrieve the list of existing buckets
    response = s3.delete_bucket(bucket_name)

# Set S3 bucket policy
def set_bucket_policy(bucket_name, bucket_policy):
    """Set the S3 bucket policy

    :param bucket_name: Bucket to create
    :param bucket_policy: Bucket policy (dict) to be set
    :return: Bucket policy in JSON (dict)
    """

    # Wasabi URL
    session = boto3.Session(profile_name=DEFAULT_PROFILE)
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key
    
    region = DEFAULT_REGION
    
    endpoint_url = 'https://s3.' + region + DEFAULT_S3_DOMAIN

    print(region)
    print(endpoint_url)
    #print(aws_access_key_id)
    #print(aws_secret_access_key)

    # Check if bucket_policy is specified
    if(len(bucket_policy) == 0):
        print("Bucket policy is not specified")
        return bucket_policy
        
    # Convert the policy from JSON dict to string
    str_bucket_policy = json.dumps(bucket_policy)

    s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

    # Set the new policy
    s3.put_bucket_policy(Bucket=bucket_name, Policy=str_bucket_policy)
    
    print(str_bucket_policy)

    # return Bucket Policy in JSON (dict)
    #return bucket_policy
    return json.loads(str_bucket_policy)

# Get S3 bucket policy
def get_bucket_policy(bucket_name):
    """Get the S3 bucket policy

    :param bucket_name: Bucket to create
    :return: Bucket policy in JSON
    """

    # Wasabi URL
    session = boto3.Session(profile_name=DEFAULT_PROFILE)
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key
    
    region = DEFAULT_REGION
    
    endpoint_url = 'https://s3.' + region + DEFAULT_S3_DOMAIN

    print(region)
    print(endpoint_url)
    #print(aws_access_key_id)
    #print(aws_secret_access_key)

    s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

    result = s3.get_bucket_policy(Bucket=bucket_name)
    bucket_policy = result['Policy']
    
    print(bucket_policy)
    
    return bucket_policy

# Delete S3 bucket policy
def delete_bucket_policy(bucket_name):
    """Delete the S3 bucket policy

    :param bucket_name: Bucket to create
    :return: True if bucket policy is delete, else False
    """

    # Wasabi URL
    session = boto3.Session(profile_name=DEFAULT_PROFILE)
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key
    
    region = DEFAULT_REGION
    
    endpoint_url = 'https://s3.' + region + DEFAULT_S3_DOMAIN

    print(region)
    print(endpoint_url)
    #print(aws_access_key_id)
    #print(aws_secret_access_key)

    s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

    s3.delete_bucket_policy(Bucket=bucket_name)
    
    print(f"{bucket_name} bucket policy deleted.")
    
    return True

# Create an S3 Object Lock bucket
def create_object_lock_bucket(bucket_name, region=None):
    """Create an S3 Object Lock bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Wasabi URL
    session = boto3.Session(profile_name=DEFAULT_PROFILE)
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key
    
    # Check if the region parameter is specified
    if region is None:
        region = DEFAULT_REGION
    
    endpoint_url = 'https://s3.' + region + DEFAULT_S3_DOMAIN

    print(region)
    print(endpoint_url)
    #print(aws_access_key_id)
    #print(aws_secret_access_key)

    s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

    # Create bucket
    try:
        if region is None:
            s3.create_bucket(
                Bucket=bucket_name,
                ObjectLockEnabledForBucket=True
                )
        else:
            location = {'LocationConstraint': region}
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration=location
                )
    except ClientError as e:
        print(e)
        return False
    return True