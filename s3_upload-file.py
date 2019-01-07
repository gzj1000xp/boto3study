import boto3
import botocore

BUCKET_NAME = 'BUCKETNAME'
FILENAME = 'LOCALNAME'
KEY = 'S3FILENAME'

s3 = boto3.resource('s3')

try:
    s3.Bucket(BUCKET_NAME).upload_file(FILENAME, KEY)
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise
