#!/usr/bin/python
# author: Adam D Scott (amviot@gmail.com)
# first created: 2015*09*28

#import requests
#import json
#from requests.auth import HTTPDigestAuth
#http://docs.python-requests.org/en/latest/user/authentication/?highlight=authentication

import requests
from requests.auth import HTTPDigestAuth
import json

class webAPI(object):
	'''webAPI class:
	   -functions like Python Requests.
	   -has:
		home = the home directory or index
		subset = the subset realm of the webful service
		action = the query, file upload, etc.
		response = the response from request submission'''
	urlType = ""
	def __init__(self,home,subset):
		self.home = home
		self.subset = subset
		self.action = ""
		self.response = ""
		self.headers = {}

	def setSubset(self,subset):
        self.subset = subset
        self.action = ""
    def resetURL(self):
        self.action = ""
        self.subset = ""

	def buildHeader(self):
		return json.dumps( self.headers )

	def buildURL(self):
		return self.home + self.subset + self.action

	def submit(self,**kwargs):
		doPost = kwargs.get("post",False)
		url = self.buildURL()
		print url
		header = self.buildHeader()
		if doPost:
			self.response = requests.post( url , headers = header )
		else:
			self.response = requests.get( url , headers = header )
		#print self.response
		return self.response
