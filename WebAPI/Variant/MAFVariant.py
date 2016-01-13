import re
from variant import variant
class MAFVariant(variant):
	def __init__(self , **kwargs):
		super(MAFVariant,self).__init__(**kwargs)
		self.positionPeptide = kwargs.get('positionPeptide',None)
		self.referencePeptide = kwargs.get('referencePeptide',None)
		self.alternatePeptide = kwargs.get('alternatePeptide',None)
		self.transcript = kwargs.get('transcript',None)
		self.assembly = kwargs.get('assembly',None)
		self.variantClass = kwargs.get('variantClass',None)
		self.variantType = kwargs.get('variantType',None)
		self.disease = kwargs.get('disease',None)

	def printVariant(self,delim):
		super(MAFVariant,self).printVariant(delim)
		if self.positionPeptide:
			print self.positionPeptide + delim ,
		if self.referencePeptide:
			print self.referencePeptide + delim ,
		if self.alternatePeptide:
			print self.alternatePeptide + delim ,
		if self.transcript:
			print self.transcript + delim ,
		if self.variantClass:
			print self.variantClass + delim ,
		if self.variantType:
			print self.variantType + delim ,
		if self.disease:
			print self.disease + delim ,
		print ""
	def attr(self):
		attributes = []
		super(MAFVariant,self).attr()
		if self.positionPeptide:
			attributes.append(self.positionPeptide)
		if self.referencePeptide:
			attributes.append(self.referencePeptide)
		if self.alternatePeptide:
			attributes.append(self.alternatePeptide)
		if self.transcript:
			attributes.append(self.transcript)
		if self.disease:
			attributes.append(self.disease)
		return attributes
	def HGVSp( self ):
		if self.gene and self.referencePeptide:
			return self.gene + ":p." + self.referencePeptide + self.positionPeptide + self.alternatePeptide
	def HGVSc( self ):
		if self.gene and self.referencePeptide:
			return self.gene + ":c." + self.codonPosition + self.reference + ">" + self.alternate
	def mafLine2Variant( self , line ):
		super(MAFVariant,self).mafLine2Variant( line )
		fields = line.split( "\t" )
		self.variantClass = fields[8]	#9	Variant_Classification
		self.variantType = fields[9]	#10	Variant_Type
		self.splitHGVSp( fields[47] ) #################################### Custom field, not reliable in general
	def splitHGVSp( self , hgvsp ):
		ref = ""
		pos = ""
		mut = ""
		parts = hgvsp.split( '.' )
		hgvsp = parts[-1]
		pattern = re.compile( "([a-zA-Z]+?)([0-9]+?)([a-zA-Z]+)" )
		change = pattern.match( hgvsp )
		if change:
			changes = change.groups()
			ref = changes[0]
			ref = self.convertAA( ref )
			self.referencePeptide = ref
			pos = changes[1]
			self.positionPeptide = pos
			mut = changes[-1]
			mut = self.convertAA( mut )
			self.alternatePeptide = mut
		return { "referencePeptide" : ref , "positionPeptide" : pos , "alternatePeptide" : mut }
	def convertAA( self , pep ):
		if pep == "Arg":
			return "R"
		if pep == "Asn":
			return "N"
		if pep == "Asp":
			return "D"
		if pep == "Gln":
			return "Q"
		if pep == "Glu":
			return "E"
		if pep == "Lys":
			return "K"
		if pep == "Phe":
			return "F"
		if pep == "Trp":
			return "W"
		if pep == "Ter":
			return "*"
		if pep == "Tyr":
			return "Y"
		return pep[0]

	def compareVariants( self , otherVariant ):
		common = 0
		attributes = self.attr()
		otherAttributes = otherVariant.attr()
		for attr in attributes:
			for otherAttr in otherAttributes:
				if attr == otherAttr:
					common += 1
		percentMatch = common / len( attributes )
		return percentMatch

	def readVariants(self,inputFile):
		variants = []
		if inputFile:
			inFile = open( inputFile , 'r' )
			for line in inFile:
				fields = line.split( '\t' )
				variants.append( fields[0] + ":" + fields[1] )
		return variants
	def reset( self ):
		self = variant.__init()

'''
mu = variant(gene="BRAF",chromosome=7,start=12345,stop=123456,reference="AT",alternate="GC",referencePeptide="A123R")
mu.printVariant('\t')
nu = variant(gene="BRAF",referencePeptide="A123R")
nu.printVariant('\t')
ou = variant(gene="BRAF",chromosome=7,start=12345,stop=123456,reference="AT",alternate="GC")
ou.printVariant('\t')
pu = variant(chromosome=7,start=12345,stop=123456,reference="AT",alternate="GC")
pu.printVariant('\t')
qu = variant(chromosome=7,start=12345,reference="AT",alternate="GC")
qu.printVariant('\t')

print qu.attr()
'''
