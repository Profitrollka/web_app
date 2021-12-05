from . import app, db
from .forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, CommentForm
from .models import User, Post, Comment
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from datetime import datetime
import os


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


@app.route('/')
def index():
    posts = Post.query.order_by(Post.created.desc())
    return render_template('index.html', title='Home', posts=posts)


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
    posts = Post.query.filter(Post.user_id==user.id).order_by(Post.created.desc())
    comments = [
        {'author': user, 'body': 'Test comment #1'},
        {'author': user, 'body': 'Test comment #2'}
    ]
    return render_template('profile.html', user=user, posts=posts, comments=comments)


@app.route('/register', methods=['GET', 'POST'])
def register():
    img = None
    img_name = None
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if 'upload' not in request.files:
                return redirect(request.url)
            file = request.files['upload']
            if file and form.allowed_file(file.filename):
                img_name = secure_filename(file.filename)
                img = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
                file.save(os.path.join(img))
            user = User(nickname=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                        email=form.email.data, avatar_path=img, avatar_name=img_name)
            user.set_password(form.password.data)
            try:
                db.session.add(user)
                db.session.commit()
                flash('Congratulations, you are now a registered user!')
                return redirect('/')
            except:
                return 'An error occurred when adding a post. Please try again later.'
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.nickname, current_user.email)
    img = None
    img_name = None
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.nickname = form.username.data
            current_user.email = form.email.data
            current_user.about_me = form.about_me.data
            if 'upload' not in request.files:
                return redirect(request.url)
            file = request.files['upload']
            if file and form.allowed_file(file.filename):
                img_name = secure_filename(file.filename)
                img = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
                file.save(os.path.join(img))
                current_user.avatar_path = img
                current_user.avatar_name = img_name
            try:
                db.session.commit()
                flash("Your changes have been saved")
            except:
                'An error occurred when adding a post. Please try again later.'
            return redirect(url_for('profile', username=current_user.nickname))
    elif request.method == 'GET':
        form.username.data = current_user.nickname
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm(current_user.id)
    img = None
    if request.method == 'POST':
        if form.validate_on_submit():
            if 'upload' not in request.files:
                return redirect(request.url)
            file = request.files['upload']
            if file and form.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                img = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(os.path.join(img))
            # if form.tag.data is not None:
            #     tag = Tag(name=form.tag.data, slug=sl)
            post = Post(title=form.title.data, intro=form.intro.data, text=form.text.data, user_id=current_user.id,
                    img_path=img, img_name=filename)
            try:
                db.session.add(post)
                db.session.commit()
                flash("Post added")
                return redirect('/')
            except:
                return 'An error occurred when adding a post. Please try again later.'
    return render_template('post.html', title='Post', form=form)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


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
                    'An error occurred when adding a post. Please try again later.'
    return render_template('single_post.html', post=post, posts=posts, comments=comments, form=form)




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