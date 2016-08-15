#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import datetime
import pytz
from flask import Flask, request
from flask import redirect
from models import ClickRecord, CoreEntity
from db import app, db

SITE_HOST = 'http://127.0.0.1:8000/'

# app = Flask(__name__)
# app.config['DEBUG'] = True


@app.route("/jump/entity/<entity_hash>", methods=['GET'])
def new_entity_detail(entity_hash):
    entity = CoreEntity.query.filter(CoreEntity.entity_hash==entity_hash).first()
    entity_id = entity.id
    referer = request.referrer
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    save_click_record(entity_id, referer, user_ip)
    return redirect(SITE_HOST + 'detail/' + entity_hash)

def save_click_record(entity_id, referer, user_ip):
    try:
        click_record = ClickRecord(entity_id=entity_id, referer=referer, user_ip=user_ip,
                                   created_time=datetime.datetime.now(pytz.timezone('Asia/Shanghai')))
        db.session.add(click_record)
        db.session.commit()
        app.logger.info('save click record SUCCESS. ENTITY ID: %s, REFERER: %s, USER IP: %s' % (entity_id, referer, user_ip))
    except Exception as e:
        db.session.rollback()
        app.logger.error(e.message)


if __name__ == "__main__":
    app.run('0.0.0.0', debug=True, port=7000)
