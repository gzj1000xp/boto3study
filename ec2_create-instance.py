import boto3
import os


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

# 常用镜像
AMZ_LINUX2 = 'ami-'
REDHAT_75 = 'ami-'

# 常用实例类型
_2C8G = 't2.large'
_4C16G = 't2.xlarge'
_8C32G = 't2.2xlarge'

# 挂载硬盘信息
_100G = [{'DeviceName': '/dev/xvda', 'Ebs': {'VolumeSize': 20, 'VolumeType': 'gp2', 'DeleteOnTermination': True}},
         {'DeviceName': '/dev/sdb', 'Ebs': {'VolumeSize': 100, 'VolumeType': 'gp2', 'DeleteOnTermination': True}}]
_150G = [{'DeviceName': '/dev/xvda', 'Ebs': {'VolumeSize': 20, 'VolumeType': 'gp2', 'DeleteOnTermination': True}},
         {'DeviceName': '/dev/sdb', 'Ebs': {'VolumeSize': 150, 'VolumeType': 'gp2', 'DeleteOnTermination': True}}]
_200G = [{'DeviceName': '/dev/xvda', 'Ebs': {'VolumeSize': 20, 'VolumeType': 'gp2', 'DeleteOnTermination': True}},
         {'DeviceName': '/dev/sdb', 'Ebs': {'VolumeSize': 200, 'VolumeType': 'gp2', 'DeleteOnTermination': True}}]
_300G = [{'DeviceName': '/dev/xvda', 'Ebs': {'VolumeSize': 20, 'VolumeType': 'gp2', 'DeleteOnTermination': True}},
         {'DeviceName': '/dev/sdb', 'Ebs': {'VolumeSize': 300, 'VolumeType': 'gp2', 'DeleteOnTermination': True}}]


def tags(INSTANCE_NAME, ENV):
    if ENV == 'ENV1':
        TAGS = [{'ResourceType': 'instance',
                 'Tags': [{'Key': 'Name', 'Value': INSTANCE_NAME}, {'Key': 'Env', 'Value': 'env1'}]}]
    elif ENV == 'ENV2':
        TAGS = [{'ResourceType': 'instance',
                 'Tags': [{'Key': 'Name', 'Value': INSTANCE_NAME}, {'Key': 'Env', 'Value': 'env2'}]}]
    elif ENV == 'ENV3':
        TAGS = [{'ResourceType': 'instance',
                 'Tags': [{'Key': 'Name', 'Value': INSTANCE_NAME}, {'Key': 'Env', 'Value': 'env3'}]}]
    else:
        print('Please give me the correct environment and hit it again.')
        TAGS = 'ERROR'
    return TAGS


# 参数定义
DRYRUN = True
INSTANCE_NAME = "INSNAME"
HARDDISK = _100G
IMAGE_ID = AMZ_LINUX2
KEY_NAME = KEY_NAME_ENV2
INSTANCE_TYPE = _4C16G
SG_ID = SG_ENV2_NO_LIMIT
SUBNET_ID = SUBNET_ENV2_PRIVATE

TAGS = tags(INSTANCE_NAME, 'ENV')
if TAGS == 'ERROR':
    exit(1)

# 执行创建
ec2 = boto3.client('ec2')
response = ec2.run_instances(
    DryRun=DRYRUN,
    BlockDeviceMappings=HARDDISK,
    ImageId=IMAGE_ID,
    InstanceType=INSTANCE_TYPE,
    KeyName=KEY_NAME,
    SecurityGroupIds=SG_ID,
    SubnetId=SUBNET_ID,
    TagSpecifications=TAGS,
    MaxCount=1,
    MinCount=1,
    DisableApiTermination=True
)

instance_id = response['Instances'][0]['InstanceId']
print(instance_id)

os.system("python3 ec2_add-volume-tags.py %s" % instance_id)
