#!/usr/bin/env python

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, URL, Length

class EmailPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class URLForm(FlaskForm):
    url = StringField('Image URL', validators=[DataRequired(),URL(require_tld=True,message="That is not a valid link url!")])
