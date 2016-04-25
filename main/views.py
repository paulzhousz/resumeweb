#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Paul'

from flask import Blueprint, render_template, redirect, request, session, url_for, flash, jsonify
import json
from flask.ext.login import login_user, login_required, logout_user, current_user

from main.forms import LoginForm
from app import db, pagenumber
import models

blueprint = Blueprint('main', __name__, url_prefix='/main', static_folder='../static')


# 返回特定页数的生效职位列表
# branch_id：当前用户所属的公司ID
# page：页码
def get_pagedpositionlist(branch_id, page=1):
    query = models.PositionInfo.query.filter(models.PositionInfo.status == '1',
                                             branch_id == models.PositionInfo.branchid)
    positionpagedlist = query.order_by(
        models.PositionInfo.enddate.desc()).paginate(
        page, per_page=pagenumber, error_out=False)
    return positionpagedlist


# 获取当前生效的职位数量
# branch_id:当前用户所属的公司ID
def position_count(branch_id):
    return get_pagedpositionlist(branch_id).total


# 返回特定页数的生效简历列表
# branch_id：当前用户所属的公司ID
# page：页码
# positionid:特定的职位，None表示所有生效职位
def get_pagedresumelist(branch_id, page=1, positionid=None):
    query = models.ResumeInfo.query.join(models.PositionInfo,
                                         models.PositionInfo.positionID == models.PositionResume.positionid)
    query = query.add_columns(models.PositionInfo.positionID, models.PositionInfo.positionname)
    query = query.join(models.PositionResume, models.ResumeInfo.resumeid == models.PositionResume.resumeid)
    query = query.filter(models.PositionInfo.branchid == branch_id)

    if positionid is not None and positionid != '':
        query = query.filter(models.PositionInfo.positionID == positionid)
    else:
        query = query.filter(models.PositionInfo.status == '1')

    resumepagedlist = query.order_by(models.ResumeInfo.posttime.desc()).paginate(
        page, per_page=pagenumber, error_out=False)

    return resumepagedlist


# 获取当前生效的职位投递简历数量
# branch_id:当前用户所属的公司ID
def resume_count(branch_id):
    return get_pagedresumelist(branch_id).total


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = models.UserInfo.query.filter_by(loginname=form.username.data).first()
        if user is not None and user.verifypassword(form.password.data):
            login_user(user, form.remember_me.data)
            branch = models.BranchInfo.query.filter_by(branchid=user.branchid).first()
            # todo 调整session存储
            session['branchname'] = branch.cname
            session['username'] = user.username
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password!')
    return render_template('main/login.html', form=form)


@blueprint.route('/index')
@login_required
def index():
    return render_template('main/index.html',
                           positionnum=position_count(current_user.branchid),
                           resumenum=resume_count(current_user.branchid))


@blueprint.route('/getpositionlist', methods=['GET', 'POST'])
@login_required
def getpositionlist():
    """
    为页面jquery.datatables返回json
    :return:json
    """
    # position_list = get_pagedresumelist(current_user.branchid, page_num)
    # items = position_list.items
    # datas = []
    # for item in items:
    #     for i in (0, len(item) - 1):
    #         if isinstance(item[i], models.ResumeInfo):
    #             datas.append(item[i].get_serialize())

    try:
        values = request.form.to_dict()
        if values.has_key('start'):
            page_num = int(values['start']) / pagenumber + 1
        else:
            page_num = 1
        position_list = get_pagedpositionlist(current_user.branchid, page_num)
        return jsonify(data=[item.get_serialize() for item in position_list.items],
                       recordsTotal=position_list.total,
                       recordsFiltered=position_list.total)
    except Exception, e:
        return jsonify(Success=False, info=e.message)


@blueprint.route('/getresumelist', methods=['GET', 'POST'])
@login_required
def getresumelist():
    """
    为简历列表页面返回datatables所需的json数据
    :return:简历列表json数据
    """
    try:
        values = request.form.to_dict()
        if values.has_key('start'):
            page_num = int(values['start']) / pagenumber + 1
        else:
            page_num = 1
        if values.has_key('pid') and values['pid'] != 'None':
            position_id = values['pid']
        else:
            position_id = None

        resume_list = get_pagedresumelist(current_user.branchid, page_num, position_id)
        items = resume_list.items
        datas = []
        for item in items:
            for i in (0, len(item) - 1):
                if isinstance(item[i], models.ResumeInfo):
                    datas.append(item[i].get_serialize())
        return jsonify(data=datas,
                       recordsTotal=resume_list.total,
                       recordsFiltered=resume_list.total)
    except Exception, e:
        return jsonify(Success=False, info=e.message)


@blueprint.route('/position')
@login_required
def position():
    return render_template('main/positionlist.html', pagenum=pagenumber)


@blueprint.route('/resume/')
@blueprint.route('/resume/<positionid>')
@login_required
def resume(positionid=None):
    if positionid is not None:
        p = models.PositionInfo.query.filter_by(positionID=positionid).first()
        positioninfo =u'['+ p.positionname + u' 来自 ' + p.source+u']'
    else:
        positioninfo=''
    return render_template('main/resumelist.html', pagenum=pagenumber, positionid=positionid,positioninfo=positioninfo)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
