# -*- coding: utf-8 -*-
from server import app
from flask_sqlalchemy import SQLAlchemy

import time

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(256))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Participator(db.Model):
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

    def __init__(self, user_id, name=None, gender=None, avatar=None, company=None, position=None, phone=None, email=None, qq=None, skills=None, free_time=None):
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

    def __repr__(self):
        return '<Participator %r>' % self.user_id


class UserRequire(db.Model):
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

    def __init__(self, user_id, title, content, condition, reward, pub_time=None, status=0, answer_user=None):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.condition = condition
        self.reward = reward
        if pub_time is None:
            self.pub_time = int(time.time()*1000)
        else:
            self.pub_time = pub_time
        self.status = status
        self.answer_user = answer_user

    def __repr__(self):
        return '<UserRequire %s>' % self.title


class AnswerRequire(db.Model):
    userrequire_id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Text)

    def __init__(self, userrequire_id, users_id):
        self.userrequire_id = userrequire_id
        self.users_id = users_id

    def __repr__(self):
        return '<AnswerRequire %s>' % self.userrequire_id