'''
Created by auto_sdk on 2016.05.19
'''
from top.api.base import RestApi
class BaichuanMicroserviceIteminfoRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.extra = None
		self.item_id = None
		self.item_url = None
		self.trace_app_key = None
		self.tracer = None

	def getapiname(self):
		return 'taobao.baichuan.microservice.iteminfo'
