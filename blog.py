from app import app, db
from app.models import User, Post, Tag, Comment

@app.shell_context_processor
def make_sell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Tag': Tag, 'Comment': Comment}
