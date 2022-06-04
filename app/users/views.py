from datetime import datetime
from flask import render_template, flash, redirect, url_for, request,  current_app
from flask_login import current_user, login_user, logout_user, login_required
from .forms import LoginForm, RegistrationForm, UpdateProfileForm
from . import bp
import app.servises
from app.utilities import ProfilePicture

from app import bcrypt


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = app.servises.user_service.first(username=form.username.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'User {form.username.data} has been logged in!', 'success')
            current_app.logger.info(f'User {user.username} logged in.')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash("Login Unsuccessful. Please check username or password.", 'danger')
            return redirect(url_for('users.login', next=request.endpoint))
    return render_template('login.html', title='Login', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@bp.route('/register', methods=['POST', 'GET'])
def register():
    picture_file = ProfilePicture(current_app.config['UPLOAD_FOLDER_PROFILE'])
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.file.data:
            picture_file = ProfilePicture(form.file.data)
            picture_file.resize_picture()
            picture_file.rename_picture()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        try:
            user = app.servises.new(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data, picture_file=picture_file.name, password=hashed_password)
            app.servises.save(user)
            if form.file.data:
                picture_file.save_picture(current_app.config['UPLOAD_FOLDER_PROFILE'])
            flash('Your account has been created! You are now able to log in', 'success')
            current_app.logger.info(f'User {user.username} is registered')
            return redirect(url_for('users.login'))
        except Exception as e:
            flash('An error occurred while saving data. Please try again later.', 'danger')
            current_app.logger.warning(f"An error occurred while saving data (register new user)")
            current_app.logger.exception(e)
            return redirect(url_for('users.register'))
    return render_template('register.html', title='Registration', form=form)


@bp.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        if form.file.data:
            picture_file = ProfilePicture(form.file.data)
            picture_file.resize_picture()
            picture_file.rename_picture()
            current_user.picture_file = picture_file.name
        try:
            app.servises.update(current_user)
            if form.file.data:
                picture_file.save_picture(current_app.config['UPLOAD_FOLDER_PROFILE'])
            flash('Your profile has been updated!', 'success')
            current_app.logger.info(f'User {current_user.username} updated profile.')
        except Exception as e:
            flash('An error occurred while saving data. Please try again later.', 'danger')
            current_app.logger.warning(f"An error occurred while saving data (update user's profile)")
            current_app.logger.exception(e)
            return redirect(url_for('users.profile'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    picture_path = url_for('static', filename='profile_pics/' + current_user.picture_file)
    return render_template('profile.html', form=form, title='Profile', picture_path=picture_path)


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        app.servises.user_service.update(current_user)



