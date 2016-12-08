# coding: utf-8

from flask import jsonify, request
from server import app

@app.route('/create_requirement', methods=['POST'])
def create_requirement():
    uid = request.form['uid']
    content = request.form['content']
    require = request.form['require']
    reward = request.form['reward']
    time = request.form['time']
    print request.form

    # todo: 插入数据库，成功，失败

    return jsonify({'status': 100})


@app.route('/bid_requirement', methods=['POST'])
def bid_requirement():
    uid = request.form['uid']
    requirement_id = request.form['requirement_id']

    # todo: 查数据库status判断该单是否已经被抢，若没被抢，

    return jsonify({'status': 100})


@app.route('/get_requirement', methods=['POST'])
def get_requirement():
    uid = request.form['uid']
    requirement_id = request.form['requirement_id']

    # todo: get需求对象，解析成json返回

    res = {
        'uid': 100,
        'content': '我想学java',
        'require': ['java', 'php'],
        'reward': '请吃饭',
        'time': '20161208 00:00:00'
    }
    return jsonify(res)

@app.route('/accept_bidder', methods=['POST'])
def accept_bidder():
    uid = request.form['uid']
    requirement_id = request.form['requirement_id']

