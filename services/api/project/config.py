
from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class BaseConfig(object):
    STATIC_FOLDER = f"{environ.get('APP_FOLDER')}/project/static"
    MEDIA_FOLDER = f"{environ.get('APP_FOLDER')}/project/media"
    
    TOKEN_EXPIRES = environ.get("TOKEN_EXPIRES", 120)

class DataBaseConfig(object):
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False