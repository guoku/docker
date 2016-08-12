# coding=utf-8
from __future__ import absolute_import
from hashlib import md5
import requests
import json

from entity_spider.api import  top
from entity_spider.api.top import  api
from entity_spider.api.exceptions import APIException
from entity_spider.config.keys import baichuan_app_key as app_key , baichuan_app_secret as app_secret
from entity_spider.utils import batch
from entity_spider.config.log import logger
from entity_spider.config.env import tae_item_detail_url
from entity_spider.utils import  walk


from pprint import  pprint


def _get_entity_props(resp):
    try :

       items =  walk(resp,'tae_items_list_response.items.x_item')

       entity_props = [ {
                'open_iid': walk(item, 'open_iid'),
                'cid':walk(item,'cid'),
                'origin_id':walk(item,'open_id'),
                'shop_name':walk(item, 'shop_name'),
                'title':walk(item,'title')
                   } for item in items]
       return entity_props
    except Exception as e:
        logger.error('get open id call error')
        raise  e

def _batch_get_entity_prop_tae(num_id_list):

    resp = requests.post('http://guoku2.wx.jaeapp.com/gk_item_list/',
                  json={'num_id_list': num_id_list})

    result = json.loads(resp.text)

    if 'error' in result:
        logger.error('tae item list get error ' )
        raise  APIException(message='TAE app engine get item list fail')
    else:

        openids = _get_entity_props(result)
        return openids


def _batch_get_entity_prop(num_id_list):
    if len(num_id_list)>50:
        raise APIException('tb api demand num id list max 50')
    req = api.TaeItemsListRequest()
    req.set_app_info(top.appinfo(app_key, app_secret))
    req.fields = "title,nick,price,cid,shop_name"
    req.num_iids = ','.join(num_id_list)
    try :
        resp = req.getResponse()
        openids = _get_entity_props(resp)
        return openids

    except Exception as e :
        raise e


def get_entitis_prop_list(num_id_list):
    entity_prop_list =  []
    for batch_list in batch(num_id_list,50):
        entity_prop_list += _batch_get_entity_prop_tae(batch_list)
    return entity_prop_list


def get_tb_entity_detail_tae(open_iid):
    resp = requests.post('http://guoku2.wx.jaeapp.com/gk_item_detail/',
                  json={'open_iid': open_iid})
    result = json.loads(resp.text)
    if 'error' in result:
        logger.error('TAE api get error %s ' %open_iid)
        raise  APIException(message='TAE app engine get fail')
    else:
        return clean_tb_entity_dic(result['tae_item_detail_get_response'])

def get_tb_entity_detail(open_iid):
    req=top.api.TaeItemDetailGetRequest()
    req.set_app_info(top.appinfo(app_key, app_secret))
    req.buyer_ip = '127.0.0.1'
    req.fields="itemInfo,priceInfo,skuInfo,stockInfo,rateInfo,descInfo,sellerInfo,mobileDescInfo,deliveryInfo,storeInfo,itemBuyInfo,couponInfo"
    # req.fields = "itemInfo,priceInfo,stockInfo,sellerInfo,mobileDescInfo,deliveryInfo,storeInfo,itemBuyInfo"
    req.open_iid = open_iid
    try :
        resp = req.getResponse()
        return clean_tb_entity_dic(resp['tae_item_detail_get_response'])

    except Exception as e :
        logger.error('get tb detail info error %s' %e)
        raise e



def merge_item_property(entity_dic):
    item_property_list = walk(entity_dic,'data.item_info.item_props.item_property', [])
    item_props = walk(entity_dic,'data.item_info.item_props')
    prop_dic = {}
    for prop in item_property_list:
        prop_dic[prop["name"]] = prop['value']
    item_props.update(prop_dic)

from datetime import datetime
from entity_spider.core.models import Entity
def clean_tb_entity_dic(entity_dic):
    # pprint(entity_dic)
    merge_item_property(entity_dic)
    cleaned_dic = {
        'category_id' : 300, #handle category later,
                             #cid will be got and saved to buylink
                             #category_id default 300, and will be saved to
        'title': walk(entity_dic, 'data.item_info.title'),
        'price': walk(entity_dic,'data.price_info.item_price.price.price').split('-')[0],
        'promotion_price':walk(entity_dic,'data.price_info.promotion_price'),
        'images': walk(entity_dic, 'data.item_info.pics.string'),
        'origin_id': None,
        'origin_source':'taobao.com',
        'shop_link': None,
        'shop_nick':walk(entity_dic, 'data.seller_info.shop_name'),
    }

    try:
        cleaned_dic['brand'] = walk(entity_dic,'data.item_info.item_props')[u'品牌']
    except Exception as e :
        cleaned_dic['brand'] = ''
    return cleaned_dic



def cal_entity_hash(hash_string):
    _hash = None
    while True:
        _hash = md5((hash_string + unicode(datetime.now())).encode(
            'utf-8')).hexdigest()[0:8]
        try:
            Entity.objects.get(entity_hash=_hash)
        except Entity.DoesNotExist:
            break
    return _hash


if __name__ == '__main__':
    print('do someting')



