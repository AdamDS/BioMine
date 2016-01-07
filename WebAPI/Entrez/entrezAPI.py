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

import xml.etree.ElementTree as ET
from WebAPI.restAPI import restAPI

class entrezAPI(restAPI):
	endpoint = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
	esearch = "esearch.fcgi?"
	esummary = "esummary.fcgi?"
	elink = "elink.fcgi?"
	epost = "epost.fcgi?"
	efetch = "efetch.fcgi?"
	pubmed = "pubmed"
	clinvar = "clinvar"
	protein = "protein"
	gene = "gene"
	defaultGroup = "grabBag"
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
		self.queries = { entrezAPI.defaultGroup : "" }
		self.uids = []
		#self.linkname = ""
		#self.databaseFrom = ""
		#self.command = ""
		self.query_key = ""
		self.web_env = ""
		self.retmax = ""
		self.retstart = ""
		self.rettype = ""
		self.retmode = ""
		self.usehistory = ""

	def addQuery( self , term , **kwargs ):
		field = kwargs.get( "field" , "" )
		group = kwargs.get( "group" , entrezAPI.defaultGroup )
		query = ""
		#print "Adding query: " + term + " " + field + " " + group , 
		if group in self.queries: #the group already has a query going
			#print "\tGroup=" + group + " exists!"
			if group != entrezAPI.defaultGroup: #not the default group
				#print "\t\tCurrent query is=" + self.queries[group]
				query = self.queries[group] + "+AND+"
			else: #anything goes in the default group
				#print "\t\tCurrent query is=" + self.queries[group]
				query = self.queries[group] + "+OR+"
		#print "\tcurrrent query is: " + query + "."
		query += term
		if field:
			query += "[" + field + "]"
		#print "\tNew query for group=" + group + " is: " + query
		tempq = { group : query }
		self.queries.update( tempq )
	def buildQuery( self ):
		query = ""
		for group in self.queries:
			if self.queries[group]:
				query += "(" + self.queries[group] + ")+OR+"
		return query
	def addID( self , uid ):
		self.uids.append( uid )
	
	def resetQuery( self ):
		self.queries = {}
	def resetID( self ):
		self.uids = []

	def buildSearchAction( self ):
		query = self.buildQuery()
		self.action = '&'.join( [ "db=" + self.database , "term=" + query ] )
		self.actionReturnParameters( )
		return self.action
	def buildWebEnvAction( self ):
		self.action = '&'.join( [ "db=" + self.database , "WebEnv=" + self.web_env , 
		"query_key=" + self.query_key ] )
		self.usehistory = ""
		self.actionReturnParameters( )
		return self.action
	def buildSummaryAction( self , ids ):
		self.uid = ','.join( ids )
		self.action = '&'.join( [ self.database , self.uid ] )
		return self.action
	def actionReturnParameters( self ):
		if self.rettype:
			self.action += "&rettype=" + self.rettype
		if self.retmode:
			self.action += "&retmode=" + self.retmode
		if self.retstart:
			self.action += "&retstart=" + self.retstart
		if self.retmax:
			self.action += "&retmax=" + self.retmax
		if self.usehistory:
			self.action += "&usehistory=" + self.usehistory
		return self.action
	
	def doBatch( self , batchSize ):
		self.usehistory = "y"
		action = self.buildSearchAction( )
		print action
		url = self.buildURL()
		response = self.submit()
		root = ET.fromstring( self.response.text )
		for webenv_generator in root.iter( "WebEnv" ):
			self.web_env = webenv_generator.text
 		for querykey_generator in root.iter( "QueryKey" ):
			self.query_key = querykey_generator.text
		count_generator = root.findall( './eSearchResult/Count' )
		self.retmax = count_generator[0].text
		print "WebEnv = " + self.web_env
		print "QueryKey = " + self.query_key
		print "Return max = " + self.retmax
		print "Batch size = " + batchSize
		self.subset = entrezAPI.esummary
		self.action = self.buildWebEnvAction()
		self.buildURL()
		summaryResponse = self.submit()

		self.subset = entrezAPI.efetch
		for returnIndexStart in range( 0 , batchSize , self.retmax ):
			self.buildWebEnvAction( )
			self.buildURL()
			batchResponse = self.submit() #list of Id's (IDList/ID/)

	def searchPubMed( self , query ):
		self.subset = entrezAPI.esearch
		self.database = entrezAPI.pubmed
		self.action = self.buildSearchAction( query )
		print self.subset
		print self.database
		print self.action
		return self.submit( )
	def searchClinVar( self , query , **kwargs ):
		self.subset = entrezAPI.esearch
		self.database = entrezAPI.clinvar
		self.action = self.buildSearchAction( query )
		print self.subset
		print self.database
		print self.action
		return self.submit( )
	
	def getClinicalSignificance( self , queries ):
		self.subset = entrezAPI.esearch
		#search ClinVar
		self.database = entrezAPI.clinvar
		query = self.buildSearchAction( queries )
		self.submit() 
		print self.response.text
		#parse the Id field within IdList
		ids = []
		root = ET.fromstring( self.response.text )
		for thisID in root.iter( 'Id' ):
			print thisID
			ids.append( thisID )
		#string ids together to search esummary
		searchIDs = ','.join( ids )
		print searchIDs
		#parse each DocumentSummary for clinical_significance
		#parse clinical_signficance for description
