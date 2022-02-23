from random import choices
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, validators, SelectFeild
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, NumberRange


class Finder(FlaskForm):
    lattitude = FloatField('lattitude', validators=[NumberRange(
        min=-90.0, max=90.0, message='Please Enter in the Correct Range'), InputRequired], description='48.182601')
    longitude = FloatField('longitude', validators=[NumberRange(
        min=-180.0, max=180.0, message='Please Enter in the Correct Range'), InputRequired], description='11.304939')
    submit = SubmitField('Search')


class LoginForm(FlaskForm):
    # Could change the validators to specify a minimum length for the username/password
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


gen_choice = [('1', 'Male'), ('2', 'Female'), ('3', 'Others')]


class SignUpForm(FlaskForm):
    # Could change the validators to specify a minimum length for the username/password
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    con_password = PasswordField(
        'Confirm Password', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired])
    last_name = StringField('Last Name', validators=[InputRequired])
    gender = SelectFeild('Gender', choices=gen_choice,
                         validators=[InputRequired])
    dob = DateField('DOB', format='%Y-%m-%d', validators=[InputRequired])
    submit = SubmitField('Sign Up')
