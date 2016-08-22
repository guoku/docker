from entity_spider.Handlers import BaseLinkHandler
from entity_spider.Parsers.taobao import TaobaoLinkParser
from entity_spider.Client.taobao import TaobaoClient
from entity_spider.config.log import logger


class TaobaoLinkHandler(BaseLinkHandler):
    def __init__(self):
        self._parser = TaobaoLinkParser()
        self._client = TaobaoClient()

    def can_handle(self, linkObj):
        return  linkObj.origin_source == 'taobao.com'

    def setBuyLinkRemoved(self):
        buylink = self.get_linkObj()
        buylink.status=0
        logger.info('{entity_title}: {entity_id} removed from taobao'\
                    .format(
                        entity_title=buylink.entity.title.encode('utf-8'),
                        entity_id=buylink.entity_id))
        buylink.save()

    def updateBuyLinkStatus(self, entity_dic):
        buylink = self.get_linkObj()
        buylink.status = entity_dic['status']
        buylink.shop_link = entity_dic['shop_link']
        logger.info('{entity_title}: {entity_id} update, status:{status}'\
                    .format(
                        entity_title=buylink.entity.title.encode('utf-8'),
                        entity_id=buylink.entity_id,
                        status=buylink.status
                    ))
        buylink.save()


    def handle_new_state(self, entity_dic):
        if entity_dic['status'] == 0:
            self.setBuyLinkRemoved()
        elif entity_dic['status'] == 1 or entity_dic['status'] == 2:
            self.updateBuyLinkStatus(entity_dic)

        print '-'*80
        # print entity_dic
        # print 'entity_id : %s' % self._linkObj.entity_id
        # print 'link : %s'% self._linkObj.link
        # print 'entity title : %s' % self._linkObj.entity.title
        # print '-'*80
