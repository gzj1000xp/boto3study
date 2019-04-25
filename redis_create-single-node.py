import boto3

REDIS_NAME = ''
REDIS_VERSION = '5.0.3'
REDIS_TYPE = 'cache.m3.medium'
PARAMETER_GROUP = 'default.redis5.0'
SECURITY_GROUP_IDS = ['sg-']
TAGS = []
MAINTENANCE_WINDOW = 'sun:23:00-mon:01:30'
SNAPSHOT_WINDOW = '05:00-06:00'

# create single-node redis
redis = boto3.client('elasticache')

response = redis.create_cache_cluster(
    CacheClusterId=REDIS_NAME,
    ReplicationGroupId='string',
    NumCacheNodes=1,
    CacheNodeType=REDIS_TYPE,
    Engine='Redis',
    EngineVersion=REDIS_VERSION,
    CacheParameterGroupName=PARAMETER_GROUP,
    CacheSubnetGroupName='redis-net',
    SecurityGroupIds=SECURITY_GROUP_IDS,
    Tags=TAGS,
    PreferredMaintenanceWindow=MAINTENANCE_WINDOW,
    Port=6379,
    AutoMinorVersionUpgrade=False,
    SnapshotRetentionLimit=1,
    SnapshotWindow=SNAPSHOT_WINDOW
)

print(response)
