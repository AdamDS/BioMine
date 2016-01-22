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

	def printVariant(self,delim , **kwargs ):
		onlyMAFVariant = kwargs.get( 'MAFVariant' , False )
		super(clinvarVariant,self).printVariant( delim , **kwargs )
		if not onlyMAFVariant:
			print "clinvarVariant: " ,
			if self.uid:
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
