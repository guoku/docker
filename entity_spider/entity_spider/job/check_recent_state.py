from __future__ import  absolute_import

import time
from entity_spider.core.models import Entity

from entity_spider.CeleryApp.tasks import check_entity
from entity_spider.CeleryApp.tasks import app, RequestsTask

from entity_spider.utils import queryset_iterator
from entity_spider.config.job import  CRAWL_LINK_INTERVAL
e_count = Entity.objects.new_or_selection().count()



@app.task(base=RequestsTask, name='entity.check_recent_entity_state')
def check_recent_entity_state():
    entities = Entity.objects.active().order_by('-id')[:3000]

    for entity in entities:
        # time.sleep(CRAWL_LINK_INTERVAL)
        check_entity.delay(entity.id)

if __name__ == '__main__':
    check_recent_entity_state()




