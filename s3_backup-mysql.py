import os
import boto3
from datetime import datetime


BUCKETNAME = ''


def putfile(s3_fileName, fileName, bucketName):
    conn.Object(bucketName, s3_fileName).put(Body=open(fileName, 'rb'))


if __name__ == '__main__':
    temp = datetime.today()
    s3_filename = 'ENV-dbbak-' + str(temp.year) + '-' + str(temp.month) + '-' + str(temp.day) + '-' + \
        str(temp.hour) + '-' + str(temp.minute) + '.sql'
    fileName = '/tmp/' + s3_filename
    os.system("mysqldump -h MYSQL_HOST -u USERNAME -pPASSWORD --all-databases > " + fileName)
    print('backup DB finished')
    conn = boto3.resource('s3')
    putfile(s3_filename, fileName, BUCKETNAME)
    print('upload to S3 finished')
