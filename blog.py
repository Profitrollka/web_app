# import app
from app import db, create_app
from app.models import User, Post, Comment, ROLE
from config import *

app = create_app(config=DevelopmentConfig)

@app.shell_context_processor
def make_sell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Comment': Comment, 'ROLE': ROLE}
