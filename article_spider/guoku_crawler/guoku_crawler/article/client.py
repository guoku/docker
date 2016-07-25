#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
import requests
import time

from time import sleep
from faker import Faker
from urlparse import urljoin

from guoku_crawler.config import logger
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError

from guoku_crawler.db import r
from guoku_crawler import config
from guoku_crawler.tasks import RequestsTask, app
from guoku_crawler.exceptions import TooManyRequests, Expired, Retry , ProxyFail


faker = Faker()


class BaseClient(requests.Session):
    def request(self, method, url,
                params=None,
                data=None,
                headers=None,
                cookies=None,
                files=None,
                auth=None,
                timeout=30,
                allow_redirects=True,
                proxies=None,
                hooks=None,
                stream=None,
                verify=None,
                cert=None,
                json=None):
        resp = None
        try:
            resp = super(BaseClient, self).request(method, url, params, data,
                                                   headers, cookies, files,
                                                   auth, timeout,
                                                   allow_redirects, proxies,
                                                   hooks, stream, verify,
                                                   cert, json)

        except ConnectionError as e:
            raise Retry(message=u'ConnectionError. %s' % e)
        except ReadTimeout as e:
            raise Retry(message=u'ReadTimeout. %s' % e)
        except BaseException as e:
            logger.error(e)

        if stream:
            return resp
        resp.utf8_content = resp.content.decode('utf-8')
        resp.utf8_content = resp.utf8_content.rstrip('\n')
        # sleep(config.REQUEST_INTERVAL)
        return resp


class RSSClient(BaseClient):
    def __init__(self):
        super(RSSClient, self).__init__()
        self._sg_user = None
        self.headers['Cookie'] = 'SUV=1387161004695182; lastdomain=null; ssuid=1407346305; pgv_pvi=5216948224; pgv_si=s6847528960; pid=ask.xgzs.lddj; cid=w.search.yjjlink; GOTO=Af90017; ss_pidf=1; ss_cidf=1; SEID=000000004658860A2AFF0B10000B66B8; CXID=0A522AD3998C91A8993D3877F703A871; SUID=F2F4C66F506C860A5667DB8B000E648F; PHPSESSID=b7oek1dhh4ks6dl3fk453hisa7; ABTEST=8|1461035006|v1; weixinIndexVisited=1; JSESSIONID=aaaqBvaz15csY4qZ9lPqv; IPLOC=CN1100; ad=MQpZyZllll2QBdmalllllVtkynYlllllbDb1Dkllll9lllllpZlll5@@@@@@@@@@; ld=kyllllllll2gaIxElllllVtm647lllllToVlakllll9llllljllll5@@@@@@@@@@; SNUID=4F20E0BE6165532C39712CD46183AAFA; sct=141'
        self.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'


class ProxyTestClient(requests.Session):
    def request(self, method, url,
                params=None,
                data=None,
                headers=None,
                cookies=None,
                files=None,
                auth=None,
                timeout=10,
                allow_redirects=True,
                proxies=None,
                hooks=None,
                stream=None,
                verify=None,
                cert=None,
                json=None):

        try:
            resp = super(ProxyTestClient, self).request(method, url, params, data,
                                                   headers, cookies, files,
                                                   auth, timeout,
                                                   allow_redirects, proxies,
                                                   hooks, stream, verify,
                                                   cert, json)
        except Exception as e:
            logger.info('test proxy fail -----exception : %s' %e)
            raise ProxyFail()

        return resp





class WeiXinClient(BaseClient):
    def __init__(self):
        super(WeiXinClient, self).__init__()
        self._sg_user = None
        self.headers['Cookie'] ='SUID=7E75CF763108990A000000005795A229; SUV=1469424170737371; ABTEST=0|1469424173|v1; weixinIndexVisited=1; SNUID=6862D96017132E78EC5BC7CD171748BE; JSESSIONID=aaaDfbo1h-vjdac5tEGwv; IPLOC=CN; LSTMV=556%2C209; LCLKINT=1483'
        self.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'


    @property
    def sg_user(self):
        return self._sg_user

    def request(self, method, url,
                params=None,
                data=None,
                headers=None,
                cookies=None,
                files=None,
                auth=None,
                timeout=30,
                allow_redirects=True,
                proxies=None,
                hooks=None,
                stream=None,
                verify=None,
                cert=None,
                json=None,
                jsonp_callback=None):
        resp = super(WeiXinClient, self).request(method, url, params, data,
                                                 headers, cookies, files,
                                                 auth, timeout,
                                                 allow_redirects, proxies,
                                                 hooks, stream, verify,
                                                 cert, json)

        logger.warning('------- requesting -------')
        logger.warning('url :  %s' % url)
        logger.warning('cooke : %s' %self.headers['Cookie'][:50] or 'No cookie')
        logger.warning('user agent : %s' %self.headers['User-Agent'][:50] or 'No UA')
        # logger.warning('content : %s' % resp.text)
        logger.warning('_______ requesting end -----')

        if stream:
            return resp

        # catch exceptions
        if resp.utf8_content.find(u'您的访问过于频繁') >= 0:
            logger.warning("content : %s " %resp.utf8_content)
            message = u'too many requests. user: %s, url: %s' % (
                self.sg_user, url)
            logger.warning(message)
            raise TooManyRequests(message)
        if resp.utf8_content.find(u'当前请求已过期') >= 0:
            message = 'link expired: %s' % url
            logger.warning(message)
            raise Expired(message)

        if jsonp_callback:
            resp.jsonp = self.parse_jsonp(resp.utf8_content, jsonp_callback)
            if resp.jsonp.get('code') == 'needlogin':
                self.refresh_cookies()
                raise Retry(message=u'need login with %s.' % self.sg_user)
        sleep(config.REQUEST_INTERVAL)
        return resp

    def refresh_cookies(self, update=False):
        self.cookies.clear()
        # if update:
        #     update_sogou_cookie.delay(self.sg_user)

        sg_users = list(config.SOGOU_USERS)
        if self.sg_user:
            sg_users.remove(self.sg_user)

        sg_user = random.choice(sg_users)
        sg_cookie = r.get('sogou.cookie.%s' % sg_user)
        if not sg_cookie:
            result = update_sogou_cookie.delay(sg_user)
            while not result.ready():
                time.sleep(0.5)
            result.get()
            logger.warning('********** done refresh cooke **********')
            sg_cookie = r.get('sogou.cookie.%s' % sg_user).decode()
        else:
            sg_cookie = sg_cookie.decode()
        self._sg_user = sg_user
        self.headers['Cookie'] = sg_cookie
        # self.headers['User-Agent'] = faker.user_agent()
        self.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'

    @classmethod
    def parse_jsonp(cls, utf8_content, callback):
        if utf8_content.startswith(callback):
            try:
                # utf8 content is a jsonp
                # here we extract the json part
                # for example, "cb({"a": 1})", where callback is "cb"
                return json.loads(utf8_content[len(callback) + 1:-1])
            except ValueError:
                logger.error("Json decode error %s", utf8_content)
                raise

def get_random_sg_user():
    sg_users = list(config.SOGOU_USERS)
    sg_user = random.choice(sg_users)
    return sg_user


@app.task(base=RequestsTask, name='weixin.update_sogou_cookie')
def update_sogou_cookie(sg_user):
    if not sg_user:
        return
    get_url = urljoin(config.PHANTOM_SERVER, '_sg_cookie')
    resp = requests.post(get_url, data={'email': sg_user})
    try :
        cookie = resp.json()['sg_cookie']
        print('-' * 80)
        print('got cookie for %s: ' % sg_user)
        print(cookie)
        print('-' * 80)
        key = 'sogou.cookie.%s' % sg_user
        r.set(key, cookie)

    except ValueError as e :
        time.sleep(25)
        logger.error("Cookie Getting Failed, no json returned")

        update_sogou_cookie(get_random_sg_user())
    except Exception as e :

        time.sleep(50)
        logger.error("Cookie Getting Failed, other error")
        update_sogou_cookie(get_random_sg_user())



