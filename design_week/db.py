#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# connect to database core, used for get entity id from entity hash
data_base_user = 'user1'
data_base_pass = '123456'
data_base_ip = '192.168.1.103'

DATABASES = {
    'DB_NAME': 'core',
    'USER':  data_base_user,
    'PASSWORD': data_base_pass,
    'HOST': data_base_ip,
    'PORT': '3306',
}

SQLALCHEMY_DATABASE_URI = ('mysql+pymysql://{USER}:{PASSWORD}@'
                           '{HOST}:{PORT}/{DB_NAME}?charset=utf8mb4'.
                           format(**DATABASES))
nut_engine = create_engine(
    SQLALCHEMY_DATABASE_URI, pool_recycle=3600,convert_unicode=True,encoding='utf-8')

nut_session = Session(nut_engine)


# a test sqlite db
engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)


