from biomine.variant.mafvariant import mafvariant

class clinvarvariant(mafvariant):
	pathogenic = "Pathogenic"
	likelyPathogenic = "Likely Pathogenic"
	likelyBenign = "Likely Benign"
	benign = "Benign"
	uncertain = "Uncertain Significance"
	def __init__(self , **kwargs):
		super(clinvarvariant,self).__init__(**kwargs)
		self.uid = kwargs.get('uid',None)
		self.trait = kwargs.get('trait',None)
		self.clinical = kwargs.get('clinical',{})
		aParentVariant = kwargs.get( 'parentVariant' , None )
		if aParentVariant:
			super( clinvarvariant , self ).copyInfo( aParentVariant )
	def copyInfo( self , copy ):
		super( clinvarvariant , self ).copyInfo( copy )
		self.uid = copy.uid
		self.trait = copy.trait
		self.clinical = copy.clinical
	def fillMissingInfo( self , copy ):
		#print "Variant.clinvarvariant::fillMissingInfo" ,
		super( clinvarvariant , self ).fillMissingInfo( copy )
		if not self.uid:
			try:
				self.uid = copy.uid
			except:
				print "no uid"
		if not self.trait:
			try:
				self.trait = copy.trait
			except:
				print "no trait"
		if not self.clinical:
			try:
				self.clinical = copy.clinical
			except:
				print "no clinical"

	def printVariant(self,delim , **kwargs ):
		onlyThisVariant = kwargs.get( 'minimal' , False )
		if not onlyThisVariant:
			super(clinvarvariant,self).printVariant( delim , **kwargs )
		print "clinvarvariant: { " ,
		if self.uid:
			print "uid= " ,
			print self.uid + delim ,
		if self.trait:
			print "trait=> {" ,
			for db in self.trait:
				print str(db) + "=>" + str(self.trait[db]) + delim ,
			print "}" ,
		if self.clinical:
			print "clinical=> {" ,
			print "description=>" + self.clinical["description"] + delim ,
			print "review_status=>" + self.clinical["review_status"] ,
			print "}" ,
		print " }"
	def getTraits( self , delim , **kwargs ):
		traits = []
		for trait in self.trait:
			traits.append( str( self.trait[trait] ) )
		return delim.join( traits )
	def attr(self):
		attributes = super(clinvarvariant,self).attr()
		if self.trait:
			attributes.append(self.trait)
		if self.clinical:
			attributes.append(self.clinical)
		if self.uid:
			attributes.append(self.uid)
		return attributes
	def linkPubMed( self , **kwargs ):
		base = "http://www.ncbi.nlm.nih.gov/pubmed?LinkName=clinvar_pubmed&from_uid="
		print base ,
		try:
			print str( self.uid )
			return ( base + str( self.uid ) )
		except:
			print "clinvarvariant Warning: no uid"
			return None
