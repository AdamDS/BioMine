# BioMine
This is a toolkit to handle variant and clinical data (see variant classes). Web accessions are included through the webapi class for 

- ClinicalTrials.gov
- NCBI Entrez services
- Ensembl ReST API
- ExAC (Harvard) ReST API

The webapi parent class can be used to more easily create classes for other URL-based web services as well.

The variant classes can be used independently of the webapi's, and they include many useful functions to conform to HGVS variant representations. The BioMine toolkit is used in other software, such as [CharGer](https://github.com/ding-lab/CharGer).
# Installation
This package works with Python 2.7. To install:
`pip install .`
All dependencies should automatically install.
# Note to developers
Please be aware of site's crawler limitations (robots.txt) & rate limitations when creating new classes for web services. Failure to do so can result in IP banning or denial of service.
# Modules
## Web API - general
Parent class of the included ReST APIs, web services, and HTML
### Example to print this readme from github:
	site = webAPI.webAPI( "https://github.com/" , "AdamDS/" )
	site.action = "WebAPIs"
	site.submit()
	page = site.parseHTMLResponse()
	readme = page.getElementById( 'readme' )
	print readme.innerHTML
## Clinical Trials - HTML
Based on [ClinicalTrials.gov](https://clinicaltrials.gov/ct2/info/linking)
## NCBI: Entrez - service
Based on [NCBI's Entrez Programming Utilities (E-utilities)](http://www.ncbi.nlm.nih.gov/books/NBK25501/)
### Search ClinVar
#### searchClinVar - search terms for ClinVar
	returns requests response object
#### searchPubMed - search terms for PubMed
	returns requests response object
## NCBI: PubChem - ReST
Based on [NCBI's Power User Gateway for PubChem](http://www.ncbi.nlm.nih.gov/home/api.shtml)
### Compound Synonyms
#### compoundSynonyms - single compound lookup
	returns tab delimited string (searched compound '\t' synonym)
#### compoundsSynonyms - array of compounds lookup
	returns tab delimited array (searched compound '\t' synonym)
#### compoundsSynonyms2File - array of compounds lookup and write to file
	no return
## Ensembl: Variant Effect Predictor - ReST
Based on [Ensembl's VEP annotator](http://rest.ensembl.org/#Variation)
### HGVS genomic variant annotation
### Use GRCh37 or GRCh38
Switch to GRCh37 or GRCh38
#### useGRCh37 - switches to annotation by GRCh37
#### useGRCh38 - switches to annotation by GRCh38
### Annotate HGVS Notation with Genomic Variant
tab delimited annotation as:
HGVS notation, chr, start, stop, ref, var, strand, classification
#### annotateHGVSScalar2Response - annotate a single mutation
	returns request response as JSONP
#### annotateHGVSScalar2tsv - annotate a single mutation
	returns dictionary with tsv annotation and error message
#### annotateHGVSScalarResponse2tsv - annotate a single mutation from response
	returns dictionary with tsv annotation and error message
#### annotateHGVSArray2Dict - annotate an array of mutations
	returns dictionary of HGVS notated mutations (key)/ response as JSONP (values)
#### annotateHGVSArray2tsv - annotate an array of mutations
	returns dictionary with tsv annotations and error messages
#### annotatedHGVSDict2tsv - annotate a dictionary of mutations of mutations (key)/ responses (values) 
	returns dictionary with tsv annotations and error messages
#### annotateHGVSArray2File - annotate an array of mutations
	no return
## ExAC - HTML
	Based on [ExAC Browser Beta](exac.broadinstitute.org/)
### Variants
#### getAlleleFrequency - retrieves allele frequency of a variant
	returns a number of the given variant
