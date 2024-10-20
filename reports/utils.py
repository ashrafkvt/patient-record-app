import boto3
from botocore.exceptions import ClientError

from patient_report.settings import (
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_REGION_NAME,
    AWS_STORAGE_BUCKET_NAME
)


def s3_client():
    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name=AWS_S3_REGION_NAME)
        return s3
    except Exception as exception:
        print(exception)
    return None


def s3_resource():
    try:
        s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                            region_name=AWS_S3_REGION_NAME)
        return s3
    except Exception as exception:
        print(exception)
    return None


def create_presigned_url(object_name):
    s3 = s3_client()
    try:
        response = s3.generate_presigned_url(
            'get_object', Params={
                'Bucket': AWS_STORAGE_BUCKET_NAME,
                'Key': object_name}, ExpiresIn=600)
    except ClientError as e:
        print(e)
        return None

    return response
