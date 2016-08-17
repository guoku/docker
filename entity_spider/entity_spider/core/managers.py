from django.db import models
from django.db.models import Q
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.contrib.auth.models import Group, GroupManager


import random

from django.db.models import Count
from django.utils.log import getLogger
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

class GKUserQuerySet(models.query.QuerySet):
    def author(self):
        return self.filter(is_active__gte = 2)

    def writer(self):
        return self.filter(is_active=3)

    def editor(self):
        return self.filter(is_active=2)

    def editor_or_admin(self):
        return self.filter(Q(is_admin=1)| Q(is_active=2))

    def active(self):
        return self.filter(is_active=1)

    def visible(self):
        return self.filter(is_active__gte=0)

    def blocked(self):
        return self.filter(is_active=0)

    def deactive(self):
        return self.filter(is_active=-1)

    def admin(self):
        return self.filter(is_admin=True)

    def authorized_author(self):
        return Group.objects.get(name='Author').user_set.all()

    def authorized_seller(self):
        return Group.objects.get(name='Seller').user_set.all()

    def authorized_user(self):
        return self.filter(groups__name__in=['Author', 'Seller']).distinct()

    def recommended_user(self):
        return self.authorized_user()\
                   .select_related('authorized_profile')\
                   .filter(authorized_profile__is_recommended_user=True)\
                   .order_by('-authorized_profile__points')


class GKUserManager(BaseUserManager):
    # use_for_related_fields = True

    def get_queryset(self):
        return GKUserQuerySet(self.model, using = self._db)

    def author(self):
        return self.get_queryset().author()

    def writer(self):
        return self.get_queryset().writer()

    def editor(self):
        return self.get_query_set().editor()

    def active(self):
        return self.get_query_set().active()

    def visible(self):
        return self.get_queryset().visible()

    def blocked(self):
        return self.get_query_set().blocked()

    def deactive(self):
        return self.get_query_set().deactive()

    def authorized_author(self):
        return self.get_queryset().authorized_author()

    def authorized_seller(self):
        return self.get_queryset().authorized_seller()

    def authorized_user(self):
        return self.get_queryset().authorized_user()

    def recommended_user(self):
        return self.get_queryset().recommended_user()

    def deactive_user_list(self):
        user_list = cache.get('deactive_user_list')
        if user_list:
            return user_list

        user_list = self.get_query_set().deactive().values_list('id', flat=True)
        cache.set('deactive_user_list', user_list, timeout=86400)
        return user_list


    def admin(self):
        return self.get_query_set().admin()

    def editor_or_admin(self):
        return self.get_query_set().editor_or_admin()

    def _create_user(self, email, password, is_active, is_admin, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError(_('please given email'))

        user = self.model(email=email, is_active=is_active, is_admin=is_admin, date_joined=now)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, is_active=1, **extra_fields):
        is_admin = extra_fields.pop("is_admin", False)
        return self._create_user(email, password, is_active, is_admin, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)




log = getLogger('django')


class EntityQuerySet(models.query.QuerySet):
    def selection(self):
        return self.filter(status=1)

    def new(self):
        return self.filter(status=0)

    def active(self):
        return self.using('slave').filter(status__gte=-1)

    def new_or_selection(self, category_id):

        if isinstance(category_id, list):
            return self.using('slave').filter(category_id__in=category_id,\
                                              status__gte=0)

        elif isinstance(category_id, int) or isinstance(category_id ,str) or isinstance(category_id , long):
            return self.using('slave').filter(category_id=category_id,\
                                              status__gte=0)
        else:
            #unicode
            try :
                category_id = int(category_id)
                return self.using('slave').filter(category_id=category_id,\
                                              status__gte=0)
            except Exception as e:
                pass

            return self.using('slave').filter(status__gte=0)


    def sort(self, category_id, like=False):
        _refresh_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if like:
            return self.new_or_selection(category_id).filter(
                selection_entity__pub_time__lte=_refresh_datetime,
                buy_links__status=2)
        else:
            return self.new_or_selection(category_id).filter(
                selection_entity__pub_time__lte=_refresh_datetime,
                buy_links__status=2).distinct() \
                .order_by('-selection_entity__pub_time')


            # self.using('slave').filter(status=Entity.selection, selection_entity__pub_time__lte=_refresh_datetime, category=category_id)\
            # .order_by('-selection_entity__pub_time').filter(buy_links__status=2)
            # def get(self, *args, **kwargs):
            # # print kwargs, args
            # return super(EntityQuerySet, self).get(*args, **kwargs)

    def sort_group(self, gid, category_ids, like=False):
        _refresh_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        like_key = 'entity:list:sort:like:%s' % hash(gid)

        if like:

            like_list = self.new_or_selection(category_ids).filter(
                    selection_entity__pub_time__lte=_refresh_datetime,
                    buy_links__status=2)

            # cache.set(like_key, like_list, timeout=3600*24)
            return like_list

        else:
            return self.new_or_selection(category_ids).filter(
                selection_entity__pub_time__lte=_refresh_datetime,
                buy_links__status=2)\
                .order_by('-selection_entity__pub_time')


class EntityManager(models.Manager):
    # entity status: new:0,selection:1
    # get the current seller's selection entities and order by created-time.
    def get_published_by_seller(self,seller):
        return self.get_query_set().using('slave').filter(status=1, user=seller).order_by('-created_time')

    def get_user_added_entities(self, seller):
        return self.get_read_queryset().filter(status__gte=-1, user=seller).order_by('-created_time')

    def get_read_queryset(self):
        return EntityQuerySet(self.model).using('slave')

    def get_query_set(self):
        return EntityQuerySet(self.model, using=self._db)

    # def get(self, *args, **kwargs):
    # # print  kwargs
    #
    # entity_hash = kwargs['entity_hash']
    # key = 'entity:%s' % entity_hash
    # # print key
    # res = cache.get(key)
    # if res:
    #         print "hit cache", type(res)
    #         return res
    #     else:
    #         print "miss cache"
    #         res = self.get_query_set().get(*args, **kwargs)
    #         # key = 'entity:%s' % entity_hash
    #         cache.set(key, res, timeout=86400)
    #         return res
    def active(self):
        return self.get_queryset().active()

    def selection(self):
        return self.get_query_set().selection()

    def new(self):
        return self.get_query_set().new()

    def new_or_selection(self, category_id=None):
        return self.get_query_set().new_or_selection(category_id)

    def sort(self, category_id, like=False):
        assert category_id is not None
        return self.get_query_set().sort(category_id, like)

    def sort_group(self, gid, category_ids, like=False):
        assert category_ids is not None
        return self.get_query_set().sort_group(gid, category_ids, like)

    def guess(self, category_id=None, count=5, exclude_id=None):
        size = count * 10
        if exclude_id:
            entity_list = self.new_or_selection(
                category_id=category_id).exclude(pk=exclude_id).filter(
                buy_links__status=2)
        else:
            entity_list = self.new_or_selection(
                category_id=category_id).filter(buy_links__status=2)
        try:
            entities = random.sample(entity_list[:size], count)
        except ValueError:
            entities = entity_list[:count]
        return entities


class SelectionEntityQuerySet(models.query.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def pending(self):
        return self.filter(is_published=False).exclude(\
            entity__status__lt=1,\
            entity__buy_links__status__in=(0, 1))

    def pending_and_removed(self):
        return self.filter(is_published=False,\
                           entity__buy_links__status__in=(0, 1),\
                           entity__status__lt=1)


class SelectionEntityManager(models.Manager):
    def get_queryset(self):
        return SelectionEntityQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def published_until(self, refresh_time=datetime.now()):
        return self.published().filter(pub_time__lte=refresh_time)

    def published_until_now(self, util_time=None):
        if util_time is None:
            util_time = datetime.now()
        return self.published().filter(pub_time__lte=util_time)

    def pending(self):
        return self.get_queryset().pending()

    def pending_and_removed(self):
        return self.get_queryset().pending_and_removed()

    def set_user_refresh_datetime(self, session, refresh_datetime=datetime.now()):
        log.info(refresh_datetime)
        # _key = "%s_selection" % session
        cache.set(session, refresh_datetime, timeout=8640000)

    def get_user_unread(self, session):
        # _key = "%s_selection" % session
        refresh_datetime = cache.get(session)
        log.info(refresh_datetime)
        if refresh_datetime is None:
            return 0

        unread_count = self.published().filter(
            pub_time__range=(refresh_datetime, datetime.now())).count()
        # log.debug(unread_count.query)
        return unread_count

    def category_sort_like(self, category_ids):
        # return self.get_queryset().published().filter(entity__category__in=category_ids).annotate(lnumber=Count('entity__likes')).order_by('-lnumber')
        res = self.published().filter(
            entity__category__in=category_ids).annotate(
            lnumber=Count('entity__likes')).order_by('-lnumber')
        # print res.query
        return res
