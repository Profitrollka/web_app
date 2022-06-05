from flask import render_template, send_from_directory, current_app
from os import path


@current_app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@current_app.route('/about')
def about():
    return render_template('about.html', title='About')


@current_app.route('/uploads/<path:name>')
def uploaded_file(name):
    return send_from_directory(path.abspath(path.dirname(__file__))+"/static/post_pics", name)

