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
	def copyInfo( self , copy ):
		self.gene = copy.gene
		self.chromosome = copy.chromosome
		self.start = copy.start
		self.stop = copy.stop
		self.reference = copy.reference
		self.alternate = copy.alternate
		self.strand = copy.strand
		self.sample = copy.sample
		self.assembly = copy.assembly
		self.dbsnp = copy.dbsnp
	def fillMissingInfo( self , copy ):
		if not self.gene and copy.gene:
			self.gene = copy.gene
		if not self.chromosome and copy.chromosome:
			self.chromosome = copy.chromosome
		if not self.start and copy.start:
			self.start = copy.start
		if not self.stop and copy.stop:
			self.stop = copy.stop
		if not self.reference and copy.reference:
			self.reference = copy.reference
		if not self.alternate and copy.alternate:
			self.alternate = copy.alternate
		if not self.strand and copy.strand:
			self.strand = copy.strand
		if not self.sample and copy.sample:
			self.sample = copy.sample
		if not self.assembly and copy.assembly:
			self.assembly = copy.assembly
		if not self.dbsnp and copy.dbsnp:
			self.dbsnp = copy.dbsnp
			
	def printVariant(self,delim , **kwargs ):
		print "variant: " ,
		if self.gene:
			print "gene= " ,
			print self.gene + delim ,
		if self.chromosome:
			print "chromosome= " ,
			print str(self.chromosome) + delim ,
		if self.start:
			print "start= " ,
			print str(self.start) + delim ,
		if self.stop:
			print "stop= " ,
			print str(self.stop) + delim ,
		if self.reference:
			print "reference= " ,
			print self.reference + delim ,
		if self.alternate:
			print "alternate= " ,
			print self.alternate + delim ,
		if self.strand:
			print "strand= " ,
			print str(self.strand) + delim ,
		if self.dbsnp:
			print "dbsnp= " ,
			print "rs" + self.dbsnp + delim ,
		if self.sample:
			print "sample= " ,
			print self.sample + delim ,
		if self.assembly:
			print "assembly= " ,
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
	def vcf( self , **kwargs ):
		delim = kwargs.get( 'delim' , ' ' )
		nullRS = kwargs.get( 'nullrs' , "." )
		if self.dbsnp:
			return delim.join( [ self.chromosome , str( self.start ) , self.dbsnp , self.reference , self.alternate , "." , "." , "." ] )
		else:
			return delim.join( [ self.chromosome , str( self.start ) , nullRS , self.reference , self.alternate , "." , "." , "." ] )
	def vcfLine2Variant( self , record , **kwargs ):
		self.chromosome = record.CHROM
		self.start = record.CHROM
		self.stop = record.CHROM
		self.reference = record.CHROM
		alternates = record.ALT.split(',')
		if len(alternates) > 1:
			self.alternate = alt
		self.dbsnp = record.ID
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
		if self.sample:
			return self.sample + "::" + self.genomicVar()
		else:
			return "nosample::" + self.genomicVar()

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
#		print str( self.alternate ) + " vs " + str( otherVar.alternate ) ,
		if self.sameGenomicReference( otherVar ):
			if otherVar.alternate == self.alternate:
#				print "True"
				return True
#		print "False"
		return False
	def sameGenomicReference( self , otherVar ):
#		print "sameGenomicReference - " ,
#		print str( self.reference ) + " vs " + str( otherVar.reference ) ,
		if self.sameGenomicPosition( otherVar ):
			if otherVar.reference == self.reference:
#				print "True"
				return True
#		print "False"
		return False
	def sameGenomicPosition( self , otherVar ):
#		print "sameGenomicPosition - " ,
#		print str( self.chromosome ) + ":" + str( self.start ) + " vs " + str( otherVar.chromosome ) + ":" + str( otherVar.start ) ,
		if otherVar.chromosome == self.chromosome and \
			str(otherVar.start) == str(self.start):
#			print "True"
			return True
#		print "False"
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
