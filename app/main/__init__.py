from flask import blueprints

bp = blueprints.Blueprint('main', __name__, template_folder='templates')

from . import forms, views
