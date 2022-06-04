from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash
from . import app, models, db


class MyBlogModelView(ModelView):

    def is_accessible(self):
        if current_user.is_authenticated:
            admin_role = models.ROLE['admin']
            return current_user.role == admin_role
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            flash("Sorry, to access this page you must be an admin.", "danger")
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))


class MyBlogAdminIndexView(AdminIndexView):

    def is_accessible(self):
        if current_user.is_authenticated:
            admin_role = models.ROLE['admin']
            return current_user.role == admin_role
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            flash("Sorry, to access this page you must be an admin.", "danger")
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))


admin = Admin(app, index_view=MyBlogAdminIndexView())
admin.add_view(MyBlogModelView(models.User, db.session))
admin.add_view(MyBlogModelView(models.Post, db.session))
admin.add_view(MyBlogModelView(models.Tag, db.session))
admin.add_view(MyBlogModelView(models.Comment, db.session))
