import json
import os
from datetime import datetime

from flask import abort, render_template, flash, redirect, url_for, request, send_from_directory, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, PostForm, CommentForm, UpdateProfileForm, SearchForm
from app.media import ProfilePicture, PostPicture
from app.models import User, Post, Comment, Tag, post_tags, ROLE
from . import app, db, bcrypt


@app.route('/')
def index():
    query = request.args.get('query')
    print(query)
    if query:
        return redirect(url_for('search', tagname=query))
    else:
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.created.desc()).paginate(page=page, per_page=4)
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
            return redirect(url_for('login', next=request.endpoint))
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    picture_file = ProfilePicture(app.config['UPLOAD_FOLDER_PROFILE'])
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.file.data:
            picture_file = ProfilePicture(form.file.data)
            picture_file.resize_picture()
            picture_file.rename_picture()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data, picture_file=picture_file.name, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            if form.file.data:
                picture_file.save_picture(app.config['UPLOAD_FOLDER_PROFILE'])
            flash('Your account has been created! You are now able to log in', 'success')
            app.logger.info(f'User {user.username} is registered')
            return redirect(url_for('login'))
        except Exception as e:
            flash('An error occurred while saving data. Please try again later.', 'danger')
            app.logger.warning(f"An error occurred while saving data (register new user)")
            app.logger.exception(e)
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
            picture_file = ProfilePicture(form.file.data)
            picture_file.resize_picture()
            picture_file.rename_picture()
            current_user.picture_file = picture_file.name
        try:
            db.session.commit()
            if form.file.data:
                picture_file.save_picture(app.config['UPLOAD_FOLDER_PROFILE'])
            flash('Your profile has been updated!', 'success')
            app.logger.info(f'User {current_user.username} updated profile.')
        except Exception as e:
            flash('An error occurred while saving data. Please try again later.', 'danger')
            app.logger.warning(f"An error occurred while saving data (update user's profile)")
            app.logger.exception(e)
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
    picture_file = PostPicture(app.config['UPLOAD_FOLDER_POST'])
    if form.validate_on_submit():
        if form.file.data:
            picture_file = PostPicture(form.file.data)
            picture_file.rename_picture()
            picture_file.resize_picture()
        post = Post(title=form.title.data, intro=form.intro.data, text=form.text.data, user_id=current_user.user_id,
                    picture_file=picture_file.name)
        post_tags_list = []
        if form.tag.data:
            for word in form.tag.data.replace(" ", "").replsce("#", "").replace("[", "").replace("]", "").split(","):
                tag = Tag.query.filter_by(tag_name=word.lower()).first()
                if tag:
                    pass
                else:
                    tag = Tag(tag_name=word.lower())
                    try:
                        db.session.add(tag)
                    except Exception as e:
                        flash('An error occurred while saving data. Please try again later.', 'danger')
                        app.logger.warning(f"An error occurred while saving data (add new tag)")
                        app.logger.exception(e)
            post_tags_list.append(tag)
        post.tags = post_tags_list
        try:
            db.session.add(post)
            db.session.commit()
            if form.file.data:
                picture_file.save_picture(app.config['UPLOAD_FOLDER_POST'])
            flash('Your post has been created!', 'success')
            app.logger.info(f'User {current_user.username} added new post.')
            return redirect(url_for('index'))
        except Exception as e:
            flash('An error occurred while saving data. Please try again later.', 'danger')
            app.logger.warning(f"An error occurred while saving data (add new post)")
            app.logger.exception(e)
            return redirect(url_for('new_post'))
    return render_template('post.html', title='New post', form=form, legend='Add Post')


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def single_post(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    posts = Post.query.order_by(Post.created.desc()).limit(5).all()
    comments = Comment.query.filter(Comment.post_id == post_id)
    if request.method == 'POST':
        if current_user.is_authenticated:
            if form.validate_on_submit():
                comment = Comment(text=form.text.data, user_id=current_user.user_id, post_id=post_id)
                try:
                    db.session.add(comment)
                    db.session.commit()
                    flash('Your comment has been added!', 'success')
                    app.logger.info(f'User {current_user.username} added new comment.')
                except Exception as e:
                    flash('An error occurred while saving data. Please try again later.', 'danger')
                    app.logger.warning(f"An error occurred while saving data (add new comment)")
                    app.logger.exception(e)
                    return redirect(url_for('single_post', post_id=post_id))
    return render_template('single_post.html', post=post, posts=posts, comments=comments, form=form, post_id=post_id,
                           post_tags=post_tags, title='Single post')


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
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
            picture_file = PostPicture(form.file.data)
            picture_file.rename_picture()
            picture_file.resize_picture()
            post.picture_file = picture_file.name
        post_tags_list = []
        for word in form.tag.data.replace(" ", "").replace("#", "").replace("[", "").replace("]", "").split(","):
            tag = Tag.query.filter_by(tag_name=word.lower()).first()
            if tag:
                pass
            else:
                tag = Tag(tag_name=word.lower())
                try:
                    db.session.add(tag)
                except Exception as e:
                    flash('An error occurred while saving data. Please try again later.', 'danger')
                    app.logger.warning(f"An error occurred while saving data (add new tag)")
                    app.logger.exception(e)
            post_tags_list.append(tag)
        post.tags = post_tags_list
        try:
            db.session.commit()
            if form.file.data:
                picture_file.save_picture(app.config['UPLOAD_FOLDER_POST'])
            flash('Your post has been updated!', 'success')
            app.logger.info(f'User {current_user.username} updated post {post.post_id}.')
            return redirect(url_for('single_post', post_id=post_id))
        except Exception as e:
            flash('An error occurred while saving data. Please try again later.', 'danger')
            app.logger.warning(f"An error occurred while saving data (update post)")
            app.logger.exception(e)
            return redirect(url_for('single_post', post_id=post_id))
    elif request.method == "GET":
        form.title.data = post.title
        form.intro.data = post.intro
        form.text.data = post.text
        form.tag.data = post.tags
    return render_template('post.html', title='Update post', form=form, legend='Update Post')


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    for comment in post.comments:
        db.session.delete(comment)
    picture_for_delete = post.picture_file
    try:
        db.session.delete(post)
        db.session.commit()
        path = os.path.join(app.root_path, 'static', app.config['UPLOAD_FOLDER_POST'], picture_for_delete)
        os.remove(path)
        flash('Your post has been deleted!', 'success')
        app.logger.info(f'User {current_user.username} deleted post {post.post_id}.')
        return redirect(url_for('index'))
    except Exception as e:
        flash('An error occurred while deleting post. Please try again later.', 'danger')
        app.logger.warning(f"An error occurred while saving data (delete post)")
        app.logger.exception(e)
        return redirect(url_for('single_post', post_id=post_id))


@app.route('/posts/search', methods=['GET'])
def search_posts():
    tags = json.loads(request.data['tags'])
    posts = db.session.query(Post).join(post_tags).join(Tag).filter(Tag.tag.in_(tags)).group_by(Post.post_id).all()
    return jsonify(posts)


@app.route('/comment/<int:comment_id>/update', methods=['GET', 'POST'])
@login_required
def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    print(comment)
    if comment.author != current_user:
        abort(403)
    form = CommentForm()
    if form.validate_on_submit():
        comment.text = form.text.data
        try:
            db.session.commit()
            flash('Your comment has been updated!', 'success')
            app.logger.info(f'User {current_user.username} updated comment {comment.comment_id}.')
            return redirect(url_for('single_post', post_id=comment.post_id))
        except Exception as e:
            flash('An error occurred while saving data. Please try again later.', 'danger')
            app.logger.warning(f"An error occurred while saving data (update comment)")
            app.logger.exception(e)
            return redirect(url_for('single_post', post_id=comment.post_id))
    elif request.method == "GET":
        form.text.data = comment.text
    return render_template('comment.html', title='Update comment', form=form, legend='Update Comment')


@app.route('/comment/<int:comment_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    try:
        db.session.delete(comment)
        db.session.commit()
        flash('Your comment has been deleted!', 'success')
        app.logger.info(f'User {current_user.username} deleted comment {comment.comment_id}.')
        return redirect(url_for('single_post', post_id=comment.post_id))
    except Exception as e:
        flash('An error occurred while deleting post. Please try again later.', 'danger')
        app.logger.warning(f"An error occurred while saving data (delete comment)")
        app.logger.exception(e)
        return redirect(url_for('single_post', post_id=comment.post_id))


@app.route('/uploads/<path:name>')
def uploaded_file(name):
    return send_from_directory(os.path.abspath(os.path.dirname(__file__))+"/static/post_pics", name)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/search_by_tag/<tagname>', methods=["GET"])
def search_by_tag(tagname):
    tag = Tag.query.filter_by(tag_name=tagname).first()
    posts_id = db.session.query(post_tags).filter_by(tag_id=tag.tag_id).all()
    posts = []
    for post_id in posts_id:
        post = Post.query.filter_by(post_id=post_id[0]).first()
        posts.append(post)
    return render_template('tags.html', title='Posts', posts=posts)


@app.route('/search_by_query', methods=["POST"])
def search_by_query():
    form =SearchForm()
    posts = Post.query
    if form.validate_on_submit():
        query = form.query.data
        posts = posts.filter(Post.text.like('%'+query+'%'))
        posts = posts.order_by(Post.created.desc()).all()

        return render_template('search.html', form=form, query=query, posts=posts)


@app.route('/admin')
@login_required
def admin():
    admin_role = ROLE['admin']
    if current_user.role == admin_role:
        return render_template('admin.html')
    else:
        flash("Sorry, to access this page you must be an admin.", "danger")
        return redirect(url_for('index'))

# Filters
@app.template_filter('get_comments_count')
def get_comments_count(post_id):
    count = 0
    comments = Comment.query.filter_by(post_id=post_id)
    for _ in comments:
        count += 1
    return count


# pass stuff to a navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

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
