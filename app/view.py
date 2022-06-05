from flask import render_template, flash, redirect, url_for, request, send_from_directory, jsonify, current_app
from flask_login import current_user, login_required
from app.forms import SearchForm
from os import path
from json import loads
from . import db
from .models import Post, Comment, Tag, post_tags, ROLE


@current_app.route('/')
def index():
    query = request.args.get('query')
    if query:
        return redirect(url_for('search', tagname=query))
    else:
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.created.desc()).paginate(page=page, per_page=4)
    return render_template('index.html', title='Home', posts=posts)


# Filters
@current_app.template_filter('get_comments_count')
def get_comments_count(post_id: int):
    count = 0
    comments = Comment.query.filter_by(post_id=post_id)
    for _ in comments:
        count += 1
    return count


@current_app.route('/posts/search', methods=['GET'])
def search_posts():
    tags = loads(request.data['tags'])
    posts = db.session.query(Post).join(post_tags).join(Tag).filter(Tag.tag.in_(tags)).group_by(Post.post_id).all()
    return jsonify(posts)


@current_app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@current_app.route('/about')
def about():
    return render_template('about.html', title='About')


@current_app.route('/search_by_tag/<tagname>', methods=["GET"])
def search_by_tag(tagname: str):
    tag = Tag.query.filter_by(tag_name=tagname).first()
    posts_id = db.session.query(post_tags).filter_by(tag_id=tag.tag_id).all()
    posts = []
    for post_id in posts_id:
        post = Post.query.filter_by(post_id=post_id[0]).first()
        posts.append(post)
    return render_template('tags.html', title='Posts', posts=posts)


@current_app.route('/search_by_query', methods=["POST"])
def search_by_query():
    form = SearchForm()
    posts = Post.query
    if form.validate_on_submit():
        query = form.query.data
        posts = posts.filter(Post.text.like('%'+query+'%'))
        posts = posts.order_by(Post.created.desc()).all()
        return render_template('search.html', form=form, query=query, posts=posts)


@current_app.route('/admin')
@login_required
def admin():
    admin_role = ROLE['admin']
    if current_user.role == admin_role:
        return render_template('admin.html')
    else:
        flash("Sorry, to access this page you must be an admin.", "danger")
        return redirect(url_for('index'))


# pass stuff to a navbar
@current_app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@current_app.route('/uploads/<path:name>')
def uploaded_file(name):
    return send_from_directory(path.abspath(path.dirname(__file__))+"/static/post_pics", name)

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
