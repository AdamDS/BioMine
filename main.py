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
	search = "http://rest.ensembl.org/"
	res = requests.get( search )
	print search
	if res:
		print "have xml"
	else:
		print res.status_code

def main( argv ):
	values = parseArgs( argv )
	inputFile = values["input"]
	outputFile = values["output"]

	search = ensemblAPI()
	search.searchVariant( "EGFR:p.L858R" )
	#search.searchVariant( "ENST00000275493:p.L858R" )
	#search.searchVariant( "9:g.22125504G>C" )

	#res = search.submitForJSON()
	res = search.submit()
	if res:
		print res.text
	else:
		print res.status_code
	print search

if __name__ == "__main__":
	main( sys.argv[1:] )
