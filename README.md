# s3pythonsamples
Samples of Python code with AWS SDK boto3 targetting Wasabi Hot Cloud Storage.

(NOTE) The sample source codes include Wasabi specific endpoints URL and also are written with assumption that the 'wasabi' profile is created in the AWS CLI configuration file.

Please refer to the following AWS document explaining details of the configuration files:
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

## Quick Start
### Runtime Setup
First of all, you need to install Python in your environment. So, please follow the [instruction](https://www.python.org/downloads/) given for your specific environment.

Next, you should install AWS SDK boto3 using the following command:
```
pip install boto3
```
### Profile and region
Then, set up a default region and the profile for Wasabi (in ~/.aws/config):
```~/.aws/config
[default]
region = ap-northeast-1
[profile wasabi]
region = ap-northeast-1
s3 =
    endpoint_url = https://s3.ap-northeast-1.wasabisys.com
s3api =
    endpoint_url = https://s3.ap-northeast-1.wasabisys.com
[plugins]
endpoint = awscli_plugin_endpoint
```

### Credentials
Then, specify the credentials provided per account to access Wasabi S3 (in ~/.aws/credentials):
```~/.aws/credentials
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
[wasabi]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

### Clone GitHub Repository
Then, you will need to clone this GitHub repository to your local environment, so you can execute the codes.
 Select any folder/directory where you want to clone the samples with the following command:
 
```
git clone https://github.com/luizcarloskazuyukifukaya/s3pythonsamples
cd s3pythonsamplesboto3
```
### Python Code Execution
Now, you are ready to start executing the samples with the following command:
```Python
python s3ShowWasabiVersion.py
```
**(Note)** Depending on your environment, "python" command could be different, for example, for Linux it could be "python3".

## References
### Wasabi API Access Key Set
For details on how to create the Access Key and the Secret Key, Please check the article provided at Wasabi Knowledge Base.
- [Creating a Wasabi API Access Key Set](https://knowledgebase.wasabi.com/hc/en-us/articles/360019677192-Creating-a-Wasabi-API-Access-Key-Set)

### AWS SDK document
Please refer to AWS SDK document for details of Python Boto3.
- [AWS SDK for Python (Boto3)](https://aws.amazon.com/sdk-for-python/ "AWS SDK")
