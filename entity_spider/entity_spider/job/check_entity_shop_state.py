from __future__ import  absolute_import

import time
from entity_spider.core.models import Entity, Buy_Link

from entity_spider.CeleryApp.tasks import check_entity
from entity_spider.CeleryApp.tasks import app, RequestsTask

from entity_spider.utils import queryset_iterator
from entity_spider.config.job import  CRAWL_LINK_INTERVAL
e_count = Entity.objects.new_or_selection().count()



@app.task(base=RequestsTask, name='entity.check_all_entity_state')
def check_all_entity_state():
    eids = Buy_Link.objects.filter(origin_source='taobao.com',shop_link__isnull=True,status=2)\
                              .values_list('entity_id',flat=True)

    entities = Entity.objects.active().filter(pk__in=eids)

    for entity in queryset_iterator(entities):
        # time.sleep(CRAWL_LINK_INTERVAL)
        check_entity.delay(entity.id)



if __name__ == '__main__':
    check_all_entity_state()

    #to do check this one
    # for i in range(20):
    #     id = i + 4154
    #     check_entity(id)


