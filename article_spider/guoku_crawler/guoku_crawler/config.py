#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys
from celery.schedules import crontab
from guoku_crawler.utils import config_from_env
from guoku_crawler.logging_conf import LOGGING
import logging.config
import logging

#config for local
#=========================
# data_base_ip = '192.168.1.117'
# data_base_user = 'guoku'
# data_base_pass = 'guoku!@#'
# phantom_server = 'http://phantomwebserver:5000'
# image_host = 'http://127.0.0.1:9766/'
# image_path = 'images/'
# local_file = True
# celery_eager = True
# celery_concurrency  = 1
# request_interval = 1

#config for remote test 48
#==========================
# data_base_ip = '10.0.2.125'
# data_base_user = 'guoku'
# data_base_pass = 'guoku1@#'
# phantom_server = 'http://phantomwebserver:5000'
# image_host = 'http://imgcdn.guoku.com/'
# image_path = 'images/'
# local_file = False
# celery_eager = True
# celery_concurrency  = 1
# request_interval = 8


#config for remote production 49
#===========================
data_base_ip = '10.0.2.90'
data_base_user = 'guoku'
data_base_pass = 'guoku!@#'
phantom_server = 'http://phantomwebserver:5000'
image_host = 'http://imgcdn.guoku.com/'
image_path = 'images/'
local_file = False
celery_eager = True
celery_concurrency  = 1
request_interval = 12

#-------------------------------

broker_ip = 'redis://localhost:6379/0'
logging.config.dictConfig(LOGGING)
logger = logging.getLogger("request")

# Database
DATABASES = {
    'DB_NAME': 'core',
    'USER':  data_base_user,
    'PASSWORD': data_base_pass,
    'HOST': data_base_ip,
    'PORT': '3306',
}

# Image
IMAGE_HOST =image_host
IMAGE_PATH = image_path
LOCAL_IMAGE_PATH = image_path
LOCAL_FILE_STORAGE = local_file
MEDIA_ROOT = ''
MOGILEFS_DOMAIN = 'prod'
MOGILEFS_TRACKERS = ['10.0.2.50:7001']
MOGILEFS_MEDIA_URL = 'images/'
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o777
FILE_UPLOAD_PERMISSIONS = 0o777
MEDIA_URL = 'images/'
STATIC_URL = 'http://static.guoku.com/static/v4/dafb5059ae45f18b0eff711a38de3d59b95bad4c/'
DEFAULT_ARTICLE_COVER = "http://imgcdn.guoku.com/images/ee7dd4a43d75ab28b3c65cc960429724.jpeg"



# System
DEBUG = True
CONNECTION_POOL = ''
PHANTOM_SERVER = phantom_server

# Celery
BROKER_URL = broker_ip
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERYD_CONCURRENCY = celery_concurrency
CELERY_DISABLE_RATE_LIMITS = False
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

CELERY_ALWAYS_EAGER = celery_eager

CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERYD_PREFETCH_MULTIPLIER = 2
CELERY_IMPORTS = (
    'guoku_crawler.article',
    'guoku_crawler.tasks'
)
CELERY_ROUTES = {
    'weixin.update_sogou_cookie':
        {
            'queue': 'cookies'
        }
}
CELERY_ANNOTATIONS = {
    'crawl_articles': {
        'rate_limit': '30/m',
    },
    'rss.crawl_list': {
        'rate_limit': '30/m',
    },
    'weixin.crawl_list': {
        'rate_limit': '30/m',
    },
    'weixin.crawl_weixin_article': {
        'rate_limit': '10/m',
    },
    'weixin.prepare_sogou_cookies': {
        'rate_limit': '10/m',
    },
    'weixin.update_sogou_cookie': {
        'rate_limit': '10/m',
    },
}
REQUEST_INTERVAL = request_interval
CELERYBEAT_SCHEDULE = {
    'crawl_all_articles': {
        'task': 'crawl_articles',
        'schedule': crontab(minute=59, hour='*/4')
    },
}

# Redis
CONFIG_REDIS_HOST = 'localhost'
CONFIG_REDIS_PORT = 6379
CONFIG_REDIS_DB = 0

# Sogou
SOGOU_USERS = [
    'waser1959@gustr.com',
    'asortafairytale@fleckens.hu',
    'adisaid@jourrapide.com',
    'rathe1981@rhyta.com',
    'andurn@fleckens.hu',
    'sanyuanmilk@fleckens.hu',
    'yundaexpress@rhyta.com',
    'sunstarorabreathfine@jourrapide.com',
    'indonesiamandheling@einrot.com',
    'charlottewalkforshame@dayrep.com',
    'shoemah55@superrito.com',
    'monan1977@fleckens.hu',
    'obsomed1977@jourrapide.com',
    'finighboy78@superrito.com',
    'artimessill1959@einrot.com',
    'suildrued41@dayrep.com',
    'drind1977@jourrapide.com',
    'duad1937@jourrapide.com',
    'alat1981@jourrapide.com',
    'paboy1973@superrito.com',
    'fuly1964@cuvox.de',
    'nelf1946@cuvox.de',
    'offam1939@cuvox.de',
    'norne1981@dayrep.com',
    'monce1934@teleworm.us',
    'overniseents93@einrot.com',
    'gavis1978@einrot.com',
    'harmuden1974@superrito.com',

    # local
    # 'saind1974@gustr.com',
    # 'forry1978@superrito.com',
    # 'wassiriour49@teleworm.us',

]

proxy_list = [
    '117.135.251.135:80',
    '117.135.251.136:80',
    '117.135.251.131:81',
    '117.135.251.134:81',
    '120.198.233.211:80',
    '124.88.67.9:81',
    '158.255.211.17:80',
    '222.130.223.139:8118',
    '206.55.232.198:80',
    '152.44.90.101:8080',
    '167.198.80.83:3128',
    '152.44.90.102:8080',
    '108.59.10.138:55555',
    '107.151.152.210:80',
    '165.139.149.169:3128',
    '205.221.83.162:3128',
    '23.253.95.85:8080',
    '107.151.152.218:80',
    '172.99.73.42:3128',
    '108.59.10.135:55555',
    '198.199.85.188:3128',
    '70.90.16.115:8080',
    '107.163.117.37:808',
    '107.163.117.24:808',
    '159.203.83.227:80',
    '107.151.136.203:80',
    '70.182.191.85:8080',
    '108.59.10.141:55555',
    '117.177.250.152:81',
    '117.177.250.152:82',
    '117.135.251.132:84',
    '117.177.250.152:83',
    '117.177.250.152:85',
    '117.177.250.152:84',
    '124.202.179.242:8118',
    '111.161.126.108:80',
    '117.135.250.133:8082',
    '61.180.67.212:80',
    '119.57.149.36:80',
    '120.198.244.29:80',
    '120.198.244.29:8080',
    '120.198.244.29:9999',
    '120.198.244.29:8081',
    '117.135.251.133:81',
    '117.135.251.131:80',
    '117.135.251.132:83',
    '117.135.251.133:84',
    '117.135.251.132:81',
    '117.135.251.134:82',
    '117.135.251.133:80',
    '117.135.251.134:84',
    '117.135.251.134:83',
    '117.135.251.131:83',
    '120.52.72.19:80',
    '117.135.251.131:81',
    '61.174.13.12:443',
    '117.135.251.135:81',
    '117.135.251.133:83',
]

SOGOU_PASSWORD = 'guoku1@#'



def load_config():
    env_config = config_from_env('GK_')
    for k, v in env_config.items():
        setattr(sys.modules[__name__], k, v)


load_config()




