from os import environ, path
from dotenv import load_dotenv
from typing import NamedTuple

basedir = path.abspath(path.dirname(__file__))
dotenv_path = path.join(basedir, '.env')
load_dotenv(dotenv_path)

# class BaseConfig:
#     """Set Flask configuration from .env file"""
#
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#
#     # Database
#     SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
#
#     # General Config
#     SECRET_KEY = environ.get('SECRET_KEY')
#     FLASK_APP = environ.get('FLASK_APP')
#     FLASK_ENV = environ.get('FLASK_ENV')


    # #Flask-Mail
    # MAIL_SERVER = environ.get('MAIL_SERVER')
    # MAIL_PORT = int(environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    # ADMINS = environ.get('ADMINS')


class BaseConfig:
    """Base configuration."""

    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER_PROFILE = environ.get('UPLOAD_FOLDER_PROFILE')
    UPLOAD_FOLDER_POST = environ.get('UPLOAD_FOLDER_POST')

    # @staticmethod
    # def init_app(app):
    #     pass

class ProductionConfig(BaseConfig):
    """Production configuration."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')


class TestingConfig(BaseConfig):
    """Test configuration."""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get("TEST_DATABASE_URL")


class Configuration(NamedTuple):
    development: str
    testing: str
    production: str


config = Configuration(development=DevelopmentConfig,
                       testing=TestingConfig,
                       production=ProductionConfig)

