class variant(object):
	def __init__(self , **kwargs):
		self.gene = kwargs.get('gene',None)
		self.chromosome = kwargs.get('chromosome',None)
		self.start = kwargs.get('start',None)
		self.stop = kwargs.get('stop',None)
		self.reference = kwargs.get('reference',None)
		self.mutant = kwargs.get('mutant',None)
		self.strand = kwargs.get('strand',None)
		self.sample = kwargs.get('sample',None)
		self.assembly = kwargs.get('assembly',None)
		self.dbsnp = kwargs.get('dbsnp',None)
	def printVariant(self,delim):
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
		if self.mutant:
			print self.mutant + delim ,
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
		if self.mutant:
			attributes.append(self.mutant)
		if self.strand:
			attributes.append(self.strand)
		if self.dbsnp:
			attributes.append(self.dbsnp)
		if self.sample:
			attributes.append(self.sample)
		return attributes
	def genomicVar( self ):
		return self.chromosome + ":" + self.start + "-" + self.stop + self.reference + ">" + self.mutant
	def mafLine2Variant( self , line ):
		fields = line.split( "\t" )
		self.gene = fields[0]	#1	Hugo_Symbol
		self.chromosome = fields[4]	#5	Chromosome
		self.start = fields[5]	#6	Start_Position
		self.stop = fields[6]	#7	End_Position
		self.strand = fields[7]	#8	Strand
		self.reference = fields[10]	#11	Reference_Allele
		self.mutant = fields[11] if fields[11] != fields[10] else fields[12]	#12	Tumor_Seq_Allele1	#13	Tumor_Seq_Allele2
		self.dbsnp = fields[13]
		self.sample = fields[15]

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
mu = variant(gene="BRAF",chromosome=7,start=12345,stop=123456,reference="AT",mutant="GC")
mu.printVariant('\t')
ou = variant(gene="BRAF",chromosome=7,start=12345,stop=123456,reference="AT",mutant="GC")
ou.printVariant('\t')
pu = variant(chromosome=7,start=12345,stop=123456,reference="AT",mutant="GC")
pu.printVariant('\t')
qu = variant(chromosome=7,start=12345,reference="AT",mutant="GC")
qu.printVariant('\t')

print qu.attr()
'''
