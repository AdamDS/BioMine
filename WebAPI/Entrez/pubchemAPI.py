#!/usr/bin/python
# author: Adam D Scott
# first created: 2015*11*27
#####
#	Operation					Function				Works With
#####
# from https://pubchem.ncbi.nlm.nih.gov/pug_rest/PUG_REST.html#_Toc409516773
#<input specification> = <domain>/<namespace>/<identifiers>
#<domain> = substance | compound | assay | <other inputs>
#compound domain <namespace> = cid | name | smiles | inchi | sdf | inchikey | formula | <structure search> | <xref> | listkey | <fast search>
#<structure search> = {substructure | superstructure | similarity | identity}/{smiles | inchi | sdf | cid}
#<fast search> = {fastidentity | fastsimilarity_2d | fastsimilarity_3d | fastsubstructure | fastsuperstructure}/{smiles | inchi | sdf | cid} | fastformula
#<xref> = xref / {RegistryID | RN | PubMedID | MMDBID | ProteinGI | NucleotideGI | TaxonomyID | MIMID | GeneID | ProbeID | PatentID}
#substance domain <namespace> = sid | sourceid/<source name> | sourceall/<source name> | name | <xref> | listkey
#<source name> = any valid PubChem depositor name
#assay domain <namespace> = aid | listkey | type/<assay type> | sourceall/<source name> | target/<assay target> | activity/<activity column name>
#<assay type> = all | confirmatory | doseresponse | onhold | panel | rnai | screening | summary | cellbased | biochemical | invivo | invitro | activeconcentrationspecified
#<assay target> = gi | proteinname | geneid | genesymbol
#<identifiers> = comma-separated list of positive integers (e.g. cid, sid, aid) or identifier strings (source, inchikey, formula); in some cases only a single identifier string (name, smiles, xref; inchi, sdf by POST only)
#<other inputs> = sources / [substance, assay] |sourcetable | conformers
### Inherited
#	endpoint	"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/PLX4032/synonyms/XML"
#	subset		"/compound/" , "/substance/" , "/assay/"
#	action		"/name/

from restAPI import restAPI
import xml.etree.ElementTree as ET
import json

class pubchemAPI(restAPI):
	endpoint = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
	compound = "/compound/"
	substance = "/substance/"
	assay = "/assay/"
	def __init__(self,**kwargs):
		subset = kwargs.get("subset",'') #compound
		self.search = kwargs.get("search",'name') #name
		self.term = kwargs.get("term",'') #vemurafenib
		self.dataProperties = kwargs.get("dataProperties",'synonyms') #synonyms
		self.dataReturn = kwargs.get("dataReturn",'') #MolecularWeight
		self.dataFormat = kwargs.get("dataFormat",'XML') #XML
		if not subset:
			super(pubchemAPI,self).__init__(pubchemAPI.endpoint,pubchemAPI.compound)
		else:
			if ( subset == pubchemAPI.compound or
				 subset == pubchemAPI.assay or
				 subset == pubchemAPI.substance ):
				super(pubchemAPI,self).__init__(pubchemAPI.endpoint,subset)
			else:
				print "ADSERROR: bad subset. restAPI.subset initializing to variant association results"
				super(pubchemAPI,self).__init__(pubchemAPI.endpoint,pubchemAPI.compound)

	def setSubset(self,subset):
		self.subset = subset
		self.action = ""
	def resetURL(self):
		self.action = ""

	def beginQuery(self):
		self.action = ""

	def buildAction( self ):
		self.action = "/".join( [ self.search , self.term , self.dataProperties , self.dataReturn , self.dataFormat ] )

	def compoundSynonyms( self , compound , **kwargs ):
		synonyms = ""
		self.term = compound
		self.search = kwargs.get( "search" , 'name' )
		self.buildAction()
		self.submit()
		#print self.response.text
		root = ET.fromstring( self.response.text )
		if root.find( "Fault" ):
			synonyms += compound + "\tNotFound\n"
		else:
			for information in root:
				for synonym in information:
					synonyms += compound + "\t" + synonym.text + "\n"
		return synonyms

	def compoundsSynonyms( self , compounds , **kwargs ):
		synonyms = ""
		self.search = kwargs.get( "search" , 'name' )
		for compound in compounds:
			synonyms += self.compoundSynonyms( compound , search = self.search )
		return synonyms

	def compoundsSynonyms2File( self , compounds , output , **kwargs ):
		self.search = kwargs.get( "search" , 'name' )
		synonyms = self.compoundsSynonyms( compound , search = self.search )
		fOut = open( output , 'w' )
		fOut.write( synonyms )
