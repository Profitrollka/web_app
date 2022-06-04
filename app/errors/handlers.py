from flask import render_template
from app import db
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title='Error 404'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', title='Error 500'), 500


@bp.app_errorhandler(413)
def request_entity_too_large(error):
    return render_template('413.html', title='Error 413'), 413


@bp.app_errorhandler(403)
def forbidden_delete_post(error):
    return render_template('403.html', title='Error 403'), 403

