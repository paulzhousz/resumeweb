#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Paul'

from flask.ext.login import UserMixin
from sqlalchemy import inspect
import datetime, decimal
from app import db, login_manager


class Serializer(object):
    """
    Mixin for retrieving public fields of model in json-compatible format
    """
    __allowed_in_json__ = None

    @classmethod
    def _serialize(cls, value):
        if type(value) in (int, float, long, bool):
            ret = str(value)
        elif type(value) is unicode:
            ret = value.encode('utf-8')
        elif isinstance(value, datetime.date):
            ret = value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, datetime.time) or isinstance(value, datetime.datetime):
            ret = value.isoformat()
        elif isinstance(value, decimal.Decimal):
            ret = str(value)
        else:
            ret = value
        return ret

    def get_serialize(self, exclude=()):
        """Returns model's PUBLIC data for jsonify"""
        data = {}
        keys = inspect(self).attrs.keys()
        public = self.__allowed_in_json__
        for col in keys:
            if public is not None:
                if col not in public:
                    continue
            if col in exclude:
                continue
            data[col] = self._serialize(getattr(self, col))
        return data


class UserInfo(UserMixin, db.Model, Serializer):
    __tablename__ = "t_userinfo"
    userid = db.Column(db.String(50), primary_key=True)
    loginname = db.Column(db.String(20))
    username = db.Column(db.String(20))
    passwordset = db.Column(db.String(100))
    branchid = db.Column(db.String(50))
    isadmin = db.Column(db.String(10))
    isenabled = db.Column(db.String(10))
    createdate = db.Column(db.String(30))
    updatedate = db.Column(db.String(30))

    def get_id(self):
        return self.userid

    def verifypassword(self, password):
        return self.passwordset == password


class BranchInfo(db.Model, Serializer):
    __tablename__ = "t_branchinfo"
    branchid = db.Column(db.String(50), primary_key=True)
    cname = db.Column(db.String(100))
    ename = db.Column(db.String(100))
    createdate = db.Column(db.String(30))
    updatedate = db.Column(db.String(30))


class PositionInfo(db.Model, Serializer):
    __tablename__ = "T_PositionInfo"

    positionID = db.Column(db.String(50), primary_key=True)
    positionname = db.Column(db.String(100))
    hiringnumber = db.Column(db.Integer)
    location = db.Column(db.String(50))
    workingtime = db.Column(db.String(20))
    degree = db.Column(db.String(20))
    sex = db.Column(db.String(10))
    language = db.Column(db.String(20))
    languagelevel = db.Column(db.String(10))
    agefrom = db.Column(db.Integer)
    ageto = db.Column(db.Integer)
    experience = db.Column(db.Integer)
    category = db.Column(db.String(100))
    major = db.Column(db.String(100))
    salary = db.Column(db.String(100))
    positiondesc = db.Column(db.String(2000))
    enddate = db.Column(db.String(20))
    source = db.Column(db.String(20))
    sourcepositionid = db.Column(db.String(50))
    sourceurl = db.Column(db.String(200))
    status = db.Column(db.String(10))
    branchid = db.Column(db.String(50))
    createdate = db.Column(db.String(30))
    updatedate = db.Column(db.String(30))


class ResumeInfo(db.Model, Serializer):
    __tablename__ = "t_resumeinfo"
    resumeid = db.Column(db.String(50), primary_key=True)
    cname = db.Column(db.String(20))
    ename = db.Column(db.String(20))
    sex = db.Column(db.String(10))
    Residence = db.Column(db.String(50))
    idtype = db.Column(db.String(20))
    idnumber = db.Column(db.String(50))
    birthdate = db.Column(db.String(20))
    marital = db.Column(db.String(10))
    phonenumber = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    email = db.Column(db.String(50))
    qqnumber = db.Column(db.String(50))
    partisan = db.Column(db.String(100))
    hukou = db.Column(db.String(100))
    address = db.Column(db.String(100))
    degree = db.Column(db.String(50))
    workingstart = db.Column(db.String(10))
    currentsalary = db.Column(db.String(50))
    jobstatus = db.Column(db.String(50))
    overseaexp = db.Column(db.String(10))
    overseadesc = db.Column(db.String(500))
    avaliabletime = db.Column(db.String(20))
    jobtime = db.Column(db.String(10))
    expectindustry = db.Column(db.String(100))
    expectsalary = db.Column(db.String(100))
    category = db.Column(db.String(100))
    eduinfo = db.Column(db.String(2000))
    traininginfo = db.Column(db.String(2000))
    workexpinfo = db.Column(db.String(2000))
    projectexpinfo = db.Column(db.String(2000))
    englishlevel = db.Column(db.String(100))
    japaneselevel = db.Column(db.String(100))
    selfevaluation = db.Column(db.String(500))
    skill = db.Column(db.String(500))
    posttime = db.Column(db.String(30))
    source = db.Column(db.String(20))
    sourceresumeid = db.Column(db.String(50))
    sourceurl = db.Column(db.String(100))
    status = db.Column(db.String(10))
    createdate = db.Column(db.String(30))
    updatedate = db.Column(db.String(30))


class PositionResume(db.Model, Serializer):
    __tablename__ = "t_positionresume"

    id = db.Column(db.String(50), primary_key=True)
    positionid = db.Column(db.String(50))
    resumeid = db.Column(db.String(50))
    createdate = db.Column(db.String(30))
    updatedate = db.Column(db.String(30))


@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(user_id)
