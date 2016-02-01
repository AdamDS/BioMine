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

import time
from WebAPI.webAPI import webAPI
import xml.etree.ElementTree as ET
import json
import AdvancedHTMLParser
import WebAPI.Variant.variant

class exacAPI(webAPI):
	endpoint = "http://exac.broadinstitute.org/"
	endpoint_harvard = "http://exac.hms.harvard.edu/rest/"
	variant = "variant/"
	gene = "gene/"
	def __init__(self,**kwargs):
		harvard = kwargs.get( "harvard" , False )
		useEndpoint = exacAPI.endpoint
		if harvard:
			useEndpoint = exacAPI.endpoint_harvard
		subset = kwargs.get("subset",'')
		if not subset:
			super(exacAPI,self).__init__(useEndpoint,exacAPI.variant)
		else:
			if ( subset == exacAPI.variant ):
				super(exacAPI,self).__init__(useEndpoint,subset)
			else:
				print "ADSERROR: bad subset. webAPI.subset initializing to variant association results"
				super(exacAPI,self).__init__(useEndpoint,exacAPI.variant)

	def setSubset(self,subset):
		self.subset = subset
		self.action = ""
	def resetURL(self):
		self.action = ""
	def buildQuery( self , query ):
		if self.subset == exacAPI.variant:
			self.action = self.buildVariant( query )
		else:
			self.action = query
	def buildVariant( self , var ):
		if var.reference == "-" or not var.reference:
			return '-'.join( [ var.chromosome , var.start , "" , var.alternate ] )
		if var.alternate == "-" or not var.alternate:
			return '-'.join( [ var.chromosome , var.start , var.reference , "" ] )
		else:
			return '-'.join( [ var.chromosome , var.start , var.reference , var.alternate ] )

	def getPage( self , var ):
		self.buildQuery( var )
		self.submit()
		return self.parseHTMLResponse()
	
	def getAlleleFrequencies( self , variants ):
		entries = {}
		for var in variants:
#			t = time.time()
			entries[var.genomicVar()] = self.getAlleleFrequency( var )
#			self.printRunTime( "getAlleleFrequency " + var.genomicVar() , self.runTime( t ) )
			#time.sleep(1)
		return entries
	def getAlleleFrequency( self , var ):
		alleleFrequency = None
		if self.endpoint == exacAPI.endpoint:
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
		else:
			self.buildQuery( var )
#			print self.buildURL()
#			t = time.time()
			self.submit( session=True )
#			self.printRunTime( "\tsubmit " + self.buildURL() , self.runTime( t ) )
			try:
#				t = time.time()
				page = json.loads( self.response.text )
#				self.printRunTime( "\t\tjson.loads " , self.runTime( t ) )
				variantInfo = page['variant']
				alleleFrequency = variantInfo.get( 'allele_freq' )
			except:
				print "CharGer Warning: could not extract allele frequency " ,
				print "from ExAC for " + var.genomicVar() + ""
		return alleleFrequency
		print "ADS Error: could not get allele frequency from ExAC"
