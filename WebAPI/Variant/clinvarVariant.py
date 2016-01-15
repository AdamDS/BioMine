from MAFVariant import MAFVariant

class clinvarVariant(MAFVariant):
	def __init__(self , **kwargs):
		super(clinvarVariant,self).__init__(**kwargs)
		self.uid = kwargs.get('uid',None)
		self.trait = kwargs.get('trait',None)
		self.clinical = kwargs.get('clinical',None)

	def printVariant(self,delim):
		super(clinvarVariant,self).printVariant(delim)
		if self.uid:
			print self.uid + delim ,
		if self.trait:
			print self.trait + delim ,
		if self.clinical:
			print self.clinical + delim ,
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
