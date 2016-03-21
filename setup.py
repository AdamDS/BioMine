#https://docs.python.org/2/distutils/examples.html
from distutils.core import setup
version = '0.4'
setup( \
	name = 'BioMine' , 
	version = version , 
	author = 'Adam D Scott' ,
	author_email = 'amviot@gmail.com' ,
	maintainer = 'Adam D Scott' ,
	maintainer_email = 'amviot@gmail.com' ,
	url = 'github.com/AdamDS/BioMine' ,
	description = 'A variety of web APIs' ,
	long_description = 'A variety of web APIs. \
		Currently, BioMine interacts with clinical and \
		genomic type sites, but its core is not restricted \
		to any single site or field. \
		Works with ClinicalTrials, Ensembl, Entrez, ExAC, \
		and relies on the use of several Variant classes.' ,
	download_url = 'github.com/AdamDS/BioMine/archive/' + \
		version + '.tar.gz' ,
	classifiers = [ \
		"License :: OSI Approved :: MIT License " , 
		"Programming Language :: Python" , 
		"Programming Language :: Python :: 2.7" , 
		"Development Status :: 4 - Beta" , 
		"Intended Audience :: Developers" , 
		"Intended Audience :: Science/Research" , 
		"Topic :: Internet" , 
		"Topic :: Scientific/Engineering" , 
		"Topic :: Scientific/Engineering :: Bio-Informatics" , 
		"Topic :: Scientific/Engineering :: Chemistry" , 
		"Topic :: Text Processing :: HTML" , 
		"Topic :: Text Processing :: XML" , 
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
		'Variant' ,
	] , #each of the directories with modules (aka packages)
	requires = [ \
		'AdvancedHTMLParser' , 
		'requests' ,
		'PyVCF' ,
	] , #auto installs with pip install
)
