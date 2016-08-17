# coding=utf-8
import  os
os.environ['DJANGO_SETTINGS_MODULE'] = 'entity_spider.config.database'

import time
import requests

from django.db import models
from django.utils.encoding import force_unicode
from django.utils import timezone

from copy import deepcopy
from json import dumps, loads
from django.utils.translation import ugettext_lazy as _

from entity_spider.core.managers import GKUserManager, EntityManager, SelectionEntityManager
from entity_spider.config.env import IMAGE_HOST
from entity_spider.core.image import HandleImage
from entity_spider.Client.taobao import TaobaoImageClient
def dbsafe_encode(value):
    _value = deepcopy(dumps(value))
    return ListObj(_value)

def dbsafe_decode(value):
    _value = deepcopy(loads(value))
    return _value


class ListObj(str):
    pass

class ListObjectField(models.Field):

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        # self.compress = kwargs.pop('compress', False)
        kwargs.setdefault('editable', False)
        super(ListObjectField, self).__init__(*args, **kwargs)

    def get_default(self):
        if self.has_default():
            if callable(self.default):
                return self.default()
            return self.default
        return super(ListObjectField, self).get_default()

    def to_python(self, value):
        if value is not None:
            try:
                value = dbsafe_decode(value)
            except:
                if isinstance(value, ListObj):
                    raise
        return value

    def get_db_prep_value(self, value, connection=None, prepared=False):
        if value is not None and not isinstance(value, ListObj):
            value = force_unicode(dbsafe_encode(value))
        return value

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def get_internal_type(self):
        return 'TextField'

    def get_db_prep_lookup(self, lookup_type, value, connection=None,
                           prepared=False):
        if lookup_type not in ['exact', 'in', 'isnull']:
            raise TypeError('Lookup type %s is not supported.' % lookup_type)
        try:
            return super(ListObjectField, self).get_db_prep_lookup(lookup_type, value, connection, prepared)
        except TypeError:
            return super(ListObjectField, self).get_db_prep_lookup(lookup_type, value, None)



class BaseModel(models.Model):
    class Meta:
        abstract = True

    def toDict(self):
        fields = []
        for f in self._meta.fields:
            fields.append(f.column)
        d = {}
        for attr in fields:
            # log.info( getattr(self, attr) )
            value = getattr(self, attr)
            if value is None:
                continue
            # log.info(value)
            d[attr] = "%s" % getattr(self, attr)
        # log.info(d)
        return d

    def pickToDict(self, *args):
        '''
          only work on simple python value fields ,
          can not use to serialize object field!
        '''
        d = {}
        for key in args:
            d[key] = getattr(self, key, None)
        return d

class GKUser(BaseModel):
    (remove, blocked, active, editor, writer) = (-1, 0, 1, 2, 3)
    USER_STATUS_CHOICES = [
        (writer, _("writer")),
        (editor, _("editor")),
        (active, _("active")),
        (blocked, _("blocked")),
        (remove, _("remove")),
    ]
    email = models.EmailField(max_length=255, unique=True)
    # is_active = models.BooleanField(_('active'), default=True)
    is_active = models.IntegerField(choices=USER_STATUS_CHOICES, default=active)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now())

    objects = GKUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Category(BaseModel):
    title = models.CharField(max_length=128, db_index=True)
    cover = models.CharField(max_length=255)
    status = models.BooleanField(default=True, db_index=True)


class Sub_Category(BaseModel):
    group = models.ForeignKey(Category, related_name='sub_categories')
    title = models.CharField(max_length=128, db_index=True)
    alias = models.CharField(max_length=128, db_index=True, default=None)
    icon = models.CharField(max_length=64, null=True, default=None)
    status = models.BooleanField(default=True, db_index=True)


class Entity(BaseModel):
    (remove, freeze, new, selection) = (-2, -1, 0, 1)
    ENTITY_STATUS_CHOICES = [
        (selection, _("selection")),
        (new, _("new")),
        (freeze, _("freeze")),
        (remove, _("remove")),
    ]

    NO_SELECTION_ENTITY_STATUS_CHOICES = [
        (new, _("new")),
        (freeze, _("freeze")),
        (remove, _("remove")),
    ]

    user = models.ForeignKey(GKUser, related_name='entities', null=True)
    entity_hash = models.CharField(max_length=32, unique=True, db_index=True)
    category = models.ForeignKey(Sub_Category, related_name='category',db_index=True)
    brand = models.CharField(max_length=256, default='')
    title = models.CharField(max_length=256, default='')
    intro = models.TextField(default='')
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=1.0)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0,
                                db_index=True)
    mark = models.IntegerField(default=0, db_index=True)
    images = ListObjectField()
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(auto_now=True, db_index=True)
    status = models.IntegerField(choices=ENTITY_STATUS_CHOICES, default=new, db_index=True)

    objects = EntityManager()

    def fetch_image(self):
        image_list = list()
        try:
            for image_url in self.images:
                if 'http' not in image_url:
                    image_url = 'http:' + image_url
                if IMAGE_HOST in image_url:
                    image_list.append(image_url)
                    continue
                r = TaobaoImageClient().get(image_url, timeout=15)
                # r = requests.get(image_url, stream=True,)
                image = HandleImage(r.raw)
                image_name = image.save()
                image_list.append("%s%s" % (IMAGE_HOST, image_name))

                self.images = image_list
                self.save()
        except Entity.DoesNotExist, e:
            pass
        except Exception as e :
            raise e



class Buy_Link(BaseModel):
    (remove, soldout, sale) = xrange(3)
    Buy_Link_STATUS_CHOICES = [
        (sale, _("sale")),
        (soldout, _("soldout")),
        (remove, _("remove")),
    ]
    entity = models.ForeignKey(Entity, related_name='buy_links')
    origin_id = models.CharField(max_length=100, db_index=True)
    origin_source = models.CharField(max_length=255)
    cid = models.CharField(max_length=255, null=True)
    link = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    foreign_price = models.DecimalField(max_digits=20, decimal_places=2,
                                        default=0)
    volume = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    default = models.BooleanField(default=False)
    shop_link = models.URLField(max_length=255, null=True)
    seller = models.CharField(max_length=255, null=True)
    status = models.PositiveIntegerField(default=sale,
                                         choices=Buy_Link_STATUS_CHOICES)

    last_update = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s%s'%(self.entity.title, self.entity.id)



class Selection_Entity(BaseModel):
    entity = models.OneToOneField(Entity, unique=True)
    is_published = models.BooleanField(default=False)
    pub_time = models.DateTimeField(db_index=True, editable=True)

    objects = SelectionEntityManager()

    class Meta:
        ordering = ['-pub_time']

    def __unicode__(self):
        return self.entity.title

    @property
    def publish_timestamp(self):
        return time.mktime(self.pub_time.timetuple())



class Shop(BaseModel):
    '''
    ONLY SUPPORT TAOBAO SHOP NOW !!!

    '''
    (other_style, dress, home, culture, sport, tec, food, mother, cosmetic, health) = range(10)
    SHOP_STYLE_CHOICES = [
        (other_style , '其他'),
        (dress,'服饰'),
        (home , '居家'),
        (culture, '文化'),
        (sport, '运动'),
        (tec, '科技'),
        (food,'美食'),
        (mother, '孕婴'),
        (cosmetic,'美容'),
        (health,'健康')
    ]

    (other, taobao, tmall, glbuy, tinter, jiyoujia) = range(6)
    SHOP_TYPE_CHOICES = [
        (other , '其他'),
        (taobao, '淘宝'),
        (tmall , '天猫'),
        (glbuy, '全球购'),
        (tinter, '天猫国际'),
    ]

    owner = models.ForeignKey(GKUser, related_name='shops')
    shop_title = models.CharField(max_length=255)
    shop_link = models.URLField(max_length=255)
    shop_style = models.IntegerField(choices=SHOP_STYLE_CHOICES, default=dress )
    shop_type = models.IntegerField(choices=SHOP_TYPE_CHOICES, default=taobao)
    tb_shop_id = models.CharField(max_length=64, null=True, blank=True)
    common_shop_link = models.URLField(max_length=255, null=True, blank=True)

    @property
    def tb_shop_link(self):
        return 'https://shop%s.taobao.com'%self.tb_shop_id


    class Meta:
        db_table = 'shop_shop'

    def __unicode__(self):
        return '%s:%s'%(self.owner, self.shop_title)


# class TBShopEntity(BaseModel):
#     tb_shop_id = models.CharField(max_length=64)
#     tb_number_iid = models.CharField(max_length=64)
#     entity_dic_json = models.TextField()
#     tb_cid = models.CharField(max_length=64)