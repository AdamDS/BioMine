#https://docs.python.org/2/distutils/examples.html
from distutils.core import setup
setup( name = 'webAPIs' , 
	   version = '0.1' ,
	   package_dir = { 'restAPI' : 'WebAPI' , 
	   				   'variant' : 'WebAPI/Variant' ,
	   				   'ensemblAPI' : 'WebAPI/Ensembl' ,
					   'entrezAPI' : 'WebAPI/Entrez' ,
					   'ctAPI' : 'WebAPI/ClinicalTrials' ,
					   } ,
	   packages = [ 'restAPI' ,
	   				'ensemblAPI' ,
					'entrezAPI' ,
					'ctAPI' ,
					'variant'
					]
	   )
