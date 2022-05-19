from app import app, db
from app.models import User, Post, Comment, ROLE


@app.shell_context_processor
def make_sell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Comment': Comment, 'ROLE': ROLE}

