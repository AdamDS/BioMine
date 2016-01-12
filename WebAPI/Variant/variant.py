import re
class variant(object):
	def __init__(self,**kwargs):
		self.gene = kwargs.get('gene',None)
		self.chromosome = kwargs.get('chromosome',None)
		self.start = kwargs.get('start',None)
		self.stop = kwargs.get('stop',None)
		self.reference = kwargs.get('reference',None)
		self.mutant = kwargs.get('mutant',None)
		self.strand = kwargs.get('strand',None)
		self.sample = kwargs.get('sample',None)
		self.positionPeptide = kwargs.get('positionPeptide',None)
		self.referencePeptide = kwargs.get('referencePeptide',None)
		self.mutantPeptide = kwargs.get('mutantPeptide',None)
		self.transcript = kwargs.get('transcript',None)
		self.assembly = kwargs.get('assembly',None)
		self.variantClass = kwargs.get('variantClass',None)
		self.variantType = kwargs.get('variantType',None)
		self.dbsnp = kwargs.get('dbsnp',None)
	def printVariant(self,delim):
		#for attr in self.attr():
		#	print str(attr) + delim
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
		if self.positionPeptide:
			print self.positionPeptide + delim ,
		if self.referencePeptide:
			print self.referencePeptide + delim ,
		if self.mutantPeptide:
			print self.mutantPeptide + delim ,
		if self.transcript:
			print self.transcript + delim ,
		if self.assembly:
			print self.assembly + delim ,
		if self.variantClass:
			print self.variantClass + delim ,
		if self.variantType:
			print self.variantType + delim ,
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
		if self.positionPeptide:
			attributes.append(self.positionPeptide)
		if self.referencePeptide:
			attributes.append(self.referencePeptide)
		if self.mutantPeptide:
			attributes.append(self.mutantPeptide)
		if self.transcript:
			attributes.append(self.transcript)
		return attributes
	def genomicVar( self ):
		return self.chromosome + ":" + self.start + "-" + self.stop + self.reference + ">" + self.mutant
	def HGVSp( self ):
		if self.gene and self.referencePeptide:
			return self.gene + ":p." + self.referencePeptide + self.positionPeptide + self.mutantPeptide
	def HGVSc( self ):
		if self.gene and self.referencePeptide:
			return self.gene + ":c." + self.codonPosition + self.reference + ">" + self.mutant
	def mafLine2Variant( self , line ):
		fields = line.split( "\t" )
		self.gene = fields[0]	#1	Hugo_Symbol
		self.chromosome = fields[4]	#5	Chromosome
		self.start = fields[5]	#6	Start_Position
		self.stop = fields[6]	#7	End_Position
		self.strand = fields[7]	#8	Strand
		self.variantClass = fields[8]	#9	Variant_Classification
		self.variantType = fields[9]	#10	Variant_Type
		self.reference = fields[10]	#11	Reference_Allele
		self.mutant = fields[11] if fields[11] != fields[10] else fields[12]	#12	Tumor_Seq_Allele1	#13	Tumor_Seq_Allele2
		self.dbsnp = fields[13]
		self.sample = fields[15]
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
			self.mutantPeptide = mut
		return { "referencePeptide" : ref , "positionPeptide" : pos , "mutantPeptide" : mut }
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
mu = variant(gene="BRAF",chromosome=7,start=12345,stop=123456,reference="AT",mutant="GC",referencePeptide="A123R")
mu.printVariant('\t')
nu = variant(gene="BRAF",referencePeptide="A123R")
nu.printVariant('\t')
ou = variant(gene="BRAF",chromosome=7,start=12345,stop=123456,reference="AT",mutant="GC")
ou.printVariant('\t')
pu = variant(chromosome=7,start=12345,stop=123456,reference="AT",mutant="GC")
pu.printVariant('\t')
qu = variant(chromosome=7,start=12345,reference="AT",mutant="GC")
qu.printVariant('\t')

print qu.attr()
'''
