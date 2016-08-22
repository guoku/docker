#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

import pytz
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Text, DECIMAL,
                        Index)

from db import db

class CoreEntity(db.Model):
    __bind_key__    = 'core'
    __tablename__   = 'core_entity'

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


class ClickRecord(db.Model):
    __tablename__ = 'click_record'

    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, nullable=False)
    referer = Column(String(1024), nullable=True)
    user_ip = Column(String(256), nullable=True)
    created_time = Column(DateTime, default=datetime.datetime.now(pytz.timezone('Asia/Shanghai')))







