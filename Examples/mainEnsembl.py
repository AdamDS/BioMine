#!/usr/bin/python
# author: Adam D Scott (amviot@gmail.com)
# first created: 2015*09*28

import sys
import getopt
from WebAPI.Ensembl.ensemblAPI import ensemblAPI
from WebAPI.Variant.MAFVariant import MAFVariant

def parseArgs( argv ):
	helpText = "python main.py" + " "
	helpText += "-i <inputFile> -o <outputFile>\n"
	helpText += "-s \"HGVS notation\" -t (boolean flag for tsv output)\n"
	inputFile = ""
	output = ""
	hgvs = ""
	tsv = False
	maf = False
	try:
		opts, args = getopt.getopt( argv , "tmh:i:o:s" , ["input=" , "output=" , "hgvs="] )
	except getopt.GetoptError:
		print "ADSERROR: Command not recognized"
		print( helpText ) 
		sys.exit(2)
	if not opts:
		print "ADSERROR: Expected flagged input"
		print( helpText ) 
		sys.exit(2)
	for opt, arg in opts:
		#print opt + " " + arg
		if opt in ( "-h" , "--help" ):
			print( helpText )
			sys.exit()
		elif opt in ( "-i" , "--input" ):
			inputFile = arg
		elif opt in ( "-o" , "--output" ):
			output = arg
		elif opt in ( "-m" , "--maf" ):
			maf = True
		elif opt in ( "-s" , "--hgvs" ):
			hgvs = arg
		elif opt in ( "-t" , "--tsv" ):
			tsv = True
	return { "input" : inputFile , "output" : output , "hgvs" : hgvs , "tsv" : tsv , "maf" : maf }
	
def checkConnection():
	ensemblInstance = "http://rest.ensembl.org/info/ping?content-type=application/json"
	res = requests.get( ensemblInstance )
	if res:
		print "have response"
	else:
		print res.status_code

def readMutations( inputFile ):
	variants = []
	if inputFile:
		inFile = open( inputFile , 'r' )
		for line in inFile:
			fields = line.split( '\t' )
			variants.append( fields[0] + ":" + fields[1] )
	return variants
def readMAF( inputFile , **kwargs ):
	userVariants = []
	try:
		inFile = open( inputFile , 'r' )
		codonColumn = kwargs.get( 'codon' , 47 )
		peptideChangeColumn = kwargs.get( 'peptideChange' , 48 )
		next(inFile)
		for line in inFile:
			var = MAFVariant()
			var.mafLine2Variant( line , peptideChange=peptideChangeColumn , codon=codonColumn )
			userVariants.append( var )
		return userVariants
	except:
		raise Exception( "ADS Error: bad .maf file" )
def sortVars( variants ):
	print "sortVars N=" ,
	strVars = {}
	print str( len( variants ) )
	for var in variants:
		print var.uniqueVar()
		strVars.update( { var.proteogenomicVar() : var } )
	listVars = []
	for varstr in sorted( strVars.keys() ):
		print varstr
		listVars.append( strVars.get( varstr ) )
	return listVars

def main( argv ):
	values = parseArgs( argv )
	inputFile = values["input"]
	outputFile = values["output"]
	hgvs = values["hgvs"]
	tsv = values["tsv"]
	maf = values["maf"]

	results = ""
	ensemblInstance = ensemblAPI()

	if maf:
		variants = readMAF( inputFile , codon=46 , peptideChange=47 )
		annotated = ensemblInstance.annotateVariantsPost( variants )
		sortedVars = sortVars( annotated )
		for var in sortedVars:
			print var.proteogenomicVar() 
	else:
		variants = readMutations( inputFile )
		if inputFile and outputFile:
			ensemblInstance.annotateHGVSArray2File( variants , outputFile )
		elif inputFile and not outputFile:
			resultsErrors = ensemblInstance.annotateHGVSArray2tsv( variants , header = True )
			results = resultsErrors["annotations"]

		if hgvs:
			if tsv:
				resultsErrors = ensemblInstance.annotateHGVSScalar2tsv( hgvs , header = True )
				results = resultsErrors["annotations"]
			else:
				ensemblInstance.annotateHGVSScalar2Response( hgvs )
				results = ensemblInstance.response.text

	print results
	print ensemblInstance.buildURL()

	#print ensemblInstance.headers
	#print ensemblInstance.data
	#print ensemblInstance.buildURL()
	#for key , value in response.iteritems():
	#	fout.write( key + "\t" + value )
	#if response:
	#	print response.text
	#else:
	#	print response.status_code
	#print ensemblInstance

if __name__ == "__main__":
	main( sys.argv[1:] )
