#https://docs.python.org/2/distutils/examples.html
from distutils.core import setup
setup( name = 'webAPIs' , 
	   version = '0.2' ,
	   package_dir = { 'webAPI' : 'WebAPI' , 
	   				   'variant' : 'WebAPI/Variant' ,
	   				   'exacAPI' : 'WebAPI/ExAC' ,
	   				   'ensemblAPI' : 'WebAPI/Ensembl' ,
					   'entrezAPI' : 'WebAPI/Entrez' ,
					   'ctAPI' : 'WebAPI/ClinicalTrials' ,
					   } ,
	   packages = [ 'webAPI' ,
	   				'exacAPI' ,
	   				'ensemblAPI' ,
					'entrezAPI' ,
					'ctAPI' ,
					'variant'
					]
	   )
