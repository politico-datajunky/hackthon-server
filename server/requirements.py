# coding: utf-8
from flask import jsonify, request
from server import app
from server.models import db, UserRequire, AnswerRequire, Participator

import time


@app.route('/api/create_requirement', methods=['POST'])
def create_requirement():
    uid = request.form.get('uid', '')
    title = request.form.get('title', '')
    content = request.form.get('content', '')
    condition = request.form.get('condition', '')
    reward = request.form.get('reward', '')

    user_require = UserRequire(uid, title, content, condition, reward)
    db.session.add(user_require)
    db.session.commit()

    res = {
        'requirement_id': user_require.id
    }
    return jsonify({'status': 100, 'data': res})


@app.route('/api/answer_requirement', methods=['POST'])
def answer_requirement():
    uid = request.form.get('uid', '')
    userrequire_id = request.form.get('requirement_id', '')
    requirement = UserRequire.query.get(userrequire_id)
    requirement.watch_time = None
    require_status = requirement.status
    answer = AnswerRequire.query.filter_by(userrequire_id=requirement.id, answer_uid=uid).first()
    if answer is None:
        return jsonify({'status': 112})
    if require_status == UserRequire.WAITING:
        answer = AnswerRequire(userrequire_id, uid, AnswerRequire.WAITING)
        db.session.add(answer)
        db.session.commit()
        res = {'status': 100, 'data': '请等待需求发布者接单'}
    else:
        res = {'status': 101, 'data': '单已被抢'}
    return jsonify(res)


@app.route('/api/get_requirement', methods=['POST'])
def get_requirement():
    userrequire_id = request.form.get('requirement_id', '')
    user_require = UserRequire.query.get(userrequire_id)
    if user_require:
        answers = AnswerRequire.query.filter_by(userrequire_id=user_require.id)
        for answer in answers:
            answer.watch_time = int(time.time())
            db.session.commit()
        publish_user = Participator.query.filter_by(user_id=user_require.user_id)\
                                         .first()
        answer_users = get_answers(user_require.id)
        res = {
            'requirement_id': user_require.id,
            'uid': user_require.user_id,
            'title': user_require.title,
            'content': user_require.content,
            'condition': user_require.condition,
            'reward': user_require.reward,
            'pub_time': user_require.pub_time,
            'accept_user_id': user_require.answer_user,
            'answer_users': answer_users,
            'status': user_require.status,
            'publish_user': {
                'uid': publish_user.user_id,
                'name': publish_user.name,
                'avatar': publish_user.avatar,
            }
        }
        return jsonify({'status': 100, 'data': res})
    else:
        return jsonify({'status': 101, 'data': '需求id错误'})


@app.route('/api/accept_answer', methods=['POST'])
def accept_answer():
    answer_user_id = request.form.get('answer_user_id', '')
    userrequire_id = request.form.get('requirement_id', '')

    user_require = UserRequire.query.get(userrequire_id)
    user_require.answer_user = answer_user_id
    user_require.status = UserRequire.ANSWERED

    answers = AnswerRequire.query.filter_by(userrequire_id=user_require.id)\
                                 .all()
    for answer in answers:
        answer.watch_time = 0
        if int(answer.answer_uid) == int(answer_user_id):
            answer.status = AnswerRequire.SUCCESS
        else:
            answer.status = AnswerRequire.FAILURE
    db.session.commit()
    return jsonify({'status': 100})


@app.route('/api/my_requirements', methods=['POST'])
def my_requirements():
    uid = request.form.get('uid', '')
    requirements = UserRequire.query.filter_by(user_id=uid).all()
    user = Participator.query.filter_by(user_id=int(uid))\
                             .first()
    data = {'user': {
        'uid': user.user_id,
        'name': user.name,
        'avatar': user.avatar
    }}
    needlist = []
    if requirements:
        for user_require in requirements:
            needlist.append({
                'needid': user_require.id,
                'content': user_require.content,
                'need': user_require.condition,
                'reward': user_require.reward,
                'pub_time': user_require.pub_time,
                'accept_user_id': user_require.answer_user,
                'answer_users': get_answers(user_require.id),
                'status': user_require.status,
                'watch_status':  False if user_require.watch_time else True
            })

        data['needlist'] = needlist
        return jsonify({'status': 100, 'data': data})
    else:
        return jsonify({'status': 101, 'data': '请求错误，未找到该用户的需求'})


@app.route('/api/my_answers', methods=['POST'])
def my_answers():
    uid = request.form.get('uid', '')
    watch_time = request.form.get('watch_time', '')
    answers = AnswerRequire.query.filter_by(answer_uid=int(uid))\
                                 .order_by('answer_time desc')\
                                 .all()
    if answers:
        answer_list = []
        for answer in answers:
            origin_watch_time = answer.watch_time
            if answer.status != AnswerRequire.WAITING:
                answer.watch_time = int(watch_time)
                db.session.commit()
                requirement = UserRequire.query.filter_by(id=answer.userrequire_id)\
                                               .first()
                require_user = Participator.query.filter_by(user_id=requirement.user_id)\
                                                 .first()
                row = {
                    'user':
                        {
                            'uid': require_user.user_id,
                            'name': require_user.name,
                            'avatar': require_user.avatar,
                            'gender': require_user.gender
                        },
                        'answer_time': answer.answer_time,
                        'publish_time': requirement.pub_time,
                        'status': answer.status,
                        'content': requirement.content,
                        'reward': requirement.reward,
                        'need': requirement.condition,
                        'watch_status': False if origin_watch_time else True
                }
                answer_list.append(row)
                return jsonify({
                    'status': 100,
                    'data': {
                        'answer_list': answer_list,
                    }
                })
            else:
                return jsonify({
                    'status': 101,
                    'data': '没有您的抢单'
                })

    else:
        return jsonify({
            'status': 101,
            'data': '没有您的抢单'
        })


@app.route('/my', methods=['POST'])
def my():
    uid = int(request.form.get('uid', ''))
    res = {
        'require': False,
        'answer': False
    }
    requiremets = UserRequire.query.filter_by(user_id=uid).all()
    answers = AnswerRequire.query.filter_by(answer_uid=uid).all()

    for require in requiremets:
        if not require.watch_time:
            res['require'] = True
            break
    for answer in answers:
        if not answer.watch_time:
            res['answer'] = True
            break

    return jsonify({
        'status': 100,
        'data': res
    })


@app.route('/init_answer', methods=['POST'])
def init_answer():
    a1 = AnswerRequire(1, 1)
    a2 = AnswerRequire(2, 2)
    a3 = AnswerRequire(3, 3)
    db.session.add(a1)
    db.session.add(a2)
    db.session.add(a3)
    db.session.commit()

    return jsonify({'status': 100})


def get_answers(userrequire_id):
    answers = AnswerRequire.query.filter_by(userrequire_id=userrequire_id)\
                                 .all()
    answer_users = []
    for answer in answers:
        user = Participator.query.filter_by(user_id=answer.answer_uid)\
                                 .first()
        answer_users.append({
            'uid': user.user_id,
            'name': user.name,
            'gender': user.gender,
            'avatar': user.avatar,
            'answer_time': answer.answer_time,
            'status': answer.status
        })
    return answer_users