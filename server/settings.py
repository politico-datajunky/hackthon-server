# -*- coding: utf-8 -*-


class Config(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost:3306/hackthon'
    ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg')
    UPLOAD_FOLDER = ''


class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:borrowday123@localhost:3306/hackthon'
