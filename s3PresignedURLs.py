# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html

import logging
import boto3
from botocore.exceptions import ClientError

# Simple presigned URLs to download an object
def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Wasabi URL
    session = boto3.Session(profile_name="wasabi")
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key
    region = 'ap-northeast-1'
    endpoint_url = 'https://s3.' + region + '.wasabisys.com'

    print(region)
    print(endpoint_url)
    print(aws_access_key_id)
    #print(aws_secret_access_key)

    s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)


    # Generate a presigned URL for the S3 object
    try:
        response = s3.generate_presigned_url('get_object',
                                            Params={'Bucket': bucket_name,
                                            'Key': object_name},
                                            ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    print(response)

    # The response contains the presigned URL
    return response


# Using presigned URLs to perform other S3 operations
def create_presigned_url_expanded(client_method_name, method_parameters=None,
                                  expiration=3600, http_method=None):
    """Generate a presigned URL to invoke an S3.Client method

    Not all the client methods provided in the AWS Python SDK are supported.

    :param client_method_name: Name of the S3.Client method, e.g., 'list_buckets'
    :param method_parameters: Dictionary of parameters to send to the method
    :param expiration: Time in seconds for the presigned URL to remain valid
    :param http_method: HTTP method to use (GET, etc.)
    :return: Presigned URL as string. If error, returns None.
    """

    # Wasabi URL
    session = boto3.Session(profile_name="wasabi")
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key
    region = 'ap-northeast-1'
    endpoint_url = 'https://s3.' + region + '.wasabisys.com'

    print(region)
    print(endpoint_url)
    print(aws_access_key_id)
    #print(aws_secret_access_key)

    s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

    # Generate a presigned URL for the S3 client method
    try:
        response = s3.generate_presigned_url(ClientMethod=client_method_name,
                                                    Params=method_parameters,
                                                    ExpiresIn=expiration,
                                                    HttpMethod=http_method)
    except ClientError as e:
        logging.error(e)
        return None

    print(response)

    # The response contains the presigned URL
    return response


# Generating a presigned URL to upload a file
def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """
    # Wasabi URL
    session = boto3.Session(profile_name="wasabi")
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key
    region = 'ap-northeast-1'
    endpoint_url = 'https://s3.' + region + '.wasabisys.com'

    print(region)
    print(endpoint_url)
    print(aws_access_key_id)
    #print(aws_secret_access_key)

    s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

    # Generate a presigned S3 POST URL
    try:
        response = s3.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    print(response['url'])
    print(response)
    
    # The response contains the presigned URL and required fields
    return response