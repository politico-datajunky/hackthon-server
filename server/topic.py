# -*- coding: utf-8 -*-
from flask import jsonify, request
from server import app
from server.models import Participator, Topic, Reply, ReplyAwesome, db

import time

"""
    topic 相关CURD操作
"""


@app.route('/api/topic', methods=['POST'])
def create_topic():
    """
        创建话题，返回话题详情
    """
    topic = Topic(
        user_id=request.form['uid'],
        content=request.form['content'],
        image=request.form['image']
    )
    db.session.add(topic)
    db.session.commit()
    return jsonify({
        'status': 100
    })


@app.route('/api/topicdetail', methods=['POST'])
def topic():
    """
        获取话题详情
    """
    uid = request.form.get('uid', None)
    topic_id = request.form.get('topicid', None)
    topic = Topic.query.filter_by(id=topic_id).first()
    if topic is None:
        return jsonify({'status': 120, 'error': 'Not found topic'})
    participator = Participator.query.filter_by(user_id=topic.user_id).first()
    replies = Reply.query.filter_by(topic_id=topic.id)
    result = []
    for reply in replies:
        reply.watch_time = int(time.time())
        db.session.commit()
        user = Participator.query.filter_by(user_id=reply.from_user).first()
        awesome = ReplyAwesome.query.filter_by(reply_id=reply.id).first()
        if awesome is None:
            awesomenum = 0
        else:
            awesomenum = len(awesome.awesome_user.split('|'))
        if awesome is None:
            ifawesomed = False
        else:
            if str(user.user_id) in awesome.awesome_user:
                ifawesomed = True
            else:
                ifawesomed = False
        result.append({
            'name': user.name,
            'headimg': user.avatar,
            'date': reply.pub_time,
            'awesomenum': awesomenum,
            'content': reply.content,
            'commentid': reply.id,
            'ifawesomed': ifawesomed
        })
    return jsonify({
        'topicid': topic.id,
        'info': {
            'name': participator.name,
            'headimg': participator.avatar,
            'date': topic.pub_date,
            'content': topic.content,
            'img': topic.image.split('|') if topic.image is not None else [],
        },
        'comment': result
    })


@app.route('/api/comment', methods=['POST'])
def create_reply():
    """
        创建话题评论
    """
    uid = request.form['uid']
    participator = Participator.query.filter_by(user_id=uid).first()
    if participator is None:
        return jsonify({'status': 112, 'error': 'user does not exist.'})
    topic_id = request.form['topicid']
    content = request.form['content']
    topic = Topic.query.filter_by(id=topic_id).first()
    reply = Reply(
        topic_id=topic.id,
        from_user=uid,
        content=content
    )
    db.session.add(reply)
    topic.reply_number += 1
    db.session.commit()
    return jsonify({
        'topicid': topic.id,
        'commentid': reply.id,
        'name': participator.name,
        'headimg': participator.avatar,
        'date': reply.pub_time,
        'content': reply.content,
        'awesomenum': 0
    })


@app.route('/api/comment_awesome', methods=['POST'])
def awesome():
    uid = request.form['uid']
    topic_id = request.form['topicid']
    reply_id = request.form['commentid']
    user_awesome = ReplyAwesome.query.filter_by(topic_id=topic_id, reply_id=reply_id).first()
    if user_awesome is None:
        user_awesome = ReplyAwesome(
            topic_id=topic_id,
            reply_id=reply_id,
            awesome_user=uid,
        )
        db.session.add(user_awesome)
    else:
        if uid in user_awesome.awesome_user:
            return jsonify({'status': 112, 'error': 'uid has awesome this!'})
        user_awesome.awesome_number += 1
        user_awesome.awesome_user = user_awesome.awesome_user + '|' + str(uid)
    db.session.commit()
    return jsonify({'commentid': user_awesome.reply_id, 'awesomenum': user_awesome.awesome_number})


@app.route('/api/topiclist', methods=['POST'])
def topiclist():
    uid = request.form['uid']
    topics = Topic.query.all()
    result = []
    for topic in topics:
        user = Participator.query.filter_by(user_id=topic.user_id).first()
        result.append({
            'headimg': user.avatar,
            'name': user.name,
            'date': topic.pub_date,
            'content': topic.content,
            'img': topic.image.split('|') if topic.image is not None else [],
            'topicid': topic.id,
            'uid': topic.user_id
        })
    return jsonify({
        'list': result
    })


@app.route('/api/replied_topic', methods=['POST'])
def replied_topic():
    """
        我回复过的话题列表
    """
    uid = request.form['uid']
    replies = Reply.query.filter_by(from_user=uid)
    result = []
    for reply in replies:
        awesome = ReplyAwesome.query.filter_by(topic_id=reply.topic_id, reply_id=reply.id).first()
        if awesome is None:
            awesomenum = 0
        else:
            awesomenum = awesome.awesome_number
        topic = Topic.query.filter_by(id=reply.topic_id).first()
        user = Participator.query.filter_by(user_id=topic.user_id).first()
        result.append({
            'date': reply.pub_time,
            'awesomenum': awesomenum,
            'content': reply.content,
            'originTopic': {
                'headimg': user.avatar,
                'name': user.name,
                'date': topic.pub_date,
                'content': topic.content,
                'topicid': topic.id
            }
        })
    return jsonify({
        'replyedList': result
    })


@app.route('/api/published_topic', methods=['POST'])
def published_topic():
    """
        我发表的话题列表
    """
    uid = request.form['uid']
    topics = Topic.query.filter_by(user_id=uid)
    result = []
    for each in topics:
        replies = Reply.query.filter_by(watch_time=None).first()
        result.append({
            'topicid': each.id,
            'date': each.pub_date,
            'content': each.content,
            'img': each.image.split('|') if each.image is not None else [],
            'replynum': each.reply_number,
            'readstatus': True if replies is not None else False
        })
    return jsonify({
        'publishedList': result
    })


@app.route('/topic/init_topic', methods=['POST'])
def init_topic():
    topic1 = Topic(
        user_id=1,
        content="今天加班好开心",
        image="/media/topic/topic1-1.jpg|/media/topic/topic1-2.jpg|/media/topic/topic1-3.jpg",
    )
    topic2 = Topic(
        user_id=3,
        content="今天加班好开心",
        image="/media/topic/topic1-1.jpg|/media/topic/topic1-2.jpg|/media/topic/topic1-3.jpg",
    )
    topic3 = Topic(
        user_id=2,
        content="今天加班好开心",
        image="/media/topic/topic1-1.jpg|/media/topic/topic1-2.jpg|/media/topic/topic1-3.jpg",
    )
    topic4 = Topic(
        user_id=1,
        content="今天加班好开心",
        image="/media/topic/topic1-1.jpg|/media/topic/topic1-2.jpg|/media/topic/topic1-3.jpg",
    )
    topic5 = Topic(
        user_id=5,
        content="今天加班好开心",
        image="/media/topic/topic1-1.jpg|/media/topic/topic1-2.jpg|/media/topic/topic1-3.jpg",
    )
    topic6 = Topic(
        user_id=4,
        content="今天加班好开心",
        image="/media/topic/topic1-1.jpg|/media/topic/topic1-2.jpg|/media/topic/topic1-3.jpg",
    )
    topic7 = Topic(
        user_id=2,
        content="今天加班好开心",
        image="/media/topic/topic1-1.jpg|/media/topic/topic1-2.jpg|/media/topic/topic1-3.jpg",
    )

    db.session.add(topic1)
    db.session.add(topic2)
    db.session.add(topic3)
    db.session.add(topic4)
    db.session.add(topic5)
    db.session.add(topic6)
    db.session.add(topic7)

    db.session.commit()

    reply1 = Reply(topic_id=topic1.id, from_user=2, content="祝好")
    reply2 = Reply(topic_id=topic1.id, from_user=3, content="祝好")
    reply3 = Reply(topic_id=topic1.id, from_user=5, content="祝好")
    reply4 = Reply(topic_id=topic2.id, from_user=1, content="祝好")
    reply5 = Reply(topic_id=topic3.id, from_user=4, content="祝好")
    reply6 = Reply(topic_id=topic4.id, from_user=3, content="祝好")
    reply7 = Reply(topic_id=topic5.id, from_user=2, content="祝好")
    reply8 = Reply(topic_id=topic6.id, from_user=2, content="祝好")
    reply9 = Reply(topic_id=topic7.id, from_user=5, content="祝好")
    reply10 = Reply(topic_id=topic3.id, from_user=5, content="祝好")
    reply11 = Reply(topic_id=topic2.id, from_user=5, content="祝好")
    reply12 = Reply(topic_id=topic4.id, from_user=2, content="祝好")
    reply13 = Reply(topic_id=topic6.id, from_user=2, content="祝好")
    reply14 = Reply(topic_id=topic5.id, from_user=2, content="祝好")

    db.session.add(reply1)
    db.session.add(reply2)
    db.session.add(reply3)
    db.session.add(reply4)
    db.session.add(reply5)
    db.session.add(reply6)
    db.session.add(reply7)
    db.session.add(reply8)
    db.session.add(reply9)
    db.session.add(reply10)
    db.session.add(reply11)
    db.session.add(reply12)
    db.session.add(reply13)
    db.session.add(reply14)
    db.session.commit()

    awesome1 = ReplyAwesome(topic_id=topic1.id, reply_id=reply1.id, awesome_number=3, awesome_user='1|2|4')
    awesome2 = ReplyAwesome(topic_id=topic1.id, reply_id=reply2.id, awesome_number=2, awesome_user='1|5')
    awesome3 = ReplyAwesome(topic_id=topic2.id, reply_id=reply4.id, awesome_number=5, awesome_user='1|2|3|4|5')
    awesome4 = ReplyAwesome(topic_id=topic2.id, reply_id=reply11.id, awesome_number=1, awesome_user='2')
    awesome5 = ReplyAwesome(topic_id=topic3.id, reply_id=reply5.id, awesome_number=1, awesome_user='4')
    awesome6 = ReplyAwesome(topic_id=topic3.id, reply_id=reply10.id, awesome_number=1, awesome_user='3')
    awesome7 = ReplyAwesome(topic_id=topic4.id, reply_id=reply6.id, awesome_number=1, awesome_user='5')
    db.session.add(awesome1)
    db.session.add(awesome2)
    db.session.add(awesome3)
    db.session.add(awesome4)
    db.session.add(awesome5)
    db.session.add(awesome6)
    db.session.add(awesome7)
    db.session.commit()
    return jsonify({'status': 'success'})
