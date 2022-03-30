import boto3
from exceptions import FileUploadException
from flask import current_app
from project.utils.functions import get_extension


def has_bucket_by_name(client, name_bucket: str) -> bool:
    try:
        client.head_bucket(Bucket=name_bucket)
        return True
    except Exception:
        return False


def upload_file(file, album_id: str, file_name: str, user_id: str) -> str:
    client = current_app.extensions["aws_client"]
    bucket_name = current_app.config["AWS_S3_BUCKET_NAME"]

    try:
        bucket_file_path = f"{album_id}/{user_id}/{file_name}.{get_extension(file.filename)}"
        client.upload_fileobj(file, bucket_name, bucket_file_path,
                              {"ACL": "public-read", "ContentType": file.content_type})

        return bucket_file_path

    except Exception as e:
        raise FileUploadException(
            message="Sorry, we has a problem to process your image",
            payload=e,
        )


def init_bucket(app):
    app.extensions["aws_client"] = boto3.client(
        "s3",
        aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"],
    )
