# -*- coding: utf-8 -*-
from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_object('settings.DevelopmentConfig')


@app.route('/login', methods=['POST'])
def login():
    """
        输入：用户名、密码
        返回用户信息
    """
    return jsonify({'username': 'Dummy', 'password': 'Dummy'})


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000
    )
