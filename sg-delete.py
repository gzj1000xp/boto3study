import boto3
from botocore.exceptions import ClientError


# 创建所需参数
GROUPID = 'sg-'

ec2 = boto3.client('ec2')

try:
    response = ec2.delete_security_group(GroupId=GROUPID)
    print('Security Group Deleted')
except ClientError as e:
    print(e)
