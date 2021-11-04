from app import db
import datetime
import re


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
