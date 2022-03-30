
from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class BaseConfig(object):
    SECRET_KEY = environ.get("SECRET_KEY")
    TOKEN_EXPIRES = environ.get("TOKEN_EXPIRES", 120)


class DataBaseConfig(object):
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AWS_ACCESS_KEY_ID = environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_DEFAULT_REGION = environ.get("AWS_DEFAULT_REGION")
    AWS_S3_LOCATION = environ.get("AWS_S3_LOCATION")
    AWS_S3_BUCKET_NAME = environ.get("AWS_S3_BUCKET_NAME")
