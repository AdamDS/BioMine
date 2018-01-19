import os
import sys
import pdb
import unittest
from biomine.variant.vepvariant import vepvariant

class testvepvariant( unittest.TestCase ):
	def test_empty_init( self ):
		v = vepvariant()
		self.assertFalse( v )

if __name__ == '__main__':
	unittest.main()
