from . import db, login_manager
from datetime import datetime
import re
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

ROLE = {'user': 0, 'moderator': 1, 'admin': 2}


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)  # db.session.query(User).get(user_id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), nullable=False, index=True, unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(24), index=True, unique=True)
    role = db.Column(db.Integer, default=ROLE['user'])
    password = db.Column(db.String(240), nullable=False,)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated = db.Column(db.DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return "User id: {}, username: {}".format(self.id, self.nickname)

    def set_password(self, user_password):
        self.password = generate_password_hash(user_password)

    def check_password(self, user_password):
        return check_password_hash(self.password, user_password)


post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                     )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    intro = db.Column(db.String(360), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    img_path = db.Column(db.String(140), nullable=True)
    img_name = db.Column(db.String(140), nullable=True)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated = db.Column(db.DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)


    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    slug = db.Column(db.String(140), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', secondary=post_tags, backref='tag')

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.name)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_id = db.Column(db.Integer)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated = db.Column(db.DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.text[:10])
