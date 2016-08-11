#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

import pytz
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Text, DECIMAL,
                        Index)
from sqlalchemy.orm import relationship, backref


Base = declarative_base()

core_gkuser_groups = Table(
    'core_gkuser_groups', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('group_id', Integer, ForeignKey('auth_group.id')),
    Column('gkuser_id', Integer, ForeignKey('core_gkuser.id'))
)


class AuthGroup(Base):
    __tablename__ = 'auth_group'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, unique=True)
    users = relationship('CoreGkuser',
                         secondary=core_gkuser_groups,
                         backref='gk_groups')

class CoreGkuser(Base):
    __tablename__ = 'core_gkuser'

    id = Column(Integer, primary_key=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime, nullable=False)
    is_superuser = Column(Integer, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    is_active = Column(Integer, nullable=False)
    is_admin = Column(Integer, nullable=False)
    date_joined = Column(DateTime, nullable=False)
    groups = relationship('AuthGroup',
                          secondary=core_gkuser_groups,
                          backref='gk_users'
                          )
    authorized_profile = relationship('CoreAuthorizedUserProfile',
                           backref=backref('user', uselist=False))


class CoreAuthorizedUserProfile(Base):
    __tablename__ = 'core_authorized_user_profile'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('core_gkuser.id'), nullable=False, unique=True)
    weixin_id = Column(String(255))
    weixin_nick = Column(String(255))
    weixin_qrcode_img = Column(String(255))
    author_website = Column(String(1024))
    weibo_id = Column(String(255))
    weibo_nick = Column(String(255))
    personal_domain_name = Column(String(64))
    weixin_openid = Column(String(255))
    rss_url = Column(String(255), nullable=True)
    gk_user = relationship('CoreGkuser',
                           backref=backref('profile', uselist=False))


class ClickRecord(Base):
    __tablename__ = 'click_record'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('core_gkuser.id'), nullable=True, unique=True)
    entity_id = Column(ForeignKey('core_entity.id'), nullable=False, unique=True)
    referer = Column(String(1024), nullable=True)
    created_time = Column(DateTime, default=datetime.datetime.now(pytz.timezone('Asia/Shanghai')))
    user = relationship('CoreGkuser')
    entity = relationship('CoreEntity')

class CoreEntity(Base):
    __tablename__ = 'core_entity'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('core_gkuser.id'), nullable=True, unique=True)
    entity_hash = Column(String(32), index=True, unique=True)
    brand = Column(String(256), default='')
    title = Column(String(256), default='')
    intro = Column(Text, default='')
    rate = Column(DECIMAL, default=1.0)
    price = Column(DECIMAL, default=0, index=True)
    mark = Column(Integer, default=0, index=True)
    images = Column(String(256))
    created_time = Column(DateTime(), index=True)
    updated_time = Column(DateTime(), index=True)
    status = Column(Integer, default=0, index=True)







