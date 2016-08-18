from __future__ import  absolute_import

import time

from entity_spider.Client import Retry
from entity_spider.Client import TaobaoRequestException
from entity_spider.Handlers import LinkHandlerException
from entity_spider.Parsers.exceptions import LinkParserException
from entity_spider.config.log import logger
from entity_spider.core.models import Entity

from entity_spider.CeleryApp.tasks import check_entity, check_link
from entity_spider.CeleryApp.tasks import app, RequestsTask

from entity_spider.utils import queryset_iterator
from entity_spider.config.job import  CRAWL_LINK_INTERVAL
e_count = Entity.objects.new_or_selection().count()



@app.task(base=RequestsTask, name='entity.check_all_entity_state')
def check_all_entity_state():
    entities = Entity.objects.active()
    start = time.time()
    for entity in queryset_iterator(entities):
        # time.sleep(CRAWL_LINK_INTERVAL)
        # check_entity.delay(entity.id)
        retry_count = 5
        if retry_count <= 0:
            logger.error('max retry count reached , for enetity : %s' % entity.id)
            return
        try:
            entity = Entity.objects.get(pk=entity.id)
            buy_links = entity.buy_links.filter(status__in=[1, 2])
            for blink in buy_links:
                check_link.delay(blink.id)

        except TaobaoRequestException as e:
            logger.error('taobao request error !!  %s' % e.message)
            logger.error('when deal with entity : %s' % entity.id)

        except (LinkParserException, LinkHandlerException) as e:
            logger.error('taobao Link parser or handler error %s ,' % e.message)

        except Retry as e:
            check_entity.delay(entity.id, retry_count - 1)

        except Exception as e:
            logger.error('when deal with entity {entity_id}'.format(entity_id=entity.id))
            logger.error('fatal error %s' % e.message)
    end = time.time()
    run_time = end - start
    logger.info('total running time for task check_all_entity_state is %f seconds' % run_time)



if __name__ == '__main__':
    check_all_entity_state()

    #to do check this one
    # for i in range(20):
    #     id = i + 4154
    #     check_entity(id)


