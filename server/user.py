# -*- coding: utf-8 -*-
from flask import jsonify
from server import app


@app.route('/login', methods=['POST'])
def login():
    """
        输入：用户名、密码
        返回用户信息
    """
    return jsonify({'username': 'Dummy', 'password': 'Dummy'})