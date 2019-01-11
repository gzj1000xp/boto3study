import boto3


INSTANCEID = ''

ec2 = boto3.resource('ec2')
instance = ec2.Instance(INSTANCEID)

print(instance.volumes.all())
