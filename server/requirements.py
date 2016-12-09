# coding: utf-8
from flask import jsonify, request
from server import app
from server.models import db, UserRequire, AnswerRequire, Participator

@app.route('/create_requirement', methods=['POST'])
def create_requirement():
    uid = request.form.get('uid', '')
    title = request.form.get('title', '')
    content = request.form.get('content', '')
    condition = request.form.get('condition', '')
    pub_time = request.form.get('pub_time', '')
    reward = request.form.get('reward', '')

    user_require = UserRequire(uid, title, content, condition, reward, pub_time)
    db.session.add(user_require)
    db.session.commit()

    res = {
        'userrequire_id': user_require.id
    }
    return jsonify(res)


@app.route('/answer_requirement', methods=['POST'])
def answer_requirement():
    uid = request.form.get('uid', '')
    userrequire_id = request.form.get('userrequire_id', '')

    require_status = UserRequire.query.get(userrequire_id).status
    if require_status == UserRequire.WAITING:
        answer_require = AnswerRequire.query\
                                      .filter_by(userrequire_id=userrequire_id)\
                                      .first()
        if answer_require:
            users_id = answer_require.users_id + ' ' + str(uid)
            answer_require.users_id = users_id
            db.session.commit()
        else:
            answer_require = AnswerRequire(userrequire_id, str(uid))
            db.session.add(answer_require)
            db.session.commit()
        res = {'status': 100, 'msg': '请等待需求发布者接单'}
    else:
        res = {'status': 101, 'msg': '单已被抢'}
    return jsonify(res)


@app.route('/get_requirement', methods=['POST'])
def get_requirement():
    userrequire_id = request.form.get('userrequire_id', '')
    user_require = UserRequire.query.get(userrequire_id)

    answer_user_ids = AnswerRequire.query.filter_by(userrequire_id=userrequire_id)\
                                         .first()\
                                         .users_id\
                                         .split(' ')
    answer_users = []
    for uid in answer_user_ids:
        user = Participator.query.filter_by(user_id=uid).first()
        answer_users.append({
            'uid': uid,
            'name': user.name,
            'gender': user.gender,
            'avatar': user.avatar
        })
    res = {
        'uid': user_require.user_id,
        'title': user_require.title,
        'content': user_require.content,
        'condition': user_require.condition,
        'reward': user_require.reward,
        'pub_time': user_require.pub_time,
        'accept_user_id': user_require.answer_user,
        'answer_users': answer_users
    }
    return jsonify(res)

@app.route('/accept_answer', methods=['POST'])
def accept_answer():
    answer_user_id = request.form.get('answer_user_id', '')
    userrequire_id = request.form.get('userrequire_id', '')

    user_require = UserRequire.query.get(userrequire_id)
    user_require.answer_user = answer_user_id
    user_require.status = UserRequire.ANSWERED
    db.session.commit()

    return jsonify({'status': 100})

