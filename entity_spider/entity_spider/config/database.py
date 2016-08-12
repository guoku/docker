from entity_spider.config.env import *

SECRET_KEY  = 'zl4j09adh-*tv7-b5&(zu!nkudhry*yy1b9--$%)&yh^4caq_7'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'core',
        'USER': data_base_user,
        'PASSWORD': data_base_pass,
        'HOST': data_base_ip,
        'PORT': '',
        'OPTIONS': {
            'use_unicode':'utf-8mb4',
            'init_command':'SET storage_engine=INNODB',
        }
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'core',
        'USER': data_base_user,
        'PASSWORD': data_base_pass,
        'HOST': data_base_ip,
        'PORT': '',
        'OPTIONS': {
            'use_unicode':'utf-8mb4',
            'init_command':'SET storage_engine=INNODB',
        }
    },
}
