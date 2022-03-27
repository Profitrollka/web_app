import os
import secrets
from datetime import datetime
from flask import abort, render_template, flash, redirect, url_for, request, send_from_directory, jsonify, make_response
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app.forms import LoginForm, RegistrationForm, PostForm, CommentForm, UpdateProfileForm
from app.models import User, Post, Comment
from . import app, db


@app.template_filter('get_nickname')
def get_username_name_by_user_key(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    return user.nickname


@app.template_filter('get_avatar')
def get_username_avatar_by_user_key(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    return user.avatar_name


@app.template_filter('get_date')
def get_date_by_datetime(datetime):
    date = str(datetime)[:10]
    return date


@app.template_filter('get_comments_count')
def get_comments_count(post_id):
    count = 0
    comments = Comment.query.filter_by(post_id=post_id)
    for comment in comments:
        count += 1
    return count


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# для генерации ошибок, ответ не кастомизирован
# @app.errorhandler(400)
# def page_not_found(error):
#     return 'Not allowed file extension, must be "jpg", "jpeg", "png"', 400

# abort(make_response(jsonify(message="Error message"), 400))
       


@app.route('/')
def index():
    posts = Post.query.order_by(Post.created.desc())
    for post in posts:
        print(post.img_path)
        img_path = post.img_path
    return render_template('index.html', title='Home', posts=posts, img_path=img_path)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'User {form.username.data} has been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash("Login Unsuccessful. Please check username or password.", 'danger')
            return redirect(url_for('login', next=request.endpoint))
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_picture(form_picture, folder):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(folder, picture_fn)
    form_picture.save(picture_path)
    return (picture_fn, picture_path)


@app.route('/register', methods=['POST', 'GET'])
def register():
    avatar_name = 'default.jpg'
    avatar_path = os.path.join(app.config['UPLOAD_FOLDER_PROFILE'], avatar_name)
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.file.data:
            img_name, img = save_picture(form.file.data, app.config['UPLOAD_FOLDER_PROFILE'])
            avatar_path = img
            avatar_name = img_name
        user = User(nickname=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                        email=form.email.data, avatar_path=img, avatar_name=img_name)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        except:
            flash('An error occurred while saving data. Please try again later.', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html', title='Registration', form=form)


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.nickname = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        current_user.first_name = form.first_name.data 
        current_user.last_name = form.last_name.data
        if form.file.data:
            img_name, img = save_picture(form.file.data, app.config['UPLOAD_FOLDER_PROFILE'])
            current_user.avatar_path = img
            current_user.avatar_name = img_name
        try:
            db.session.commit()
            flash('Your profile has been updated!', 'success')
        except:
            flash('An error occurred while saving data. Please try again later.', 'danger')
            return redirect(url_for('profile'))
    elif request.method == "GET":
        form.username.data = current_user.nickname
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    avatar_path = url_for('static', filename='profile_pics/' + current_user.avatar_name)
    return render_template('profile.html', form=form, title='Profile', avatar_path=avatar_path)

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm(current_user.id)
    img_path = None
    if form.validate_on_submit():
        if form.file.data:
            img_name, img = save_picture(form.file.data, app.config['UPLOAD_FOLDER_POSTS'])
        post = Post(title=form.title.data, intro=form.intro.data, text=form.text.data, user_id=current_user.id,
                img_path=img, img_name=img_name)
        try:
            db.session.add(post)
            db.session.commit()
            flash('Your post has been added!', 'success')
            return redirect(url_for('index'))
        except:
            flash('An error occurred while saving data. Please try again later.', 'danger')
            return redirect(url_for('post'))
    return render_template('post.html', title='Add post', form=form)


@app.route('/post/<int:id>', methods=['GET', 'POST'])
def single_post(id):
    user = current_user
    form = CommentForm()
    post = Post.query.get(id)
    posts = Post.query.order_by(Post.created.desc())
    comments = Comment.query.filter(Comment.post_id == id)
    if request.method == 'POST':
        if current_user.is_authenticated:
            if form.validate_on_submit():
                comment = Comment(text=form.text.data, user_id=current_user.id, post_id=id)
                try:
                    db.session.add(comment)
                    db.session.commit()
                except:
                    flash('An error occurred while saving data. Please try again later.', 'danger')
                    return redirect('single_post')
    # if comments is None:
    #     return render_template('single_post.html', post=post, posts=posts, form=form)
    return render_template('single_post.html', post=post, posts=posts, comments=comments, form=form, title='Single post')    


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# @app.route('/error400')
# def error400():
#     return render_template('400.html', title='Error')



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