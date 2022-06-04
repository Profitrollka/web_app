from .users.forms import *
from .posts.forms import *


class SearchForm(FlaskForm):
    query = StringField("Query", validators=[DataRequired()])
    submit = SubmitField('Login')
