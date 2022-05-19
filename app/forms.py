from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length, Email
from email_validator import validate_email, EmailNotValidError
from .models import User
from . import app


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password'), Length(min=6, max=30)])
    file = FileField("Avatar", validators=[FileAllowed(app.config['ALLOWED_EXTENSIONS'])])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        excluded_chars = "*?!^+%&/()=][}{#$"
        for char in self.username.data:
            if char in excluded_chars:
                raise ValidationError(f"Character {char} is not allowed in username.")
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_first_name(self):
        excluded_chars = "*?!^+%&/()=][}{#$"
        for char in self.first_name.data:
            if char in excluded_chars:
                raise ValidationError(f"Character {char} is not allowed in first name.")

    def validate_last_name(self):
        excluded_chars = "*?!^+%&/()=][}{#$"
        for char in self.last_name.data:
            if char in excluded_chars:
                raise ValidationError(f"Character {char} is not allowed in first name.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
        try:
            validate_email(email.data)
        except EmailNotValidError:
            raise ValidationError('Email address is not valid')


class UpdateProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    first_name = StringField("First name", validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(min=2, max=20)])
    file = FileField("Update Profile Picture", validators=[FileAllowed(app.config['ALLOWED_EXTENSIONS'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if current_user.username != username.data:
            try:
                user = User.query.filter_by(username=username.data).first()
                if user:
                    raise ValidationError('That username is taken. Please choose a different one.')
            except:
                pass

    def validate_first_name(self, first_name):
        if current_user.first_name != first_name.data:
            excluded_chars = "*?!^+%&/()=][}{#$"
            for char in first_name.data:
                if char in excluded_chars:
                    raise ValidationError(f"Character {char} is not allowed in first name.")

    def validate_last_name(self, last_name):
        if current_user.last_name != last_name.data:
            excluded_chars = "*?!^+%&/()=][}{#$"
            for char in last_name.data:
                if char in excluded_chars:
                    raise ValidationError(f"Character {char} is not allowed in first name.")

    def validate_email(self, email):
        if current_user.email != email.data:
            try:
                user = User.query.filter_by(email=email.data).first()
                if user:
                    raise ValidationError('That email is taken. Please choose a different one.')
                validate_email(email.data)
            except EmailNotValidError:
                raise ValidationError('Email address is not valid')


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=0, max=100)])
    intro = TextAreaField("Intro", validators=[DataRequired(), Length(min=0, max=360)])
    text = TextAreaField("Text", validators=[DataRequired(), Length(min=2, max=3000)])
    tag = TextAreaField("Tags", validators=[Length(max=64)])
    file = FileField("Add photos", validators=[FileAllowed(app.config['ALLOWED_EXTENSIONS'])])
    submit = SubmitField('Add post')


class CommentForm(FlaskForm):
    text = TextAreaField("Your comment", validators=[DataRequired(), Length(min=0, max=100)])
    submit = SubmitField('Add comment')
