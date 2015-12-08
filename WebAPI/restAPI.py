#!/usr/bin/python
# author: Adam D Scott (amviot@gmail.com)
# first created: 2015*09*28

#import requests
#import json
#from requests.auth import HTTPDigestAuth
#http://docs.python-requests.org/en/latest/user/authentication/?highlight=authentication
#CGT API section 2.3,
#"The API uses a process called Digest Authentication as a security
# measure to verify user requests submitted to the database."

import requests
from requests.auth import HTTPDigestAuth
import json

class restAPI(object):
	'''REST API class, has 
		endpoint = the endpoint
		subset = the subset realm of the RESTful service
		action = the query, file upload, etc.'''
	def __init__(self,endpoint,subset):
		self.response = None
		self.endpoint = endpoint
		self.subset = subset
		self.action = ""
		self.headers = {}
		self.data = {}

	def setSubset(self,subset):
		self.subset = subset
		self.action = ""
	def resetURL(self):
		self.action = ""

	def beginQuery(self):
		self.action = ""

	def queryAll(self):
		return self.site + "?query=NOT%20asdf"

	def partial(self,term,value):
		self.action += term + ":" + str(value)
	def addPartial(self,condition,term,value):
		self.action += "%20" + condition + "%20" + term + ":" + str(value)

	def exact(self,term,value):
		self.action += term + "=" + str(value)
	def addExact(self,condition,term,value):
		self.action += "%20" + condition + "%20" + term + "=" + str(value)

	def multiOr(self,term,values):
		values = map(str,values)
		stripped = [ v.strip() for v in values ]
		self.action += term + ":OR(" + ','.join(stripped) + ")"
	def addMultiOr(self,condition,term,values):
		values = map(str,values)
		stripped = [ v.strip() for v in values ]
		self.action += "%20" + condition + "%20" + term + ":OR(" + ','.join(stripped) + ")"

	def buildURL(self):
		return self.endpoint + self.subset + self.action

	def buildURLJSON(self):
		return self.endpoint + self.subset + self.action + "&_type=json"

	def addData( self , field , value ):
		self.data[field] = value
	def buildData( self ):
		json.dumps( self.data )
		return self.data

	def addHeader( self , field , value ):
		self.headers[field] = value
	def buildHeader( self ):
		return json.dumps( self.headers )

	def submit(self,**kwargs):
		contentHeaders = kwargs.get("content",'')
		dataIn = kwargs.get("data",'')
		doPost = kwargs.get("post",False)
		if contentHeaders:
			self.addHeader( "Content-Type" , contentHeaders )
		url = self.buildURL()
		headers = self.buildHeader()
		data = self.buildData()
		print url
		if self.headers:
			if self.data:
				if doPost:
					self.response = requests.post( url , headers = headers , data = data )
				else:
					self.response = requests.get( url , headers = headers , data = data )
			else:
				if doPost:
					self.response = requests.post( url , headers = headers )
				else:
					self.response = requests.get( url , headers = headers )
		else:
			if self.data:
				self.buildData()
				if doPost:
					self.response = requests.post( url , data = data )
				else:
					self.response = requests.get( url , data = data )
			else:
				if doPost:
					self.response = requests.post( url )
				else:
					self.response = requests.get( url )
		#print self.response
		return self.response

	def submitDigest(self,username,password):
		url = self.buildURL()
		self.response = requests.get( url , auth=HTTPDigestAuth( username , password ) )
		return self.response

	def submitJSON(self):
		url = self.buildURL()
		self.submit( content = "application/json")

	def submitXML(self):
		url = self.buildURL()
		self.submit( content = "text/xml")