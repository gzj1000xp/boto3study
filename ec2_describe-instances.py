import boto3
import json

Filters = [
    {
        'Name': 'tag:Env',
        'Values': ['test']
    },
    {
        'Name': 'tag:Name',
        'Values': ['*']
    }
]
InstanceIds = []
Dryrun = True


ec2 = boto3.client('ec2')
response = ec2.describe_instances(Filters=Filters)

# print(response)
print(json.dumps(response, indent=4, sort_keys=True, default=str))