import boto3
import sys


InstanceIds = [sys.argv[1]]
Dryrun = True


ec2 = boto3.client('ec2')
response = ec2.describe_instances(InstanceIds=InstanceIds)

# print(len(response['Reservations']))
for i in range(len(response['Reservations'])):
    target_ip = response['Reservations'][i]['Instances'][0]['NetworkInterfaces'][0]['PrivateIpAddress']
    instance_type = response['Reservations'][i]['Instances'][0]['InstanceType']
    instance_id = response['Reservations'][i]['Instances'][0]['InstanceId']
    instance_tags = response['Reservations'][i]['Instances'][0]['Tags']
    block_device_mappings = response['Reservations'][i]['Instances'][0]['BlockDeviceMappings']
    volume_id = []
    device_name = []

    for j in range(len(instance_tags)):
        if instance_tags[j]['Key'] == 'Name':
            instance_name = response['Reservations'][i]['Instances'][0]['Tags'][j]['Value']
        elif instance_tags[j]['Key'] == 'Env':
            instance_env = response['Reservations'][i]['Instances'][0]['Tags'][j]['Value']
        elif instance_tags[j]['Key'] == 'Usage':
            instance_usage = response['Reservations'][i]['Instances'][0]['Tags'][j]['Value']
        elif instance_tags[j]['Key'] == 'Service':
            instance_usage = response['Reservations'][i]['Instances'][0]['Tags'][j]['Value']
        else:
            pass

    for k in range(len(block_device_mappings)):
        device_name.append(block_device_mappings[k]['DeviceName'])
        volume_id.append(block_device_mappings[k]['Ebs']['VolumeId'])

    # print(volume_id)
    for l in range(len(volume_id)):
        volume = boto3.resource('ec2').Volume(volume_id[l])
        tag = volume.create_tags(
            DryRun=Dryrun,
            Tags=[
                {
                    'Key': 'Name',
                    'Value': instance_name
                },
                {
                    'Key': 'Env',
                    'Value': instance_env
                }
            ]
        )
        print(tag)
