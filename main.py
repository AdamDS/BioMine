#!/usr/bin/python
# author: Adam D Scott (amviot@gmail.com)
# first created: 2015*09*28

import sys
import getopt
import requests
import json
import tempfile
from ensemblAPI import ensemblAPI
from requests.auth import HTTPDigestAuth
from xmlutils.xml2json import xml2json
import xml.etree.ElementTree as ET

def parseArgs( argv ):
	helpText = "python main.py" + " "
	helpText += "-i <inputFile> -o <outputFile>\n"
	inputFile = ""
	output = ""
	try:
		opts, args = getopt.getopt( argv , "h:i:o:" , ["input=" , "output="] )
	except getopt.GetoptError:
		print "ADSERROR: Command not recognized"
		print( helpText ) 
		sys.exit(2)
	if not opts:
		print "ADSERROR: Expected flagged input"
		print( helpText ) 
		sys.exit(2)
	for opt, arg in opts:
		print opt + " " + arg
		if opt in ( "-h" , "--help" ):
			print( helpText )
			sys.exit()
		elif opt in ( "-i" , "--input" ):
			inputFile = arg
		elif opt in ( "-o" , "--output" ):
			output = arg
	return { "input" : inputFile , "output" : output }
	
def checkConnection():
	search = "http://rest.ensembl.org/vep/human/hgvs/EGFR:p.L858R"
	res = requests.get( search )
	if res:
		print "have response"
	else:
		print res.status_code

def main( argv ):
	values = parseArgs( argv )
	inputFile = values["input"]
	outputFile = values["output"]

	inFile = None
	variants = []
	if inputFile:
		inFile = open( inputFile , 'r' )
		for line in inFile:
			fields = line.split( '\t' )
			variants.append( fields[0] + ":" + fields[1] )

	search = ensemblAPI()
	res = search.annotateVariants( variants , content = "text/json" )
	#res = search.annotateVariant( "EGFR:p.L858R" )
	#search.annotateVariant( "ENST00000275493:p.L858R" )
	#search.annotateVariant( "9:g.22125504G>C" )

	#res = search.submitForJSON()
	#res = search.submit()
	for key , value in res.iteritems():
		print key + " => " + value
	#if res:
	#	print res.text
	#else:
	#	print res.status_code
	#print search

if __name__ == "__main__":
	main( sys.argv[1:] )
