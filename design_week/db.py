#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
from sqlalchemy import create_engine


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
engine = create_engine(
    SQLALCHEMY_DATABASE_URI, pool_recycle=3600,convert_unicode=True,encoding='utf-8')

session = Session(engine)


