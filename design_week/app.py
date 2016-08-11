#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime

import pytz
from flask import Flask, request

from models import ClickRecord

app = Flask(__name__)
app.config['DEBUG'] = True

from db import session


@app.route("/click_record/", methods=['GET'])
def entity_detail():
    user_id = request.args.get('user_id')
    entity_id = request.args.get('entity_id')
    referer = request.args.get('referer')
    save_click_record(user_id, entity_id, referer)
    return 'is working'

def save_click_record(user_id, entity_id, referer):
    try:
        click_record = ClickRecord(user_id=user_id, entity_id=entity_id, referer=referer,
                                   created_time=datetime.datetime.now(pytz.timezone('Asia/Shanghai')))
        session.add(click_record)
        session.commit()
        app.logger.info('save click record SUCCESS. USER ID: %s, ENTITY ID: %s, REFERER: %s' % (user_id, entity_id, referer))
    except Exception as e:
        session.rollback()
        app.logger.error(e.message)



if __name__ == "__main__":
    app.run('0.0.0.0', debug=True, port=7000)
