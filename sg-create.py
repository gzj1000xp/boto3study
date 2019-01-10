import boto3
from botocore.exceptions import ClientError


# 创建所需参数
DESCRIPTION = 'for test purpose'
GROUPNAME = 'test'
VPCID = ''
DRYRUN = False

ec2 = boto3.client('ec2')

response = ec2.create_security_group(
    Description=DESCRIPTION,
    GroupName=GROUPNAME,
    VpcId=VPCID,
    DryRun=DRYRUN
)

security_group_id = response['GroupId']
print(security_group_id)

try:
    data = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 8888,
             'ToPort': 8888,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 5555,
             'ToPort': 5555,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])
    print('Ingress Successfully Set %s' % data)
except ClientError as e:
    print(e)
