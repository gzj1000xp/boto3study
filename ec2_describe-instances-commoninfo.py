import boto3


def p():
    print('+++++++++++++++++++++++++')
    print('instance_id: ' + instance_id)
    print('instance_name: ' + instance_name)
    print('instance_ip: ' + target_ip)
    print('instance_environment: ' + instance_env)
    print('instance_type: ' + instance_type)
    print('volume_id: ' + str(volume_id))
    print('device_name: ' + str(device_name))


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
InstanceIds = ['*']
Dryrun = True


ec2 = boto3.client('ec2')
response = ec2.describe_instances(Filters=Filters)


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

    p()
