# -*- coding: utf-8 -*-
from flask import jsonify, request
from server import app

"""
    topic 相关CURD操作
"""


@app.route('/topic', methods=['POST'])
def create_topic():
    """
        创建话题，返回话题详情
    """
    print request.form.__dict__
    # todo 创建话题
    return jsonify({'topic_id': 'Dummy', 'content': 'Dummy'})


@app.route('/topic/<topic_id>/', methods=['GET', 'DELETE'])
def topic(topic_id):
    """
        GET 获取话题
        DELTE 删除话题
    """
    # todo 数据库查询话题详情
    if request.method == 'GET':
        return jsonify({'topic_id': topic_id, 'title': 'Dummy'})
    # todo 删除话题
    return jsonify({'msg': 'success'})