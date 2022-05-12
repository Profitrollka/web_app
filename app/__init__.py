from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object('config.BaseConfig')
file_handler_for_logs = RotatingFileHandler('logs/blog.log', maxBytes=10240, backupCount=10)
file_handler_for_logs.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
file_handler_for_logs.setLevel(logging.INFO)
app.logger.addHandler(file_handler_for_logs)

db = SQLAlchemy(app)
# migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from . import view, models, errors

