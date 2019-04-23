import boto3

InstanceIds = ['']
DRYRUN = True


def p():
    print('+++++++++++++++++++++++++')
    print('instance_id: ' + instance_id)
    print('instance_name: ' + instance_name)
    print('instance_ip: ' + target_ip)
    print('instance_environment: ' + instance_env)
    print('instance_type: ' + instance_type)
    print('volume_id: ' + str(volume_id))
    # print('device_name: ' + str(device_name))
    # print('volume_size: ' + str(volume_size))
    print('ami_id: ' + ami_id)
    # print('blockdevice_mapping: ' + str(block_device_mappings))
    print('blockdevice_mapping: ' + str(BLOCK_DEVICE_MAPPING))


def get_volume_id():
    # 从当前instance的信息中读出volume_id信息，记录至列表中
    for i in range(len(block_device_mappings)):
        device_name.append(block_device_mappings[i]['DeviceName'])
        volume_id.append(block_device_mappings[i]['Ebs']['VolumeId'])


def get_volume_size():
    # describe volumes
    response_volume = ec2.describe_volumes(VolumeIds=volume_id)
    for i in range(len(block_device_mappings)):
        volume_size.append(response_volume["Volumes"][i]["Size"])


def get_block_device_mapping():
    # write
    for a in range(len(block_device_mappings)):
        BLOCK_DEVICE_MAPPING[a]['Ebs'] = dict()
    for b in range(len(block_device_mappings)):
        BLOCK_DEVICE_MAPPING[b]['DeviceName'] = device_name[b]
        BLOCK_DEVICE_MAPPING[b]['Ebs']['VolumeSize'] = volume_size[b]
        BLOCK_DEVICE_MAPPING[b]['Ebs']['VolumeType'] = 'gp2'
        BLOCK_DEVICE_MAPPING[b]['Ebs']['DeleteOnTermination'] = True


ec2 = boto3.client('ec2')
response = ec2.describe_instances(InstanceIds=InstanceIds)

# describe instance
for i in range(len(response['Reservations'])):
    target_ip = response['Reservations'][i]['Instances'][0]['NetworkInterfaces'][0]['PrivateIpAddress']
    instance_type = response['Reservations'][i]['Instances'][0]['InstanceType']
    instance_id = response['Reservations'][i]['Instances'][0]['InstanceId']
    instance_tags = response['Reservations'][i]['Instances'][0]['Tags']
    block_device_mappings = response['Reservations'][i]['Instances'][0]['BlockDeviceMappings']
    ami_id = response['Reservations'][i]['Instances'][0]['ImageId']
    volume_id = []
    volume_size = []
    device_name = []
    BLOCK_DEVICE_MAPPING = []

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
    # init BLOCK_DEVICE_MAPPING
    for k in range(len(block_device_mappings)):
        BLOCK_DEVICE_MAPPING.append(dict())

    get_volume_id()
    get_volume_size()
    get_block_device_mapping()
    p()
