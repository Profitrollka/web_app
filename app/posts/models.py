from datetime import datetime
from app import db


post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('post.post_id'), primary_key=True),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.tag_id'), primary_key=True)
                     )


class Post(db.Model):

    post_id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(360), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    picture_file = db.Column(db.String(50), nullable=True, default='default.jpeg')
    tags = db.relationship('Tag', secondary=post_tags, back_populates='posts')
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated = db.Column(db.DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Post ('{self.post_id}', '{self.title}')"


class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    posts = db.relationship('Post', secondary=post_tags, back_populates="tags")

    def __repr__(self):
        return f"#{self.tag_name}"


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated = db.Column(db.DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<{self.comment_id}:{self.text}>"