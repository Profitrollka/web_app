from flask import render_template
from . import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title='Error 404'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', title='Error 500'), 500

# @app.errorhandler(413)
# def request_entity_too_large(error):
#     return 'File Too Large', 413


@app.errorhandler(403)
def forbidden_delete_post(error):
    return 'Only post author can delete post', 403