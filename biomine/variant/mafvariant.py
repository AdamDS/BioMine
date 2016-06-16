import re
from biomine.variant.variant import variant

class mafvariant(variant):
	def __init__(self , **kwargs):
		super(mafvariant,self).__init__(**kwargs)
		self.referencePeptide = kwargs.get('referencePeptide',"")
		self.positionPeptide = kwargs.get('positionPeptide',None)
		self.alternatePeptide = kwargs.get('alternatePeptide',"")
		self.transcriptPeptide = kwargs.get('transcriptPeptide',None)
		self.positionCodon = kwargs.get('positionCodon',None)
		self.transcriptCodon = kwargs.get('transcriptCodon',None)
		self.variantClass = kwargs.get('variantClass',None)
		self.variantType = kwargs.get('variantType',None)
		self.disease = kwargs.get('disease',None)
		aParentVariant = kwargs.get( 'parentVariant' , None )
		if aParentVariant:
			super( mafvariant , self ).copyInfo( aParentVariant )
	def copyInfo( self , copy ):
		super( mafvariant , self ).copyInfo( copy )
		try:
			self.referencePeptide = copy.referencePeptide
		except:
			pass
		try:
			self.positionPeptide = copy.positionPeptide
		except:
			pass
		try:
			self.alternatePeptide = copy.alternatePeptide
		except:
			pass
		try:
			self.transcriptPeptide = copy.transcriptPeptide
		except:
			pass
		try:
			self.positionCodon = copy.positionCodon
		except:
			pass
		try:
			self.transcriptCodon = copy.transcriptCodon
		except:
			pass
		try:
			self.variantClass = copy.variantClass
		except:
			pass
		try:
			self.variantType = copy.variantType
		except:
			pass
		try:
			self.disease = copy.disease
		except:
			pass
	def fillMissingInfo( self , copy ):
		#print "Variant.mafvariant::fillMissingInfo" ,
		super( mafvariant , self ).fillMissingInfo( copy )
		if not self.referencePeptide:
			self.referencePeptide = copy.referencePeptide
		if not self.positionPeptide:
			self.positionPeptide = copy.positionPeptide
		if not self.alternatePeptide:
			self.alternatePeptide = copy.alternatePeptide
		if not self.transcriptPeptide:
			self.transcriptPeptide = copy.transcriptPeptide
		if not self.positionCodon:
			self.positionCodon = copy.positionCodon
		if not self.transcriptCodon:
			self.transcriptCodon = copy.transcriptCodon
		if not self.variantClass:
			self.variantClass = copy.variantClass
		if not self.variantType:
			self.variantType = copy.variantType
		if not self.disease:
			self.disease = copy.disease

	def printVariant(self,delim , **kwargs ):
		onlyThisVariant = kwargs.get( 'minimal' , False )
		if not onlyThisVariant:
			super(mafvariant,self).printVariant(delim , **kwargs )
			print "mafvariant: { " ,
			if self.referencePeptide:
				print "referencePeptide= " ,
				print self.referencePeptide + delim ,
			if self.positionPeptide:
				print "positionPeptide= " ,
				print str(self.positionPeptide) + delim ,
			if self.alternatePeptide:
				print "alternatePeptide= " ,
				print self.alternatePeptide + delim ,
			if self.transcriptPeptide:
				print "transcriptPeptide= " ,
				print self.transcriptPeptide + delim ,
			if self.positionCodon:
				print "positionCodon= " ,
				print str(self.positionCodon) + delim ,
			if self.transcriptCodon:
				print "transcriptCodon= " ,
				print self.transcriptCodon + delim ,
			if self.variantClass:
				print "variantClass= " ,
				print self.variantClass + delim ,
			if self.variantType:
				print "variantType= " ,
				print self.variantType + delim ,
			if self.disease:
				print "disease= " ,
				print self.disease + delim ,
			print " }"
	def attr(self):
		attributes = []
		super(mafvariant,self).attr()
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
#		print "biomine::variant::mafvariant::mafLine2Variant - " , 
		super(mafvariant,self).mafLine2Variant( line , **kwargs )
		codonColumn = kwargs.get( 'codon' , 48 )
		deltaPeptideColumn = kwargs.get( 'peptideChange' , 49 )
		fields = line.split( "\t" )
		self.variantClass = fields[8]	#9	Variant_Classification
		self.variantType = fields[9]	#10	Variant_Type
		self.splitHGVSc( fields[int(codonColumn)] )
		self.splitHGVSp( fields[int(deltaPeptideColumn)] ) #################################### Custom field, not reliable in general

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
#		print "biomine::variant::mafvariant::typeIsIndel - " ,
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
#		print "samePeptideReference - " ,
		if otherVar.referencePeptide == self.referencePeptide and \
			otherVar.positionPeptide == self.positionPeptide: #same genomic position & reference
				return True
		return False
	def samePeptideChange( self , otherVar ):
#		print "samePeptideChange - " ,
		if self.samePeptideReference( otherVar ):
			if otherVar.alternatePeptide == self.alternatePeptide:
				return True
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
#		print "biomine::variant::mafvariant::HGVSp"
		hgvsp = ""
		if self.transcriptPeptide:
			hgvsp += str(self.transcriptPeptide)
		elif self.gene:
			hgvsp += str(self.gene)
		hgvsp += ":p."
		if self.referencePeptide:
			hgvsp += str(self.referencePeptide)
		if self.positionPeptide:
			hgvsp += str(self.positionPeptide)
		if self.alternatePeptide:
			hgvsp += str(self.alternatePeptide)
		return hgvsp
	def splitHGVSp( self , hgvsp ):
##		print "biomine::variant::mafvariant::splitHGVSp - "
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
				print "biomine::variant::mafvariant Warning: could not find amino acid change or intronic change"
				print "  Hint: Is the input amino acid change column correct?"
				print "    Problem variant: " ,
				self.printVariant(',')
		else:
			parts = hgvsp.split('\.')
			pos = parts[-1]
		return [ ref , pos , mut ]
	def convertAA( self , pep ):
#		print "mafvariant::convertAA - " + pep
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
#		print "biomine::variant::mafvariant::hgvspIsNonCoding - " ,
		pattern = re.compile( "(NULL)" )
		match = pattern.match( hgvsp )
		if match: #then its a complex indel
			return True
		return False

### Codon
	def hgvscIsNonCoding( self , hgvsc ):
#		print "biomine::variant::mafvariant::hgvscIsNonCoding - " ,
		pattern = re.compile( "([NULL|\*|\+|\-])" )
		match = pattern.match( hgvsc )
		if match: #then its a complex indel
			return True
		return False
	def hgvscIsIndel( self , hgvsc ):
#		print "biomine::variant::mafvariant::hgvscIsIndel - " ,
		pattern = re.compile( "(.*?[del|ins].*?)" )
		match = pattern.match( hgvsc )
		if match: #then its a complex indel
			complexPattern = re.compile( "(delins)" )
			complexMatch = complexPattern.match( hgvsc )
			if complexMatch:
				return 2
			else:
				return 1
		return 0
	def HGVSc( self ):
#		print "biomine::variant::mafvariant::HGVSc"
		hgvsc = ""
		if self.transcriptCodon:
			hgvsc += str(self.transcriptCodon)
		elif self.gene:
			hgvsc += str(self.gene)
		hgvsc += ":c."
		if self.positionCodon:
			hgvsc += str(self.positionCodon).replace( "-" , "_" )
		if self.reference != "-" and self.alternate != "-":
			if self.start == self.stop: #snp
				hgvsc += str(self.reference) + ">" \
				+ str(self.alternate)
			else: #complex
				hgvsc += "del" + str(self.reference) \
				+ "ins" + str(self.alternate)
		elif self.reference == "-" and self.alternate != "-":
			hgvsc += "ins" + str(self.alternate)
		elif self.reference != "-" and self.alternate == "-":
			hgvsc += "del" + str(self.reference)
		return hgvsc
	def HGVSct( self ):
		return str(self.transcriptCodon) + ":c." \
		+ str( self.positionCodon ).replace( "-" , "_" ) \
		+ str(self.reference) + "_" \
		+ str(self.alternate)
	def codingHGVS( self ):
#		print "biomine::variant::mafvariant::codingHGVS"
		return self.HGVSc() + '::' + self.HGVSp()
	def proteogenomicVar( self ):
#		print "biomine::variant::mafvariant::proteogenomicVar"
		return self.genomicVar() + "::" + self.codingHGVS()
	def uniqueProteogenomicVar( self ):
#		print "biomine::variant::mafvariant::uniqueProteogenomicVar"
		if self.sample:
			return self.sample + "::" + self.proteogenomicVar()
		else:
			return "nosample::" + self.proteogenomicVar()
	def splitHGVSc( self , hgvsc , xDot="c\." ):
#		print "biomine::variant::mafvariant::splitHGVSc - " ,
		pattern = re.compile( xDot + "(.*)" )
		change = pattern.match( hgvsc )
		pos = ""
		if change:
			hgvsc = change.groups()[0]
			indel = self.hgvscIsIndel( hgvsc ) 
			isNon = self.hgvscIsNonCoding( hgvsc ) 
			posOnly = self.hasCodonPositionOnly( hgvsc )
			if not posOnly:
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
			print "biomine::variant::mafvariant Warning: could not find HGVS codon change"
			print "  Hint: Is the input codon column correct?"
			print "    Problem variant: " ,
			self.printVariant(',')
		return [ "" , "" , "" ]
	def hasCodonPositionOnly( self , hgvsc ):
#		print "biomine::variant::mafvariant::hasCodonPositionOnly - " ,
		noncoding = self.hgvscIsNonCoding( hgvsc )
		if noncoding:
			return True
		else:
			pattern = re.compile( "([a-zA-Z])" )
			pos = pattern.match( hgvsc )
			if pos and noncoding != "NULL":
				return False
			return True
	def splitNonCodingHGVSc( self , hgvsc ):
#		print "biomine::variant::mafvariant::splitNonCodingHGVSc - " ,
		if self.hgvscIsNonCoding( hgvsc ):
			pattern = re.compile( "([NULL|\*|\-|\+])(\d+)(.*)" )
			match = pattern.match( hgvsc )
			parts = match.groups()
			if parts[0] == "NULL":
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
#		print "biomine::variant::mafvariant::splitComplexHGVSc - " ,
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
#		print "biomine::variant::mafvariant::splitSimpleIndelHGVSc - " ,
		pattern = re.compile( "(del)" )
		matches = pattern.match( hgvsc )
		if matches:
			self.splitSimpleDeletion( hgvsc )
		else:
			self.splitSimpleInsertion( hgvsc )
	def splitSimpleDeletionHGVSc( self , hgvsc ):
#		print "biomine::variant::mafvariant::splitSimpleDeletionHGVSc - " ,
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
#		print "biomine::variant::mafvariant::splitSimpleInsertionHGVSc - " ,
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
