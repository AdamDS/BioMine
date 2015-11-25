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
import xml.etree.ElementTree as ET
import json

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
	def useGRCh38(self):
		ensemblAPI.endpoint = "http://rest.ensembl.org"
	def useGRCh37(self):
		ensemblAPI.endpoint = "http://grch37.rest.ensembl.org"

	def setSubset(self,subset):
		self.subset = subset
		self.action = ""
	def resetURL(self):
		self.action = ""

	def beginQuery(self):
		self.action = ""

	def annotateHGVSScalar2Response( self , hgvsNotated , **kwargs ):
		out = kwargs.get( "content" , '' )
		self.action = hgvsNotated + "?"
		return self.submit( content = out )
	def annotateHGVSArray2Dict( self , hgvsNotatedArray , **kwargs ):
		out = kwargs.get("content",'')
		resultDict = {}
		for var in hgvsNotatedArray:
			self.beginQuery();
			hgvsNotated = var.strip()
			if out:
				self.annotateHGVSScalar2Response( hgvsNotated , content = out )
			else:
				self.annotateHGVSScalar2Response( hgvsNotated )
			resultDict[hgvsNotated] = self.response.text
		return resultDict
	def annotateHGVSScalar2tsv( self , hgvsNotated , **kwargs ):
		out = "text/xml"
		head = kwargs.get( "header" , '' )
		self.action = hgvsNotated + "?"
		self.submit( content = out )
		#print self.response.text
		geneVariant = hgvsNotated.split( ":" )
		return self.annotateHGVSScalarResponse2tsv( geneVariant , content = out , header = head )

	def annotateHGVSScalarResponse2tsv( self, geneVariant , **kwargs ):
		head = kwargs.get( "header" , True )
		annotations = []
		errors = []
		#print self.response.text
		if head:
			annotations.append( '\t'.join( [ "Gene" , "Mutation" , "Chromosome" , "Start" , "Stop" , "Reference" , "Variant" , "Strand" , "Mutation_Type" ] ) )
		root = ET.fromstring( self.response.text )
		for result in root.iter('data'):
			if not result.get('error'):
				allele = result.get('allele_string')
				alleles = ["" , ""]
				if allele:
					alleles = allele.split( '/' )
				start = result.get('start')
				if not start:
					start = ""
				stop = result.get('end')
				if not stop:
					stop = ""
				chromosome = result.get('seq_region_name')
				if not chromosome:
					chromosome = ""
				strand = result.get('strand')
				if not strand:
					strand = ""
				consequence = result.get('most_severe_consequence')
				if not consequence:
					consequence = ""
				annotations.append( '\t'.join( [ geneVariant[0] , geneVariant[1] , chromosome , start , stop , alleles[0] , alleles[1] , strand , consequence ] ) )
			else:
				#print response
				errors.append( '\t'.join( [ geneVariant[0] , geneVariant[1] , result.get('error') ] ) )
		return { "annotations" : annotations , "errors" : errors }
	def annotatedHGVSDict2tsv( self, resultDict , **kwargs ):
		head = kwargs.get( "header" , True )
		annotations = []
		errors = []
		if head:
			annotations.append( '\t'.join( [ "Gene" , "Mutation" , "Chromosome" , "Start" , "Stop" , "Reference" , "Variant" , "Strand" , "Mutation_Type" ] ) )
		for hgvsNotated , response in resultDict.iteritems():
			geneVariant = hgvsNotated.strip().split( ":" )
			output = self.annotateHGVSScalarResponse2tsv( geneVariant , response , header = False )
			annotations.extend( output["annotations"] )
			errors.extend( output["errors"] )
		return { "annotations" : annotations , "errors" : errors }
	#def annotateHGVSList( self , variants ): #Ensembl hasn't made this possible...yet
	#	self.beginQuery();
	#	variantList = []
	#	for var in variants:
	#		variantList.append( var.strip() )
	#	json.dumps( variantList )
	#	self.addHeader( "Accept" , "application/json" )
	#	self.addData( "hgvs_notation" , variantList )
	#	return self.submit( content = "text/xml" , data = variantList , post = True )

	def annotateHGVSList2tsv( self , variantArray ):
		resultDict = self.annotateHGVSArray2Dict( variantArray , content = "text/xml" )
		return self.annotatedHGVSDict2tsv( resultDict , header = False )
		
	def fOutAnnotateHGVS( self , outputFile , variantArray ):
		output = self.annotatedHGVS2tsv( variantArray )
		fout = open( outputFile , 'w' )
		fout.write( '\t'.join( [ "Gene" , "Mutation" , "Chromosome" , "Start" , "Stop" , "Reference" , "Variant" , "Strand" , "Mutation_Type" ] ) + "\n" )
		for annotation in output["annotations"]:
			fout.write( annotation + "\n" )
		ferr = open( outputFile + ".err" , 'w' )
		for error in output["errors"]:
			ferr.write( error + "\n" )
		#annotations = []
		#for key , value in responses.iteritems():
		#	variant = key.strip().split( ":" )
		#	root = ET.fromstring(value)
		#	for result in root.iter('data'):
		#		allele = result.get('allele_string')
		#		alleles = allele.split( "/" )
		#		start = result.get('start')
		#		stop = result.get('end')
		#		chromosome = result.get('seq_region_name')
		#		strand = result.get('strand')
		#		consequence = result.get('most_severe_consequence')
				#annotations.append( '\t'.join( [ variant[0] , variant[1] , chromosome , start , stop , alleles[0] , alleles[1] , strand , consequence ] ) )
		#		fout.write( '\t'.join( [ variant[0] , variant[1] , chromosome , start , stop , alleles[0] , alleles[1] , strand , consequence ] ) )
		#		print variant
		#for annotation in annotations:
		#	fout.write( annotation + "\n" )
