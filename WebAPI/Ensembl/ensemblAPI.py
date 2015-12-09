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
			self.annotateHGVSScalar2Response( hgvsNotated , content = out )
			resultDict[hgvsNotated] = self.response.text
		return resultDict

	def HGVSAnnotationHeader( self ):
		return "\t".join( [ "Gene" , "Mutation" , "Chromosome" , "Start" , "Stop" , "Reference" , "Variant" , "Strand" , "Mutation_Type" ] ) + "\n"
	def HGVSAnnotatedHeader( self , inputFile ):
		header = inputHeader( inputFile )
		return "\t".join( [ header.strip() , "Gene" , "Mutation" , "Chromosome" , "Start" , "Stop" , "Reference" , "Variant" , "Strand" , "Mutation_Type" ] ) + "\n"
	def HGVSErrorHeader( self ):
		return "\t".join( [ "Gene" , "Mutation" , "Error" ] ) + "\n"

	def annotateHGVSScalar2tsv( self , hgvsNotated , **kwargs ):
		out = "text/xml"
		head = kwargs.get( "header" , '' )
		line = kwargs.get( "line" , '' )
		self.action = hgvsNotated + "?"
		self.submit( content = out )
		#print self.response.text
		geneVariant = hgvsNotated.split( ":" )
		return self.annotateHGVSScalarResponse2tsv( geneVariant , content = out , header = head , line = line )
	def annotateHGVSScalarResponse2tsv( self, geneVariant , **kwargs ):
		head = kwargs.get( "header" , True )
		line = kwargs.get( "line" , '' )
		annotations = ""
		errors = ""
		#print self.response.text
		if head:
			annotations += self.HGVSAnnotationHeader()
			errors += self.HGVSErrorHeader()
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
				annotations += "\t".join( [ line.strip() , geneVariant[0] , geneVariant[1] , chromosome , start , stop , alleles[0] , alleles[1] , strand , consequence ] ) + "\n"
			else:
				#print response
				annotations = self.nullLine()
				errors += "\t".join( [ geneVariant[0] , geneVariant[1] , result.get('error') ] ) + "\n"
		return { "annotations" : annotations , "errors" : errors }
	def annotateHGVSArray2tsv( self , hgvsNotatedArray , **kwargs ):
		out = "text/xml"
		head = kwargs.get( "header" , '' )
		annotations = ""
		errors = ""
		for var in hgvsNotatedArray:
			self.beginQuery();
			hgvsNotated = var.strip()
			self.annotateHGVSScalar2Response( hgvsNotated , content = out )
			results = self.annotateHGVSScalarResponse2tsv( hgvsNotated.split( ":" ) , content = out , header = head )
			head = False
			annotations += results["annotations"]
			errors += results["errors"]
		return { "annotations" : annotations , "errors" : errors }
	def annotatedHGVSDict2tsv( self, resultDict , **kwargs ):
		head = kwargs.get( "header" , True )
		annotations = ""
		errors = ""
		if head:
			annotations += self.HGVSAnnotationHeader()
			errors += self.HGVSErrorHeader()
		for hgvsNotated , response in resultDict.iteritems():
			geneVariant = hgvsNotated.strip().split( ":" )
			output = self.annotateHGVSScalarResponse2tsv( geneVariant , response , header = False )
			annotations += output["annotations"]
			errors += output["errors"]
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
	#def annotateHGVSList2tsv( self , variantArray ):
	#	resultDict = self.annotateHGVSArray2Dict( variantArray , content = "text/xml" )
	#	return self.annotatedHGVSDict2tsv( resultDict , header = False )
	def annotateHGVSFile( self , inputFile , col1 , col2 , **kwargs ):
		output = kwargs.get( "output" , '' )
		if output:
			print output
			fout = open( output , 'w' )
			fout.write( self.HGVSAnnotatedHeader( inputFile ) )
			inFile = open( inputFile , 'r' )
			next( inFile )
			for line in inFile:
				columns = line.split( "\t" )
				fields = [ columns[col1] , columns[col2] ]
				#print fields[0] + ":" + fields[1] + "\t\t" + line
				annotated = self.annotateHGVSScalar2tsv( ':'.join( fields ) )
				if annotated:
					fout.write( line.strip() + "\t" + annotated["annotations"].strip() + "\n" )
				else:
					fout.write( line.strip() + "\t" + self.nullLine() + "\n" )
	
	def annotateHGVSArray2File( self , variantArray , outputFile ):
		output = self.annotateHGVSArray2tsv( variantArray )
		fout = open( outputFile , 'w' )
		fout.write( self.HGVSAnnotationHeader() )
		for annotation in output["annotations"]:
			fout.write( annotation )
		ferr = open( outputFile + ".err" , 'w' )
		ferr.write( self.HGVSErrorHeader() )
		for error in output["errors"]:
			ferr.write( error )

	def nullLine( self ):
		nulls = ""
		for i in range(0,9):
			nulls += "NULL\t"
		return nulls.rstrip()

def inputHeader( inputFile ):
	inFile = open( inputFile , 'r' )
	if inFile:
		line = next(inFile).decode()
		print line
		return line
	else:
		return ""
