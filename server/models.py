# -*- coding: utf-8 -*-
from server import app
from flask_sqlalchemy import SQLAlchemy

import time

db = SQLAlchemy(app)


class User(db.Model):
    """
        用户表，记录登录信息
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(256))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Participator(db.Model):
    """
        用户拓展信息表
        skills 按照 | 分隔
        free_time 格式为{1:["12-13"]}星期一，12点到13点
    """
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=True)
    gender = db.Column(db.Integer, default=3)
    avatar = db.Column(db.Text, nullable=True)
    company = db.Column(db.String(32), nullable=True)
    position = db.Column(db.String(32), nullable=True)
    phone = db.Column(db.String(11), nullable=True)
    email = db.Column(db.String(32), nullable=True)
    qq = db.Column(db.String(16), nullable=True)
    skills = db.Column(db.Text, nullable=True)
    free_time = db.Column(db.Text, nullable=True)
    care_users = db.Column(db.Text, nullable=True)
    cared_users = db.Column(db.Text, nullable=True)

    def __init__(self,
                 user_id,
                 name=None,
                 gender=None,
                 avatar=None,
                 company=None,
                 position=None,
                 phone=None,
                 email=None,
                 qq=None,
                 skills=None,
                 free_time=None,
                 care_users=None,
                 cared_users=None):
        self.user_id = user_id
        self.name = name
        self.gender = gender
        self.avatar = avatar
        self.company = company
        self.position = position
        self.phone = phone
        self.email = email
        self.qq = qq
        self.skills = skills
        self.free_time = free_time
        self.care_users = care_users
        self.cared_users = cared_users

    def __repr__(self):
        return '<Participator %r>' % self.user_id


class UserRequire(db.Model):
    """
        用户需求表 存储用户发送的需求
        condition 为用户在发布需求时要求的技能，用|分隔
        status 0表示可抢状态，1表示发布需求的用户已确定了人选，这个状态下就不能抢单了
    """
    WAITING = 0
    ANSWERED = 1

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)
    condition = db.Column(db.Text, nullable=True)
    reward = db.Column(db.String(256), nullable=True)
    pub_time = db.Column(db.Integer)
    status = db.Column(db.Integer, default=0)
    answer_user = db.Column(db.Integer, nullable=True)
    watch_time = db.Column(db.Integer, nullable=True)

    def __init__(self, user_id, title, content, condition, reward,
                 pub_time=None, status=0, answer_user=None):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.condition = condition
        self.reward = reward
        if pub_time is None:
            self.pub_time = int(time.time())
        else:
            self.pub_time = pub_time
        self.status = status
        self.answer_user = answer_user

    def __repr__(self):
        return '<UserRequire %s>' % self.title


class AnswerRequire(db.Model):
    """
        需求抢单表 存储需求的抢单用户
    """
    WAITING = 0
    SUCCESS = 1
    FAILURE = 2

    id = db.Column(db.Integer, primary_key=True)
    userrequire_id = db.Column(db.Integer)
    answer_uid = db.Column(db.Integer)
    answer_time = db.Column(db.Integer)
    status = db.Column(db.Integer)
    watch_time = db.Column(db.Integer, nullable=True)

    def __init__(self, userrequire_id, answer_uid, status=0, answer_time=None):
        self.userrequire_id = userrequire_id
        self.answer_uid = answer_uid
        self.status = status
        if answer_time is None:
            self.answer_time = int(time.time())
        else:
            self.answer_time = answer_time

    def __repr__(self):
        return '<AnswerRequire %s>' % self.userrequire_id


class Topic(db.Model):
    """
        话题表
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    content = db.Column(db.Text, nullable=True)
    image = db.Column(db.Text, nullable=True)
    pub_date = db.Column(db.Integer, nullable=True)
    reply_number = db.Column(db.Integer, default=0)

    def __init__(self, user_id, content, image=None, pub_date=None, reply_number=0):
        self.user_id = user_id
        self.content = content,
        self.image = image,
        if pub_date is None:
            self.pub_date = int(time.time())
        self.reply_number = reply_number

    def __repr__(self):
        return '<Topic %s>' % self.id


class Reply(db.Model):
    """
        话题回复
    """
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer)
    from_user = db.Column(db.Integer, nullable=True)
    to_user = db.Column(db.Integer, nullable=True)
    content = db.Column(db.Text, nullable=True)
    pub_time = db.Column(db.Integer)
    watch_time = db.Column(db.Integer, nullable=True)

    def __init__(self, topic_id, from_user=None, to_user=None, content=None, pub_time=None, watch_time=None):
        self.topic_id = topic_id
        self.from_user = from_user
        self.to_user = to_user
        self.content = content
        if pub_time is None:
            self.pub_time = int(time.time())
        self.watch_time = watch_time

    def __repr__(self):
        return '<Reply %s>' % self.id


class ReplyAwesome(db.Model):
    """
        话题或者回复的赞
    """
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, nullable=True)
    reply_id = db.Column(db.Integer, nullable=True)
    awesome_number = db.Column(db.Integer, default=1)
    awesome_user = db.Column(db.Text, nullable=True)

    def __init__(self, topic_id=None, reply_id=None, awesome_number=1, awesome_user=None):
        self.topic_id = topic_id
        self.reply_id = reply_id
        self.awesome_number = awesome_number
        self.awesome_user = awesome_user

    def __repr__(self):
        return '<ReplyAwesome %d>' % self.id


class Skill(db.Model):
    """
        可选技能
    """
    id = db.Column(db.Integer, primary_key=True)
    skills = db.Column(db.Text)

    def __init__(self, skills):
        self.skills = skills