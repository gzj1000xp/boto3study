import boto3

# 创建所需参数
GROUPID = 'sg-'

ec2 = boto3.client('ec2')

response = ec2.authorize_security_group_ingress(
    GroupId = GROUPID,
    IpPermissions=[
        {'IpProtocol': 'tcp',
         'FromPort': 8822,
         'ToPort': 8822,
         'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
    ],

)

print(response)
