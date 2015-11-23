#!/usr/bin/python
# author: Adam D Scott
# first created: 2015*11*23
#####
#	Operation					Function				Works With
#####
### Inherited
#	endpoint	"http://rest.ensembl.org"
#	subset		"/vep/human/hgvs/"
#	action		query=

from restAPI import restAPI

class vepAPI(restAPI):
	endpoint = "http://rest.ensembl.org"
	species = "human"
	hgvs = "/vep/" + species + "/hgvs/"
	def __init__(self,**kwargs):
		subset = kwargs.get("subset",'')
		if not subset:
			super(vepAPI,self).__init__(vepAPI.endpoint,vepAPI.hgvs)
		else:
			if ( subset == vepAPI.hgvs or subset == vepAPI.variantID ):
				super(vepAPI,self).__init__(vepAPI.endpoint,subset)
			else:
				print "ADSERROR: bad subset. restAPI.subset initializing to variant association results"
				super(vepAPI,self).__init__(vepAPI.endpoint,vepAPI.hgvs)

	def setSubset(self,subset):
		self.subset = subset
		self.action = ""
	def resetURL(self):
		self.action = ""

	def beginQuery(self):
		self.action = ""
	def search(self,variant):
		self.action = variant + "?"
