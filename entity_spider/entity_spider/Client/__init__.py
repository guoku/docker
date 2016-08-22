#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import  absolute_import

import json
import random
import requests

from time import sleep
from faker import Faker

from urlparse import urljoin

from entity_spider.config.log import logger
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError

from entity_spider.config import celery_config
from entity_spider.Client.exceptions import *
import time

faker = Faker()


class BaseClient(requests.Session):
    def get_header(self):
        return {}

    def crawl_url(self, url,delay=0):
        time.sleep(delay)
        return self.get(url, headers=self.get_header())

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
        headers = self.get_header() or headers
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
        except Exception as e :
            raise Retry(message=u'other exception ')
        if stream:
            return resp
        # resp.utf8_content = resp.content.decode('utf-8')
        # resp.utf8_content = resp.utf8_content.rstrip('\n')
        return resp


