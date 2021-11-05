from . import app
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<int:user_id>')
def profile(user_id):
    return "Profile page of user {}".format(user_id)

# @app.route('/login/', methods=['post', 'get'])
# def login():
#     if current_user.is_authenticated:
# 	return redirect(url_for('admin'))
#     form = LoginForm()
#     if form.validate_on_submit():
# 	user = db.session.query(User).filter(User.username == form.username.data).first()
# 	if user and user.check_password(form.password.data):
# 	    login_user(user, remember=form.remember.data)
# 	     return redirect(url_for('admin'))
# 	flash("Invalid username/password", 'error')
# 	return redirect(url_for('login'))
#     return render_template('login.html', form=form)

# @app.route('/contact/', methods=['get', 'post'])
# def contact():
#     form = ContactForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         email = form.email.data
#         message = form.message.data
#
#         # здесь логика БД
#         feedback = Feedback(name=name, email=email, message=message)
#         db.session.add(feedback)
#         db.session.commit()
#
#         send_mail("New Feedback", app.config['MAIL_DEFAULT_SENDER'], 'mail/feedback.html',
#                   name=name, email=email)
#
#         flash("Message Received", "success")
#         return redirect(url_for('contact'))
#
#     return render_template('contact.html', form=form)
#
#
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