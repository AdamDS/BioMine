class variant(object):
	def __init__(self , **kwargs):
		self.gene = kwargs.get('gene',None)
		self.chromosome = kwargs.get('chromosome',None)
		self.start = kwargs.get('start',None)
		self.stop = kwargs.get('stop',None)
		self.reference = kwargs.get('reference',None)
		self.alternate = kwargs.get('alternate',None)
		self.strand = kwargs.get('strand',None)
		self.sample = kwargs.get('sample',None)
		self.assembly = kwargs.get('assembly',None)
		self.dbsnp = kwargs.get('dbsnp',None)
	def printVariant(self,delim , **kwargs ):
#		print "variant: " ,
		if self.gene:
			print self.gene + delim ,
		if self.chromosome:
			print str(self.chromosome) + delim ,
		if self.start:
			print str(self.start) + delim ,
		if self.stop:
			print str(self.stop) + delim ,
		if self.reference:
			print self.reference + delim ,
		if self.alternate:
			print self.alternate + delim ,
		if self.strand:
			print self.strand + delim ,
		if self.dbsnp:
			print "rs" + self.dbsnp + delim ,
		if self.sample:
			print self.sample + delim ,
		if self.assembly:
			print self.assembly + delim ,
		print ""
	def attr(self):
		attributes = []
		if self.gene:
			attributes.append(self.gene)
		if self.chromosome:
			attributes.append(self.chromosome)
		if self.start:
			attributes.append(self.start)
		if self.stop:
			attributes.append(self.stop)
		if self.reference:
			attributes.append(self.reference)
		if self.alternate:
			attributes.append(self.alternate)
		if self.strand:
			attributes.append(self.strand)
		if self.dbsnp:
			attributes.append(self.dbsnp)
		if self.sample:
			attributes.append(self.sample)
		return attributes
	def genomicVar( self ):
		return str(self.chromosome) + ":" \
		+ str(self.start) + "-" \
		+ str(self.stop) \
		+ str(self.reference) \
		+ ">" + str(self.alternate)
	def HGVSg( self ):
		return str(self.chromosome) + ":g." \
		+ str(self.start) \
		+ str(self.reference) + ">" \
		+ str(self.alternate)
	def mafLine2Variant( self , line , **kwargs ):
##		print "variant::mafLine2Variant - " ,
		fields = line.split( "\t" )
		self.gene = fields[0]	#1	Hugo_Symbol
		self.chromosome = fields[4]	#5	Chromosome
		self.start = fields[5]	#6	Start_Position
		self.stop = fields[6]	#7	End_Position
		self.strand = fields[7]	#8	Strand
		self.reference = fields[10]	#11	Reference_Allele
		self.alternate = fields[11] if fields[11] != fields[10] else fields[12]	#12	Tumor_Seq_Allele1	#13	Tumor_Seq_Allele2
		self.dbsnp = fields[13]
		self.sample = fields[15]
	def uniqueVar( self ):
		return self.sample + "::" + self.genomicVar()

	def isIndel( self ):
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

	def sameGenomicVariant( self , otherVar ):
#		print "sameGenomicVariant - " ,
		if self.sameGenomicReference( otherVar ):
			if otherVar.alternate == self.alternate:
		#		print "comparing ::" + self.genomicVar()
		#		print ":: vs ::" + otherVar.genomicVar()
				return True
#		print "not the same genomic variant"
		return False
	def sameGenomicReference( self , otherVar ):
#		print "sameGenomicReference - " ,
		if self.sameGenomicPosition( otherVar ):
			if otherVar.reference == self.reference:
		#		print "comparing ::" + self.genomicVar()
		#		print ":: vs ::" + otherVar.genomicVar()
				return True
#		print "not the same genomic reference"
		return False
	def sameGenomicPosition( self , otherVar ):
		if otherVar.chromosome == self.chromosome and \
			otherVar.start == self.start:
			return True
		return False
'''
mu = variant(gene="BRAF",chromosome=7,start=12345,stop=123456,reference="AT",alternate="GC")
mu.printVariant('\t')
ou = variant(gene="BRAF",chromosome=7,start=12345,stop=123456,reference="AT",alternate="GC")
ou.printVariant('\t')
pu = variant(chromosome=7,start=12345,stop=123456,reference="AT",alternate="GC")
pu.printVariant('\t')
qu = variant(chromosome=7,start=12345,reference="AT",alternate="GC")
qu.printVariant('\t')

print qu.attr()
'''
