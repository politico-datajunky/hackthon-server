# -*- coding: utf-8 -*-
from flask import jsonify, request
from server import app
from server.models import Participator, Topic, Reply, db

"""
    topic 相关CURD操作
"""


@app.route('/topic', methods=['POST'])
def create_topic():
    """
        创建话题，返回话题详情
    """
    participator = Participator.query.filter_by(user_id=int(request.form['uid']))
    image = ""
    topic = Topic(
        user_id=request.form['uid'],
        content=request.form['content'],
        image=image
    )
    return jsonify({
        'topic_id': topic.id,
        'uid': topic.user_id,
        'name': participator.name,
        'avatar': participator.avatar,
        'content': topic.content,
        'image': topic.image,
        'time': topic.pub_date,
        'reply_number': topic.reply_number
    })


@app.route('/topic/<topic_id>/', methods=['POST'])
def topic(topic_id):
    """
        获取话题详情
    """
    if request.method == 'GET':
        return jsonify({'topic_id': topic_id, 'title': 'Dummy'})
    return jsonify({'msg': 'success'})


@app.route('/topiclist', methods=['POST'])
def topiclist():
    uid = request.form['uid']
    page = request.form['page']
    page_count = request.form['page_count']
    topics = []
    return jsonify({'uid': uid, 'list': topics})