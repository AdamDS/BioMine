from WebAPI.Variant.MAFVariant import MAFVariant

class clinvarVariant(MAFVariant):
	pathogenic = "Pathogenic"
	likelyPathogenic = "Likely Pathogenic"
	likelyBenign = "Likely Benign"
	benign = "Benign"
	uncertain = "Uncertain Significance"
	def __init__(self , **kwargs):
		super(clinvarVariant,self).__init__(**kwargs)
		self.uid = kwargs.get('uid',None)
		self.trait = kwargs.get('trait',None)
		self.clinical = kwargs.get('clinical',{})
		aParentVariant = kwargs.get( 'parentVariant' , None )
		if aParentVariant:
			super( clinvarVariant , self ).copyInfo( aParentVariant )
	def copyInfo( self , copy ):
		super( clinvarVariant , self ).copyInfo( copy )
		self.uid = copy.uid
		self.trait = copy.trait
		self.clinical = copy.clinical
	def fillMissingInfo( self , copy ):
		if type( self ) == clinvarVariant:
			print self.mro()
			super( clinvarVariant , self ).fillMissingInfo( copy )
		else:
			MAFVariant.fillMissingInfo( self , copy )
		if not self.uid and copy.uid:
			self.uid = copy.uid
		if not self.trait and copy.trait:
			self.trait = copy.trait
		if not self.clinical and copy.clinical:
			self.clinical = copy.clinical

	def printVariant(self,delim , **kwargs ):
		onlyThisVariant = kwargs.get( 'minimal' , False )
		if not onlyThisVariant:
			super(clinvarVariant,self).printVariant( delim , **kwargs )
		print "clinvarVariant: " ,
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
		print ""
	def attr(self):
		attributes = super(clinvarVariant,self).attr()
		if self.trait:
			attributes.append(self.trait)
		if self.clinical:
			attributes.append(self.clinical)
		if self.uid:
			attributes.append(self.uid)
		return attributes
