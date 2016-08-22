from __future__ import absolute_import
from bs4 import BeautifulSoup
from entity_spider.config.log import logger
from lxml import  etree

class BaseEntityParser(object):
    def __init__(self, resp):
        self._resp = resp


    def parse(self):
        res = {

            'title': self.title,
            'brand': self.brand,
        }

    @property
    def title(self):
        return 'not implement'

    @property
    def band(self):
        return 'not implement'

    @property
    def price(self):
        return 'not implement'




class BaseParser(object):
    def __init__(self, resp):
        self._resp = resp
        if not self._resp is None:
            self._soup = BeautifulSoup(self._resp.text)
            self._headers = self._resp.headers
            self._tree = etree.HTML(self._resp.text)

    def parse(self):
        raise NotImplemented()



class BaseBuyLinkParser(object):

    (ENTITY_REMOVE, ENTITY_SOLDOUT, ENTITY_NORMAL) = (0, 1, 2)

    def __init__(self):
        pass

        # self._metas = self._resp.xpath('//meta/@content').extract()
    def get_item_status(self, response):
        raise 'not Implement '

    @property
    def status(self):
        return self.get_item_status()

    def parse(self,resp):

        self._resp = resp
        self._soup = BeautifulSoup(resp.text)
        self._headers  = resp.headers
        self._tree = etree.HTML(self._resp.text)

        status = self.status
        if self.ENTITY_REMOVE  == status:
            return {
                'status': self.ENTITY_REMOVE
            }
        else:
            return {
                'origin_id': self.origin_id,
                'origin_source': self.origin_source,
                'cid': self.cid,
                'shop_link': self.shop_link,
                'shop_id': self.shop_id,
                'status': status
            }

    @property
    def brand(self):
        raise NotImplemented()

    @property
    def request_url(self):
        return self._resp.url

    @property
    def origin_id(self):
        raise NotImplemented()

    @property
    def origin_source(self):
        raise NotImplemented()

    @property
    def cid(self):
        raise NotImplemented()

    @property
    def link(self):
        raise NotImplemented()

    @property
    def price(self):
        raise NotImplemented()

    @property
    def foreign_price(self):
        raise NotImplemented()

    @property
    def shop_link(self):
        raise NotImplemented()

    @property
    def shop_id(self):
        raise NotImplemented()

    @property
    def seller(self):
        raise NotImplemented()

    @property
    def is_sold_out(self):
        raise NotImplemented()

    @property
    def is_removed(self):
        raise NotImplemented()




