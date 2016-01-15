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
from WebAPI.webAPI import webAPI
from variant import variant
from variant import MAFVariant
from variant import clinvarVariant
import re

class entrezAPI(webAPI):
	endpoint = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
	esearch = "esearch.fcgi?"
	esummary = "esummary.fcgi?"
	elink = "elink.fcgi?"
	epost = "epost.fcgi?"
	efetch = "efetch.fcgi?"
	pubmed = "PubMed"
	clinvar = "ClinVar"
	protein = "Protein"
	gene = "Gene"
	dbsnp = "dbSNP"
	dbvar = "dbVar"
	omim = "OMIM"
	defaultGroup = "grabBag"
	largestBatchSize = 500
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
		self.assembly = "GRCh37"

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
	def prepQuery( self , userVariants ): #expects a list of variants
		for var in userVariants:
			thisGroup = var.uniqueVar()
			self.addQuery( var.gene , field="gene" , group=thisGroup )
			self.addQuery( var.chromosome , field="chr" , group=thisGroup )
			self.addQuery( var.start + ":" + var.stop , field="chrpos37" , group=thisGroup )
			self.addQuery( "human" , field="orgn" , group=thisGroup )
			#self.addQuery( var.variantClass , "vartype" )
			#self.addQuery( var.referencePeptide + var.positionPeptide + var.alternatePeptide , "Variant name" )
			#var.referencePeptide , var.positionPeptide , var.alternatePeptide
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
		self.action = "db=" + self.database + "&id=" + self.uid
		return self.action
	def actionReturnParameters( self ):
		if self.rettype:
			self.action += "&rettype=" + self.rettype
		if self.retmode:
			self.action += "&retmode=" + self.retmode
		if self.retstart:
			self.action += "&retstart=" + str(self.retstart)
		if self.retmax:
			self.action += "&retmax=" + str(self.retmax)
		if self.usehistory:
			self.action += "&usehistory=" + self.usehistory
		return self.action
	def setRetmax( self , total ):
		if total > entrezAPI.largestBatchSize:
			self.retmax = entrezAPI.largestBatchSize
		else:
			self.retmax = total
	
	def doBatch( self , batchSize ):
		self.usehistory = "y"
		action = self.buildSearchAction( )
		url = self.buildURL()
		response = self.submit()
		root = self.getXMLroot()
		self.web_env = self.getEntry( root , 'WebEnv' )
		self.query_key = self.getEntry( root , 'QueryKey' )
		totalRecords = 0
		totalRecords = self.getEntry( root , 'Count' )
		self.setRetmax( totalRecords )
		self.subset = entrezAPI.esummary
		self.action = self.buildWebEnvAction()
		self.buildURL()
		summaryResponse = self.submit()
		return self.getClinVarEntry()
	
	def getEntry( self , generator , text ):
		for entrygen in generator.iter( text ):
			return entrygen.text

	def parseClinVarTitle( self , DocumentSummary ):
		title = self.getEntry( DocumentSummary , 'title' )
		lhs = title.split( '(' )
		refseqID = lhs[0]
		hgvsp = lhs[-1].rstrip( ')' )
		var = MAFVariant()
		refmut = var.splitHGVSp( hgvsp )
		ref = refmut["referencePeptide"]
		pos = refmut["positionPeptide"]
		alt = refmut["alternatePeptide"]
		return { "title" : title , \
		"referencePeptide" : ref , \
		"positionPeptide" : pos , \
		"alternatePeptide" : alt }

	def getClinVarEntry( self ):
		print "\tgetClinVarVariantEntry"
		root = self.getXMLroot()
		variants = {}
		for DocumentSummary in root.iter( 'DocumentSummary' ):
			uid = DocumentSummary.attrib["uid"]
			var = clinvarVariant( uid=uid )
			self.getClinVarVariantEntry( var , DocumentSummary )
			self.getClinVarTraitEntry( var , DocumentSummary )
			self.getClinVarClinicalEntry( var , DocumentSummary )
			try:
				variants[var.genomicVar()] = var
			except:
				variants["null"] = var
		return variants
	def getClinVarVariantEntry( self , var , DocumentSummary ):
		print "\tgetClinVarVariantEntry"
		titleDetails = self.parseClinVarTitle( DocumentSummary )
		var.referencePeptide = titleDetails["referencePeptide"]
		var.positionPeptide = titleDetails["positionPeptide"]
		var.alternatePeptide = titleDetails["alternatePeptide"]
		for variation in DocumentSummary.iter( 'variation' ):
			for variation_xref in DocumentSummary.iter( 'variation_xref' ):
				dbs = self.getEntry( variation_xref , 'db_source' )
				if dbs == entrezAPI.dbsnp:
					var.dbSNP = self.getEntry( variation_xref , 'db_id' )
					#print "dbSNP rs" + var.dbSNP
				#if dbs == entrezAPI.omim:
					#var.omim = self.getEntry( variation_xref , 'db_id' )
					#print "OMIM " + var.omim
			for assembly_set in variation.iter( 'assembly_set' ):
				assembly_name = self.getEntry( assembly_set , 'assembly_name' )
				if assembly_name == self.assembly:
					var.chromosome = assembly_set.find( 'chr' ).text
					var.start = assembly_set.find( 'start' ).text
					var.stop = assembly_set.find( 'stop' ).text
					var.alternate = assembly_set.find( 'alt' ).text
					var.reference = assembly_set.find( 'ref' ).text
					#assembly_acc_ver = assembly_set.find( 'assembly_acc_ver' )
		for gene in DocumentSummary.iter( 'gene' ):
			var.gene = self.getEntry( gene , 'symbol' )
			var.strand = self.getEntry( gene , 'strand' )
	def getClinVarTraitEntry( self , var , DocumentSummary ):
		print "\tgetClinVarTraitEntry"
		for trait in DocumentSummary.iter( 'trait' ):
			trait_name = self.getEntry( trait , 'trait_name' )
			trait_xrefs = {}
			var.trait = { trait_name : trait_xrefs }
			for trait_xref in trait.iter( 'trait_xref' ):
				db_source = self.getEntry( trait_xref , 'db_source' )
				db_id = self.getEntry( trait_xref , 'db_id' )
				txr = {}
				if trait_name in trait_xrefs:
					txr = trait_xrefs[trait_name]
				txr.update( { db_source : db_id } )
				trait_xrefs.update( { trait_name : txr } )
				var.trait.update( { trait_name : trait_xrefs } )
	def getClinVarClinicalEntry( self , var , DocumentSummary ):
		print "\tgetClinVarClinicalEntry"
		for clinical_significance in DocumentSummary.iter( 'clinical_significance' ):
			var.clinical["description"] = self.getEntry( clinical_significance , 'description' ).strip()
			var.clinical["review_status"] = self.getEntry( clinical_significance , 'review_status' ).strip()

	def searchPubMed( self , query ):
		self.subset = entrezAPI.esearch
		self.database = entrezAPI.pubmed
		self.action = self.buildSearchAction( query )
		#print self.subset
		#print self.database
		#print self.action
		return self.submit( )
	def searchClinVar( self , query , **kwargs ):
		self.subset = entrezAPI.esearch
		self.database = entrezAPI.clinvar
		self.action = self.buildSearchAction( query )
		#print self.subset
		#print self.database
		#print self.action
		return self.submit( )
	
	def getSNPGlobalMAF( self , rs ):
		self.addQuery( rs )
		self.subset = entrezAPI.esummary
		self.submit()
		root = self.getXMLroot()
		entries = {}
		for DocSum in root.iter( 'DocSum' ):
			print ""
	
	def getXMLroot( self ):
		#print self.response.text
		return ET.fromstring( self.response.text )
