import boto3


BUCKET_NAME = 'BUCKETNAME'
KEY = 'S3FILENAME'

s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)

response = bucket.delete_objects(
    Delete={
        'Objects': [
            {
                'Key': KEY
            },
        ],
        'Quiet': True
    }
)
