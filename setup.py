#https://docs.python.org/2/distutils/examples.html
from distutils.core import setup
setup( name = 'webAPIs' , 
	   version = '0.0' ,
	   package_dir = { 'restAPI' : 'WebAPI' , 
	   				   #'WebAPI' : 'restAPI' ,
	   				   'ensemblAPI' : 'WebAPI/Ensembl' ,#: 'ensemblAPI' ,
					   'entrezAPI' : 'WebAPI/Entrez' ,#: 'entrezAPI' ,
					   'ctAPI' : 'WebAPI/ClinicalTrials' ,#: 'ctAPI' ,
					   } ,
	   packages = [ 'restAPI' ,#'WebAPI' ,
	   				'ensemblAPI' ,#'Ensembl' ,
					'entrezAPI' ,#'Entrez' ,
					'ctAPI' ,#'ClinicalTrials'
					]
	   )
