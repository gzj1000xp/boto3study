import boto3


BUCKETNAME = 'BUCKETNAME'
s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKETNAME)

for object in bucket.objects.all():
    print(object)
