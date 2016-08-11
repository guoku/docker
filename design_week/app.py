#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import datetime
import pytz
from flask import Flask, request
from flask import redirect
from models import ClickRecord, CoreEntity
from db import nut_session, db_session

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/jump/entity/<entity_hash>", methods=['GET'])
def new_entity_detail(entity_hash):
    entity = nut_session.query(CoreEntity).filter(CoreEntity.entity_hash==entity_hash).first()
    entity_id = entity.id
    referer = request.referrer
    save_click_record(entity_id, referer)
    return redirect("http://127.0.0.1:8000/detail/" + entity_hash)

def save_click_record(entity_id, referer):
    try:
        click_record = ClickRecord(entity_id=entity_id, referer=referer,
                                   created_time=datetime.datetime.now(pytz.timezone('Asia/Shanghai')))
        db_session.add(click_record)
        db_session.commit()
        app.logger.info('save click record SUCCESS. ENTITY ID: %s, REFERER: %s' % (entity_id, referer))
    except Exception as e:
        db_session.rollback()
        app.logger.error(e.message)


if __name__ == "__main__":
    app.run('0.0.0.0', debug=True, port=7000)
