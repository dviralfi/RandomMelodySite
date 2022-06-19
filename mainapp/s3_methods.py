import boto3
import os

BUCKET_NAME = "random-melody-site-bucket-dviralafi"


def upload_file(file_path):
    
    s3_client = boto3.client(
        's3',aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )

    file_name = file_path.split("/")[-1]

    response = s3_client.upload_file(file_path, BUCKET_NAME, file_name)

    return response


def get_presigned_url_file(file_name):
    presigned_url = boto3.client(
                's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
            ).generate_presigned_url(

            ClientMethod='get_object', 
            Params={
                'Bucket': BUCKET_NAME,
                 'Key': file_name,
                },
            ExpiresIn=3600)
    return presigned_url