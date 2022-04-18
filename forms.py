from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, HiddenField, IntegerField, MultipleFileField, TextAreaField
from wtforms.validators import InputRequired, Email, Length
from app import db
from tables import Asset

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    first_name = StringField('First name', validators=[InputRequired(), Length(min=4, max=15)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class Asset_selector(FlaskForm):
    autocomplete = StringField('Asset', validators=[InputRequired()])
    add_favorites = BooleanField('Add to favorites')

class repair_request(FlaskForm):
    description = TextAreaField('Description', validators=[InputRequired()])
    files = MultipleFileField('Attachments', render_kw={'multiple': True})
    damage_case = BooleanField('Damage case')
    depannage_required = BooleanField('Depannage required')