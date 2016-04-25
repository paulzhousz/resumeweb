#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Paul'

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('User name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me?')
    submit = SubmitField('Login')
