from datetime import datetime
import re
from flask_login import UserMixin
from . import db, login_manager

ROLE = {'user': 0, 'moderator': 1, 'admin': 2}


@login_manager.user_loader
def load_user(usr_id):
    return User.query.get(int(usr_id))


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(20), nullable=False, index=True, unique=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(24), index=True, unique=True)
    role = db.Column(db.Integer, default=ROLE['user'])
    password = db.Column(db.String(60), nullable=False,)
    about_me = db.Column(db.String(140))
    picture_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated = db.Column(db.DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    #with user.posts we'll receive array of posts, backref allows as to receive object of class User with post.author
    posts = db.relationship('Post', backref='author', cascade="all,delete-orphan", lazy=True)
    comments = db.relationship('Comment', backref='author', cascade="all,delete-orphan", lazy=True)  
    # followed = db.relationship('User', secondary='followers', primaryjoin=(followers.c.follower_id==id), secondaryjoin=(followed.c.followed_id==id),
    #                             backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def get_id(self):
        return (self.user_id)




# followers = db.Table('followers',
#                     db.Column('folower_id', db.Integer, db.ForeignKey('user.id')),
#                     db.Column('folowed_id', db.Integer, db.ForeignKey('user.id')))


class Post(db.Model):
    post_id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(360), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    picture_file = db.Column(db.String(20), nullable=True, default='default.jpeg')
    created = db.Column(db.DateTime, nullable=False, index=True, default=datetime.utcnow)
    updated = db.Column(db.DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    # tags =db.relationship('post_tags', secondary='post', join=(post_tags.c.post_id==id), backref=db.backref('Post', lazy='dynamic'), lazy='dynamic')


    def __repr__(self):
        return f"Post ('{self.post_id}', '{self.title}')"


# post_tags = db.Table('post_tags',
#                      db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
#                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
#                      )


# class Tag(db.Model):
#     tag_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), nullable=False)
#     slug = db.Column(db.String(140), nullable=False)
#     created = db.Column(db.DateTime, default=datetime.utcnow)
#     posts = db.relationship('Post', secondary=post_tags, backref='tag')

#     def __repr__(self):
#         return "<{}:{}>".format(self.id, self.name)


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated = db.Column(db.DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<{self.comment_id}:{self.text}>"


