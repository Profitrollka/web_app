from . import app, db
from .forms import LoginForm, RegistrationForm, EditProfileForm
from .models import User
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime


@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.nickname == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        flash("Invalid username or password", 'error')
        return redirect(url_for('login', next=request.endpoint))
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(nickname=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    comments = [
        {'author': user, 'body': 'Test comment #1'},
        {'author': user, 'body': 'Test comment #2'}
    ]
    return render_template('profile.html', user=user, posts=posts, comments=comments)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(nickname=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.nickname, current_user.email)
    if form.validate_on_submit():
        current_user.nickname = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved")
        return redirect(url_for('profile', username=current_user.nickname))
    elif request.method == 'GET':
        form.username.data = current_user.nickname
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

#
#
# @app.route('/cookie/')
# def cookie():
#     if not request.cookies.get('foo'):
#         res = make_response("Setting a cookie")
#         res.set_cookie('foo', 'bar', max_age=60 * 60 * 24 * 365 * 2)
#     else:
#         res = make_response("Value of cookie foo is {}".format(request.cookies.get('foo')))
#     return res
#
#
# @app.route('/delete-cookie/')
# def delete_cookie():
#     res = make_response("Cookie Removed")
#     res.set_cookie('foo', 'bar', max_age=0)
#     return res
#
#
# @app.route('/article', methods=['POST', 'GET'])
# def article():
#     if request.method == 'POST':
#         res = make_response("")
#         res.set_cookie("font", request.form.get('font'), 60 * 60 * 24 * 15)
#         res.headers['location'] = url_for('article')
#         return res, 302
#
#     return render_template('article.html')
#
#
# @app.route('/visits-counter/')
# def visits():
#     if 'visits' in session:
#         session['visits'] = session.get('visits') + 1
#     else:
#         session['visits'] = 1
#     return "Total visits: {}".format(session.get('visits'))
#
#
# @app.route('/delete-visits/')
# def delete_visits():
#     session.pop('visits', None)  # удаление посещений
#     return 'Visits deleted'
#
#
# @app.route('/session/')
# def updating_session():
#     res = str(session.items())
#
#     cart_item = {'pineapples': '10', 'apples': '20', 'mangoes': '30'}
#     if 'cart_item' in session:
#         session['cart_item']['pineapples'] = '100'
#         session.modified = True
#     else:
#         session['cart_item'] = cart_item
#
# return res