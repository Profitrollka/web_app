from wtforms import SubmitField, TextAreaField, StringField
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=0, max=100)])
    intro = TextAreaField("Intro", validators=[DataRequired(), Length(min=0, max=360)])
    text = CKEditorField("Text", validators=[DataRequired(), Length(min=2, max=3000)])
    tag = TextAreaField("Tags", validators=[Length(max=64)])
    file = FileField("Add photos", validators=[FileAllowed(ALLOWED_EXTENSIONS)])
    submit = SubmitField('Add post')


class CommentForm(FlaskForm):
    text = TextAreaField("Your comment", validators=[DataRequired(), Length(min=0, max=100)],
                         render_kw={"placeholder": "Add comment..."})
    submit = SubmitField('Add comment')