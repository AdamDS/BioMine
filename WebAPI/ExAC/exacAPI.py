#!/usr/bin/python
# author: Adam D Scott
# first created: 2016*1*11
#####
#	Operation					Function				Works With
#####
### Inherited
#	endpoint	"exac.broadinstitute.org"
#	subset		"/variant/"
#	action		

from WebAPI.webAPI import webAPI
import xml.etree.ElementTree as ET
import json
import AdvancedHTMLParser

class exacAPI(webAPI):
	endpoint = "http://exac.broadinstitute.org"
	variant = "/variant/"
	def __init__(self,**kwargs):
		subset = kwargs.get("subset",'')
		if not subset:
			super(exacAPI,self).__init__(exacAPI.endpoint,exacAPI.variant)
		else:
			if ( subset == exacAPI.variant ):
				super(exacAPI,self).__init__(exacAPI.endpoint,subset)
			else:
				print "ADSERROR: bad subset. webAPI.subset initializing to variant association results"
				super(exacAPI,self).__init__(exacAPI.endpoint,exacAPI.variant)

	def setSubset(self,subset):
		self.subset = subset
		self.action = ""
	def resetURL(self):
		self.action = ""
	def buildQuery( self , var ):
		self.action = '-'.join( [ var.chromosome , var.start , var.reference , var.mutant ] )

	def getPage( self , var ):
		self.buildQuery( var )
		self.submit()
		return self.parseHTMLResponse()
		
	def getAlleleFrequency( self , var ):
		page = self.getPage( var )
		if page:
			dl = page.getElementsByTagName( 'dl' )
			if dl:
				dt = dl.getElementsByTagName( 'dt' )
				if dt:
					j = 0
					for i in range( 0 , len( dt ) ):
						if dt[i].innerHTML == "Allele Frequency":
							j = i
					dd = dl.getElementsByTagName( 'dd' )
					if dd:
						alleleFrequency = dd[j].innerHTML
						return float(alleleFrequency)
		return
		print "ADS Error: could not get allele frequency from ExAC"
