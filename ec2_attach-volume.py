import boto3


INSTANCEID = ''
VOLUMEID = ''
DEVICENAME = ''
DRYRUN = True

ec2 = boto3.resource('ec2')
instance = ec2.Instance(INSTANCEID)

response = instance.attach_volume(
    Device=DEVICENAME,
    VolumeId=VOLUMEID,
    DryRun=DRYRUN
)