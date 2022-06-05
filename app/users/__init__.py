from flask import Blueprint
from ..core import Service
from .models import User

bp = Blueprint('users', __name__, template_folder='templates')


class UsersService(Service):
    __model__ = User


from app.users import forms, models, views