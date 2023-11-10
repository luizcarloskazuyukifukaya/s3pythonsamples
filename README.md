# s3pythonsamples
Samples of Python code with AWS SDK boto3 targetting Wasabi Hot Cloud Storage.

(NOTE) The sample source code includes Wasabi specific endpoints URL and also is written with assumption that the 'wasabi' profile is created in the AWS configuration file.

Please refer to the following AWS document explaining details of the configuration files:
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

The following is a sample of the confi file for the use with the sample code provided here:
--------------------------------------------------------
~/.aws/config
--------------------------------------------------------
[default]
region = ap-northeast-1
[profile wasabi]
region = ap-northeast-1
s3 =
    endpoint_url = https://s3.ap-northeast-1.wasabisys.com
s3api =
    endpoint_url = https://s3.ap-northeast-1.wasabisys.com
[profile NVirginia1]
region = us-east-1
s3 =
    endpoint_url = https://s3.us-east-1.wasabisys.com
s3api =
    endpoint_url = https://s3.us-east-1.wasabisys.com
[profile NVirginia2]
region = us-east-2
s3 =
    endpoint_url = https://s3.us-east-2.wasabisys.com
s3api =
    endpoint_url = https://s3.us-east-2.wasabisys.com
[profile Texas]
region = us-central-1
s3 =
    endpoint_url = https://s3.us-central-1.wasabisys.com
s3api =
    endpoint_url = https://s3.us-central-1.wasabisys.com
[profile Oregon]
region = us-west-1
s3 =
    endpoint_url = https://s3.us-west-1.wasabisys.com
s3api =
    endpoint_url = https://s3.us-west-1.wasabisys.com
[profile Toronto]
region = ca-central-1
s3 =
    endpoint_url = https://s3.ca-central-1.wasabisys.com
s3api =
    endpoint_url = https://s3.ca-central-1.wasabisys.com
[profile Amsterdam]
region = eu-central-1
s3 =
    endpoint_url = https://s3.eu-central-1.wasabisys.com
s3api =
    endpoint_url = https://s3.eu-central-1.wasabisys.com
[profile Frankfurt]
region = eu-central-2
s3 =
    endpoint_url = https://s3.eu-central-2.wasabisys.com
s3api =
    endpoint_url = https://s3.eu-central-2.wasabisys.com
[profile London]
region = eu-west-1
s3 =
    endpoint_url = https://s3.eu-west-1.wasabisys.com
s3api =
    endpoint_url = https://s3.eu-west-1.wasabisys.com
[profile Paris]
region = eu-west-2
s3 =
    endpoint_url = https://s3.eu-west-2.wasabisys.com
s3api =
    endpoint_url = https://s3.eu-west-2.wasabisys.com
[profile Tokyo]
region = ap-northeast-1
s3 =
    endpoint_url = https://s3.ap-northeast-1.wasabisys.com
s3api =
    endpoint_url = https://s3.ap-northeast-1.wasabisys.com
[profile Osaka]
region = ap-northeast-2
s3 =
    endpoint_url = https://s3.ap-northeast-2.wasabisys.com
s3api =
    endpoint_url = https://s3.ap-northeast-2.wasabisys.com
[profile Singapore]
region = ap-southeast-1
s3 =
    endpoint_url = https://s3.ap-southeast-1.wasabisys.com
s3api =
    endpoint_url = https://s3.ap-southeast-1.wasabisys.com
[profile Sydney]
region = ap-southeast-2
s3 =
    endpoint_url = https://s3.ap-southeast-2.wasabisys.com
s3api =
    endpoint_url = https://s3.ap-southeast-2.wasabisys.com
[profile kfukaya]
region = ap-northeast-1
s3 =
    endpoint_url = https://s3.ap-northeast-1.wasabisys.com
s3api =
    endpoint_url = https://s3.ap-northeast-1.wasabisys.com
[profile wcn]
region = ap-northeast-1
s3 =
    endpoint_url = https://s3.ap-northeast-1.wasabisys.com
s3api =
    endpoint_url = https://s3.ap-northeast-1.wasabisys.com
[profile AusAWS]
region = ap-southeast-2
s3 =
    endpoint_url = https://s3.ap-southeast-2.amazonaws.com
s3api =
    endpoint_url = https://s3.ap-southeast-2.amazonaws.com
[profile AusWasabi]
region = ap-southeast-2
s3 =
    endpoint_url = https://s3.ap-southeast-2.wasabisys.com
s3api =
    endpoint_url = https://s3.ap-southeast-2.wasabisys.com
[plugins]
endpoint = awscli_plugin_endpoint
--------------------------------------------------------
~/.aws/config EOF
--------------------------------------------------------

The following is a sample of the credentials file for the use with the sample code provided here:
--------------------------------------------------------
~/.aws/credentials
--------------------------------------------------------
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
[wasabi]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
[NVirginia1]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
[NVirginia2]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
[Texas]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
[Oregon]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
[Toronto]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
[Amsterdam]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
[Frankfurt]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
[London]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
[Paris]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
[Tokyo]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
[Osaka]
aws_access_key_id = YOUR_ACCESS_KEY_ID
--------------------------------------------------------
~/.aws/credentials EOF
--------------------------------------------------------
