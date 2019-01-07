import boto3

s3 = boto3.resource('s3')
s3.create_bucket(Bucket='BUCKETNAME', CreateBucketConfiguration={'LocationConstraint': 'cn-north-1'})
