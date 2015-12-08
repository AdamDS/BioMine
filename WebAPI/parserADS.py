#!/usr/bin/python
# author: Adam D Scott (amviot@gmail.com)
# first created: 2015*10*06

import sys
import getopt
#import getpass

class parse(object):
	def __init__(self,**kwargs):
		self.__flags = kwargs.get("flags","")
		self.__help = kwargs.get("help","Help!")
		self.__login = kwargs.get("login",False)

	def (self,):
		helpText = "python main.py" + "\n\tRequired input:\n"
		helpText += "\t\t-u <username> -k <key>\tOR\t-c <API credentials file: user \\n key>" + "\n"
		helpText += "\tOptional inputs:\n"
		helpText += "\t\t-o <outputfile> -a <REST API site>\n"
		username = ""
		password = ""
		api = ""
		try:
			opts, args = getopt.getopt( argv , "hc:a:u:k:" , ["cred=" , "api=" , "user=" , "key="] )
		except getopt.GetoptError:
			print "ADSERROR: Command not recognized"
			print( helpText ) 
			sys.exit(2)
		if not opts:
			print "ADSERROR: Expected flagged input"
			print( helpText ) 
			sys.exit(2)
		for opt, arg in opts:
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
		return { "username" : username , "password" : password , "api" : api }
