# -*- coding: utf-8 -*-
from flask import jsonify
from server import app


@app.route('/topic/<topic_id>/', methods=['GET'])
def topic(topic_id):
    """
        返回话题详情
    """
    return jsonify({'topic_id': topic_id, 'title': 'Dummy'})
