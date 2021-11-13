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
    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField("Last name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign in')


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


class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

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

class PostForm(FlaskForm):

    title = StringField("Title", validators=[DataRequired(), Length(min=0, max=140)])
    intro = TextAreaField("Intro", validators=[DataRequired(), Length(min=0, max=360)])
    text = TextAreaField("Text", validators=[DataRequired()])
    file = FileField("Files")
    ALLOWED_EXTENSIONS = set(['png', 'jpg'])
    submit = SubmitField('Add post')

    def __init__(self, user_id, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.user_id = user_id

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS






