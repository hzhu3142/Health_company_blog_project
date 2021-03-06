# blog_post/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField
from wtforms.validators import DataRequired

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextField('Text', validators=[DataRequired()])
    submit = SubmitField('Post')

