import os
import sys
import pdb
import unittest
from biomine.webapi import webapi

class testwebapi( unittest.TestCase ):
	def test_empty_init( self ):
		e = webapi()
		self.assertFalse( e )

if __name__ == '__main__':
	unittest.main()
