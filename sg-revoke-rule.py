import boto3


# 创建所需参数
GROUPID = 'sg-'
GROUPNAME = 'test'
DRYRUN = False

ec2 = boto3.client('ec2')

response = ec2.revoke_security_group_ingress(
    GroupId=GROUPID,
    IpPermissions=[
        {'IpProtocol': 'tcp',
         'FromPort': 5555,
         'ToPort': 5555,
         'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
    ],
)

print(response)
