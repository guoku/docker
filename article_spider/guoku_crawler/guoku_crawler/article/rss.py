#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from hashlib import md5

import datetime
from bs4 import BeautifulSoup
from dateutil import parser
from guoku_crawler.article.weixin import caculate_identity_code, createArticle, is_article_exist
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from guoku_crawler import config
from guoku_crawler.article.client import RSSClient
from guoku_crawler.tasks import RequestsTask, app
from guoku_crawler.common.image import fetch_image
from guoku_crawler.db import session
from guoku_crawler.models import CoreArticle
from guoku_crawler.models import CoreAuthorizedUserProfile as Profile
from guoku_crawler.config import logger
from guoku_crawler.exceptions import Retry
from lxml.html.clean import Cleaner
import hashlib
rss_client = RSSClient()
image_host = getattr(config, 'IMAGE_HOST', None)
skip_image_domain = 'feedsportal.com'


def caculate_rss_identity_code(title, userid, item_link):
    link_hash = hashlib.sha1(item_link.encode('utf-8')).hexdigest()
    title_hash = hashlib.sha1(title.encode('utf-8')).hexdigest()
    return "%s_%s_%s" % (userid,title_hash,link_hash)

@app.task(base=RequestsTask, name='rss.crawl_list')
def crawl_rss_list(authorized_user_id, page=1, crawl_all=False):
    authorized_user = session.query(Profile).get(authorized_user_id)
    blog_address = authorized_user.rss_url
    params = {
        'feed': 'rss2',
        'paged': page
    }
    if crawl_all:
        get_all_rss_articles(blog_address, params, authorized_user, page)
    else:
        get_rss_list(blog_address, params, authorized_user, page)
    if authorized_user.rss_url == 'http://blog.kakkoko.com/1/feed':
        try:
            while True:
                page_num = blog_address.split('/')[-2]
                next_page_num = str(int(page_num)+1)
                blog_address_split = blog_address.split('/')
                blog_address_split[-2] = next_page_num
                blog_address = '/'.join(blog_address_split)
                if rss_client.get(blog_address).status_code == 200:
                    get_rss_list(blog_address, params, authorized_user, page)
                else:
                    break
        except Exception as e:
            logger.error(e.message)
            return


def get_rss_list(blog_address, params, authorized_user, page):
    go_next = True
    try:
        response = rss_client.get(blog_address,
                              params=params
                              )
    except Exception as e:
        logger.error(e.message)
        return
    xml_content = BeautifulSoup(response.utf8_content, 'xml')
    # REFACTOR HERE
    # TODO :  parser
    item_list = xml_content.find_all('item')
    for item in item_list:
        title = item.title.text
        identity_code = caculate_rss_identity_code(title,authorized_user.user.id,item.link.text)
        try:
            article = session.query(CoreArticle).filter_by(
                identity_code=identity_code,
                creator=authorized_user.user
            ).one()
            go_next = False
            logger.info('ARTICLE EXIST :%s'  % title)
        except NoResultFound:
            content = item.encoded.string if item.encoded else item.description.text
            cleaner = Cleaner(kill_tags=['script', 'iframe'])
            content = cleaner.clean_html(content)
            article = CoreArticle(
                creator=authorized_user.user,
                identity_code=identity_code,
                title=title,
                content=content,
                updated_datetime=datetime.datetime.now(),
                created_datetime=parser.parse(item.pubDate.text),
                publish=CoreArticle.published,
                cover=config.DEFAULT_ARTICLE_COVER,
                origin_url=item.link.text,
                source=2,# source 2 is from rss.
            )
            session.add(article)
            session.commit()
            crawl_rss_images.delay(article.content, article.id)


        except MultipleResultsFound as e:
            logger.warning('article dup %s' %article.id)
            pass
        logger.info('article %s finished.', article.id)



    if len(item_list) < 10:
        go_next = False
        logger.info('current page is the last page; will not go next page')

    page += 1
    if page>30 :
        logger.info('page range > 30 quiting')
        return

    if go_next:
        logger.info('prepare to get next page: %d', page)
        crawl_rss_list.delay(authorized_user_id=authorized_user.id,
                             page=page)


def get_all_rss_articles(blog_address, params, authorized_user, page):
    try:
        response = rss_client.get(blog_address,
                              params=params
                              )
    except Exception as e:
        logger.error(e.message)
        return
    xml_content = BeautifulSoup(response.utf8_content, 'xml')
    # REFACTOR HERE
    # TODO :  parser
    item_list = xml_content.find_all('item')
    for item in item_list:
        title = item.title.text
        identity_code = caculate_rss_identity_code(title,authorized_user.user.id,item.link.text)
        try:
            article = session.query(CoreArticle).filter_by(
                identity_code=identity_code,
                creator=authorized_user.user
            ).one()
            logger.info('ARTICLE EXIST :%s'  % title)
        except NoResultFound:
            content = item.encoded.string if item.encoded else item.description.text
            cleaner = Cleaner(kill_tags=['script', 'iframe'])
            content = cleaner.clean_html(content)
            article = CoreArticle(
                creator=authorized_user.user,
                identity_code=identity_code,
                title=title,
                content=content,
                updated_datetime=datetime.datetime.now(),
                created_datetime=parser.parse(item.pubDate.text),
                publish=CoreArticle.published,
                cover=config.DEFAULT_ARTICLE_COVER,
                origin_url=item.link.text,
                source=2,# source 2 is from rss.
            )
            session.add(article)
            session.commit()
            crawl_rss_images.delay(article.content, article.id)


        except MultipleResultsFound as e:
            logger.warning('article dup %s' %article.id)
            pass
        logger.info('article %s finished.', article.id)

    page += 1
    logger.info('prepare to get next page: %d', page)
    crawl_rss_list.delay(authorized_user_id=authorized_user.id,
                             page=page, crawl_all=True)


@app.task(base=RequestsTask, name='rss.crawl_rss_images')
def crawl_rss_images(content_string, article_id):
    if not content_string:
        return
    article = session.query(CoreArticle).get(article_id)
    article_soup = BeautifulSoup(content_string)
    image_tags = article_soup.find_all('img')
    if image_tags:
        for i, image_tag in enumerate(image_tags):
            img_src = (
                image_tag.attrs.get('src') or image_tag.attrs.get('data-src')
            )
            if img_src and (not skip_image_domain in img_src):
                logger.info('fetch_image for article %d: %s', article.id,
                             img_src)
                try :
                    gk_img_rc = fetch_image(img_src, rss_client, full=False)
                except Retry as e :
                    continue
                if gk_img_rc:
                    full_path = "%s%s" % (image_host, gk_img_rc)
                    image_tag['src'] = full_path
                    image_tag['data-src'] = full_path
                    image_tag['height'] = 'auto'
                    if i == 0:
                        article.cover = full_path
            content_html = article_soup.decode_contents(formatter="html")
            article.content = content_html
            session.commit()

#comment here

class RssParser():
    def __init__(self, url, authorized_user):
        self.url = url
        self.authorized_user = authorized_user
        self.page = 1

    def get_article(self):
        response = rss_client.get(self.url, params={'paged': self.page})
        self.page += 1
        xml_content = BeautifulSoup(response.utf8_content, 'xml')
        item_list = xml_content.find_all('item')
        articles = []
        for item in item_list:
            title = item.title.text
            identity_code = caculate_rss_identity_code(title, self.authorized_user.user.id, item.link.text)
            content = item.encoded.string if item.encoded else item.description.text
            cleaner = Cleaner(kill_tags=['script', 'iframe'])
            content = cleaner.clean_html(content)
            articles.append({'title': title, 'creator': self.authorized_user.user,
                             'identity_code': identity_code, 'content': content,
                             'updated_datetime': datetime.datetime.now(), 'created_datetime': parser.parse(item.pubDate.text),
                             'publish': CoreArticle.published, 'cover': config.DEFAULT_ARTICLE_COVER,
                             'origin_url': item.link.text, 'source': 2})
        return articles

    def get_pages(self):
        pass

def crawl_rss(authorized_user_id):
    authorized_user = session.query(Profile).get(authorized_user_id)
    rss_url = authorized_user.rss_url
    parser = RssParser(rss_url, authorized_user)
    next_page = True
    while True:
        articles = parser.get_article()
        for article in articles:
            if is_article_exist(article, authorized_user):
                logger.info('article exist : %s', article['title'])
                next_page = False

            else:
                article = createArticle(article)
                crawl_rss_images.delay(article.content, article.id)

        if next_page:
            articles = parser.get_article()


