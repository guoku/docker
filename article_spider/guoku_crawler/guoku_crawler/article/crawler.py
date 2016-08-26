#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import datetime
import time

from sqlalchemy import or_

from guoku_crawler.db import session, r
from guoku_crawler.tasks import RequestsTask, app
from guoku_crawler.article.rss import  crawl_rss_list
from guoku_crawler.article.weixin import crawl_user_weixin_articles_by_authorized_user_id, build_cookie_pool, \
    is_phantomjs_gen_cookie_ok, get_new_cookie, keep_cookie_pool, is_weixin_crawler_ok
from guoku_crawler.models import CoreGkuser, AuthGroup, CoreArticle
from guoku_crawler.models import CoreAuthorizedUserProfile as Profile
from guoku_crawler.config import logger

yesterday_start = datetime.datetime.combine(
    datetime.date.today() - datetime.timedelta(days=1),
    datetime.time.min
)
today_start = datetime.datetime.combine(
    datetime.date.today(),
    datetime.time.min
)


@app.task(base=RequestsTask, name='crawl_articles')
def crawl_articles():
    keep_cookie_pool()
    r.delete('skip_users')
    users = get_auth_users()
    for user in users:
        # time.sleep(5)
        try :
            crawl_user_articles.delay(user.profile.id)
        except Exception as e :
            logger.error('fatal , exception when crawl %s' %user)
    logger.info('*'*80)
    logger.info('this round crawl all articles finished.')
    logger.info('*' * 80)


@app.task(base=RequestsTask, name='crawl_user_articles')
def crawl_user_articles(authorized_user_id):
    # crawl rss article if user has rss url,
    # else crawl weixin article from sogou.
    authorized_user = session.query(Profile).get(authorized_user_id)

    if authorized_user.rss_url:
        crawl_rss_list.delay(authorized_user_id)
    else:
        crawl_user_weixin_articles_by_authorized_user_id.delay(authorized_user_id)


def get_auth_users():
    try:
        users = session.query(CoreGkuser).filter(
            CoreGkuser.authorized_profile.any(
                or_(
                    Profile.weixin_id.isnot(None),
                    Profile.rss_url.isnot(None)
                )),
            CoreGkuser.groups.any(AuthGroup.name == 'Author')
        ).all()
    except Exception as e:
        logger.error(e.message)
        session.rollback()
        users = get_auth_users()
    return users




if __name__ == '__main__':
    # crawl_rss(60)
    # crawl_articles()
    # crawl_rss_list(111)
    is_weixin_crawler_ok(49)
    crawl_user_weixin_articles_by_authorized_user_id(41)
    print('*' * 80)
