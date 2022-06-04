from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import logging
from logging.handlers import RotatingFileHandler
from flask_ckeditor import CKEditor


# from flask_mail import Mail
# from flask_sqlalchemy import SQLAlchemy
# from flask_security import Security

# db = SQLAlchemy()
# mail = Mail()
# security = Security()
# migrate = Migrate()
# bcrypt = Bcrypt()
# ckeditor = CKEditor()
# login_manager = LoginManager()
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
#
#
# def create_app(config_filename='config'):
#     app = Flask(__name__)
#     app.config.from_object('config.BaseConfig')
#
#     migrate.init_app(app, db)
#     bcrypt.init_app(app)
#     ckeditor.init_app(app)
#     login_manager.init_app(app)
#     db.init_app(app)
#
#     file_handler_for_logs = RotatingFileHandler('logs/blog.log', maxBytes=10240, backupCount=10)
#     file_handler_for_logs.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
#     file_handler_for_logs.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler_for_logs)
#
#     from app.errors import bp as errors_bp
#     app.register_blueprint(errors_bp)
#
#     from app.users import bp as users_bp
#     app.register_blueprint(users_bp)
#
#     return app

app = Flask(__name__)
ckeditor = CKEditor(app)
app.config.from_object('config.BaseConfig')
file_handler_for_logs = RotatingFileHandler('logs/blog.log', maxBytes=10240, backupCount=10)
file_handler_for_logs.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
file_handler_for_logs.setLevel(logging.INFO)
app.logger.addHandler(file_handler_for_logs)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.users import bp as users_bp
app.register_blueprint(users_bp)

from app.posts import bp as posts_bp
app.register_blueprint(posts_bp)

from . import view, models, errors
from app.admin import *





