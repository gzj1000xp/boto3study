import boto3

# 名称
ELB_NAME = ''

# 安全组
SG_HTTP_BASIC = ['sg-']

# 子网
SUBNET_PROD_PRIVATE = 'subnet-'
SUBNET_PROD_PUBLIC = 'subnet-'
SUBNET_PROD_PUBLIC_B = 'subnet-'
SUBNET_ALPHA_PRIVATE = 'subnet-'
SUBNET_ALPHA_PUBLIC = 'subnet-'
SUBNET_DEV_PRIVATE = 'subnet-'
SUBNET_DEV_PUBLIC = 'subnet-'
SUBNET_DEV_PUBLIC_B = 'subnet-'

# 内网or公网
SCHEME_PUBLIC = 'internet-facing'
SCHEME_PRIVATE = 'internal'

# 7层OR4层
APP = 'application'
NET = 'network'

# 参数定义
DRYRUN = True
SG_ID = SG_HTTP_BASIC
# SUBNET_ID = SUBNET_ENV2_PRIVATE
SCHEME = SCHEME_PUBLIC
TYPE = APP


# 执行创建
elb = boto3.client('elbv2')

response = elb.create_load_balancer(
    Name=ELB_NAME,
    Subnets=[
        SUBNET_PROD_PUBLIC,
        SUBNET_PROD_PUBLIC_B,
    ],
    SecurityGroups=[
        SG_ID,
    ],
    Scheme=SCHEME,
    Tags=[
        {
            'Key': 'NAME',
            'Value': ELB_NAME
        },
    ],
    Type=TYPE,
    IpAddressType='ipv4'
)

