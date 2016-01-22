import re
from WebAPI.Variant.variant import variant

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

	def printVariant(self,delim , **kwargs ):
		onlyVariant = kwargs.get( 'variant' , False )
		super(MAFVariant,self).printVariant(delim , **kwargs )
		if not onlyVariant:
			print "MAFVariant: " ,
			if self.referencePeptide:
				print self.referencePeptide + delim ,
			if self.positionPeptide:
				print self.positionPeptide + delim ,
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
	def asIndel( self ):
		if self.isIndel():
			self.positionPeptide + \
			self.peptide
			
	def determineLengthOfIndel( self ):
		lengthOfIndel = 0
		endDeletion = 0
		if self.isIndel():
			lenRef = len(self.reference)
			lenAlt = len(self.alternate)
			lengthOfIndel = lenAlt - lenRef
			if lenRef > 1:
				print "is del"
		return lengthOfIndel
	def isIndel( self ):
		if self.variatnType == "INS" or self.variantType == "DEL":
			return True
		return False
	def HGVSc( self ):
		return str(self.gene) + ":c." \
		+ str(self.codonStart) + \
		+ str(self.reference) + ">"\
		+ str(self.alternate)
	def HGVSct( self ):
		return str(self.transcript) + ":c." \
		+ str(self.codonStart) \
		+ str(self.reference) + "_" \
		+ str(self.alternate)
	def HGVSp( self ):
		if self.gene and self.referencePeptide:
			return self.gene + ":p." + self.referencePeptide + self.positionPeptide + self.alternatePeptide
	def HGVSc( self ):
		if self.gene and self.referencePeptide:
			return self.gene + ":c." + self.codonPosition + self.reference + ">" + self.alternate
	def mafLine2Variant( self , line , **kwargs ):
		print "MAFVariant::mafLine2Variant"
		super(MAFVariant,self).mafLine2Variant( line , **kwargs )
		deltaPeptideColumn = kwargs.get( 'peptideChange' , 49 )
		fields = line.split( "\t" )
		self.variantClass = fields[8]	#9	Variant_Classification
		self.variantType = fields[9]	#10	Variant_Type
		self.splitHGVSp( fields[deltaPeptideColumn] ) #################################### Custom field, not reliable in general
		print self.printVariant(',')
	def splitHGVSp( self , hgvsp ):
		#print "MAFVariant::splitHGVSp"
		ref = ""
		pos = ""
		mut = ""
		#print hgvsp
		pattern = re.compile( "(p\.)(.*)" )
		change = pattern.match( hgvsp )
		if change: #peptide
			hgvsp = change.groups()[-1]
			#print hgvsp
			pattern = re.compile( "([a-zA-Z]+?)([0-9]+?)([a-zA-Z\*]+)" )
			change = pattern.match( hgvsp )
			if change:
				changes = change.groups()
				ref = changes[0]
				#print ref + "->" ,
				ref = self.convertAA( ref )
				#print ref
				self.referencePeptide = ref
				pos = changes[1]
				self.positionPeptide = pos
				#print pos
				mut = changes[-1]
				#print mut + "->" , 
				mut = self.convertAA( mut )
				#print mut
				self.alternatePeptide = mut
		else: #intronic
			pattern = re.compile( "(e)([0-9]+?)([\+\-][0-9]+?)" )
			change = pattern.match( hgvsp )
			if change:
				changes = change.groups()
				ref = changes[0]
				#print ref + "->" ,
				ref = self.convertAA( ref )
				#print ref
				self.referencePeptide = ref
				pos = changes[1]
				self.positionPeptide = pos
				#print pos
				mut = changes[2] 
				#print mut + "->" , 
				mut = self.convertAA( mut )
				#print mut
				self.alternatePeptide = mut
		return { "referencePeptide" : ref , "positionPeptide" : pos , "alternatePeptide" : mut }
	def convertAA( self , pep ):
		#print "MAFVariant::convertAA - " + pep
		pattern = re.compile( "(fs)" )
		fs = pattern.match( pep )
		if fs:
			return "fs"
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

	def samePeptideReference( self , otherVar ):
		print "samePeptideReference - " ,
		if self.sameGenomicReference( otherVar ):
			if otherVar.referencePeptide == self.referencePeptide and \
				otherVar.positionPeptide == self.positionPeptide: #same genomic position & reference
				print "comparing ::" + str(self.printVariant(','))
				print ":: vs ::" + str(otherVar.printVariant(','))
				return True
		return False
	def samePeptideChange( self , otherVar ):
		print "samePeptideChange - " ,
		if self.samePeptideReference( otherVar ):
			if otherVariant.alternatePeptide == var.alternatePeptide:
				print "comparing ::" + self.printVariant(',')
				print ":: vs ::" + otherVar.printVariant(',')
				return True
		return False
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
