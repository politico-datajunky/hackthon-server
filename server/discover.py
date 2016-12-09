# coding: utf-8

import random
from difflib import SequenceMatcher as SM
from flask import jsonify, request
from server import app
from server.models import Participator, Skill


@app.route('/api/discover_home', methods=['POST'])
def discover_home():
    user_num = Participator.query.count()
    uids = random.sample(xrange(1, user_num), 4)
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
    return jsonify({'status': 100, 'data': res})


@app.route('/api/discover_search', methods=['POST'])
def discover_search():
    skill = request.form.get('skill', '')

    matched_skills = []
    skills = Skill.query.first().skills.split('|')
    for s in skills:
        ratio = SM(None, skill.lower(), s).ratio()
        if ratio >= 0.5:
            matched_skills.append((s, ratio))
    res = []
    matched_skills = sorted(matched_skills, key=lambda x: x[1], reverse=True)
    users = Participator.query.all()

    for matched_skill in matched_skills:
        for user in users:
            user_skills = user.skills.split('|')
            for user_skill in user_skills:
                if user_skill == matched_skill[0]:
                    res.append({
                        'uid': user.user_id,
                        'name': user.name,
                        'gender': user.gender,
                        'avatar': user.avatar,
                        'position': user.position,
                        'skills': user_skills
                    })
                    break
    if res:
        return jsonify({'status': 100, 'data': res})
    else:
        return jsonify({'status': 101, 'data': '未找到相关结果'})
