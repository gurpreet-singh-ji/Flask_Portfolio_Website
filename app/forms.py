from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length

class LoginForm(FlaskForm):
    username=StringField('Name',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired(),Length(min=6)])
    submit=SubmitField('submit')