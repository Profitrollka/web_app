from app import db
import datetime
import re

ROLE = {'user': 0, 'moderator': 1, 'admin': 2}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(24), index=True, unique=True)
    role = db.Column(db.Integer, default=ROLE['user'])
    password = db.Column(db.String(24))
    created = db.Column(db.Datetime, index=True, default=datetime.datetime.now)
    updated = db.Column(db.Datetime, index=True, default=None)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(self, *args, **kwargs)

    def __repr__(self):
        return "User: {}".format(self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    text = db.Column(db.String(16838))
    user_id = db.Column(db.Integer, db.Foreingkey('user.id'))
    slug = db.Column(db.String(140), index=True, unique=True)
    timestamp = db.Column(db.Datetime, index=True, default=datetime.datetime.now)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    post_id = db.Column(db.Integer, db.Foreingkey('post.id'))
    user_id = db.Column(db.Integer, db.Foreingkey('user.id'))
    comment_id = db.Column(db.Integer)
    timestamp = db.Column(db.Datetime, index=True, default=datetime.datetime.now)



