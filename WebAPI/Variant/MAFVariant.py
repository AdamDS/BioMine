import re
from WebAPI.Variant.variant import variant

class MAFVariant(variant):
	def __init__(self , **kwargs):
		super(MAFVariant,self).__init__(**kwargs)
		self.referencePeptide = kwargs.get('referencePeptide',None)
		self.positionPeptide = kwargs.get('positionPeptide',None)
		self.alternatePeptide = kwargs.get('alternatePeptide',None)
		self.transcriptPeptide = kwargs.get('transcript',None)
		self.positionCodon = kwargs.get('positionPeptide',None)
		self.transcriptCodon = kwargs.get('transcript',None)
		self.assembly = kwargs.get('assembly',None)
		self.variantClass = kwargs.get('variantClass',None)
		self.variantType = kwargs.get('variantType',None)
		self.disease = kwargs.get('disease',None)

	def printVariant(self,delim , **kwargs ):
		onlyVariant = kwargs.get( 'variant' , False )
		super(MAFVariant,self).printVariant(delim , **kwargs )
		if not onlyVariant:
	#		print "MAFVariant: " ,
			if self.referencePeptide:
				print self.referencePeptide + delim ,
			if self.positionPeptide:
				print self.positionPeptide + delim ,
			if self.alternatePeptide:
				print self.alternatePeptide + delim ,
			if self.transcriptPeptide:
				print self.transcriptPeptide + delim ,
			if self.positionCodon:
				print self.positionCodon + delim ,
			if self.transcriptCodon:
				print self.transcriptCodon + delim ,
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
		if self.transcriptPeptide:
			attributes.append(self.transcriptPeptide)
		if self.positionCodon:
			attributes.append(self.positionCodon)
		if self.transcriptCodon:
			attributes.append(self.transcriptCodon)
		if self.disease:
			attributes.append(self.disease)
		return attributes
			
	def mafLine2Variant( self , line , **kwargs ):
#		print "WebAPI::Variant::MAFVariant::mafLine2Variant - " , 
		super(MAFVariant,self).mafLine2Variant( line , **kwargs )
		codonColumn = kwargs.get( 'codon' , 48 )
		deltaPeptideColumn = kwargs.get( 'peptideChange' , 49 )
		fields = line.split( "\t" )
		self.variantClass = fields[8]	#9	Variant_Classification
		self.variantType = fields[9]	#10	Variant_Type
		self.splitHGVSc( fields[int(codonColumn)] )
		self.splitHGVSp( fields[int(deltaPeptideColumn)] ) #################################### Custom field, not reliable in general
		#print self.printVariant(',')

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

	def typeIsIndel( self ):
#		print "WebAPI::Variant::MAFVariant::typeIsIndel - " ,
#		print self.variantType
		if self.variantType == "INS" or self.variantType == "DEL":
			return True
		return False

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

### Peptide
	def samePeptideReference( self , otherVar ):
##		print "samePeptideReference - " ,
		if otherVar.referencePeptide == self.referencePeptide and \
			otherVar.positionPeptide == self.positionPeptide: #same genomic position & reference
#		#		print "comparing ::" + str(self.HGVSp())
#		#		print ":: vs ::" + str(otherVar.HGVSp())
				return True
##		print " not the same peptide reference"
		return False
	def samePeptideChange( self , otherVar ):
##		print "samePeptideChange - " ,
		if self.samePeptideReference( otherVar ):
			if otherVar.alternatePeptide == self.alternatePeptide:
#		#		print "comparing ::" + str(self.HGVSp())
#		#		print ":: vs ::" + str(otherVar.HGVSp())
				return True
##		print " not the same peptide change"
		return False
	def hgvspIsIndel( self , hgvsp ):
		pattern = re.compile( "([a-zA-Z]+?)([0-9]+?)([a-zA-Z\*]+)" )
		change = pattern.match( hgvsp )
		if change:
			fsPattern = re.compile( "(fs)" )
			fsMatch = fsPattern.match( hgvsp )
			if fsMatch:
				return 2
			else:
				return 1
		return 0
	def HGVSp( self ):
#		print "WebAPI::Variant::MAFVariant::HGVSp"
		hgvsp = ""
		if self.transcriptPeptide:
			hgvsp += str(self.transcriptPeptide)
		elif self.gene:
			hgvsp += str(self.gene)
		hgvsp += ":p."
		if self.reference:
			hgvsp += str(self.referencePeptide)
		if self.positionPeptide:
			hgvsp += str(self.positionPeptide)
		if self.alternate:
			hgvsp += str(self.alternatePeptide)
		return hgvsp
	def splitHGVSp( self , hgvsp ):
##		print "WebAPI::Variant::MAFVariant::splitHGVSp - "
##		print hgvsp
		ref = ""
		pos = ""
		mut = ""
		isNon = self.hgvspIsNonCoding( hgvsp )
		if not isNon:
			changep = re.match( "p\.([a-zA-Z]+?)([0-9]+?)([a-zA-Z\*\=]+)" , hgvsp )
			changee = re.match( "(e)([0-9]+?)([\+\-][0-9]+?)" , hgvsp )
			if changep: #peptide
				changes = changep.groups()
				ref = changes[0]
				ref = self.convertAA( ref )
				self.referencePeptide = ref
				pos = changes[1]
				self.positionPeptide = pos
				mut = changes[-1]
				mut = self.convertAA( mut )
				self.alternatePeptide = mut
			elif changee: #intronic
				changes = changee.groups()
				ref = changes[0]
				ref = self.convertAA( ref )
				self.referencePeptide = ref
				pos = changes[1]
				self.positionPeptide = pos
				mut = changes[2] 
				mut = self.convertAA( mut )
				self.alternatePeptide = mut
			else:
				print "WebAPI::Variant::MAFVariant Warning: could not find amino acid change or intronic change"
				print "  Hint: Is the input amino acid change column correct?"
				print "    Problem variant: " ,
				self.printVariant(',')
		else:
			parts = hgvsp.split('\.')
			pos = parts[-1]
		return [ ref , pos , mut ]
	def convertAA( self , pep ):
		#print "MAFVariant::convertAA - " + pep
		pattern = re.compile( "(fs)" )
		fs = pattern.match( pep )
		if fs:
			return "fs"
		if pep == "=":
			return ""
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
	def hgvspIsNonCoding( self , hgvsp ):
##		print "WebAPI::Variant::MAFVariant::hgvspIsNonCoding - " ,
##		print hgvsp
		pattern = re.compile( "(NULL)" )
		match = pattern.match( hgvsp )
		if match: #then its a complex indel
			return True
		return False

### Codon
	def hgvscIsNonCoding( self , hgvsc ):
#		print "WebAPI::Variant::MAFVariant::hgvscIsNonCoding - " ,
#		print hgvsc
		pattern = re.compile( "([NULL|\*|\+|\-])" )
		match = pattern.match( hgvsc )
		if match: #then its a complex indel
	#		print match.group()
			return True
#		print match
		return False
	def hgvscIsIndel( self , hgvsc ):
#		print "WebAPI::Variant::MAFVariant::hgvscIsIndel - " ,
#		print hgvsc
		pattern = re.compile( "(.*?[del|ins].*?)" )
		match = pattern.match( hgvsc )
		#print match
		if match: #then its a complex indel
			complexPattern = re.compile( "(delins)" )
			complexMatch = complexPattern.match( hgvsc )
			if complexMatch:
				return 2
			else:
				return 1
		return 0
	def HGVSc( self ):
#		print "WebAPI::Variant::MAFVariant::HGVSc"
		hgvsc = ""
		if self.transcriptCodon:
			hgvsc += str(self.transcriptCodon)
		elif self.gene:
			hgvsc += str(self.gene)
		hgvsc += ":c."
		if self.positionCodon:
			hgvsc += str(self.positionCodon)
		if self.reference:
			hgvsc += str(self.reference)
		hgvsc += ">"
		if self.alternate:
			hgvsc += str(self.alternate)
		return hgvsc
	def HGVSct( self ):
		return str(self.transcriptCodon) + ":c." \
		+ str(self.positionCodon) \
		+ str(self.reference) + "_" \
		+ str(self.alternate)
	def codingHGVS( self ):
#		print "WebAPI::Variant::MAFVariant::codingHGVS"
		if self.gene and self.referencePeptide:
			return self.HGVSc() + ', ' + self.HGVSp()
		return self.HGVSc()
	def proteogenomicVar( self ):
#		print "WebAPI::Variant::MAFVariant::proteogenomicVar"
		return self.genomicVar() + ", " + self.codingHGVS()
	def uniqueProteogenomicVar( self ):
#		print "WebAPI::Variant::MAFVariant::uniqueProteogenomicVar"
		if self.sample:
			return self.sample + "::" + self.genomicVar() + ", " + self.codingHGVS()
		else:
			return "nosample::" + self.genomicVar() + ", " + self.codingHGVS()
	def splitHGVSc( self , hgvsc ):
#		print "WebAPI::Variant::MAFVariant::splitHGVSc - " ,
#		print hgvsc
		pattern = re.compile( "c\.(.*)" )
		change = pattern.match( hgvsc )
		pos = ""
		if change:
			hgvsc = change.groups()[0]
			indel = self.hgvscIsIndel( hgvsc ) 
			isNon = self.hgvscIsNonCoding( hgvsc ) 
			posOnly = self.hasCodonPositionOnly( hgvsc )
	#		print posOnly
			if not posOnly:
		#		print "not just codon position"
		#		print "indel: " ,
		#		print indel
		#		print "hgvsc: " ,
		#		print hgvsc
		#		print "noncoding: " ,
		#		print isNon
				if ( self.typeIsIndel( hgvsc ) ) or ( indel > 0 ):
					if indel == 2: #then its a complex indel
						return self.splitComplexIndelHGVSc( hgvsc )
					elif indel == 1: #simple indel
						return self.splitSimpleIndelHGVSc( hgvsc )
				elif isNon:
					return self.splitNonCodingHGVSc( hgvsc )
				else: #then its a snv
					return self.splitSNVHGVSc( hgvsc )
			else:
				if indel > 0:
					startStop = hgvsc.split('_')
					pos = hgvsc[0]
				else:
					pos = hgvsc
				self.positionCodon = pos
			return [ "" , pos , "" ]
		else:
			print "WebAPI::Variant::MAFVariant Warning: could not find HGVS codon change"
			print "  Hint: Is the input codon column correct?"
			print "    Problem variant: " ,
			self.printVariant(',')
		return [ "" , "" , "" ]
	def hasCodonPositionOnly( self , hgvsc ):
#		print "WebAPI::Variant::MAFVariant::hasCodonPositionOnly - " ,
#		print hgvsc + " => " ,
		noncoding = self.hgvscIsNonCoding( hgvsc )
#		print noncoding
		if noncoding:
	#		print "non-coding info "
			return True
		else:
			pattern = re.compile( "([a-zA-Z])" )
			pos = pattern.match( hgvsc )
			if pos and noncoding != "NULL":
		#		print "more codon info "
				return False
	#		print "codon position only "
			return True
	def splitNonCodingHGVSc( self , hgvsc ):
#		print "WebAPI::Variant::MAFVariant::splitNonCodingHGVSc - " ,
#		print hgvsc + " => " ,
		if self.hgvscIsNonCoding( hgvsc ):
			pattern = re.compile( "([NULL|\*|\-|\+])(\d+)(.*)" )
			match = pattern.match( hgvsc )
			parts = match.groups()
	#		print parts
			if parts[0] == "NULL":
		#		print parts[0]
				return [ "" , parts[0] , "" ]
			elif parts[0]:
				pos = str(match.groups()[0]) + str(match.groups()[1])
			else:
				pos = str(match.groups()[1])
			return [ "" , pos , "" ]
		return [ "" , "" , "" ]
	def splitSNVHGVSc( self , hgvsc ):
		pattern = re.compile( "(\d+?)([0-9]+?)([a-zA-Z\*]+)" )
		change = pattern.match( hgvsc )
		ref = ""
		pos = ""
		mut = ""
		if change:
			changes = change.groups()
			ref = changes[0]
			pos = changes[1]
			self.positionCodon = pos
			mut = changes[-1]
			self.positionCodon = pos
		return [ ref , pos , mut ]
	def splitComplexHGVSc( self , hgvsc ):
#		print "WebAPI::Variant::MAFVariant::splitComplexHGVSc - " ,
#		print hgvsc
		pattern = re.compile( "(\d+?)\_(\d+?)del(\w+)ins([AGCT]*?)" )
		matches = pattern.match( hgvsc )
		parts = matches.groups()
		ref = ""
		pos = ""
		mut = ""
		if len(parts) > 1:
			mut = parts[-1]
		else:
			mut = self.alternate
		if len(parts) > 2:
			ref = parts[2]
		else:
			ref = self.reference
		pos = parts[0]
		self.positionCodon = parts[0]
		return [ ref , pos , mut ]
	def splitSimpleIndelHGVSc( self , hgvsc ):
#		print "WebAPI::Variant::MAFVariant::splitSimpleIndelHGVSc - " ,
#		print hgvsc
		pattern = re.compile( "(del)" )
		matches = pattern.match( hgvsc )
		if matches:
			self.splitSimpleDeletion( hgvsc )
		else:
			self.splitSimpleInsertion( hgvsc )
	def splitSimpleDeletionHGVSc( self , hgvsc ):
#		print "WebAPI::Variant::MAFVariant::splitSimpleDeletionHGVSc - " ,
#		print hgvsc
		pattern = re.compile( "(\d+?)\_(\d+?)del(\w+)" )
		matches = pattern.match( hgvsc )
		parts = matches.groups()
		ref = ""
		if len(parts) > 2:
			ref = parts[2]
		else:
			ref = self.reference
		pos = parts[0]
		self.positionCodon = parts[0]
		return [ ref , pos ]
	def splitSimpleInsertionHGVSc( self , hgvsc ):
#		print "WebAPI::Variant::MAFVariant::splitSimpleInsertionHGVSc - " ,
#		print hgvsc
		pattern = re.compile( "(\d+?)\_(\d+?)ins(\w+)" )
		matches = pattern.match( hgvsc )
		parts = matches.groups()
		mut = ""
		if len(parts) > 2:
			mut = parts[2]
		else:
			mut = self.reference
		pos = parts[0]
		self.positionCodon = parts[0]
		return [ pos , mut ]
	def plausibleCodonFrame( self , otherVar ):
		start = int(self.start)
		#stop = self.stop
		ostart = int(otherVar.start)
		#ostop = otherVar.stop
		maxShift = 2
		if start+maxShift >= ostart and start-maxShift <= ostart:
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
