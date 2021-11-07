"""Flask configuration variables."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class BaseConfig:
    """Set Flask configuration from .env file."""

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_MIGRATE_REPO = path.join(basedir, 'db_repository')
    # SQLALCHEMY_ECHO = False

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    #Flask-Mail #
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = int(environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    ADMINS = environ.get('ADMINS')
