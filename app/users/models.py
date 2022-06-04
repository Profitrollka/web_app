from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager


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
    picture_file = db.Column(db.String(50), nullable=False, default='default.jpeg')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    #with user.posts we'll receive array of posts, backref allows as to receive object of class User with post.author
    posts = db.relationship('Post', backref='author', cascade="all,delete-orphan", lazy=True)
    comments = db.relationship('Comment', backref='author', cascade="all,delete-orphan", lazy=True)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated = db.Column(db.DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    # followed = db.relationship('User', secondary='followers', primaryjoin=(followers.c.follower_id==id), secondaryjoin=(followed.c.followed_id==id),
    #                             backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def get_id(self):
        return (self.user_id)


# followers = db.Table('followers',
#                     db.Column('folower_id', db.Integer, db.ForeignKey('user.id')),
#                     db.Column('folowed_id', db.Integer, db.ForeignKey('user.id')))
