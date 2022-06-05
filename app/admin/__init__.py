from flask import Blueprint

bp = Blueprint('admin_bp', __name__, template_folder='templates')

from app.admin import views