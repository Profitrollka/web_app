from os import remove
from flask import abort, render_template, flash, redirect, url_for, request,  current_app
from flask_login import current_user, login_required
from .forms import PostForm, CommentForm
from . import bp
import app.servises
from app.utilities import PostPicture
from os.path import join


@bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    picture_file = PostPicture(current_app.config['UPLOAD_FOLDER_POST'])
    if form.validate_on_submit():
        if form.file.data:
            picture_file = PostPicture(form.file.data)
            picture_file.rename_picture()
            picture_file.resize_picture()
        post = app.servises.post_service.new(title=form.title.data, intro=form.intro.data, text=form.text.data,
                                             user_id=current_user.user_id, picture_file=picture_file.name)
        post_tags_list = []
        if form.tag.data:
            for word in form.tag.data.replace(" ", "").replace("#", "").replace("[", "").replace("]", "").split(","):
                tag = app.servises.tag_service.find(tag_name=word.lower()).first()
                if tag:
                    pass
                else:
                    tag = app.servises.tag_service.new(tag_name=word.lower())
                    try:
                        app.servises.tag_service.save(tag)
                    except Exception as e:
                        flash('An error occurred while saving data. Please try again later.', 'danger')
                        current_app.logger.warning(f"An error occurred while saving data (add new tag)")
                        current_app.logger.exception(e)
            post_tags_list.append(tag)
        post.tags = post_tags_list
        try:
            app.servises.post_service.save(post)
            if form.file.data:
                picture_file.save_picture(current_app.config['UPLOAD_FOLDER_POST'])
            flash('Your post has been created!', 'success')
            current_app.logger.info(f'User {current_user.username} added new post.')
            return redirect(url_for('index'))
        except Exception as e:
            flash('An error occurred while saving data. Please try again later.', 'danger')
            current_app.logger.warning(f"An error occurred while saving data (add new post)")
            current_app.logger.exception(e)
            return redirect(url_for('posts.new_post'))
    return render_template('post.html', title='New post', form=form, legend='Add Post')


@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def single_post(post_id: int):
    form = CommentForm()
    post = app.servises.post_service.get_or_404(post_id)
    posts = app.servises.post_service.get_order_by('created', 'desc', 5)
    comments = app.servises.comment_service.find(post_id=post_id)
    post_tags = app.servises.tag_service.get(post_id)
    if request.method == 'POST':
        if current_user.is_authenticated:
            if form.validate_on_submit():
                comment = app.servises.comment_service.new(text=form.text.data, user_id=current_user.user_id,
                                                        post_id=post_id)
                try:
                    app.servises.comment_service.save(comment)
                    flash('Your comment has been added!', 'success')
                    current_app.logger.info(f'User {current_user.username} added new comment.')
                except Exception as e:
                    flash('An error occurred while saving data. Please try again later.', 'danger')
                    current_app.logger.warning(f"An error occurred while saving data (add new comment)")
                    current_app.logger.exception(e)
                    return redirect(url_for('posts.single_post', post_id=post_id))
    return render_template('single_post.html', post=post, posts=posts, comments=comments, form=form, post_id=post_id,
                           post_tags=post_tags, title='Single post')


@bp.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id: int):
    post = app.servises.post_service.get_or_404(post_id)
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
            tag = app.servises.tag_service.find(tag_name=word.lower()).first()
            if tag:
                pass
            else:
                tag = app.servises.tag_service.new(tag_name=word.lower())
                try:
                    app.servises.tag_service.save(tag)
                except Exception as e:
                    flash('An error occurred while saving data. Please try again later.', 'danger')
                    current_app.logger.warning(f"An error occurred while saving data (add new tag)")
                    current_app.logger.exception(e)
            post_tags_list.append(tag)
        post.tags = post_tags_list
        try:
            app.servises.post_service.save(post)
            if form.file.data:
                picture_file.save_picture(current_app.config['UPLOAD_FOLDER_POST'])
            flash('Your post has been updated!', 'success')
            current_app.logger.info(f'User {current_user.username} updated post {post.post_id}.')
            return redirect(url_for('posts.single_post', post_id=post_id))
        except Exception as e:
            flash('An error occurred while saving data. Please try again later.', 'danger')
            current_app.logger.warning(f"An error occurred while saving data (update post)")
            current_app.logger.exception(e)
            return redirect(url_for('posts.single_post', post_id=post_id))
    elif request.method == "GET":
        form.title.data = post.title
        form.intro.data = post.intro
        form.text.data = post.text
        form.tag.data = post.tags
    return render_template('post.html', title='Update post', form=form, legend='Update Post')


@bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id: int):
    post = app.servises.post_service.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    for comment in post.comments:
        app.servises.comment_service.delete(comment)
    picture_for_delete = post.picture_file
    try:
        app.servises.post_service.delete(post)
        path = join(current_app.root_path, 'static', current_app.config['UPLOAD_FOLDER_POST'], picture_for_delete)
        remove(path)
        flash('Your post has been deleted!', 'success')
        current_app.logger.info(f'User {current_user.username} deleted post {post.post_id}.')
        return redirect(url_for('index'))
    except Exception as e:
        flash('An error occurred while deleting post. Please try again later.', 'danger')
        current_app.logger.warning(f"An error occurred while saving data (delete post)")
        current_app.logger.exception(e)
        return redirect(url_for('posts.single_post', post_id=post_id))


@bp.route('/comment/<int:comment_id>/update', methods=['GET', 'POST'])
@login_required
def update_comment(comment_id: int):
    comment = app.servises.comment_service.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    form = CommentForm()
    if form.validate_on_submit():
        comment.text = form.text.data
        try:
            app.servises.comment_service.save(comment)
            flash('Your comment has been updated!', 'success')
            current_app.logger.info(f'User {current_user.username} updated comment {comment.comment_id}.')
            return redirect(url_for('posts.single_post', post_id=comment.post_id))
        except Exception as e:
            flash('An error occurred while saving data. Please try again later.', 'danger')
            current_app.logger.warning(f"An error occurred while saving data (update comment)")
            current_app.logger.exception(e)
            return redirect(url_for('posts.single_post', post_id=comment.post_id))
    elif request.method == "GET":
        form.text.data = comment.text
    return render_template('comment.html', title='Update comment', form=form, legend='Update Comment')


@bp.route('/comment/<int:comment_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_comment(comment_id: int):
    comment = app.servises.comment_service.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    try:
        app.servises.comment_service.delete(comment)
        flash('Your comment has been deleted!', 'success')
        current_app.logger.info(f'User {current_user.username} deleted comment {comment.comment_id}.')
        return redirect(url_for('posts.single_post', post_id=comment.post_id))
    except Exception as e:
        flash('An error occurred while deleting post. Please try again later.', 'danger')
        current_app.logger.warning(f"An error occurred while saving data (delete comment)")
        current_app.logger.exception(e)
        return redirect(url_for('posts.single_post', post_id=comment.post_id))
