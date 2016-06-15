#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime
from bs4 import BeautifulSoup
from dateutil import parser
from guoku_crawler.article.weixin import is_article_exist

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

# @app.task(base=RequestsTask, name='rss.crawl_list')
# def crawl_rss_list(authorized_user_id, page=1, crawl_all=False):
#     authorized_user = session.query(Profile).get(authorized_user_id)
#     blog_address = authorized_user.rss_url
#     params = {
#         'feed': 'rss2',
#         'paged': page
#     }
#     if crawl_all:
#         # get_all_rss_articles(blog_address, params, authorized_user, page)
#         pass
#     else:
#         get_rss_list(blog_address, params, authorized_user, page)
#     if authorized_user.rss_url == 'http://blog.kakkoko.com/1/feed':
#         try:
#             while True:
#                 page_num = blog_address.split('/')[-2]
#                 next_page_num = str(int(page_num)+1)
#                 blog_address_split = blog_address.split('/')
#                 blog_address_split[-2] = next_page_num
#                 blog_address = '/'.join(blog_address_split)
#                 if rss_client.get(blog_address).status_code == 200:
#                     get_rss_list(blog_address, params, authorized_user, page)
#                 else:
#                     break
#         except Exception as e:
#             logger.error(e.message)
#             return


# def get_rss_list(blog_address, params, authorized_user, page):
#     go_next = True
#     try:
#         response = rss_client.get(blog_address,
#                               params=params
#                               )
#     except Exception as e:
#         logger.error(e.message)
#         return
#     xml_content = BeautifulSoup(response.utf8_content, 'xml')
#     # REFACTOR HERE
#     # TODO :  parser
#     item_list = xml_content.find_all('item')
#     for item in item_list:
#         title = item.title.text
#         identity_code = caculate_rss_identity_code(title,authorized_user.user.id,item.link.text)
#         try:
#             article = session.query(CoreArticle).filter_by(
#                 identity_code=identity_code,
#                 creator=authorized_user.user
#             ).one()
#             go_next = False
#             logger.info('ARTICLE EXIST :%s'  % title)
#         except NoResultFound:
#             content = item.encoded.string if item.encoded else item.description.text
#             cleaner = Cleaner(kill_tags=['script', 'iframe'])
#             content = cleaner.clean_html(content)
#             article = CoreArticle(
#                 creator=authorized_user.user,
#                 identity_code=identity_code,
#                 title=title,
#                 content=content,
#                 updated_datetime=datetime.datetime.now(),
#                 created_datetime=parser.parse(item.pubDate.text),
#                 publish=CoreArticle.published,
#                 cover=config.DEFAULT_ARTICLE_COVER,
#                 origin_url=item.link.text,
#                 source=2,# source 2 is from rss.
#             )
#             session.add(article)
#             session.commit()
#             crawl_rss_images.delay(article.content, article.id)   #Todo test使用, 生产环境需取消注释
#
#
#         except MultipleResultsFound as e:
#             logger.warning('article dup %s' %article.id)
#             pass
#         logger.info('article %s finished.', article.id)
#
#
#
#     if len(item_list) < 10:
#         go_next = False
#         logger.info('current page is the last page; will not go next page')
#
#     page += 1
#     if go_next:
#         logger.info('prepare to get next page: %d', page)
#         crawl_rss_list.delay(authorized_user_id=authorized_user.id,
#                              page=page)
#         return
#     return

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
                except Exception as e:
                    logger.error(e.message)
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

class RssParser(object):
    def __init__(self, url, authorized_user):
        self.url = url
        self.authorized_user = authorized_user
        self.page = 1

    def get_pages(self):
        if is_valid_page(self.url) and not is_valid_page(self.url, params={'paged': self.page}):
            return [self.url]
        while True:
            if is_valid_page(self.url, params={'paged': self.page}):
                self.page *= 2
            else:
                break
        big = self.page
        small = self.page/2
        while small < big - 1:
            middle = (big + small)//2
            if is_valid_page(self.url, params={'paged': middle}):
                small = middle
            else:
                big = middle

        return ['{url}?paged={page}'.format(url=self.url, page=page) for page in range(1, big)]


    def can_handle(self, url):
        if url in ('http://blog.kakkoko.com/1/feed'):
            return False
        return True

    def parse(self, url):
        try:
            response = rss_client.get(url)
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
                                 'updated_datetime': datetime.datetime.now(),
                                 'created_datetime': parser.parse(item.pubDate.text),
                                 'publish': CoreArticle.published, 'cover': config.DEFAULT_ARTICLE_COVER,
                                 'origin_url': item.link.text, 'source': 2})
        except Exception as e:
            logger.error(e.message)
            return []
        return articles


class KakkokoParser(RssParser):
    def can_handle(self, url):
        if url == 'http://blog.kakkoko.com/1/feed':
            return True
        return False

    def get_pages(self):
        urls = []
        page = 1
        while True:
            url = 'http://blog.kakkoko.com/{page}/feed'.format(page=page)
            if is_valid_page(url):
                page += 1
                urls.append(url)
            else:
                break
        return urls


def is_valid_page(url, params=None):
    try:
        response = rss_client.get(url, params=params)
    except Exception as e:
        logger.error(e.message)
        return False
    if response.status_code == 200:
        return True
    return False
@app.task(base=RequestsTask, name='rss.new_crawl_list')
def crawl_rss(authorized_user_id):

    authorized_user = session.query(Profile).get(authorized_user_id)
    logger.info('start to crawle rss link %s' % authorized_user.rss_url)
    rss_url = authorized_user.rss_url
    parser = RssParser(rss_url, authorized_user)
    if parser.can_handle(rss_url):
        pages = parser.get_pages()
        if rss_url == 'http://www.mensweardog.cn/feed':
            crawl_mensweardog(pages, authorized_user, parser)
        else:
            crawl_rss_process(pages, authorized_user, parser)
    else:
        logger.error('default parser went wrong. Try another parser')
        if rss_url == 'http://blog.kakkoko.com/1/feed':
            parser = KakkokoParser(rss_url, authorized_user)
            pages = parser.get_pages()
            crawl_rss_process(pages, authorized_user, parser)

def crawl_mensweardog(pages, authorized_user, parser):
    '''
    this rss don't contain full content, need to crawle from article url
    :param pages:
    :param authorized_user:
    :param parser:
    :return:
    '''
    for page in pages:
        logger.info('prepare to get next page: %s', page)
        articles = parser.parse(page)
        for article in articles:
            if not is_article_exist(article, authorized_user):
                try:
                    origin_url = article['origin_url']
                    response = rss_client.get(origin_url)
                    article_soup = BeautifulSoup(response.utf8_content, from_encoding='utf8', isHTML=True)
                    content = article_soup.select(".entry-content")[0]
                    cleaner = Cleaner(kill_tags=['script', 'iframe'])
                    content = cleaner.clean_html(unicode(content))
                    article = create_rss_article(article)
                    article.content = content
                    crawl_rss_images.delay(article.content, article.id)
                except Exception as e:
                    logger.error(e.message)
        if is_last_page_crawled(pages[-1], authorized_user, parser):
            logger.info('-' * 80)
            logger.info('all the articles have beed crawled for authorized user %d' % authorized_user.id)
            logger.info('-' * 80)
            break


def crawl_rss_process(pages, authorized_user, parser):
    for page in pages:
        logger.info('prepare to get next page: %s', page)
        articles = parser.parse(page)
        for article in articles:
            if not is_article_exist(article, authorized_user):
                try:
                    article = create_rss_article(article)
                    crawl_rss_images.delay(article.content, article.id)
                except Exception as e:
                    logger.error(e.message)
        if is_last_page_crawled(pages[-1], authorized_user, parser):
            logger.info('-' * 80)
            logger.info('all the articles have beed crawled for authorized user %d' % authorized_user.id)
            logger.info('-' * 80)
            break

def is_last_page_crawled(url, authorized_user, parser):
    articles = parser.parse(url)
    if is_article_exist(articles[-1], authorized_user):
        return True
    return False


def create_rss_article(article):
    article = CoreArticle(
        creator=article.get('creator'),
        identity_code=article.get('identity_code'),
        title=article.get('title'),
        content=article.get('content'),
        updated_datetime=article.get('updated_datetime'),
        created_datetime=article.get('created_datetime'),
        publish=article.get('publish'),
        cover=article.get('cover'),
        origin_url=article.get('origin_url'),
        source=article.get('source'),
    )
    session.add(article)
    session.commit()
    logger.info('create article %d, %s' % (article.id, article.title))
    return article