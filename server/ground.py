# -*- coding: utf-8 -*-
from flask import jsonify, request
from server import app
from server.models import UserRequire, Participator, AnswerRequire, db

import time

"""
    广场相关接口
"""


@app.route('/ground', methods=['POST'])
def ground():
    page = int(request.form['page'])
    page_count = int(request.form['page_count'])
    requires = UserRequire.query.order_by('pub_time').paginate(page=page, per_page=page_count).items
    results = []
    for each in requires:
        participator = Participator.query.filter_by(user_id=each.user_id).first()
        apply_users = AnswerRequire.query.filter_by(userrequire_id=each.id).first()

        if apply_users is None:
            apply_users = []
        else:
            users = apply_users.users_id.split('|')
            users = Participator.query.filter(Participator.user_id.in_(users))
            apply_users = []
            for user in users:
                apply_users.append({'uid': user.user_id, 'name': user.name})
        results.append({
            'uid': each.user_id,
            'user_name': participator.name,
            'user_avatar': participator.avatar,
            'title': each.title,
            'content': each.content,
            'condition': each.condition,
            'reward': each.reward,
            'pub_time': each.pub_time,
            'status': each.status,
            'answer_user': each.answer_user,
            'apply_users': apply_users
        })
    return jsonify({'requirements': results})


@app.route('/ground/search', methods=['POST'])
def ground_search():
    body = dict(request.form).keys()
    requires = UserRequire.query.all()
    if 'uid' in body:
        requires = UserRequire.query.filter_by(user_id=request.form['uid'])
    if 'skill' in body:
        requires = UserRequire.query.filter(UserRequire.condition.like('%'+request.form['skill']+'%'))
    results = []
    for each in requires:
        participator = Participator.query.filter_by(user_id=each.user_id).first()
        apply_users = AnswerRequire.query.filter_by(userrequire_id=each.id).first()

        if apply_users is None:
            apply_users = []
        else:
            users = apply_users.users_id.split('|')
            users = Participator.query.filter(Participator.user_id.in_(users))
            apply_users = []
            for user in users:
                apply_users.append({'uid': user.user_id, 'name': user.name})
        results.append({
            'uid': each.user_id,
            'user_name': participator.name,
            'user_avatar': participator.avatar,
            'title': each.title,
            'content': each.content,
            'condition': each.condition,
            'reward': each.reward,
            'pub_time': each.pub_time,
            'status': each.status,
            'answer_user': each.answer_user,
            'apply_users': apply_users
        })
    return jsonify({'requirements': results})


@app.route('/ground/init_requirement', methods=['POST'])
def init_requirement():
    requirement1 = UserRequire(
        user_id=1,
        title='请帮忙查看一下imei为xxxx的用户积分为什么没有加上?',
        content='rt',
        condition='积分墙',
        reward='一颗棒棒糖',
        pub_time=int(time.time()*1000),
        status=1,
        answer_user=1
    )
    requirement2 = UserRequire(
        user_id=2,
        title='帮忙教java',
        content='我想学习java有谁能教我一下...',
        condition='java',
        reward='请吃饭',
        pub_time=int(time.time()*1000)
    )
    requirement3 = UserRequire(
        user_id=3,
        title='求帮忙解释dsp是个啥',
        content='快要接触多盟的dsp平台，谁比较熟悉帮忙讲解一下',
        condition='dsp|PM',
        reward='请喝咖啡',
        pub_time=int(time.time()*1000)
    )
    requirement4 = UserRequire(
        user_id=4,
        title='我家电脑坏了，怎么破',
        content='我家电脑坏了，有谁能帮忙修一下吗？今晚家里没人。。。',
        condition='java',
        reward='请吃饭',
        pub_time=int(time.time()*1000)
    )
    requirement5 = UserRequire(
        user_id=5,
        title='关于python多线程开发的问题',
        content='最近在学，多线程开发，想找人碰一下坑',
        condition='python',
        reward='玩游戏',
        pub_time=int(time.time()*1000)
    )
    db.session.add(requirement1)
    db.session.add(requirement2)
    db.session.add(requirement3)
    db.session.add(requirement4)
    db.session.add(requirement5)
    db.session.commit()

    # apply_users1 = AnswerRequire(
    #     userrequire_id=requirement1.id,
    #     users_id='1|3|4'
    # )
    # apply_users2 = AnswerRequire(
    #     userrequire_id=requirement2.id,
    #     users_id='1|2|4'
    # )
    # apply_users3 = AnswerRequire(
    #     userrequire_id=requirement3.id,
    #     users_id='1|3|5'
    # )
    # apply_users4 = AnswerRequire(
    #     userrequire_id=requirement4.id,
    #     users_id='2|3|4'
    # )
    # apply_users5 = AnswerRequire(
    #     userrequire_id=requirement5.id,
    #     users_id='3|4|5'
    # )
    # db.session.add(apply_users1)
    # db.session.add(apply_users2)
    # db.session.add(apply_users3)
    # db.session.add(apply_users4)
    # db.session.add(apply_users5)
    # db.session.commit()
    return jsonify({'status': 'success'})