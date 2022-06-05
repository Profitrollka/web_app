from flask import request, redirect, url_for, render_template, current_app, jsonify
from app import db
from app.models import Post, Comment, Tag, post_tags
from json import loads
from .forms import SearchForm
from . import bp


@bp.route('/')
def index():
    query = request.args.get('query')
    if query:
        return redirect(url_for('main.search', tagname=query))
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


@bp.route('/posts/search', methods=['GET'])
def search_posts():
    tags = loads(request.data['tags'])
    posts = db.session.query(Post).join(post_tags).join(Tag).filter(Tag.tag.in_(tags)).group_by(Post.post_id).all()
    return jsonify(posts)


@bp.route('/search_by_tag/<tagname>', methods=["GET"])
def search_by_tag(tagname: str):
    tag = Tag.query.filter_by(tag_name=tagname).first()
    posts_id = db.session.query(post_tags).filter_by(tag_id=tag.tag_id).all()
    posts = []
    for post_id in posts_id:
        post = Post.query.filter_by(post_id=post_id[0]).first()
        posts.append(post)
    return render_template('tags.html', title='Posts', posts=posts)


@bp.route('/search_by_query', methods=["POST"])
def search_by_query():
    form = SearchForm()
    posts = Post.query
    if form.validate_on_submit():
        query = form.query.data
        posts = posts.filter(Post.text.like('%'+query+'%'))
        posts = posts.order_by(Post.created.desc()).all()
        return render_template('search.html', form=form, query=query, posts=posts)


# pass stuff to a navbar
@bp.context_processor
def base():
    form = SearchForm()
    return dict(form=form)
