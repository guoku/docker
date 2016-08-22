'''
Created by auto_sdk on 2016.04.07
'''
from top.api.base import RestApi
class BaichuanItemFilterRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.item_filter_request = None

	def getapiname(self):
		return 'taobao.baichuan.item.filter'
