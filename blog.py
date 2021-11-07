from app import app, db
from app.models import User, Post, Tag, Comment, ROLE
import logging
from logging.handlers import RotatingFileHandler
import os


@app.shell_context_processor
def make_sell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Tag': Tag, 'Comment': Comment, 'ROLE': ROLE}

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/blog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Blog startup')