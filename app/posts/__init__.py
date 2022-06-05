from flask import Blueprint
from ..core import Service
from .models import Post, Tag, Comment

bp = Blueprint('posts', __name__, template_folder='templates')


class PostsService(Service):
    __model__ = Post


class PostsService(Service):
    __model__ = Post


class TagsService(Service):
    __model__ = Tag


class CommentsService(Service):
    __model__ = Comment


from app.posts import forms, models, views
