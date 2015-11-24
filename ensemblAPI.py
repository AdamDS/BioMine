#!/usr/bin/python
# author: Adam D Scott
# first created: 2015*11*23
#####
#	Operation					Function				Works With
#####
### Inherited
#	endpoint	"http://rest.ensembl.org"
#	subset		"/vep/human/hgvs/"
#	action		

from restAPI import restAPI

class ensemblAPI(restAPI):
	endpoint = "http://grch37.rest.ensembl.org"
	species = "human"
	hgvs = "/vep/" + species + "/hgvs/"
	translation = "/map/translation/"
	def __init__(self,**kwargs):
		subset = kwargs.get("subset",'')
		if not subset:
			super(ensemblAPI,self).__init__(ensemblAPI.endpoint,ensemblAPI.hgvs)
		else:
			if ( subset == ensemblAPI.hgvs or subset == ensemblAPI.translation ):
				super(ensemblAPI,self).__init__(ensemblAPI.endpoint,subset)
			else:
				print "ADSERROR: bad subset. restAPI.subset initializing to variant association results"
				super(ensemblAPI,self).__init__(ensemblAPI.endpoint,ensemblAPI.hgvs)

	def setSubset(self,subset):
		self.subset = subset
		self.action = ""
	def resetURL(self):
		self.action = ""

	def beginQuery(self):
		self.action = ""

	def useGRCh38(self):
		ensemblAPI.endpoint = "http://rest.ensembl.org"

	def useGRCh37(self):
		ensemblAPI.endpoint = "http://grch37.rest.ensembl.org"

	def searchVariant(self,variant):
		self.action = variant + "?"

	def searchProteinAnnotations( self , variants ):
		for transcript , proteinAnno in variants:
			self.beginQuery();
			self.searchVariant( transcript + ":" + proteinAnno );
			print self.buildURL();
