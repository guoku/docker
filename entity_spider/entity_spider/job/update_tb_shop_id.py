from __future__ import absolute_import
from entity_spider.core.models import Shop

from entity_spider.CeleryApp.tasks import app, RequestsTask
from entity_spider.Client.taobao import TaobaoClient
from entity_spider.Parsers.taobao import TaobaoShopParser
from entity_spider.config.log import logger
from entity_spider.Parsers.exceptions import LinkParserException

@app.task(base=RequestsTask,name='shop.update_all_shop_id')
def update_all_tb_shop_id():
    shops = Shop.objects.filter(tb_shop_id=None).exclude(tb_shop_id=0)
    # shops = Shop.objects.all()
    for shop in shops :
        update_tb_shop_by_id.delay(shop.id)
        # update_tb_shop_by_id(shop.id)
    logger.info('-'*80)
    logger.info('update tb shop id done')
    logger.info('-'*80)


@app.task(base=RequestsTask, name='shop.shop_update_shop_id')
def update_tb_shop_by_id(shop_id):
    try:
        shop = Shop.objects.get(pk=shop_id)
        link  = shop.shop_link
        shop_parser = TaobaoShopParser(TaobaoClient().crawl_url(link))
        shop.tb_shop_id =  shop_parser.parse().get('shop_id')
        shop.common_shop_link = 'http://shop%s.taobao.com'%shop.tb_shop_id
        logger.info('tb_shop_id for shop id %s is : %s' %(shop_id,shop.tb_shop_id))
        shop.save()

    except LinkParserException as e :
        logger.error('shop offline or shop page parse error for shop : %s , link : %s' %(shop.shop_title, shop.shop_link))
        shop.tb_shop_id = 0
        shop.save()
    except Exception as e :
        logger.error('fatal: update shop id fail %s' %e.message )


if __name__ == '__main__':
    update_all_tb_shop_id()
    # update_tb_shop_by_id(110)