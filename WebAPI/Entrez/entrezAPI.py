#!/usr/bin/python
# author: Adam D Scott
# first created: 2015*12*06
#####
#	Operation	Function						Returns
#	esearch		term queries					id(s)
#	esummary	id search						entry details
#	efetch		download file of id				file
#	elink		linked entries in db A & B		dictionary of query keys & entry value
#	epost		id search						dictionary of query keys & entry value
#####
# Test sites
# http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=Leu858Arg
# http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id=16609
# http://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=gene&db=protein&id=194680922,50978626,28558982,9507199,6678417&linkname=protein_gene&cmd=neighbor_history
### Inherited
#	endpoint	"http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
#	subset		"/esearch.fcgi"
#	action		"?db=pubmed&term=astma&usehistory=y"

#from restAPI import restAPI
#import xml.etree.ElementTree as ET
#import json
from ..restAPI import restAPI

class entrezAPI(restAPI):
	endpoint = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
	esearch = "esearch.fcgi"
	esummary = "esummary.fcgi"
	elink = "elink.fcgi"
	epost = "epost.fcgi"
	efetch = "efetch.fcgi"
	pubmed = "pubmed"
	clinvar = "clinvar"
	protein = "protein"
	gene = "gene"
	def __init__(self,**kwargs):
		subset = kwargs.get("subset",'')
		if not subset:
			super(entrezAPI,self).__init__(entrezAPI.endpoint,entrezAPI.esearch)
		else:
			if ( subset == entrezAPI.esearch or subset == entrezAPI.esummary or
				 subset == entrezAPI.elink or subset == entrezAPI.epost or 
				 subset == entrezAPI.efetch ):
				super(entrezAPI,self).__init__(entrezAPI.endpoint,subset)
			else:
				print "ADSERROR: bad subset. restAPI.subset initializing to variant association results"
				super(entrezAPI,self).__init__(entrezAPI.endpoint,entrezAPI.hgvs)
		self.database = kwargs.get("database",entrezAPI.clinvar)
		self.queries = []
		self.uids = []
		#self.linkname = ""
		#self.databaseFrom = ""
		#self.command = ""
		#self.query_key = ""
		#self.web_env = ""

	def addQuery( self , field , term ):
		self.queries.append( term + "[" + field + "]" )
	def addID( self , uid ):
		self.uids.append( uid )
	
	def resetQuery( self ):
		self.queries = []
	def resetID( self ):
		self.uids = []

	def buildSearchAction( self , query ):
		self.query = ','.join( query )
		return '&'.join( [ self.database , self.query ] )
	
	def buildSummaryAction( self , ids ):
		self.uid = ','.join( ids )
		return '&'.join( [ self.database , self.uid ] )

	def searchPubMed( self , query , **kwargs ):
		self.subset = entrezAPI.esearch
		self.database = entrezAPI.pubmed
		self.action = entrezAPI.buildSearchAction( query )
		return self.submit( )
	def searchClinVar( self , query , **kwargs ):
		self.subset = entrezAPI.esearch
		self.database = entrezAPI.clinvar
		self.action = entrezAPI.buildSearchAction( query )
		return self.submit( )
	
	def getClinicalSignificance( self , queries ):
		self.subset = entrezAPI.esummary
		#search ClinVar
		self.database = entrezAPI.clinvar
		query = buildSearchAction( queries )
		self.submit() 
		print self.response.text
		#parse the Id field within IdList
		ids = []
		root = ET.fromString( self.response.text )
		for thisID in root.iter( 'Id' ):
			ids.append( ids )
		#string ids together to search esummary
		searchIDs = ','.join( ids )
		print searchIDs
		#parse each DocumentSummary for clinical_significance
		#parse clinical_signficance for description
