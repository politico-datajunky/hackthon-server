# -*- coding: utf-8 -*-


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'mysql://root@localhost/hackthon'


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://root@localhost/hackthon'