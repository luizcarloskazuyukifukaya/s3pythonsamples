# AWS S3 boto3 reference
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/create_user.html

import boto3

session = boto3.Session(profile_name="wasabi")
credentials = session.get_credentials()
aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key

region = 'ap-northeast-1'
endpoint_url = 'https://iam.' + region + '.wasabisys.com'

print(region)
print(endpoint_url)
#print(aws_access_key_id)
#print(aws_secret_access_key)

s3 = boto3.client('iam',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)
def main():
    # Specify the user name to be created
    # NewUserName = "new-user" # with serial number
    # NewUserName = "test-user" # with serial number
    NewUserName = "test500-user" # with serial number
    groupName = "support" # static group name
    # groupName = "TestGroup" # static group name
    # groupName = "TestGroup2" # static group name
    groupName = "test500" # static group name
    
    # Create multiple users
    # user_num = 5
    user_num = 5
    print(f"Creating {user_num} users")

    for num in range(user_num):
        username = f"{NewUserName}{num}"
        print(username)
        print(f"Target group {groupName}")
        
        CreateUserInGroup(username, groupName)
    
    print("Done")

def CreateUserInGroup(userName, groupName):    
    # Check whether the user already exist
    no_user_creation = True

    # List all users
    r = s3.list_users()
    for user in r["Users"]:
        if user["UserName"] == userName:
            print(f'{userName} already exist!')
            no_user_creation = False
    # print(type(r))
    # print(r)
        
    if no_user_creation:
        print(f"No user found with the name of {userName}")

        # Create new user now
        r = s3.create_user(
        #    Path='string',
            UserName=userName,
        #    PermissionsBoundary='string',
            Tags=[
                {
                    'Key': 'UserName',
                    'Value': f'{userName}'
                },
            ]
        )        
        # print(type(r))
        # print(r)

    # User could be already created but may not be in the group        
    print(f"Now add to the group {groupName}")
    
    r = s3.add_user_to_group(
        GroupName = groupName,
        UserName = userName
        )
    # print(type(r))
    # print(r)

if __name__ == '__main__':
    main()


