from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField, FileField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from email_validator import validate_email, EmailNotValidError
from .models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField("Last name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    file = FileField("Files")
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(nickname=self.username.data).first()
        if user is not None:
            raise ValidationError('Username is already exists, please use different username')

    def validate_email(self, email):
        user = User.query.filter_by(email=self.email.data).first()
        if user is not None:
            raise ValidationError('Email address is already exist')
        try:
            validate_email(email.data)
        except EmailNotValidError:
            raise ValidationError('Email address is not valid')

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS


class EditProfileForm(FlaskForm):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField("Last name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

    file = FileField("Files")
    submit = SubmitField('Submit')

    def __init__(self, original_username, original_email, original_first_name, original_last_name, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
        self.original_first_name = original_first_name
        self.original_last_name = original_last_name

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(nickname=self.username.data).first()
            if user is not None:
                raise ValidationError('Username is already exists, please use different username')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Email address is already exist')
            try:
                validate_email()
            except EmailNotValidError:
                raise ValidationError('Email address is not valid')

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

class PostForm(FlaskForm):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    title = StringField("Title", validators=[DataRequired(), Length(min=0, max=140)])
    intro = TextAreaField("Intro", validators=[DataRequired(), Length(min=0, max=360)])
    text = TextAreaField("Text", validators=[DataRequired()])
    file = FileField("Files")
    submit = SubmitField('Add post')

    def __init__(self, user_id, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.user_id = user_id

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS


class CommentForm(FlaskForm):
    text = TextAreaField("Your comment", validators=[DataRequired(), Length(min=0, max=100)])
    submit = SubmitField('Add comment')












