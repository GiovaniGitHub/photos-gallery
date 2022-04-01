import boto3
from botocore.exceptions import ClientError
from flask import current_app

from exceptions import FileUploadException
from project.utils.functions import get_extension


def has_bucket_by_name(client, name_bucket: str) -> bool:
    try:
        client.head_bucket(Bucket=name_bucket)
        return True
    except Exception:
        return False


def upload_file(file, album_id: str, file_name: str, user_id: str) -> str:
    client = current_app.extensions["aws_client"]
    

    try:
        bucket_file_path = f"{user_id}/{file_name}.{get_extension(file.filename)}"
        client.upload_fileobj(file, str(album_id), bucket_file_path,
                                {"ACL": "public-read", "ContentType": file.content_type})
        return bucket_file_path
    except ClientError as e:
        print(e)
        raise e
    except Exception as e:
        raise FileUploadException(
            message="Sorry, we has a problem to process your image",
            payload=e,
        )


def init_bucket(app):
    bucket_name = app.config["AWS_S3_BUCKET_NAME"]
    app.extensions["aws_client"] = boto3.client(
        "s3",
        region_name="us-east-1",
        endpoint_url=f"https://{bucket_name}.s3.amazonaws.com",
        aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"],
    )
