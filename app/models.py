from datetime import datetime
import re
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager

ROLE = {'user': 0, 'moderator': 1, 'admin': 2}


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), nullable=False, index=True, unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(24), index=True, unique=True)
    role = db.Column(db.Integer, default=ROLE['user'])
    password = db.Column(db.String(60), nullable=False,)
    about_me = db.Column(db.String(140))
    avatar_path = db.Column(db.String(140), nullable=False)
    avatar_name = db.Column(db.String(20), nullable=False, default='default.jpeg')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated = db.Column(db.DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True) 
    #with user.posts we'll receive array of posts, backref allows as to receive object of class User with post.author
    # followed = db.relationship('User', secondary='followers', primaryjoin=(followers.c.follower_id==id), secondaryjoin=(followed.c.followed_id==id),
    #                             backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f"User('{self.nickname}', '{self.email}')"

    def set_password(self, user_password):
        self.password = generate_password_hash(user_password)

    def check_password(self, user_password):
        return check_password_hash(self.password, user_password)


followers = db.Table('followers',
                    db.Column('folower_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('folowed_id', db.Integer, db.ForeignKey('user.id')))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(360), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    img_path = db.Column(db.String(140), nullable=True)
    img_name = db.Column(db.String(140), nullable=True)
    created = db.Column(db.DateTime, nullable=False, index=True, default=datetime.utcnow)
    updated = db.Column(db.DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    # tags =db.relationship('post_tags', secondary='post', join=(post_tags.c.post_id==id), backref=db.backref('Post', lazy='dynamic'), lazy='dynamic')


    def __repr__(self):
        return f"Post ('{self.title}', '{self.created}')"


post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                     )


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
    comment_id = db.Column(db.Integer, nullable=True)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated = db.Column(db.DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<{self.id}:{self.text[:10]}>"


