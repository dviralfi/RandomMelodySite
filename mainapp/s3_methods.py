import os
import boto3
from pathlib import Path

BUCKET_NAME = "random-melody-site-bucket-dviralafi"
REGION_NAME = 'us-east-1'


def get_s3_client():

    # Setup Automatic Cleaning

    return boto3.client(
        's3',aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )


def get_s3_session():
    return boto3.Session(
    aws_access_key_id     = os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name           = REGION_NAME,
    )


def upload_file(file_path):
    
    s3_client = get_s3_client()

    file_name = Path(file_path).name

    response = s3_client.upload_file(file_path, BUCKET_NAME, file_name)

    return response


def get_presigned_url_of_file(file_name):
    presigned_url = get_s3_client().generate_presigned_url(
            ClientMethod='get_object', 
            Params={
                'Bucket': BUCKET_NAME,
                 'Key': file_name,
                },
            ExpiresIn=3600)
    return presigned_url


def delete_uploaded_file(file_name):
    s3_client = boto3.resource(
        's3',aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )
    s3_client.Object(BUCKET_NAME, file_name).delete()


def clean_deleted_user_files(username):
    botoSession = get_s3_session()
    s3 = botoSession.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    anonymous_users_keys = bucket.objects.filter(Prefix=username)
    anonymous_users_keys.delete()

