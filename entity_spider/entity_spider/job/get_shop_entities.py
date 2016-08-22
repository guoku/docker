from __future__ import absolute_import
from entity_spider.core.models import Shop, GKUser, Buy_Link, Entity
from entity_spider.job.update_tb_shop_id import update_tb_shop_by_id
from entity_spider.CeleryApp.tasks import app, RequestsTask
from entity_spider.config.log import logger
from entity_spider.Parsers.taobao import TaobaoShopParser, TaobaoLinkParser
from entity_spider.Client.taobao import TaobaoClient
from entity_spider.api import  top
from entity_spider.utils import batch , cal_entity_hash,pick
from entity_spider.Client.exceptions import Retry
from pprint import  pprint

import redis
from entity_spider.config.env import redis_host

class RetryFailed(Exception):
    pass


def prepare_origin_id_set():
    r = get_redis()

    set_key = 'oid_set'
    r.delete(set_key)
    origin_ids = Buy_Link.objects.all().values_list('origin_id', flat=True)
    for oid in origin_ids :
        r.sadd(set_key, oid)

def add_origin_id_set(origin_id):
    r = get_redis()
    set_key='oid_set'
    r.sadd(set_key, origin_id)

def get_redis():
    r = redis.StrictRedis(host=redis_host)
    return r


@app.task(name='shop.get_all_shop_entities')
def get_all_shop_entities():
    prepare_origin_id_set()
    shops = Shop.objects.all()
    for shop in shops:
        get_shop_entities.delay(shop.id)


    logger.info('-'*60)
    logger.info('get all shop entities done')
    logger.info('-'*60)


def get_shop_entities_tb_id_list(shoplink):
    return TaobaoShopParser(TaobaoClient().crawl_url(shoplink))\
                            .shop_entities_tb_id_list


def get_tb_shop_id(shoplink):
    return  TaobaoShopParser(TaobaoClient().crawl_url(shoplink))\
                                           .shop_id

from entity_spider.api.tools import get_entitis_prop_list

@app.task(base=RequestsTask, name='shop.get_shop_entities')
def get_shop_entities(shop_id, retry_count=5):
    try:
        shop = Shop.objects.get(pk=shop_id)
        user = shop.owner
        entities_ids = get_shop_entities_tb_id_list(shop.tb_shop_link)
        tb_shop_id =  get_tb_shop_id(shop.tb_shop_link)
        entity_props =  get_entitis_prop_list(entities_ids)
        tb_item_list = zip(entities_ids, entity_props)
        for item in tb_item_list:
            crawl_tb_entity.delay(item, tb_shop_id=tb_shop_id, user_id=user.id)

    except Retry as e:
        retry_count = retry_count  -1
        if retry_count >= 0 :
            logger.info('retry get_shop_entities : %s' %shop_id)
            get_shop_entities.delay(shop_id, retry_count=retry_count)
            return
        else :
            raise RetryFailed('max retry count exeeded , for shop :%s' %shop_id)

    except Exception as e:
        logger.error('fatal error : %s when dealing shop  %s' %(e, shop_id))
        raise e



def is_entity_exist(tb_entity_id):
    r = get_redis()
    set_key = 'oid_set'
    if  r.sismember(set_key,tb_entity_id):
        return True
    else:
        return False

    #--------------------

    try:
       bl =  Buy_Link.objects.get(origin_id=tb_entity_id, origin_source='taobao.com')
    except Buy_Link.DoesNotExist as e :
       return False
    except Buy_Link.MultipleObjectsReturned as e:
        return True

    return True

from entity_spider.api.tools import \
                             get_tb_entity_detail, \
                             clean_tb_entity_dic,\
                             get_tb_entity_detail_tae


def update_tb_buy_link_status(origin_id, status, user_id):
    try :
       bl =  Buy_Link.objects.get(origin_id=origin_id, origin_source='taobao.com')
       bl.status = status
       # bl.entity.user_id = user_id
       # bl.entity.save()
       bl.save()
    except Buy_Link.DoesNotExist as e:
        logger.error('update none existing buy link: origin_id %s'%origin_id)
    except Buy_Link.MultipleObjectsReturned as e:
        bl = Buy_Link.objects.filter(origin_id=origin_id, origin_source='taobao.com')[0]
        bl.status = status
        # bl.entity.user_id = user_id
        # bl.entity.save()
        bl.save()
        logger.error('should not have more than one buylink , tb_open_id: %s' %origin_id)

@app.task(base=RequestsTask, name='entity.crawl_tb_entity')
def crawl_tb_entity(item, tb_shop_id, user_id ,retry_count=5):
    try :
        #todo , block existing entity here
        #item is a tuple
        origin_id = item[1]['origin_id']
        if is_entity_exist(origin_id):
            # update_tb_buy_link_status(origin_id, 2, user_id)
            logger.info('origin_id:%s, existed'% origin_id)
            return

        partial_entity = item[1]
        open_iid = partial_entity['open_iid']
        entity_dic = get_tb_entity_detail_tae(open_iid)
        entity_dic.update(partial_entity)
        entity_dic.update(
            {
                'shop_link': 'http://shop%s.taobao.com'%tb_shop_id,
                'link': 'http://item.taobao.com/item.htm?id=%s'%entity_dic['origin_id'],
                'entity_hash': cal_entity_hash("%s%s%s"%(entity_dic['origin_id'], entity_dic['title'],entity_dic['shop_nick']))
             })
    except Retry as e:
        retry_count = retry_count  -1
        if retry_count >= 0 :
            logger.info('retry crawl_tb_entity for item %s'%item)
            crawl_tb_entity.delay(item,tb_shop_id,user_id, retry_count=retry_count)
            return
        else :
            raise RetryFailed('max retry count exeeded , for tb entity :%s' %item)
    # if everything ok,
    # do not use task , or sql request will brust at same time
    create_entity(entity_dic, user_id)


# TODO : route this task to single concurrency single route
@app.task(name='entity.create_entity')
def create_entity(entity_dic, user_id=None):

    real_entity = pick(entity_dic,
                       ['entity_hash',
                        'brand',
                        'title',
                        'price',
                        'images',
                        'category_id',
                        ])

    real_entity['user_id'] = user_id
    real_entity['status'] = Entity.new

    real_buylink = pick(entity_dic, [
                        'origin_id',
                        'cid',
                        'origin_source',
                        'link',
                        'price',
                        'shop_link'
    ])

    if not is_entity_exist(entity_dic['origin_id']):
        try:

            new_entity = Entity.objects.create(
               **real_entity
            )
            real_buylink['entity'] =  new_entity
            real_buylink['default'] = True
            new_buy_link =  Buy_Link.objects.create(
                 **real_buylink
            )
            crawl_entity_images.delay(new_entity.id)

            # guess_entity_category(new_entity.id)
            add_origin_id_set(real_buylink['origin_id'])
            logger.info('finished entity %s'%new_entity.title)
        except Exception as e :
            logger.error('fatal , create entity fail %s' %entity_dic)
            raise e
    else:
        logger.info('entity exist : %s %s' %(entity_dic['title'], entity_dic['origin_id']))




@app.task(base=RequestsTask, name='entity.guess_category')
def guess_entity_category(entity_id):
    '''
    TODO: implement
    :param entity_id:
    :return:
    '''
    raise NotImplemented()

@app.task(base=RequestsTask,name='entity.crawl_entity_images')
def crawl_entity_images(entity_id, retry_count=5):
    '''
    TODO : implement
    :param entity_id:
    :return:
    '''

    try :
        entity = Entity.objects.get(pk=entity_id)
        entity.fetch_image()
        logger.info('image fetch finished for %s : %s'%(entity_id,entity.title ))
    except  Entity.DoesNotExist as e:
        logger.error('try to crawl image of none exist entity: %s'%entity_id)
        logger.error('%s'%e)
        raise e

    except Exception as e:
        logger.error('image fetch error for entity : %s %s' %(entity.id, entity.title))
        pass








if __name__ == '__main__':
    # print get_shop_entities_tb_id_list('https://jiazazhi.taobao.com/')
    # prepare_origin_id_set()
    # get_shop_entities(17)
    get_shop_entities(17)
    # get_all_shop_entities()

    # crawl_entity_images.delay(4649857)

    pass
