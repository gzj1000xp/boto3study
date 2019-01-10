import boto3
import json

SGID = 'sg-'

ec2 = boto3.resource('ec2')
sg = ec2.SecurityGroup(SGID)

print(sg.description)
print(sg.group_name)
# print(sg.group_id)
print(sg.ip_permissions)

for i in range(len(sg.ip_permissions)):
    sgipjs = json.dumps(sg.ip_permissions[i])
    print(sgipjs)

print(sg.ip_permissions_egress)
print(sg.tags)


