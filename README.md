# webAPIs
Integrating URL APIs through a more common framework.
# Installation
This package uses Python 2.7.
To install run:
	python setup.py install
## Dependencies
[Requests](http://docs.python-requests.org/en/latest/)
	pip install requests
[AdvancedHTMLParser](https://pypi.python.org/pypi/AdvancedHTMLParser)
	pip install AdvancedHTMLParser
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
