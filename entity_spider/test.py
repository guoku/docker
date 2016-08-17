from __future__ import absolute_import
import os
import  entity_spider.config as config

os.environ['DJANGO_SETTINGS_MODULE'] = 'entity_spider.config.database'

from entity_spider.core.models import Entity

entities_count = Entity.objects.all().count()
print entities_count

