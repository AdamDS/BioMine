#!/usr/bin/python
# author: Adam D Scott (amviot@gmail.com)
# first created: 2015*12*06

import sys
import getopt
#import requests
#import json
#import tempfile
#from entrezAPI import entrezAPI
#from requests.auth import HTTPDigestAuth
#from xmlutils.xml2json import xml2json
#import xml.etree.ElementTree as ET
#import WebAPI
from WebAPI.Entrez.entrezAPI import entrezAPI
#import WebAPI.Entrez.entrezAPI

def parseArgs( argv ):
	helpText = "python main.py" + " "
	helpText += "-d \"database\" "
	helpText += "-q \"query\" "
	helpText += "(-o \"outputFormat\")\n"
	inputFile = ""
	output = ""
	database = ""
	query = ""
	try:
		opts, args = getopt.getopt( argv , "h:i:d:q:o:" , ["input=" , "database=" , "query=" , "output="] )
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
		elif opt in ( "-i" , "--inputFile" ):
			inputFile = arg
		elif opt in ( "-d" , "--database" ):
			database = arg
		elif opt in ( "-q" , "--query" ):
			query = arg
		elif opt in ( "-o" , "--output" ):
			output = arg
	return { "input" : inputFile , "database" : database , "query" : query , "output" : output }
	
def checkConnection():
	entrezInstance = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=asthma[mesh]+AND+leukotrienes[mesh]+AND+2009[pdat]"
	summaryTest = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=20113659,20074456"
	res = requests.get( entrezInstance )
	if res:
		print "have response"
	else:
		print res.status_code

def readDBSearches( inputFile ):
	searches = []
	dbs = []
	if inputFile:
		inFile = open( inputFile , 'r' )
		for line in inFile:
			fields = line.split( "\t" )
			dbs.append( fields[0].strip() )
			searches.append( fields[1].strip() )
	return { "databases" : dbs , "searches" : searches }
	
def main( argv ):
	values = parseArgs( argv )
	inputFile = values["input"]
	outputFormat = values["output"]
	database = values["database"]
	query = values["query"]

	results = ""
	queries = readDBSearches( inputFile )
	entrezInstance = entrezAPI()

	if inputFile and outputFormat:
		results = entrezInstance.searchPubMed( searches , outputFormat , search = search , identifier = identifier )
	elif inputFile and not outputFormat:
		results = entrezInstance.getPubMedDetails( searches , search = search , identifier = identifier )

	print results

	if query:
		results = entrezInstance.searchPubMed( queries )

	print results

	#print entrezInstance.headers
	#print entrezInstance.data
	#print entrezInstance.buildURL()
	#for key , value in response.iteritems():
	#	fout.write( key + "\t" + value )
	#if response:
	#	print response.text
	#else:
	#	print response.status_code
	#print entrezInstance

if __name__ == "__main__":
	main( sys.argv[1:] )
