import boto3

# 名称
ELB_NAME = ''

# 安全组
SG_HTTP_BASIC = ['sg-095c85e35bbe52cf5']

# 子网
SUBNET_PROD_PRIVATE = 'subnet-451b9621'
SUBNET_PROD_PUBLIC = 'subnet-cd23a3a9'
SUBNET_PROD_PUBLIC_B = 'subnet-0675974d08fd79717'
SUBNET_ALPHA_PRIVATE = 'subnet-04ecc376675ae9f11'
SUBNET_ALPHA_PUBLIC = 'subnet-0d2d3df7c786088cf'
SUBNET_DEV_PRIVATE = 'subnet-d9a924bd'
SUBNET_DEV_PUBLIC = 'subnet-409b1624'
SUBNET_DEV_PUBLIC_B = 'subnet-01ce93821d6812384'

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

