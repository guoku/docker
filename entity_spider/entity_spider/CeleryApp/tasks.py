from __future__  import  absolute_import

import requests
from celery import Celery, Task
from entity_spider.config import celery_config
from entity_spider.Client.exceptions import TaobaoRequestException, Retry
from entity_spider.Handlers.taobao import TaobaoLinkHandler
from entity_spider.Handlers.exceptions import LinkHandlerException
from entity_spider.Parsers.exceptions import LinkParserException
from entity_spider.config.log import logger

app = Celery('tasks')
app.config_from_object(celery_config)

def get_link_handlers():
    return [TaobaoLinkHandler(),]

class RequestsTask(Task):
    def run(self, *args, **kwargs):
        pass

    abstract = True
    compression = 'gzip'
    default_retry_delay = 5
    send_error_emails = True
    max_retries = 3

    def __call__(self, *args, **kwargs):
        try:
            return super(RequestsTask, self).__call__(*args, **kwargs)
        except (requests.Timeout, requests.ConnectionError) as e:
            raise self.retry(exc=e)



from entity_spider.core.models import Entity,Buy_Link,GKUser

@app.task(base=RequestsTask, name='entity.check_entity')
def check_entity(entity_id,retry_count=5):
    if retry_count <= 0 :
        logger.error('max retry count reached , for enetity : %s'% entity_id)
        return
    try :
        entity = Entity.objects.get(pk=entity_id)
        buy_links = entity.buy_links.filter(status__in=[1,2])
        for blink in buy_links:
            check_link(blink.id)

    except TaobaoRequestException as e :
        logger.error('taobao request error !!  %s'  %e.message)
        logger.error('when deal with entity : %s' %entity_id)

    except (LinkParserException, LinkHandlerException) as e:
        logger.error('taobao Link parser or handler error %s ,' %e.message)

    except Retry as e:
        check_entity.delay(entity_id,retry_count-1)

    except Exception as e :
        logger.error('when deal with entity {entity_id}'.format(entity_id=entity_id))
        logger.error('fatal error %s' %e.message)


def isTaobaoLinkObj(linkObj):
    pass

def getEntityCrawlUrl(linkObj):
    pass



@app.task(base=RequestsTask, name='buylink.craw_link')
def check_link(linkObj_id):
        linkObj= Buy_Link.objects.get(id=linkObj_id)
        handlers = get_link_handlers()
        for handler in handlers:
            if handler.can_handle(linkObj):
                handler.handle(linkObj)




if __name__ == '__main__':
    check_entity(1396)

