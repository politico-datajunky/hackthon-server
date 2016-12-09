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
        if len(request.form['skills']) == 1:
            participator.skills = request.form['skills'][0]
        elif len(request.form['skills']) == 0:
            participator.skills = None
        else:
            participator.skills = '&'.join(request.form['skills'])
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
