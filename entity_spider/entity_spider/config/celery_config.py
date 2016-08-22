from __future__ import  absolute_import
from entity_spider.config.env import *


from celery.schedules import crontab


BROKER_URL = broker_url
CELERY_RESULT_BACKEND = broker_url
CELERYD_CONCURRENCY = celery_concurrency
CELERY_DISABLE_RATE_LIMITS = False
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

CELERY_ALWAYS_EAGER = celery_eager

CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle','json']
CELERYD_PREFETCH_MULTIPLIER = 2
CELERY_IMPORTS = (
    'entity_spider.CeleryApp.tasks',
    'entity_spider.job.get_shop_entities',
    # 'entity_spider.job.check_entity_state',
    # 'entity_spider.job.update_tb_shop_id',

)

CELERYBEAT_SCHEDULE = {
    'crawl_all_articles': {
        'task': 'entity.check_all_entity_state',
        'schedule': crontab(minute='0', hour='2',day_of_week=6)
    },
    'update_all_tb_shop_id': {
        'task': 'shop.update_all_shop_id',
        'schedule': crontab(minute='0', hour='1')
    },

}

#
# CELERY_ROUTES = {
#     'entity.create_entity':
#         {
#             'queue': 'CREATE_QUE'
#         }
# }