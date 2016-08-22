'''
Created by auto_sdk on 2016.04.20
'''
from top.api.base import RestApi
class UserGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.nick = None
		self.top_mix_params = None

	def getapiname(self):
		return 'taobao.user.get'
