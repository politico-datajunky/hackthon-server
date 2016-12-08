# -*- coding: utf-8 -*-


class Config(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost:3306/hackthon'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost:3306/hackthon'