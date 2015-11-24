#!/usr/bin/python
# author: Adam D Scott (amviot@gmail.com)
# first created: 2015*09*28

import sys
import getopt
import requests
import json
import tempfile
from vepAPI import vepAPI
from requests.auth import HTTPDigestAuth
from xmlutils.xml2json import xml2json
import xml.etree.ElementTree as ET

def parseArgs( argv ):
	helpText = "python main.py" + "\n\tRequired input:\n"
	helpText += "\t\t-u <username> -k <key>\tOR\t-c <API credentials file: user \\n key>" + "\n"
	helpText += "\tOptional inputs:\n"
	helpText += "\t\t-o <outputfile>\n"# -a <REST API site>\n"
	username = ""
	password = ""
	api = ""
	output = ""
	try:
		opts, args = getopt.getopt( argv , "hc:a:u:k:o:" , ["cred=" , "api=" , "user=" , "key=" , "output="] )
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
		elif opt in ( "-c" , "--cred" ):
			[username,password] = list( open( arg ) )
		elif opt in ( "-a" , "--api" ):
			api = arg
		elif opt in ( "-u" , "--user" ):
			username = arg
		elif opt in ( "-k" , "--key" ):
			password = arg
		elif opt in ( "-o" , "--output" ):
			output = arg
	return { "username" : username , "password" : password , "api" : api , "output" : output }
	
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
	username = values["username"].strip()
	password = values["password"].strip()
	output = values["output"]

	search = vepAPI()
	search.searchVariant( "EGFR:p.L858R" )
	#search.searchVariant( "ENST00000275493:p.L858R" )
	#search.searchVariant( "9:g.22125504G>C" )
	res = search.submit()
	if res:
		print res.text
	else:
		print res.status_code
	print search

if __name__ == "__main__":
	main( sys.argv[1:] )
