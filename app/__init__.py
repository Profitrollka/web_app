from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import logging
from logging.handlers import RotatingFileHandler
from flask_ckeditor import CKEditor
from config import config
# from flask_mail import Mail
# from flask_security import Security

# mail = Mail()
# security = Security()

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
ckeditor = CKEditor()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


def create_app(config="development"):
    app = Flask(__name__)
    app.config.from_object(config)

    migrate.init_app(app, db)
    bcrypt.init_app(app)
    ckeditor.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    file_handler_for_logs = RotatingFileHandler('logs/blog.log', maxBytes=10240, backupCount=10)
    file_handler_for_logs.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
    file_handler_for_logs.setLevel(logging.INFO)
    app.logger.addHandler(file_handler_for_logs)

    with app.app_context():
        from . import view
        from .utilities import Picture, PostPicture, ProfilePicture

        from app.errors import bp as errors_bp
        app.register_blueprint(errors_bp)

        from app.users import bp as users_bp
        app.register_blueprint(users_bp)

        from app.posts import bp as posts_bp
        app.register_blueprint(posts_bp)

        # from app.admin import bp as admin_bp
        # app.register_blueprint(admin_bp)

    return app

from . import models
# from app.admin import *





