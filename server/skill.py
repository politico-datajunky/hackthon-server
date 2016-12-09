# coding: utf-8

from flask import jsonify, request
from server import app
from server.models import db, Skill


@app.route('/add_skill', methods=['POST'])
def add_skill():
    skill_added = request.form.get('skill', '')
    skills = Skill.query.first()
    if skill_added not in skills.skills.split('|'):
        skills.skills += '|'+skill_added
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'msg': '该项技能已存在'})


@app.route('/init_skills', methods=['POST'])
def init_skills():
    skills = 'python|java|php|go|ruby|c|c++|数据分析|ps|axure|视觉设计|产品|设计|视频剪辑|音乐剪辑|flash|ppt|excel|谈判技巧|商务'
    s = Skill(skills)
    db.session.add(s)
    db.session.commit()
    return jsonify({'status': 'success'})
