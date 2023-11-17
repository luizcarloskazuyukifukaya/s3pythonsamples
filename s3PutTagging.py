# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/put_object_tagging.html#

import boto3

# Define the target bucket and prefix
#target_bucket = "kfukaya-tagging"
target_bucket = "kfukaya-sydney-bucket"
target_file = "test.txt"

# Specify the tagging (dict)
target_tagging = { 'TagSet': [
                                { 'Key': 'Key1', 'Value': 'Value1'},
                                { 'Key': 'Key2', 'Value': 'Value2'},
                                { 'Key': 'Key3', 'Value': 'Value3'},
                                { 'Key': 'Key4', 'Value': 'Value4'},
                                { 'Key': 'Key5', 'Value': 'Value5'},
                                { 'Key': 'Key6', 'Value': 'Value6'},
                                { 'Key': 'Key7', 'Value': 'Value7'},
                                { 'Key': 'Key8', 'Value': 'Value8'},
                                { 'Key': 'Key9', 'Value': 'Value9'},
                                { 'Key': 'Key10', 'Value': 'Value10'},
                                { 'Key': 'Key11', 'Value': 'Value11'},
                                { 'Key': 'Key12', 'Value': 'Value12'},
                                { 'Key': 'Key13', 'Value': 'Value13'},
                                { 'Key': 'Key14', 'Value': 'Value14'},
                                { 'Key': 'Key15', 'Value': 'Value15'},
                                { 'Key': 'Key16', 'Value': 'Value16'},
                                { 'Key': 'Key17', 'Value': 'Value17'},
                                { 'Key': 'Key18', 'Value': 'Value18'},
                                { 'Key': 'Key19', 'Value': 'Value19'},
                                { 'Key': 'Key20', 'Value': 'Value20'},
                                { 'Key': 'Key21', 'Value': 'Value21'},
                                { 'Key': 'Key22', 'Value': 'Value22'},
                                { 'Key': 'Key23', 'Value': 'Value23'},
                                { 'Key': 'Key24', 'Value': 'Value24'},
                                { 'Key': 'Key25', 'Value': 'Value25'},
#                                { 'Key': 'Key26', 'Value': 'Value26'},
                            ]
                }

print(target_bucket)
print(target_file)

session = boto3.Session(profile_name="wasabi")
credentials = session.get_credentials()
aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key
##region = 'ap-northeast-1'
region = 'ap-southeast-2'
endpoint_url = 'https://s3.' + region + '.wasabisys.com'

print(region)
print(endpoint_url)
print(aws_access_key_id)
print(aws_secret_access_key)

s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

r = s3.put_object_tagging(
    Bucket=target_bucket,
    Key=target_file,
    Tagging=target_tagging
)

print(type(r))
print(r)