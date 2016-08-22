#config for local
#=========================
# data_base_ip = '192.168.1.113'
# data_base_user = 'guoku'
# data_base_pass = 'guoku!@#'
#
# celery_eager = False
# celery_concurrency  = 30
# broker_url = 'redis://127.0.0.1:6379'
# redis_host = '127.0.0.1'
#
#
# image_host = 'http://127.0.0.1:9766/'
# image_path = 'images/'
# local_file =  True
#

#config for test.guoku.com
#=========================
# data_base_ip = '10.0.2.125'
# data_base_user = 'guoku'
# data_base_pass = 'guoku1@#'
#
# celery_eager = False
# celery_concurrency  = 10
# broker_url = 'redis://redis:6379'

# image_host = 'http://imgcdn.guoku.com/'
# image_path = 'images/'
# local_file = False
# redis_host = 'redis:6379'

#config for production
#=========================
data_base_ip = '10.0.2.90'
data_base_user = 'guoku'
data_base_pass = 'guoku!@#'

celery_eager = False
celery_concurrency  = 10
broker_url = 'redis://redis:6379'

image_host = 'http://imgcdn.guoku.com/'
image_path = 'images/'
local_file = False
redis_host = 'redis:6379'



tae_item_detail_url = 'http://guoku2.wx.jaeapp.com/gk_item_detail/'
IMAGE_HOST =image_host
IMAGE_PATH = image_path
LOCAL_IMAGE_PATH = image_path
LOCAL_FILE_STORAGE = local_file
MEDIA_ROOT = ''
MOGILEFS_DOMAIN = 'prod'
MOGILEFS_TRACKERS = ['10.0.2.50:7001']
MOGILEFS_MEDIA_URL = 'images/'
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o777
FILE_UPLOAD_PERMISSIONS = 0o777
MEDIA_URL = 'images/'
STATIC_URL = 'http://static.guoku.com/static/v4/dafb5059ae45f18b0eff711a38de3d59b95bad4c/'

DEFAULT_ARTICLE_COVER = 'http://imgcdn.guoku.com/images/ee7dd4a43d75ab28b3c65cc960429724.jpeg'