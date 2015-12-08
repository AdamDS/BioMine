class variant(object):
	def __init__(self,**kwargs):
		self.gene = kwargs.get('gene',None)
		self.chromosome = kwargs.get('chromosome',None)
		self.start = kwargs.get('start',None)
		self.stop = kwargs.get('stop',None)
		self.reference = kwargs.get('reference',None)
		self.change = kwargs.get('change',None)
		self.HGVSp = kwargs.get('HGVSp',None)
		self.transcript = kwargs.get('transcript',None)
	def printVariant(self,delim):
		if self.gene != None:
			print self.gene + delim ,
		if self.chromosome != None:
			print str(self.chromosome) + delim ,
		if self.start != None:
			print str(self.start) + delim ,
		if self.stop != None:
			print str(self.stop) + delim ,
		if self.reference != None:
			print self.reference + delim ,
		if self.change != None:
			print self.change + delim ,
		if self.HGVSp != None:
			print self.HGVSp + delim ,
		if self.transcript != None:
			print self.transcript + delim ,
		print ""
	def attr(self):
		attributes = []
		if self.gene != None:
			attributes.append(self.gene)
		if self.chromosome != None:
			attributes.append(self.chromosome)
		if self.start != None:
			attributes.append(self.start)
		if self.stop != None:
			attributes.append(self.stop)
		if self.reference != None:
			attributes.append(self.reference)
		if self.change != None:
			attributes.append(self.change)
		if self.HGVSp != None:
			attributes.append(self.HGVSp)
		if self.transcript != None:
			attributes.append(self.transcript)
		return attributes

	def readVariants(self,inputFile):
		variants = []
		if inputFile:
			inFile = open( inputFile , 'r' )
			for line in inFile:
				fields = line.split( '\t' )
				variants.append( fields[0] + ":" + fields[1] )
		return variants

'''
mu = variant(gene="BRAF",chromosome=7,start=12345,stop=123456,reference="AT",change="GC",HGVSp="p.A123R")
mu.printVariant('\t')
nu = variant(gene="BRAF",HGVSp="p.A123R")
nu.printVariant('\t')
ou = variant(gene="BRAF",chromosome=7,start=12345,stop=123456,reference="AT",change="GC")
ou.printVariant('\t')
pu = variant(chromosome=7,start=12345,stop=123456,reference="AT",change="GC")
pu.printVariant('\t')
qu = variant(chromosome=7,start=12345,reference="AT",change="GC")
qu.printVariant('\t')

print qu.attr()
'''
