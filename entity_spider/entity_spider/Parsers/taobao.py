# coding=utf-8
from entity_spider.Parsers import BaseBuyLinkParser
from entity_spider.config.log import logger
from entity_spider.Parsers.exceptions import LinkParserException
from entity_spider.Parsers import BaseParser
from entity_spider.Client.taobao import TaobaoClient
import  re
import urllib


class TaobaoLinkParser(BaseBuyLinkParser):

    def get_item_status(self, tree=None):
        tree = tree or self._tree
        # item['status'] = 2
        if 'noitem.htm' in self._resp.url:
            return self.ENTITY_REMOVE

        soldout = tree.xpath('//p[@class="tb-hint"]/strong/text()')
        if len(soldout) > 0:
            return self.ENTITY_SOLDOUT
        soldout = tree.xpath('//strong[@class="sold-out-tit"]/text()')
        if len(soldout) > 0:
            return self.ENTITY_SOLDOUT
        return self.ENTITY_NORMAL

    @classmethod
    def get_taobao_item_id_from_item_url(cls, url):
        return 'not implement url parse'

    def parse_taobao_id_from_url(self,url):
        url = url or self._resp.url
        params = url.split("?")[1]
        for param in params.split("&"):
            tokens = param.split("=")
            if len(tokens) >= 2 and (tokens[0] == "id" or tokens[0] == "item_id" or tokens[0] == "itemid"):
                return tokens[1]
        return None



    @property
    def origin_id(self):
        id = None
        try:
            id = self._headers['at_itemid']
        except KeyError as e:
            id = self.parse_taobao_id_from_url(self._resp.url)
        return id

    @property
    def origin_source(self):
        return 'taobao.com'

    @property
    def cid(self):
        cat = self._headers.get('x-category')
        try:
            _cid = cat.split('/')
            return _cid[-1]
        except AttributeError as e:
            logger.error("get cid error : %s", e.message)
            raise LinkParserException('can not get x-category')

    def get_ptag(self):
        ptag = self.soup.select("em.tb-rmb-num")
        if len(ptag) > 0:
            return ptag
        ptag = self.soup.select("strong.tb-rmb-num")
        if len(ptag) > 0:
            return ptag
        ptag = self.soup.select("span.originPrice")
        if len(ptag) > 0:
            return ptag

        return None

    @property
    def shop_id(self):
        mscope = self._soup.select('meta[name="microscope-data"]')
        if len(mscope) == 0 :
            raise  LinkParserException('can not find mscope data for origin id : %s' % self.origin_id)

        try :
            scope_values =  [tuple(item.split('='))  for item in  mscope[0].attrs['content'].split(';')]
            for (name , value ) in  scope_values:
                if 'shopId' == name.strip() :
                    return value
        except KeyError as e:
            # if _chaoshi
            # todo handle chaoshi LINK here
            raise LinkParserException('can not find shopId for origin id : %s' %self.origin_id)



    @property
    def shop_link(self):
        try:
            shop_id = self.shop_id
            return 'http://shop{shop_id}.taobao.com'.format(shop_id=self.shop_id)

        except LinkParserException as e :
            html = self._resp.text
            shopidtag = re.findall('shopId:"(\d+)', html)
            if len(shopidtag) > 0:
                return "http://shop" + shopidtag[0] + ".taobao.com"
            shopidtag = self._soup.select("div.tb-shop-info-ft a")
            if shopidtag:
                shop_link = shopidtag[0].attrs.get('href')
                if shop_link.startswith('//'):
                    shop_link = shop_link[2:]
                return shop_link
            shopidtag = tb_shop_name = self.soup.select("div.tb-shop-name a")
            if shopidtag:
                return tb_shop_name[0].attrs.get('href')
            return "http://chaoshi.tmall.com/"




    @property
    def price(self):
        ptag = self.get_ptag()
        if ptag:
            pr = ptag[0].string
            ps = re.findall("\d+\.\d+", pr or '')
            if ps:
                return float(ps[0])
            else:
                return 0.0
        else:
            raise LinkParserException('can not get price element ')
            return 0.0

    @property
    def brand(self):
        seller_soup = self._soup.select("ul.attributes-list li")
        if not seller_soup:
            seller_soup = self.soup.select("ul#J_AttrUL li")
        if seller_soup > 0:
            for brand_li in seller_soup:
                if brand_li.text.find(u'品牌') >= 0:
                    return brand_li.text.split(u':')[1].strip()
        return ''


class ShopEntityListPage(BaseParser):

    @property
    def entity_tb_id_list(self):
        content = urllib.unquote(self._resp.text)
        try :
            id_list_str = re.search('itemIds=([\d,]*)', content).group(1)
        except AttributeError as e :
            id_list_str = re.search(r'item_list=(.*?)&rn=',content).group(1)
        return id_list_str.split(',')

    @property
    def total_page_count(self):
        # 1 for taobao , 2 for tmall

        search = re.search(r'<span class=\\\"page-info\\\">\d+\/(\d+)<\/span>',self._resp.text)
        if search is None:
            try :
                return int(self._soup.select('.ui-page-s-len')[0].text.split('/')[-1])
            except Exception :
                raise Exception('can not find shop page info ')
        else:
            return int(search.group(1))




class ShopEntityListPageList(BaseParser):
    '''
        implement the iterator protocol
    '''
    def __init__(self, *args, **kwargs):
        super(ShopEntityListPageList, self).__init__(*args, **kwargs)
        self._current_page_num = 0
        self._asynSearchString = self.get_asyncSearch_string()

    def __iter__(self):
        return self

    def __getitem__(self, index):
        return self.get_page(index)

    def __len__(self):
        return self.page_count

    def get_asyncSearch_string(self):
        try :

            async_path =  self._soup.select('#J_ShopAsynSearchURL')[0]['value']
            return re.sub('/search.htm',async_path,self._resp.url)

        except IndexError as e  :

            return self._resp.url






    def next(self):
        page = self.get_next_page()
        self._current_page_num += 1
        return page

    def get_next_page(self):
        next_page_num = self._current_page_num + 1
        logger.info('get shop entity list page %s'%next_page_num)
        if self.has_page(next_page_num):
            return self.get_page(next_page_num)
        else :
            raise StopIteration()
            return None

    def get_page(self, page_num):
        if not self.has_page(page_num):
            raise IndexError()
        page_url = self.get_page_url(page_num)
        return ShopEntityListPage(TaobaoClient().crawl_url(page_url))


    def get_page_url(self, page_num):
        # page_url = re.sub('pageNo=\d+', 'pageNo=%s'%page_num, self._asynSearchString)
        page_url = self._asynSearchString+ '&pageNo=%s'%page_num
        return page_url


    def has_page(self,page_num):
        return page_num > 0 and page_num <= self.page_count

    @property
    def page_count(self):
        if not getattr(self, '_page_count', None) is None :
            return self._page_count
        else :
            # page_info =  self._soup.select('.page_info')[0].text
            page_count =  ShopEntityListPage(TaobaoClient().crawl_url(self._asynSearchString)).total_page_count
            self._page_count = page_count
            return page_count


class TaobaoShopParser(BaseParser):
    def parse(self):
        return {
            'shop_id': self.shop_id
        }

    @property
    def shop_id(self):
        mscope = self._soup.select('meta[name="microscope-data"]')
        if len(mscope) == 0 :
            raise  LinkParserException('can not find mscope data for shop link %s ' %self._resp.url)

        try :
            scope_values =  [tuple(item.split('='))  for item in  mscope[0].attrs['content'].split(';')]
            for (name , value ) in  scope_values:
                if 'shopId' == name.strip() :
                    return value
        except KeyError as e:
            # if _chaoshi
            # todo handle chaoshi LINK here
            raise LinkParserException('can not find shopId for origin id : %s' %self.origin_id)

    def get_entity_pages(self):
        elist_url = 'http://shop%s.taobao.com/search.htm'%self.shop_id
        page_list = ShopEntityListPageList(TaobaoClient().crawl_url(elist_url))
        return page_list

    @property
    def shop_entities_tb_id_list(self):
        entities_tb_id_list = []
        for page in self.get_entity_pages():
            entities_tb_id_list += page.entity_tb_id_list
        return entities_tb_id_list


class TOPAPIParser(object):
    pass






