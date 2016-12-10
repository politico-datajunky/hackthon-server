# -*- coding: utf-8 -*-
import os
from flask import jsonify, request
from server import app
from server.models import User, Participator, db
# from werkzeug import secure_filename


@app.route('/api/login', methods=['POST'])
def login():
    """
        输入：用户名、密码
        返回用户信息
    """
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user is None or password != user.password:
        return jsonify({'status': 110, 'error': 'password or username wrrong!'})
    participator = Participator.query.filter_by(user_id=user.id).first()
    return jsonify({
        'status': 100,
        'userinfo': {
            'uid': user.id,
            'username': participator.name,
            'gender': participator.gender,
            'avatar': participator.avatar,
            'company': participator.company,
            'position': participator.position,
            'skills': participator.skills.split('|'),
            'free_time': participator.free_time,
            'phone': participator.phone,
            'email': participator.email,
            'qq': participator.qq
        }
    })


@app.route('/api/user', methods=['POST'])
def update_user():
    """
        更新用户信息，只更新POST body中存在的字段
    """
    uid = request.form['uid']
    participator = Participator.query.filter_by(user_id=uid).first()
    if participator is None:
        return jsonify({
            'status': 119,
            'error': 'uid wrrong!'
        })
    body = dict(request.form)
    if 'name' in body:
        participator.name = request.form['name']
    if 'gender' in body:
        participator.gender = request.form['gender']
    if 'company' in body:
        participator.company = request.form['company']
    if 'position' in body:
        participator.position = request.form['position']
    if 'phone' in body:
        participator.phone = request.form['phone']
    if 'email' in body:
        participator.email = request.form['email']
    if 'qq' in body:
        participator.qq = request.form['qq']
    if 'skills' in body:
        if len(request.form['skills']) == 0:
            participator.skills = None
        else:
            participator.skills = request.form['skills']
    if 'free_time' in body:
        participator.free_time = request.form['free_time']
    if 'avatar' in body:
        participator.avatar = request.form['avatar']
    db.session.commit()
    return jsonify({
        'status': 100,
        'userinfo': {
            'uid': participator.user_id,
            'username': participator.name,
            'gender': participator.gender,
            'avatar': participator.avatar,
            'company': participator.company,
            'position': participator.position,
            'skills': participator.skills.split('|'),
            'free_time': participator.free_time,
            'phone': participator.phone,
            'email': participator.email,
            'qq': participator.qq
        }
    })


@app.route('/api/user/care', methods=['POST'])
def care():
    """
        关注用户
    """
    uid = int(request.form['uid'])
    care_uid = int(request.form['care_id'])
    user = Participator.query.filter_by(user_id=uid).first()
    care_user = Participator.query.filter_by(user_id=care_uid).first()
    if user is None or care_user is None:
        return jsonify({
            'status': 110,
            'error': 'uid wrrong!'
        })
    if not user.care_users:
        user.care_users = str(care_uid)
    else:
        user.care_users += '|' + str(care_uid)
    if not care_user.cared_users:
        care_user.cared_users = str(uid)
    else:
        care_user.cared_users += '|' + str(uid)
    db.session.commit()
    result = []
    for care_user in user.care_users.split('|'):
        someone = Participator.query.filter_by(user_id=care_user).first()
        result.append({
            'uid': someone.user_id,
            'name': someone.name,
            'avatar': someone.avatar
        })
    return jsonify({
        'status': 100,
        'care_list': result
    })


@app.route('/api/user/carelist', methods=['POST'])
def carelist():
    """
        获取用户关注列表
    """
    uid = request.form['uid']
    user = Participator.query.filter_by(user_id=uid).first()
    if user is None:
        return jsonify({
            'status': 110,
            'error': 'uid wrrong!'
        })
    result = []
    if user.care_users:
        for care_user in user.care_users.split('|'):
            someone = Participator.query.filter_by(user_id=care_user).first()
            result.append({
                'uid': someone.user_id,
                'name': someone.name,
                'avatar': someone.avatar
            })
    return jsonify({
        'status': 100,
        'care_list': result
    })


@app.route('/api/userdetail', methods=['POST'])
def user_detail():
    uid = request.form['uid']
    request_userid = request.form['detail_userid']
    user = Participator.query.filter_by(user_id=request_userid).first()
    if user is None:
        return jsonify({
            'status': 110,
            'error': 'uid wrrong!'
        })
    return jsonify({
        'status': 100,
        'userinfo': {
            'uid': user.user_id,
            'username': user.name,
            'gender': user.gender,
            'avatar': user.avatar,
            'company': user.company,
            'position': user.position,
            'skills': user.skills.split('|') if user.skills is not None else [],
            'free_time': user.free_time,
            'phone': user.phone,
            'email': user.email,
            'qq': user.qq,
            'is_care': uid in user.cared_users if user.cared_users is not None else False
        }
    })


@app.route('/api/user/cancel', methods=['POST'])
def cancel_care():
    """
        取消关注
    """
    uid = request.form['uid']
    care_userid = request.form['care_id']
    user = Participator.query.filter_by(user_id=uid).first()

    if user.care_users:
        users = user.care_users.split('|')
        if care_userid in users:
            users.remove(care_userid)
        user.care_users = '|'.join(users)
    care_user = Participator.query.filter_by(user_id=care_userid).first()
    if care_user.cared_users:
        users = care_user.cared_users.split('|')
        if uid in users:
            users.remove(uid)
        care_user.cared_users = '|'.join(users)
    db.session.commit()
    return jsonify({'status': 100})


@app.route('/init_user', methods=['POST'])
def init_user():
    user1 = User('100000', '100000')
    user2 = User('100001', '100001')
    user3 = User('100002', '100002')
    user4 = User('100003', '100003')
    user5 = User('100004', '100004')

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.commit()

    partcipator1 = Participator(
        user_id=user1.id,
        name='洞洞',
        gender=1,
        avatar='/static/defalut-avatar',
        company='多盟',
        position='客户端工程师',
        phone='18510001000',
        email='huangdongdong@domob.cn',
        qq=None,
        skills='java|android|photoshop',
        free_time='{1:["13-15", "19-20"],2:[],3:[],4:[],5:[],6:[],7:[]}'
    )
    partcipator2 = Participator(
        user_id=user2.id,
        name='左烨',
        gender=1,
        avatar='/static/defalut-avatar',
        company='小蓝标',
        position='销售',
        phone='18510001000',
        email='huangdongdong@domob.cn',
        qq=None,
        skills='blabla',
        free_time='{1:["13-15", "19-20"],2:[],3:["15-18"],4:["10-11"],5:[],6:[],7:[]}'
    )
    partcipator3 = Participator(
        user_id=user3.id,
        name='洞洞',
        gender=1,
        avatar='/static/defalut-avatar',
        company='多盟',
        position='客户端工程师',
        phone='18510001000',
        email='huangdongdong@domob.cn',
        qq=None,
        skills='java|android|photoshop',
        free_time='{1:["13-15", "19-20"],2:[],3:[],4:[],5:[],6:[],7:[]}'
    )
    partcipator4 = Participator(
        user_id=user4.id,
        name='洞洞',
        gender=1,
        avatar='/static/defalut-avatar',
        company='多盟',
        position='客户端工程师',
        phone='18510001000',
        email='huangdongdong@domob.cn',
        qq=None,
        skills='java|android|photoshop',
        free_time='{1:["13-15", "19-20"],2:[],3:[],4:[],5:[],6:[],7:[]}'
    )
    partcipator5 = Participator(
        user_id=user5.id,
        name='洞洞',
        gender=1,
        avatar='/static/defalut-avatar',
        company='多盟',
        position='客户端工程师',
        phone='18510001000',
        email='huangdongdong@domob.cn',
        qq=None,
        skills='java|android|photoshop',
        free_time='{1:["13-15", "19-20"],2:[],3:[],4:[],5:[],6:[],7:[]}'
    )

    db.session.add(partcipator1)
    db.session.add(partcipator2)
    db.session.add(partcipator3)
    db.session.add(partcipator4)
    db.session.add(partcipator5)

    db.session.commit()
    return jsonify({'status': 'success'})
