# -*- coding: utf-8 -*-
from flask import jsonify, request
from server import app
from server.models import db
from server.models import User, Participator


@app.route('/login', methods=['POST'])
def login():
    """
        输入：用户名、密码
        返回用户信息
    """
    username = 'Dummy'
    password = 'Dummy'
    user = User.query.filter_by(username=username).first()
    if user is None or password != user.password:
        return jsonify({'status': 110, 'error': 'password or username wrrong!'})
    participator = Participator.query.get(user_id=user.id)
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


@app.route('/user/<uid>', methods=['POST'])
def update_user(uid):
    body = request.form.__dict__
    return jsonify({'uid': ''})
