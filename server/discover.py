# coding: utf-8

import random
from difflib import SequenceMatcher as SM
from flask import jsonify, request
from server import app
from server.models import Participator, Skill


@app.route('/api/discover_home', methods=['POST'])
def discover_home():
    user_id = int(request.form['uid'])
    user_num = Participator.query.count()
    uids = random.sample(xrange(1, user_num), 4)
    hot = []
    for uid in uids:
        if len(hot) >= 2:
            break
        if uid != user_id:
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
    for uid in uids:
        if uid != user_id:
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
    return jsonify({'status': 100, 'data': res})


@app.route('/api/discover_search', methods=['POST'])
def discover_search():
    uid = request.form['uid']
    skill = request.form.get('skill', '')
    matched_skills = []
    skills = Skill.query.first().skills.split('|')
    for s in skills:
        ratio = SM(None, skill.lower(), s).ratio()
        if ratio >= 0.5:
            matched_skills.append((s, ratio))
    res = []
    matched_skills = sorted(matched_skills, key=lambda x: x[1], reverse=True)
    for matched_skill in matched_skills:
        users = Participator.query.filter(Participator.skills.like('%'+matched_skill[0]+'%'))
        for user in users:
            user_skills = user.skills.split('|')
            if matched_skill[0].upper() in user_skills:
                res.append({
                    'uid': user.user_id,
                    'name': user.name,
                    'gender': user.gender,
                    'avatar': user.avatar,
                    'position': user.position,
                    'skills': user_skills
                })
    if res:
        return jsonify({'status': 100, 'data': res})
    else:
        return jsonify({'status': 101, 'data': '未找到相关结果'})
