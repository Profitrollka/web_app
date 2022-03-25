from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField, FileField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length, Email
from email_validator import validate_email, EmailNotValidError
from .models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    first_name = StringField("First name", validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password'), Length(min=6, max=30)])
    file = FileField("Add avatar")
    submit = SubmitField('Sign Up')


    def validate_username(self, username):
        excluded_chars = "*?!^+%&/()=][}{#$"
        for char in self.username.data:
            if char in excluded_chars:
                raise ValidationError(f"Character {char} is not allowed in username.")
        user = User.query.filter_by(nickname=self.username.data).first()
        if user is not None:
            raise ValidationError('Username is already exists, please use different username')


    def validate_first_name(self, first_name):
        excluded_chars = "*?!^+%&/()=][}{#$"
        for char in self.first_name.data:
            if char in excluded_chars:
                raise ValidationError(f"Character {char} is not allowed in first name.")


    def validate_last_name(self, last_name):
        excluded_chars = "*?!^+%&/()=][}{#$"
        for char in self.last_name.data:
            if char in excluded_chars:
                raise ValidationError(f"Character {char} is not allowed in first name.")


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


class ProfileForm(FlaskForm):
    first_name = StringField("First name")
    last_name = StringField("Last name")
    username = StringField("Username")
    email = StringField("Email")
    about_me = PasswordField("About me")

    def __init__(self, original_first_name, original_last_name, original_username, original_email, original_about_me, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
        self.original_first_name = original_first_name
        self.original_last_name = original_last_name
        self.original_about_me = original_about_me


class EditProfileForm(FlaskForm):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    first_name = StringField("First name", validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password'), Length(min=6, max=30)])
    file = FileField("Add avatar")
    submit = SubmitField('Submit')

    def __init__(self, original_username, original_email, original_first_name, original_last_name, original_about_me, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
        self.original_first_name = original_first_name
        self.original_last_name = original_last_name
        self.original_about_me = original_about_me


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
    text = TextAreaField("Text", validators=[DataRequired(), Length(min=2, max=3000)])
    file = FileField("Add photos")
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












