'''
Created by auto_sdk on 2015.03.26
'''
from top.api.base import RestApi
class OpensecurityUidChangeRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.open_uid_isv = None

	def getapiname(self):
		return 'taobao.opensecurity.uid.change'
