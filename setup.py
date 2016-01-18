#https://docs.python.org/2/distutils/examples.html
from distutils.core import setup
version = '0.4'
setup( \
	name = 'WebAPIs' , 
	version = version , 
	author = 'Adam D Scott' ,
	author_email = 'amviot@gmail.com' ,
	maintainer = 'Adam D Scott' ,
	maintainer_email = 'amviot@gmail.com' ,
	url = 'github.com/AdamDS/WebAPIs' ,
	description = 'A variety of web APIs' ,
	long_description = 'A variety of web APIs. \
		Currently, WebAPIs interacts with clinical and \
		genomic type sites, but its core is not restricted \
		to any single site or field.
		Works with ClinicalTrials, Ensembl, Entrez, ExAC, \
		and relies on the use of several Variant classes.' ,
	download_url = 'github.com/AdamDS/WebAPIs/archive/' + \
		version + '.tar.gz' ,
	classifiers = [ \
	] ,
	platforms = [ \
		'2.7'
	] ,
	license = 'MIT' ,
	#ClinicalTrials - none - cite data used: https://clinicaltrials.gov/ct2/about-site/terms-conditions
	#Entrez - not apparent/none given - cite data used: - copyrights: https://www.ncbi.nlm.nih.gov/home/about/policies.shtml
	#Ensembl ReST - Apache 2 - https://raw.githubusercontent.com/Ensembl/ensembl-rest/master/LICENSE
	#ExAC - MIT - https://raw.githubusercontent.com/hms-dbmi/exac_browser/master/LICENSE
	#PubChem - not apparent/none given - cite data used: https://pubchem.ncbi.nlm.nih.gov/citations.html - copyrights: https://www.ncbi.nlm.nih.gov/home/about/policies.shtml
	package_dir = { 'WebAPI' : 'WebAPI' , 
	} ,
	packages = [ \
		'WebAPI' ,
		'WebAPI.ClinicalTrials' ,
		'WebAPI.Entrez' ,
		'WebAPI.Ensembl' ,
		'WebAPI.ExAC' ,
		'WebAPI.Variant' ,
	] , #each of the directories with modules (aka packages)
	install_requires = [ \
		'AdvancedHTMLParser' , 
		'requests' ,
	] , #auto installs with pip install
)
