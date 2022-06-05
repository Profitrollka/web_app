from wtforms import SubmitField, StringField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    query = StringField("Query", validators=[DataRequired()])
    submit = SubmitField('Login')