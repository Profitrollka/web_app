from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length, Email
from flask_ckeditor import CKEditorField
from .models import User
from . import app


class ExtraValidatorsMixin(object):

    EXCLUDED_CHARS = "*?!^+%&/()=][}{#$"

    @classmethod
    def _check_excluded_chars(cls, field_for_check):
        for char in field_for_check:
            if char in cls.EXCLUDED_CHARS:
                raise ValidationError(f"Character {char} is not allowed.")

    @classmethod
    def validate_username(cls, form, username):
        cls._check_excluded_chars(username.data)

    @classmethod
    def validate_last_name(cls, form, last_name):
        cls._check_excluded_chars(last_name.data)

    @classmethod
    def validate_first_name(cls, form, first_name):
        cls._check_excluded_chars(first_name.data)

    @staticmethod
    def validate_if_username_is_taken(user_name):
        if User.query.filter_by(username=user_name).first():
            raise ValidationError(f'Username {user_name} is taken. Please choose a different one.')

    @staticmethod
    def validate_if_email_is_taken(email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError(f'Email {email} is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm, ExtraValidatorsMixin):
    first_name = StringField("First name", validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    about_me = CKEditorField("About me", validators=[Length(min=0, max=140)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password'), Length(min=6, max=30)])
    file = FileField("Avatar", validators=[FileAllowed(app.config['ALLOWED_EXTENSIONS'])])
    submit = SubmitField('Sign Up')


class UpdateProfileForm(FlaskForm, ExtraValidatorsMixin):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    about_me = CKEditorField("About me", validators=[Length(min=0, max=140)])
    first_name = StringField("First name", validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(min=2, max=20)])
    file = FileField("Update Profile Picture", validators=[FileAllowed(app.config['ALLOWED_EXTENSIONS'])])
    submit = SubmitField('Update')


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=0, max=100)])
    intro = TextAreaField("Intro", validators=[DataRequired(), Length(min=0, max=360)])
    text = CKEditorField("Text", validators=[DataRequired(), Length(min=2, max=3000)])
    tag = TextAreaField("Tags", validators=[Length(max=64)])
    file = FileField("Add photos", validators=[FileAllowed(app.config['ALLOWED_EXTENSIONS'])])
    submit = SubmitField('Add post')


class CommentForm(FlaskForm):
    text = TextAreaField("Your comment", validators=[DataRequired(), Length(min=0, max=100)])
    submit = SubmitField('Add comment')


class SearchForm(FlaskForm):
    query = StringField("Query", validators=[DataRequired()])
    submit = SubmitField('Login')
