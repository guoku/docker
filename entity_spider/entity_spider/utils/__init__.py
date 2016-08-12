# coding=utf-8
import gc
import time
from pprint import pprint
from entity_spider.config.log import logger

def queryset_iterator(queryset, chunksize=5000):
    '''''
    Iterate over a Django Queryset ordered by the primary key

    This method loads a maximum of chunk size (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.

    Note that the implementation of the iterator does not support ordered query sets.
    '''
    # pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    # queryset = queryset.order_by('pk')
    # while pk < last_pk:
    #     for row in queryset.filter(pk__gt=pk)[:chunksize]:
    #         pk = row.pk
    #         yield row
    #     time.sleep(10)
    #     gc.collect()

    pk = last_pk
    while pk > 0 :
        for row in queryset.order_by('-pk').filter(pk__lt=pk)[:chunksize]:
            pk = row.pk
            yield row
        time.sleep(1)
        gc.collect()


def batch(iterable , bsize):
    l = len(iterable)
    for ndx in range(0,l,bsize):
        yield  iterable[ndx:min(ndx+bsize, l)]





def _walk(dic, path, default=None):
    the_path = path[:]
    if len(the_path) == 0 :
        return dic
    try :
        key = the_path.pop(0)
        if key.isdigit():
            key = int(key)
        return _walk(dic[key], the_path, default)
    except Exception as e:
        # pprint(e)
        # logger.error('parse entity dict erorr for path: %s'% path)
        return default


def walk(dic, path_str, default=None):
    the_path = path_str.split('.')
    return _walk(dic, the_path, default)

from entity_spider.core.models import Entity
from datetime import datetime
from hashlib import md5
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


def pick(source, keys, base=None):
    res = {}
    for key in keys:
        if key in source:
            res[key] = source[key]
    if not base is None:
        return base.update(res)
    return res