#https://docs.python.org/2/distutils/examples.html
from distutils.core import setup
version = "0.7"
setup( \
	name = 'BioMine' , 
	version = version , 
	author = 'Adam D Scott' ,
	author_email = 'adam@adamscottphd.com' ,
	maintainer = 'Adam D Scott' ,
	maintainer_email = 'adam@adamscottphd.com' ,
	url = 'https://github.com/AdamDS/BioMine' ,
	description = 'Bioinformatics data-mining' ,
	long_description = 'Bioinformatics data-mining. \
		Currently, BioMine interacts with clinical and \
		genomic type sites, but its core is not restricted \
		to any single site or field. \
		Works with clinicaltrials, ensembl, entrez, exac, \
		and relies on the use of several variant classes.' ,
	download_url = 'https://github.com/AdamDS/BioMine/archive/v' + \
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
	] ,
	license = 'MIT' ,
	#clinicaltrials - none - cite data used: https://clinicaltrials.gov/ct2/about-site/terms-conditions
	#entrez - not apparent/none given - cite data used: - copyrights: https://www.ncbi.nlm.nih.gov/home/about/policies.shtml
	#ensembl ReST - Apache 2 - https://raw.githubusercontent.com/ensembl/ensembl-rest/master/LICENSE
	#exac - MIT - https://raw.githubusercontent.com/hms-dbmi/exac_browser/master/LICENSE
	#PubChem - not apparent/none given - cite data used: https://pubchem.ncbi.nlm.nih.gov/citations.html - copyrights: https://www.ncbi.nlm.nih.gov/home/about/policies.shtml
	package_dir = { 'biomine' : 'biomine' , 
	} ,
	packages = [ \
		'biomine' ,
		'biomine.webapi' ,
		'biomine.webapi.clinicaltrials' ,
		'biomine.webapi.entrez' ,
		'biomine.webapi.ensembl' ,
		'biomine.webapi.exac' ,
		'biomine.variant' ,
		'biomine.parsers' ,
		'biomine.writers' ,
	] , #each of the directories with modules (aka packages)
	requires = [ \
		'AdvancedHTMLParser' , 
		'requests' ,
		'PyVCF' ,
		'TransVar' ,
	] , #auto installs with pip install
	dependency_links = ['https://github.com/zwdzwd/transvar/archive/v2.1.23.20160321.tar.gz']
)
