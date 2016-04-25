#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Paul'
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class DevConfig(Config):
    DEBUG = True
    USER_RELOADER = False
    DB_NAME = 'app.db'
    DB_PATH = os.path.join(basedir, DB_NAME)
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
