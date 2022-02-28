from flask_wtf import FlaskForm 
from wtforms import StringField,PasswordField,SubmitField, validators
from wtforms.validators import DataRequired , EqualTo

class LoginForm(FlaskForm):
    #Could change the validators to specify a minimum length for the username/password
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login') 

