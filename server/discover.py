# coding: utf-8

import random
from flask import jsonify, request
from server import app
from server.models import Participator

@app.route('/discover_home', methods=['POST'])
def discover_home():
    user_num = Participator.query.count()
    print user_num
    uids = random.sample(xrange(1, user_num), 4)
    # user_id = random.randint(1, user_num)
    hot = []
    for uid in uids[:2]:
        user = Participator.query.get(uid)
        hot.append({
            'uid': user.user_id,
            'name': user.name,
            'gender': user.gender,
            'avatar': user.avatar,
            'position': user.position,
            'skills': user.skills.split('|')
        })
    recommend = []
    for uid in uids[2:user_num]:
        user = Participator.query.get(uid)
        recommend.append({
            'uid': user.user_id,
            'name': user.name,
            'gender': user.gender,
            'avatar': user.avatar,
            'position': user.position,
            'skills': user.skills.split('|')
        })
    res = {
        'hot': hot,
        'recommend': recommend
    }
    return jsonify(res)