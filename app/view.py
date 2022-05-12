import os
import secrets
from PIL import Image
from datetime import datetime
from flask import abort, render_template, flash, redirect, url_for, request, send_from_directory, jsonify, make_response
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, PostForm, CommentForm, UpdateProfileForm
from app.models import User, Post, Comment
from . import app, db, bcrypt


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=4)
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'User {form.username.data} has been logged in!', 'success')
            app.logger.info(f'User {user.username} logged in.')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash("Login Unsuccessful. Please check username or password.", 'danger')
            app.logger.info(f'User {user.username} failed to log in.')
            return redirect(url_for('login', next=request.endpoint))
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


def rename_and_resize_picture(form_picture: str, folder: str, output_size: tuple[int, int] = (1024, 1024)):
    """
    Function generate random name for picture, using token_hex and resize it.
    :param: form_picture - data that form for uploding picture contains.
    :param: folder - folder for saving picture
    :param: output_size - size that we want to receive after resizing.
    :return: picture_fn - picture filename, picture_path - path to picture in the project

    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static', folder, picture_fn)
    i = Image.open(form_picture)
    i.resize(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/register', methods=['POST', 'GET'])
def register():
    picture_file = 'default.jpg'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.file.data:
            picture_file = rename_and_resize_picture(form.file.data, app.config['UPLOAD_FOLDER_PROFILE'], (125, 125))
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data, picture_file=picture_file, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            app.logger.info(f'User {user.username} is registered')
            return redirect(url_for('login'))
        except:
            flash('An error occurred while saving data. Please try again later.', 'danger')
            app.logger.warning(f"An error occurred while saving data (register new user)")
            return redirect(url_for('register'))
    return render_template('register.html', title='Registration', form=form)


@app.route('/profile', methods=['POST', 'GET'])
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
            img_name = rename_and_resize_picture(form.file.data, app.config['UPLOAD_FOLDER_PROFILE'], (125, 125))
            current_user.picture_file = img_name
        try:
            db.session.commit()
            flash('Your profile has been updated!', 'success')
            app.logger.info(f'User {current_user.username} updated profile.')
        except:
            flash('An error occurred while saving data. Please try again later.', 'danger')
            app.logger.warning(f"An error occurred while saving data (update user's profile)")
            return redirect(url_for('profile'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    picture_path = url_for('static', filename='profile_pics/' + current_user.picture_file)
    return render_template('profile.html', form=form, title='Profile', picture_path=picture_path)


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    img_name = 'default.jpeg'
    if form.validate_on_submit():
        if form.file.data:
            img_name = rename_and_resize_picture(form.file.data, app.config['UPLOAD_FOLDER_POST'], (1023, 1023))
        post = Post(title=form.title.data, intro=form.intro.data, text=form.text.data, user_id=current_user.user_id,
                    picture_file=img_name)
        try:
            db.session.add(post)
            print('post added')
            print(post)
            db.session.commit()
            print('post commited')
            flash('Your post has been created!', 'success')
            app.logger.info(f'User {current_user.username} added new post.')
            return redirect(url_for('index'))
        except:
            flash('An error occurred while saving data. Please try again later.', 'danger')
            app.logger.warning(f"An error occurred while saving data (add new post)")
            return redirect(url_for('new_post'))
    return render_template('post.html', title='New post', form=form, legend='Add Post')


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def single_post(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    posts = Post.query.order_by(Post.created.desc())
    comments = Comment.query.filter(Comment.post_id == post_id)
    if request.method == 'POST':
        if current_user.is_authenticated:
            if form.validate_on_submit():
                comment = Comment(text=form.text.data, user_id=current_user.user_id, post_id=post_id)
                try:
                    db.session.add(comment)
                    db.session.commit()
                    flash('Your cooment has been added!', 'success')
                    app.logger.info(f'User {current_user.username} added new comment.')
                except:
                    flash('An error occurred while saving data. Please try again later.', 'danger')
                    app.logger.warning(f"An error occurred while saving data (add new comment)")
                    return redirect(url_for('single_post', post_id=post_id))
    # if comments is None:
    #     return render_template('single_post.html', post=post, posts=posts, form=form)
    return render_template('single_post.html', post=post, posts=posts, comments=comments, form=form, post_id=post_id,
                           title='Single post')


@app.route('/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.intro = form.intro.data
        post.text = form.text.data
        if form.file.data:
            img_name = rename_and_resize_picture(form.file.data, app.config['UPLOAD_FOLDER_POST'], (1023, 1023))
            post.picture_file = img_name
        try:
            db.session.commit()
            flash('Your post has been updated!', 'success')
            app.logger.info(f'User {current_user.username} updated post {post.post_id}.')
            return redirect(url_for('single_post', post_id=post_id))
        except:
            flash('An error occurred while saving data. Please try again later.', 'danger')
            app.logger.warning(f"An error occurred while saving data (update post)")
            return redirect(url_for('single_post', post_id=post_id))
    elif request.method == "GET":
        form.title.data = post.title
        form.intro.data = post.intro
        form.text.data = post.text
    return render_template('post.html', title='Update post', form=form, legend='Update Post')


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted!', 'success')
        app.logger.info(f'User {current_user.username} deleted post {post.post_id}.')
        return redirect(url_for('index'))
    except:
        flash('An error occurred while deleting post. Please try again later.', 'danger')
        app.logger.warning(f"An error occurred while saving data (delete post)")
        return redirect(url_for('single_post', post_id=post_id))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# Filters
@app.template_filter('get_comments_count')
def get_comments_count(post_id):
    count = 0
    comments = Comment.query.filter_by(post_id=post_id)
    for comment in comments:
        count += 1
    return count

# @app.template_filter('get_username')
# def get_username_name_by_user_key(user_id):
#     user = User.query.filter_by(id=user_id).first_or_404()
#     return user.username


# @app.template_filter('get_avatar')
# def get_username_avatar_by_user_key(user_id):
#     user = User.query.filter_by(id=user_id).first_or_404()
#     picture_path = url_for('static', filename='profile_pics/' + current_user.picture_file)
#     return picture_path


# @app.template_filter('get_date')
# def get_date_by_datetime(datetime):
#     date = str(datetime)[:10]
#     return date

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
