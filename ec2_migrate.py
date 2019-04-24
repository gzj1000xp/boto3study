import boto3
import os
import time

# 安全组
SG_ENV3_NO_LIMIT = ['sg-']
SG_ENV2_NO_LIMIT = ['sg-']
SG_ENV1_NO_LIMIT = ['sg-']
SG_DEFAULT = ['sg-']

# 子网
SUBNET_ENV1_PRIVATE = 'subnet-'
SUBNET_ENV1_PUBLIC = 'subnet-'
SUBNET_ENV2_PRIVATE = 'subnet-'
SUBNET_ENV2_PUBLIC = 'subnet-'
SUBNET_ENV3_PRIVATE = 'subnet-'
SUBNET_ENV3_PUBLIC = 'subnet-'

# key
KEY_NAME_ENV1 = 'KEYNAME'
KEY_NAME_ENV2 = 'KEYNAME'
KEY_NAME_ENV3 = 'KEYNAME'

# parameters for creating image
ORI_INSTANCE_ID = ''
DRYRUN = False
ENV = ''
INSTANCE_NAME = ''
IMAGE_NAME = ''
IMAGE_DESCRIPTION = IMAGE_NAME


# functions
def p():
    print('+++++++++++++++++++++++++')
    print('instance_id: ' + instance_id)
    print('instance_name: ' + instance_name)
    print('instance_ip: ' + target_ip)
    print('instance_environment: ' + instance_env)
    print('instance_type: ' + instance_type)
    print('volume_id: ' + str(list(volume_id)))
    print('blockdevice_mapping: ' + str(BLOCK_DEVICE_MAPPING))


def tags(INSTANCE_NAME, ENV):
    if ENV == 'PROD':
        TAGS = [{'ResourceType': 'instance',
                 'Tags': [{'Key': 'Name', 'Value': INSTANCE_NAME}, {'Key': 'Env', 'Value': 'prod'}]}]
    elif ENV == 'ALPHA':
        TAGS = [{'ResourceType': 'instance',
                 'Tags': [{'Key': 'Name', 'Value': INSTANCE_NAME}, {'Key': 'Env', 'Value': 'alpha'}]}]
    elif ENV == 'DEV':
        TAGS = [{'ResourceType': 'instance',
                 'Tags': [{'Key': 'Name', 'Value': INSTANCE_NAME}, {'Key': 'Env', 'Value': 'dev'}]}]
    elif ENV == 'TOOL':
        TAGS = [{'ResourceType': 'instance',
                 'Tags': [{'Key': 'Name', 'Value': INSTANCE_NAME}, {'Key': 'Env', 'Value': 'public'}]}]
    else:
        print('Please give me the correct environment and hit it again.')
        TAGS = 'ERROR'
    return TAGS


def get_volume_id():
    # 从当前instance的信息中读出volume_id信息，记录至列表中
    for i in range(len(block_device_mappings)):
        device_name[block_device_mappings[i]['Ebs']['VolumeId']] = block_device_mappings[i]['DeviceName']
        volume_id_list.append(block_device_mappings[i]['Ebs']['VolumeId'])
        volume_id[block_device_mappings[i]['Ebs']['VolumeId']] = volume_id_list[i]


def get_volume_size():
    # describe volumes
    response_volume = ec2.describe_volumes(VolumeIds=volume_id_list)
    for i in range(len(volume_id_list)):
        volume_size[response_volume["Volumes"][i]["VolumeId"]] = response_volume["Volumes"][i]["Size"]


def get_block_device_mapping():
    # write
    for a in range(len(volume_id_list)):
        BLOCK_DEVICE_MAPPING[a]['Ebs'] = dict()
    for b in range(len(volume_id_list)):
        BLOCK_DEVICE_MAPPING[b]['DeviceName'] = device_name[volume_id_list[b]]
        BLOCK_DEVICE_MAPPING[b]['Ebs']['VolumeSize'] = volume_size[volume_id_list[b]]
        BLOCK_DEVICE_MAPPING[b]['Ebs']['VolumeType'] = 'gp2'
        BLOCK_DEVICE_MAPPING[b]['Ebs']['DeleteOnTermination'] = True


# describe instance
ec2 = boto3.client('ec2')
response = ec2.describe_instances(InstanceIds=[ORI_INSTANCE_ID])

for i in range(len(response['Reservations'])):
    target_ip = response['Reservations'][i]['Instances'][0]['NetworkInterfaces'][0]['PrivateIpAddress']
    instance_type = response['Reservations'][i]['Instances'][0]['InstanceType']
    instance_id = response['Reservations'][i]['Instances'][0]['InstanceId']
    instance_tags = response['Reservations'][i]['Instances'][0]['Tags']
    block_device_mappings = response['Reservations'][i]['Instances'][0]['BlockDeviceMappings']
    volume_id = {}
    volume_id_list = []
    volume_size = {}
    device_name = {}
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

# create image
response_create_image = ec2.create_image(
    Description=IMAGE_DESCRIPTION,
    DryRun=DRYRUN,
    InstanceId=ORI_INSTANCE_ID,
    Name=IMAGE_NAME,
    NoReboot=True
)

ami_id = response_create_image['ImageId']
print(ami_id)

# 查询image创建状态
image_flag = 1
while image_flag:
    response_describe_images = ec2.describe_images(
        ImageIds=[ami_id],
        DryRun=DRYRUN
    )
    image_status = response_describe_images['Images'][0]['State']
    if image_status == 'available':
        print("Image is available now! Continue...")
        break
    time.sleep(5)
    print("Waiting image to be ready...")

# create new ec2 instance
IMAGE_ID = ami_id
KEY_NAME = KEY_NAME_ENV2
INSTANCE_TYPE = instance_type
SG_ID = SG_ENV2_NO_LIMIT
SUBNET_ID = SUBNET_ENV2_PRIVATE
TAGS = tags(INSTANCE_NAME, ENV)
if TAGS == 'ERROR':
    exit(1)

response_create_instance = ec2.run_instances(
    DryRun=DRYRUN,
    ImageId=IMAGE_ID,
    BlockDeviceMappings=BLOCK_DEVICE_MAPPING,
    InstanceType=INSTANCE_TYPE,
    KeyName=KEY_NAME,
    SecurityGroupIds=SG_ID,
    SubnetId=SUBNET_ID,
    TagSpecifications=TAGS,
    MaxCount=1,
    MinCount=1,
    DisableApiTermination=True
)

new_instance_id = response_create_instance['Instances'][0]['InstanceId']
new_private_ip = response_create_instance['Instances'][0]['NetworkInterfaces'][0]['PrivateIpAddress']

print("+++++++++++++++++++++++++")
print("new instance id: " + new_instance_id)
print("new instance name: " + INSTANCE_NAME)
print("new private ip: " + new_private_ip)

time.sleep(5)

os.system("python3 ec2_add-volume-tags.py %s" % new_instance_id)


# clean snapshots
os.system("python3 ec2_delete_image.py %s" % IMAGE_ID)

print("Migaration finished! ")
