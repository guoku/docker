from __future__ import absolute_import
import time

from guoku_crawler import config
from guoku_crawler.article.client import ProxyTestClient
from guoku_crawler.exceptions import ProxyFail
from guoku_crawler.config import logger

import  requests

proxy_list = config.proxy_list
ptest_client = ProxyTestClient()

def check_proxy(proxy):
    url = 'http://www.sina.com.cn'
    logger.info('testing proxy: %s' %proxy)
    try:
        resp = ptest_client.get(url=url, proxies={'http':proxy})
    except ProxyFail as e:
        return False

    # print resp.text
    return True

def update_proxy_list():
    final_list = []
    for proxy in list(set(proxy_list)):
        if check_proxy(proxy):
            final_list.append(proxy)

    return final_list


if __name__ == '__main__':
    logger.info('origin proxy count : %s' % len(config.proxy_list))
    refresh_list = update_proxy_list()
    print refresh_list
    logger.info('final proxy count : %s' % len(refresh_list))

