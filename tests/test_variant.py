import os
import sys
import unittest
from biomine.variant.variant import variant

class testbreakteststeps( unittest.TestCase ):
	def test_empty_init( self ):
		v = variant()
		self.assertTrue( v.gene == "" )
		self.assertTrue( v.chromosome == None )
		self.assertTrue( v.start == None )
		self.assertTrue( v.stop == None )
		self.assertTrue( v.reference == "-" )
		self.assertTrue( v.alternate == "-" )
		self.assertTrue( v.strand == "+" )
		self.assertTrue( v.sample == None )
		self.assertTrue( v.assembly == None )
		self.assertTrue( v.dbsnp == None )

#	def test_setStrand( self ):
#		v = variant()
#		self.assertTrue( v.strand == "+" )
#		v.setStrand( -1 )
#		self.assertTrue( v.strand == "-" )
#		v.setStrand( 1 )
#		self.assertTrue( v.strand == "+" )

	def test_sameGenomicPosition( self ):
		v = variant( chromosome = 3 , start = 6 )
		w = variant( chromosome = 3 , start = 6 )
		self.assertTrue( v.sameGenomicPosition( w ) )
		w.chromosome = 4
		self.assertFalse( v.sameGenomicPosition( w ) )
		w.start = 9
		self.assertFalse( v.sameGenomicPosition( w ) )
		w.chromosome = 3 
		w.start = 9
		self.assertFalse( v.sameGenomicPosition( w ) )

if __name__ == '__main__':
	unittest.main()
