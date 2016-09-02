from __future__ import absolute_import

from entity_spider.api import  top
from pprint import pprint
import json
from entity_spider.config.keys import baichuan_app_secret as app_secret,baichuan_app_key as  app_key

appkey = app_key
secret = app_secret


def item_list(ids=None):
    req = top.api.TaeItemsListRequest()
    req.set_app_info(top.appinfo(app_key, app_secret))
    req.fields = "title,nick,price"
    req.num_iids = ids or "18166313052"
    try:
        resp = req.getResponse()
        # pprint(resp)
        return resp
    except Exception as e:
        # pprint(e)
        return None


def tae_item_detail(open_iid):
    req=top.api.TaeItemDetailGetRequest()
    req.set_app_info(top.appinfo(appkey,secret))

    req.buyer_ip="127.0.0.1"
    req.fields="itemInfo,priceInfo,skuInfo,stockInfo,rateInfo,descInfo,sellerInfo,mobileDescInfo,deliveryInfo,storeInfo,itemBuyInfo,couponInfo"
    req.open_iid=open_iid
    try:
        resp= req.getResponse()
        return resp
    except Exception,e:
        pprint(e)
        return None

def seller_info():
    req=top.api.ShopGetRequest()
    req.set_app_info(top.appinfo(app_key,app_secret))

    req.fields="sid,cid,title,nick,desc,bulletin,pic_path,created,modified"
    req.nick="huangdingxiang2011"
    try:
        resp= req.getResponse()
        pprint(resp)
    except Exception,e:
        pprint(e)

def seller_item_list():
    # -*- coding: utf-8 -*-

    req=top.api.TaeItemsSelectRequest()
    req.set_app_info(top.appinfo(app_key,app_secret))

    req.seller_nick="huangdingxiang2011"
    req.page_no=1
    req.page_size=20
    req.fields="title,auction_id,category,categoryName,pict_url,reserve_price,skus"
    try:
        resp= req.getResponse()
        pprint(resp)
    except Exception,e:
        pprint(e)


def quick_item_info_from_id(id):
    ilist = item_list("%s"%id)

    items = ilist.get('tae_items_list_response',{})\
                    .get('items',{})\
                    .get('x_item', [])

    open_iid = None

    if len(items):
        open_iid  = items[0].get('open_iid')
        item_info = tae_item_detail(open_iid)
        pprint(item_info)

    else :
        print('item not found')



import requests

def get_shop_list():
    pass



if __name__ == '__main__':
    # item_list()
    # seller_item_list()
    # seller_info()
    # tae_item_detail()
    quick_item_info_from_id(531879375795)
