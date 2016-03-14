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

from WebAPI.webAPI import webAPI
import xml.etree.ElementTree as ET
import json
from WebAPI.Variant.MAFVariant import MAFVariant
from WebAPI.Variant.vepVariant import vepVariant

class ensemblAPI(webAPI):
	endpoint = "http://grch37.rest.ensembl.org"
	species = "human"
	hgvs = "/vep/" + species + "/hgvs/"
	region = "/vep/" + species + "/region/"
	sequence = "/sequence/region/" + species + "/"
	translation = "/map/translation/"
	blosum = "Blosum62"
	csn = "CSN"	
	compara = "Conservation"
	exac = "ExAC"
	genesplicer = "GeneSplicer"
	maxentscan = "MaxEntScan"
	updown = "UpDownDistance"
	callback = "callback"
	canonical = "canonical"
	ccds = "ccds"
	dbnsfp = "dbNSFP"
	dbscsnv = "dbscSNV"
	domains = "domains"
	hgvs = "hgvs"
	mirna = "miRNA"
	numbers = "numbers"
	protein = "protein"
	refseq = "xref_refseq"
	def __init__(self,**kwargs):
		subset = kwargs.get("subset",'')
#optional defaults as given by http://rest.ensembl.org/documentation/info/vep_hgvs_get
		blosum = kwargs.get( ensemblAPI.blosum , False )
		csn = kwargs.get( ensemblAPI.csn , False )
		compara = kwargs.get( ensemblAPI.compara , False )
		exac = kwargs.get( ensemblAPI.exac , False )
		genesplicer = kwargs.get( ensemblAPI.genesplicer , False )
		maxentscan = kwargs.get( ensemblAPI.maxentscan , False )
		updown = kwargs.get( ensemblAPI.updown , 5000 )
		callback = kwargs.get( ensemblAPI.callback , "" )
		canonical = kwargs.get( ensemblAPI.canonical , False )
		ccds = kwargs.get( ensemblAPI.ccds , False )
		dbnsfp = kwargs.get( ensemblAPI.dbnsfp , "" )
		dbscsnv = kwargs.get( ensemblAPI.dbscsnv , False )
		domains = kwargs.get( ensemblAPI.domains , False )
		hgvs = kwargs.get( ensemblAPI.hgvs , False )
		mirna = kwargs.get( ensemblAPI.mirna , False )
		numbers = kwargs.get( ensemblAPI.numbers , False )
		protein = kwargs.get( ensemblAPI.protein , False )
		refseq = kwargs.get( ensemblAPI.refseq , False )
		if not subset:
			super(ensemblAPI,self).__init__(ensemblAPI.endpoint,ensemblAPI.hgvs)
		else:
			if ( subset == ensemblAPI.hgvs or \
				subset == ensemblAPI.translation or \
				subset == ensemblAPI.region ):
				super(ensemblAPI,self).__init__(ensemblAPI.endpoint,subset)
			else:
				print "ADSERROR: bad subset. webAPI.subset initializing to variant association results"
				super(ensemblAPI,self).__init__(ensemblAPI.endpoint,ensemblAPI.hgvs)

	def doAllOptions( self , **kwargs ):
		"WebAPI::Ensembl::ensemblAPI::doAllOptions"
		self.blosum = True
		self.csn = True
		self.compara = True
		self.exac = True
		self.genesplicer = True
		self.maxentscan = True
		self.canonical = True
		self.ccds = True
		self.dbscsnv = True
		self.domains = True
		self.hgvs = True
		self.mirna = True
		self.numbers = True
		self.protein = True
		self.refseq = True
		self.doOptions( **kwargs )

	def getOptions( self ):
		return {	ensemblAPI.blosum : int(self.blosum) ,
					ensemblAPI.csn : int(self.csn) ,
					ensemblAPI.compara : int(self.compara) ,
					ensemblAPI.exac : int(self.exac) ,
					ensemblAPI.genesplicer : int(self.genesplicer) ,
					ensemblAPI.maxentscan : int(self.maxentscan) ,
					ensemblAPI.updown : self.updown ,
					ensemblAPI.callback : self.callback ,
					ensemblAPI.canonical : int(self.canonical) ,
					ensemblAPI.ccds : int(self.ccds) ,
					ensemblAPI.dbnsfp : self.dbnsfp ,
					ensemblAPI.dbscsnv : int(self.dbscsnv) ,
					ensemblAPI.domains : int(self.domains) ,
					ensemblAPI.hgvs : int(self.hgvs) ,
					ensemblAPI.mirna : int(self.mirna) ,
					ensemblAPI.numbers : int(self.numbers) ,
					ensemblAPI.protein : int(self.protein) ,
					ensemblAPI.refseq : int(self.refseq) ,
		}
	def getOptionsText( self ):
		return {	ensemblAPI.blosum : "blosum62" , #unsure
					ensemblAPI.csn : "csn" ,
					ensemblAPI.compara : "conservation" ,
					ensemblAPI.exac : "exac_maf" , #maybe?
					ensemblAPI.genesplicer : "gene_splicer" , #unsure
					ensemblAPI.maxentscan : "MaxEntScan" ,
					ensemblAPI.updown : "UpDownDistance" ,
					ensemblAPI.callback : "callback" ,
					ensemblAPI.canonical : "canonical" ,
					ensemblAPI.ccds : "ccds" ,
					ensemblAPI.dbnsfp : "dbnsfp" , #unsure
					ensemblAPI.dbscsnv : "dbscSNV" , #unsure
					ensemblAPI.domains : "domains" ,
					ensemblAPI.hgvs : [ "hgvsc" , "hgvsp" ] ,
					ensemblAPI.mirna : "mirna" , #unsure
					ensemblAPI.numbers : [ "exon" , "intron" ] ,
					ensemblAPI.protein : "protein_id" ,
					ensemblAPI.refseq : "refseq_transcript_ids" ,
		}
		
	def setSubset(self,subset):
		self.subset = subset
		self.action = ""
	def resetURL(self):
		self.action = ""

	def beginQuery(self):
		self.action = ""
	def doOptions( self , **kwargs ):
#		print "WebAPI::Ensembl::ensemblAPI::doOptions"
		toData = kwargs.get( 'data' , False )
		self.action = "?"
		options = self.getOptions()
		for option in options:
			if option == ensemblAPI.updown or \
			option == ensemblAPI.dbnsfp or \
			option == ensemblAPI.callback:
				if toData:
					self.addData( option , options[option] )
				else:
					self.action += str(option) + "=" + str(options[option]) + "&"
			elif options[option]:
				if toData:
					self.addData( option , options[option] )
				else:
					self.action += str(option) + "=1&"

	def annotateHGVSScalar2Response( self , hgvsNotated , **kwargs ):
		out = kwargs.get( "content" , '' )
		self.action = hgvsNotated + "?"
		self.doOptions()
		return self.submit( content = out )
	def annotateHGVSArray2Dict( self , hgvsNotatedArray , **kwargs ):
		out = kwargs.get("content",'')
		resultDict = {}
		for var in hgvsNotatedArray:
			self.beginQuery()
			hgvsNotated = var.strip()
			self.annotateHGVSScalar2Response( hgvsNotated , content = out )
			resultDict[hgvsNotated] = self.response.text
		return resultDict
	def annotateVariantsPost( self , variants , **kwargs ):
		#https://github.com/Ensembl/ensembl-rest/wiki/POST-Requests
#		print "WebAPI::Ensembl::ensemblAPI::annotateVariantsPost"
		maxPost = 400
		lengthVariants = len(variants)
		annotatedVariants = {} #dict of vepVariants
		for i in range(0,lengthVariants,maxPost):
			j = i - 1
			if lengthVariants < maxPost:
				j += lengthVariants
			else:
				j += maxPost
			subsetVariants = []
			if len( variants ) == 1:
				subsetVariants = variants
			else:
				subsetVariants = variants[i:j]
			formattedVariants = []
			nullValue = "."
			delim = " "
			needReferences = self.checkInsertionsReference( subsetVariants , nullValue=nullValue , delim=delim )
			self.fullReset()
			self.setSubset( ensemblAPI.region )
			self.doAllOptions( data=True )
			for var in subsetVariants:
				inputVariant = var.vcf( delim=delim , null=nullValue )
				if var.reference == "-":
					if var.genomicVar() in needReferences:
						print inputVariant + "  -->  " ,
						inputVariant = delim.join( [ var.chromosome , str( int( var.start ) + 1 ) , str( int( var.stop ) - 1 ) , var.reference + "/" + var.alternate , var.strand ] )
					#	if vals[3] == nullValue:
					#		inputVariant = needReferences[var.genomicVar()]
				if var.alternate == "-":
					vals = inputVariant.split( delim )
					if vals[4] == nullValue:
						vals[4] = "-"
					inputVariant = delim.join( vals )
				print inputVariant
				formattedVariants.append( inputVariant )
				vepVar = vepVariant( inputVariant=inputVariant , parentVariant=var )
				annotatedVariants[inputVariant] = vepVar
 			#following examples from documentation
			self.addData( "variants" , formattedVariants )
			self.addHeader( "Accept" , "application/json" )
			self.addHeader( "Content-Type" , "application/json" )
			self.submit( post=True , **kwargs )
			if self.response.ok and self.response.text:
				root = self.response.json()
				for rootElement in root:
					var = vepVariant()
					var.parseEntryFromVEP( rootElement )
					var.setInputVariant()
					annotatedVariants[var.inputVariant] = var
			else:
				print "ensemblAPI Error: cannot access desired XML fields/tags for variants " ,
				print "[" + str(i) + ":" + str(j) + "]"
		return annotatedVariants
	def checkInsertionsReference( self , variants , **kwargs ):
		self.setSubset( ensemblAPI.sequence )
		needReferences = {}
		inputRegions = []
		for var in variants:
			if var.reference == "-":
				inputRegion = var.region()
				needReferences[var.genomicVar()] = var.region()
				inputRegions.append( inputRegion )
		if needReferences:
			self.addData( "regions" , inputRegions )
			inputRegions = []
			self.addHeader( "Accept" , "application/json" )
			self.addHeader( "Content-Type" , "text/xml" )
			self.submit( post=True , **kwargs )
			if self.response.ok and self.response.text:
				needReferences = self.updateMissingReferences( variants , needReferences , **kwargs )
			else:
				print "References needed: " ,
				print needReferences
		return needReferences
	def updateMissingReferences( self , variants , needReferences , **kwargs):
		nullValue = kwargs.get( 'nullValue' , '.' )
		delim = kwargs.get( 'delim' , ' ' )
		for var in variants:
			genVar = var.genomicVar()
			if genVar in needReferences:
				root = self.response.json()
				for rootElement in root:
					ID = rootElement.get( 'id' )
					vals = ID.split( ':' )
					if vals[5] == "1":
						vals[5] = "+"
					elif vals[5] == "-1":
						vals[5] = "-"
					inputRegion = vals[2] + ":" \
								+ vals[3] + ".." \
								+ vals[4] + ":" \
								+ vals[5]
					print var.region() + "\t----\t" + inputRegion
					if var.region() == inputRegion:
						vcfValues = [ vals[2] , vals[3] , nullValue ]
						refSeq = rootElement.get( 'seq' )
						print refSeq + "  -->  " ,
						#vcfValues.append( refSeq[0] )
						vcfValues.append( nullValue )
						print vcfValues ,
						print "  -->  " ,
						vcfValues.append( refSeq[0] + var.alternate )
						#vcfValues.append( var.alternate )
						vcfValues.append( nullValue )
						vcfValues.append( nullValue )
						vcfValues.append( nullValue )
						print vcfValues
						needReferences[genVar] = delim.join( vcfValues )
		return needReferences	
	#def parseJSON( self , json ):
#		print "WebAPI::Ensembl::ensemblAPI::parseJSON - json: " ,
#		print json
		#if type( json ) == list:
#			print "json is a list"
			#for sub in json:
#				print sub
				#if type( sub ) == list or type( sub ) == dict:
					#self.parseJSON( sub )
		#elif type( json ) == dict:
#			print "json is a dict"
			#for sub in sorted(json.keys()):
#				print sub
				#if type( json.get( sub ) ) == list or type( json.get( sub ) ) == dict:
					#self.parseJSON( json.get( sub ) )

#if transcript not in transcripts dict, add new transcript annotation (transcript => [protein change , cdna ])

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
		self.doOptions()
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
				annotations += "\t".join( [ line.strip() , geneVariant[0] , geneVariant[1].strip() , chromosome , start , stop , alleles[0] , alleles[1] , strand , consequence ] ) + "\n"
			else:
				#print response
				annotations = self.nullLine( 10 )
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
	#	self.doOptions()
	#	return self.submit( content = "text/xml" , data = variantList , post = True )
	#def annotateHGVSList2tsv( self , variantArray ):
	#	resultDict = self.annotateHGVSArray2Dict( variantArray , content = "text/xml" )
	#	return self.annotatedHGVSDict2tsv( resultDict , header = False )
	def annotateHGVSFile( self , inputFile , col1 , col2 , **kwargs ):
		output = kwargs.get( "output" , '' )
		if output:
			#print output
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
					fout.write( line.strip() + "\t" + self.nullLine( 10 ) + "\n" )
	
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

	def annotateVariants( self , variants , **kwargs ):
		if variants:
			self.subset = ensemblAPI.region
			for var in variants:
				if annotated:
					annotations.update( )

	def nullLine( self , columns ):
		nulls = ""
		for i in range(0,columns-1):
			nulls += "NULL\t"
		return nulls.rstrip()

	@classmethod
	def setSpecies( cls , species ):
		cls.species = species
		cls.hgvs = "/vep/" + species + "/hgvs/"
		cls.region = "/vep/" + species + "/region/"
	def useGRCh38( cls ):
		cls.endpoint = "http://rest.ensembl.org"
	def useGRCh37( cls ):
		cls.endpoint = "http://grch37.rest.ensembl.org"

	@staticmethod
	def inputHeader( inputFile ):
		inFile = open( inputFile , 'r' )
		if inFile:
			line = next(inFile).decode()
			#print line
			return line
		else:
			return ""
