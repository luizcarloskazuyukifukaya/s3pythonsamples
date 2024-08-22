# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/select_object_content.html

import boto3

def show_wasabi_system_details(region):
    # session = boto3.Session(profile_name="wasabi")
    session = boto3.Session(profile_name="wasabi")
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key

    # default Wasabi US East 1 (N. Virginia)
    endpoint_url = 'https://s3.' + region + '.wasabisys.com'

    print(region)
    print(endpoint_url)
    #print(aws_access_key_id)
    #print(aws_secret_access_key)

    #s3 = boto3.client('s3')
    s3 = boto3.client('s3',
            region_name=region,
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key)

    #print(s3)
    # Retrieve the list of existing buckets
    r = s3.list_buckets()

    print('Wasabi Object Storage Server version: ' + (r['ResponseMetadata']['HTTPHeaders']['server']))
    print('Current Date: ' + (r['ResponseMetadata']['HTTPHeaders']['date']))
    
    #sqs = boto3.resource('sqs')
    #print(sqs)
    #queue = sqs.Queue(url=endpoint_url)
    #print(queue.url)


# Main function defined here
import sys

def main():
    #-----------------------------------------------------    
    wasabi_regions = [
                'us-east-1', 
                'us-east-2', 
                'us-central-1', 
                'us-west-1', 
                'ca-central-1', 
                'eu-central-1', 
                'eu-central-2', 
                'eu-west-1', 
                'eu-west-2', 
                'eu-south-1', 
                'ap-northeast-1', 
                'ap-northeast-2', 
                'ap-southeast-1', 
                'ap-southeast-2'
                ]
    
    if len(sys.argv) == 1:
        # Show all regions
        for target_region in wasabi_regions:
            show_wasabi_system_details(target_region)
            print('---------------------------')
    else:
        regionNum = len(sys.argv) - 1 # Number of parameters = number of regions
        for i in range(regionNum):
            target_region = sys.argv[i+1] # target region specified by the parameter
            try:
                wasabi_regions.index(target_region)
                show_wasabi_system_details(target_region)
            except ValueError:
                # When the target_region is not included in the wasabi_regions[]
                print(f"[INFO] {target_region} does not exist")
            print('---------------------------')
    print('Done')

# for the execution of this script only
if __name__ == "__main__":
    main()
