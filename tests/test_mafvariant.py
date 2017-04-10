import os
import sys
import unittest
from biomine.variant.mafvariant import mafvariant

class testmafvariant( unittest.TestCase ):
	def test_empty_init( self ):
		v = mafvariant()
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
		self.assertTrue( v.referencePeptide == "" )
		self.assertTrue( v.positionPeptide == None )
		self.assertTrue( v.alternatePeptide == "" )
		self.assertTrue( v.transcriptPeptide == None )
		self.assertTrue( v.positionCodon == None )
		self.assertTrue( v.transcriptCodon == None )
		self.assertTrue( v.variantClass == None )
		self.assertTrue( v.variantType == None )
		self.assertTrue( v.disease == None )

	def test_mafLine2Variant( self ):
		mafLine = "\t".join( [ \
			"BRAF" , "." , "." , "GRCh37" , "7" , "140453136" , "140453136" , \
			"+" , "Missense_Mutation" , "SNP" , "A" , "A" , "T" , \
			"rs113488022" , "." , "test-t" , "test-n" , "A" , "A" , "." , \
			"." , "." , "." , "." , "." , "." , "." , "." , "." , "." , "." , \
			"." , "c.1799T>A" , "p.Val600Glu" , "p.V600E" , \
			"ENST00000288602" , "ENSP00000288602" \
		] ) #columns in each row: 0-6	7-12	13-19	20-30	31-34	35-36
		v = mafvariant( )
		v.mafLine2Variant( mafLine , codon = 32 , peptideChange = 33 )
		self.assertTrue( v.gene == "BRAF" )
		self.assertTrue( v.chromosome == "7" )
		self.assertTrue( v.start == "140453136" )
		self.assertTrue( v.stop == "140453136" )
		self.assertTrue( v.reference == "A" )
		self.assertTrue( v.alternate == "T" )
		self.assertTrue( v.strand == "+" )
		self.assertTrue( v.sample == "test-t" )
		self.assertTrue( v.assembly == "GRCh37" )
		self.assertTrue( v.dbsnp == "rs113488022" )
		self.assertTrue( v.referencePeptide == "V" )
		self.assertTrue( v.positionPeptide == "600" )
		self.assertTrue( v.alternatePeptide == "E" )
		self.assertTrue( v.transcriptPeptide == None )
		self.assertTrue( v.positionCodon == "1799" )
		self.assertTrue( v.transcriptCodon == None )
		self.assertTrue( v.variantClass == "Missense_Mutation" )
		self.assertTrue( v.variantType == "SNP" )
		self.assertTrue( v.disease == None )

	def test_convertAA( self ):
		aa = "Glu"
		self.assertTrue( mafvariant().convertAA( aa ) == "E" )
		aa = "Ile"
		self.assertTrue( mafvariant().convertAA( aa ) == "I" )
		aa = "Ala"
		self.assertTrue( mafvariant().convertAA( aa ) == "A" )
		aa = "Ser"
		self.assertTrue( mafvariant().convertAA( aa ) == "S" )
		aa = "Gly"
		self.assertTrue( mafvariant().convertAA( aa ) == "G" )

	def test_splitHGVSp( self ):
		hgvsp = "p.Val600Glu"
		vals = mafvariant().splitHGVSp( hgvsp )
		self.assertTrue( vals[0] == "V" )
		self.assertTrue( vals[1] == "600" )
		self.assertTrue( vals[2] == "E" )
		
		hgvsp = "p.V600E"
		vals = mafvariant().splitHGVSp( hgvsp )
		self.assertTrue( vals[0] == "V" )
		self.assertTrue( vals[1] == "600" )
		self.assertTrue( vals[2] == "E" )
		
		hgvsp = "NP_004949.1:p.Glu2419Lys"
		var = mafvariant()
		vals = var.splitHGVSp( hgvsp )
		self.assertTrue( vals[0] == "E" )
		self.assertTrue( vals[1] == "2419" )
		self.assertTrue( vals[2] == "K" )
		self.assertTrue( var.referencePeptide == "E" )
		self.assertTrue( var.positionPeptide == "2419" )
		self.assertTrue( var.alternatePeptide == "K" )
		self.assertTrue( var.transcriptPeptide == "NP_004949.1" )

#EPHB2:1:23111545-23111545G>A::NM_017449.4:c.787G>A::NP_059145.2:p.V263Ile
		hgvsp = "NP_059145.2:p.V263Ile"
		var = mafvariant()
		vals = var.splitHGVSp( hgvsp )
		self.assertTrue( vals[0] == "V" )
		self.assertTrue( vals[1] == "263" )
		self.assertTrue( vals[2] == "I" )
		self.assertTrue( var.referencePeptide == "V" )
		self.assertTrue( var.positionPeptide == "263" )
		self.assertTrue( var.alternatePeptide == "I" )
		self.assertTrue( var.transcriptPeptide == "NP_059145.2" )
		#self.assertTrue( vals[0]

#COL4A5:X:107939525-107939525A>G::NM_033380.2:c.A>G::NP_203699.1:p.  --  p.?
		hgvsp = "NP_203699.1:p.?"
		var = mafvariant()
		vals = var.splitHGVSp( hgvsp )
		self.assertTrue( vals[0] == "" )
		self.assertTrue( vals[1] == "" )
		self.assertTrue( vals[2] == "" )
		self.assertTrue( var.referencePeptide == "" )
		self.assertTrue( var.positionPeptide is None )
		self.assertTrue( var.alternatePeptide == "" )
		self.assertTrue( var.transcriptPeptide == "NP_203699.1" )

#EPHB2:1:23189553-23189553G>T::NM_017449.4:c.835G>T::NP_059145.2:p.Ala279Ser
		hgvsp = "NP_059145.2:p.Ala279Ser"
		var = mafvariant()
		vals = var.splitHGVSp( hgvsp )
		self.assertTrue( vals[0] == "A" )
		self.assertTrue( vals[1] == "279" )
		self.assertTrue( vals[2] == "S" )
		self.assertTrue( var.referencePeptide == "A" )
		self.assertTrue( var.positionPeptide == "279" )
		self.assertTrue( var.alternatePeptide == "S" )
		self.assertTrue( var.transcriptPeptide == "NP_059145.2" )

	def test_splitHGVSc( self ):
		hgvsc = "NM_004958.3:c.7255G>A"				#snv coding
		var = mafvariant()
		vals = var.splitHGVSc( hgvsc )
		self.assertTrue( vals[0] == "G" )
		self.assertTrue( vals[1] == "7255" )
		self.assertTrue( vals[2] == "A" )
		self.assertTrue( var.reference == "-" )
		self.assertTrue( var.positionCodon == "7255" )
		self.assertTrue( var.alternate == "-" )
		self.assertTrue( var.transcriptCodon == "NM_004958.3" )
		
		hgvsc = "NM_004958.3:c.7255G>A"				#snv coding
		var = mafvariant()
		vals = var.splitHGVSc( hgvsc , override = True )
		self.assertTrue( vals[0] == "G" )
		self.assertTrue( vals[1] == "7255" )
		self.assertTrue( vals[2] == "A" )
		self.assertTrue( var.reference == "G" )
		self.assertTrue( var.positionCodon == "7255" )
		self.assertTrue( var.alternate == "A" )
		self.assertTrue( var.transcriptCodon == "NM_004958.3" )
		
	def test_splitSNVHGVSc( self ):
		"""
		Substitutions
		c.76A>C
		c.-14G>C denotes a G to C substitution 14 nucleotides 5' of the ATG translation initiation codon
		c.88+1G>T denotes the G to T substitution at nucleotide +1 of an intron (in the coding DNA positioned between nucleotides 88 and 89)
		c.89-2A>C denotes the A to C substitution at nucleotide -2 of an intron (in the coding DNA positioned between nucleotides 88 and 89)
		c.*46T>A denotes a T to A substitution 46 nucleotides 3' of the translation termination codon
		"""
		hgvsc = "1799T>A"								#snv coding
		vals = mafvariant().splitSNVHGVSc( hgvsc )
		self.assertTrue( vals[0] == "T" )
		self.assertTrue( vals[1] == "1799" )
		self.assertTrue( vals[2] == "A" )

		hgvsc = "1290-2A>C"							#snv non-coding
		vals = mafvariant().splitSNVHGVSc( hgvsc , noncoding = True )
		self.assertTrue( vals[0] == "A" )
		self.assertTrue( vals[1] == "1290-2" )
		self.assertTrue( vals[2] == "C" )

		hgvsc = "2301+15A>C"							#snv non-coding
		vals = mafvariant().splitSNVHGVSc( hgvsc , noncoding = True )
		self.assertTrue( vals[0] == "A" )
		self.assertTrue( vals[1] == "2301+15" )
		self.assertTrue( vals[2] == "C" )

		hgvsc = "-14G>C"							#snv non-coding
		vals = mafvariant().splitSNVHGVSc( hgvsc , noncoding = True )
		self.assertTrue( vals[0] == "G" )
		self.assertTrue( vals[1] == "-14" )
		self.assertTrue( vals[2] == "C" )

		hgvsc = "*46T>A"							#snv non-coding
		vals = mafvariant().splitSNVHGVSc( hgvsc , noncoding = True )
		self.assertTrue( vals[0] == "T" )
		self.assertTrue( vals[1] == "*46" )
		self.assertTrue( vals[2] == "A" )

	def test_splitComplexHGVSc( self ):
		#c.112_117delinsTG (alternatively c.112_117delAGGTCAinsTG) denotes the replacement of nucleotides 112 to 117 (AGGTCA) by TG
		hgvsc = "5077_5080delGCTGinsTTGATTCTGC"		#complex coding del ins
		vals = mafvariant().splitComplexHGVSc( hgvsc , multiple = True )
		self.assertTrue( vals[0] == "GCTG" )
		self.assertTrue( vals[1] == "5077" )
		self.assertTrue( vals[2] == "TTGATTCTGC" )

		#c.113delinsTACTAGC (alternatively c.113delGinsTACTAGC) denotes the replacement of nucleotide 113 by 7 new nucleotides (TACTACG)
		#c.114_115delinsA (alternative c.[114G>A; 115delT])
		hgvsc = "3672+5_3672+11delTGCTTTTinsG"		#complex non-coding del ins
		vals = mafvariant().splitComplexHGVSc( hgvsc , multiple = True )
		self.assertTrue( vals[0] == "TGCTTTT" )
		self.assertTrue( vals[1] == "3672+5" )
		self.assertTrue( vals[2] == "G" )

		hgvsc = "48+6_48+7delinsTT"					#complex non-coding delins
		vals = mafvariant().splitComplexHGVSc( hgvsc , multiple = True , null = "-" )
		self.assertTrue( vals[0] == "-" )
		self.assertTrue( vals[1] == "48+6" )
		self.assertTrue( vals[2] == "TT" )

	def test_splitInsertionHGVSc( self ):
		"""
		Insertions
		c.76_77insT denotes that a T is inserted between nucleotides 76 and 77 of the coding DNA reference sequence
		c.123+54_123+55insAB012345.2:g.76_420 denotes an intronic insertion ( between nucleotides c.123+54 and 123+55) of 345 nucleotides (nucleotides 76 to 420 like in GenBank file AB012345 version 2)
		NOTE: descriptions like c.123+54_123+55ins345 and c.123+54_123+55insAlu are not allowed: "ins345" and "insAlu" are not specified and the description can not be used to reconstruct the exact change described.
		"""
		hgvsc = "62insC"								#ins coding single
		vals = mafvariant().splitInsertionHGVSc( hgvsc , null = "-" )
		self.assertTrue( vals[0] == "-" )
		self.assertTrue( vals[1] == "62" )
		self.assertTrue( vals[2] == "C" )

		hgvsc = "577_580insAAAC"						#ins coding multiple
		vals = mafvariant().splitInsertionHGVSc( hgvsc , multiple = True , null = "-" )
		self.assertTrue( vals[0] == "-" )
		self.assertTrue( vals[1] == "577" )
		self.assertTrue( vals[2] == "AAAC" )

		hgvsc = "3672+5insT"							#ins non-coding
		vals = mafvariant().splitInsertionHGVSc( hgvsc , null = "-" )
		self.assertTrue( vals[0] == "-" )
		self.assertTrue( vals[1] == "3672+5" )
		self.assertTrue( vals[2] == "T" )

		hgvsc = "-115insG"							#ins upstream
		vals = mafvariant().splitInsertionHGVSc( hgvsc , null = "-" )
		self.assertTrue( vals[0] == "-" )
		self.assertTrue( vals[1] == "-115" )
		self.assertTrue( vals[2] == "G" )

		hgvsc = "*226_*229insCTTA"					#ins 3' UTR
		vals = mafvariant().splitInsertionHGVSc( hgvsc , multiple = True , null = "-" )
		self.assertTrue( vals[0] == "-" )
		self.assertTrue( vals[1] == "*226" )
		self.assertTrue( vals[2] == "CTTA" )

	def test_splitDeletionHGSVc( self ):
		"""
		Deletions
		c.76_78del (alternatively c.76_78delACT)
		uncharacterised breakpoints
		c.(87+1_88-1)_(923+1_924-1)del denotes a deletion starting at an unknown 
			position in intron 2 between coding DNA nucleotides 87+1 and 88-1, 
			and ending at an unknown position between coding DNA nucleotides 
			923+1 and 924-1
		c.(?_-30)_(*220_?)del denotes the deletion of the entire gene
		c.88+101_oGJB2:c.355-1045del denotes a deletion which ends in the 
			flanking GJB2 gene at position 355-1045 (in the intron between 
			nucleotides 354 and 355) on the reverse strand (the genes are thus 
			located and fused in opposite transcriptional directions, see 
			Discussion)
		for all descriptions the most 3' position possible is arbitrarily assigned to have been changed (see FAQ);
		ACTTTGTGCC to ACTTGCC is described as c.5_7del (c.5_7delTGT, not as c.4_6delTTG)
		ctttagGCATG to cttagGCATG in an intron is described as c.301-3delT (not as c.301-5delT)
		TCACTGTCTGCGGTAATC to TCACTG CGGTAATC is described as c.7_10del (c.7_10delTCTG) and not as c.4_7del (c.4_7delCTGT).
		AAAGAAGAGGAG to AAAG GAG is described as c.5_9del (c.5_9delAAGAG) and not as c.3_7del (c.3_7delAGAAG)
		Exceptions
		using a coding DNA reference sequence there is an exception to the rule around exon/intron and exon/exon borders when identical nucleotides flank the exon/intron or exon/exon border;
		when the exon 3/intron 3 border is ..CAGgtg.. and RNA analysis shows no effect on splicing but a deletion of a G the change ..CAGgtg.. to ..CAgtg.. is described as c.3delG and not c.3+1delG.
		when exon 3 ends with ..CAA.. and exon 4 starts with ..ACG.. and the sequence of genomic DNA shows that the last A-nucleotide of exon 3 is deleted (and not the first A-nucleotide in exon 4), the deletion changing ..CAAACG.. to ..CAACG.. is described as c.3delA and not c.4delA
		c.1210-12T(5_9) (not c.1210-6T(5_9)) describes the variable stretch of 5 to 9 T-residues in intron 9 of the CFTR gene. The most commonly used CFTR coding DNA reference sequence contains a stretch of 7 T's (see Repeated sequences). 
		"""
		hgvsc = "62delC"								#del coding single
		vals = mafvariant().splitDeletionHGVSc( hgvsc , null = "-" )
		self.assertTrue( vals[0] == "C" )
		self.assertTrue( vals[1] == "62" )
		self.assertTrue( vals[2] == "-" )

		hgvsc = "577_580delAAAC"						#del coding multiple
		vals = mafvariant().splitDeletionHGVSc( hgvsc , multiple = True , null = "-" )
		self.assertTrue( vals[0] == "AAAC" )
		self.assertTrue( vals[1] == "577" )
		self.assertTrue( vals[2] == "-" )

		hgvsc = "3672+5delT"							#del non-coding
		vals = mafvariant().splitDeletionHGVSc( hgvsc , null = "-" )
		self.assertTrue( vals[0] == "T" )
		self.assertTrue( vals[1] == "3672+5" )
		self.assertTrue( vals[2] == "-" )

		hgvsc = "-115delG"							#del upstream
		vals = mafvariant().splitDeletionHGVSc( hgvsc , null = "-" )
		self.assertTrue( vals[0] == "G" )
		self.assertTrue( vals[1] == "-115" )
		self.assertTrue( vals[2] == "-" )

		hgvsc = "*226_*229delCTTA"					#del 3' UTR
		vals = mafvariant().splitDeletionHGVSc( hgvsc , multiple = True , null = "-" )
		self.assertTrue( vals[0] == "CTTA" )
		self.assertTrue( vals[1] == "*226" )
		self.assertTrue( vals[2] == "-" )

#	def test_splitDuplicationHGVSc( self ):
#		"""
#		Duplications
#		duplicating insertions should be described as duplications (see Discussion)
#		g.7_8[4] (or g.5_6[4], or g.5TG[4], not g.7_10dup) is the preferred description of  the addition of two extra TG's to the variable TG repeated sequence changing ACTTTGTGCC to ACTTTGTGTGTGCC (see Repeated sequences)
#		duplications with uncharacterised breakpoints (see Uncertainties)
#		c.(87+1_88-1)_(301+1_302-1)dup denotes a duplication of exons 3 to 4 starting at an unknown position in intron 2 (between coding DNA nucleotides 87+1 and 88-1) and ending at an unknown position in intron 5 (between coding DNA nucleotides 301+1 and 302-1). The description indicates that exons 2 and 5 have been tested and shown not to be duplicated
#		NOTE: the description c.88-?_301+?dup does not specify start/end of the duplication and is not correct when flanking sequences have been tested (see Uncertainties)
#		NOTE: the description "dup" (see Standards) may by definition only be used when the additional copy is directly 3'-flanking of the original copy (tandem duplication). In many cases there will be no experimental proof, the additional copy may be anywhere in the genome (i.e. inserted). (see Recommendations).
#		c.(1031+1_1032-1)_(1357+1_1358+1)[3]  denotes a direct triplication of an exon, starting at an unknown position in the flanking upstream intron (upstream of coding DNA nucleotide 1032) and ending at an unknown position in the flanking downstram intron (downstream of coding DNA nucleotide 1357) (see Repeated sequences)
#		"""
#		print( "Duplication" )
#		hgvsc = "c.1270-6_1270-5dupCT"					#dup non-coding/intronic
#		vals = mafvariant().splitDuplicationHGVSc( hgvsc )
#		print( vals )
#		self.assertTrue( vals[0] == "-" )
#		self.assertTrue( vals[1] == "1270-6" )
#		self.assertTrue( vals[2] == "CT" )
#
#		#g.5dupT (or g.5dup, not g.5_6insT) denotes a duplication of T at position 5
#		hgvsc = "c.450dupC"								#dup coding single
#		vals = mafvariant().splitDuplicationHGVSc( hgvsc )
#		print( vals )
#		self.assertTrue( vals[0] == "-" )
#		self.assertTrue( vals[1] == "450" )
#		self.assertTrue( vals[2] == "C" )
#
#		#g.7_8dup (or g.7_8dupTG, not g.5_6dup, not g.8_9insTG) denotes a TG duplication
#		#c.77_79dup (or c.77_79dupCTG) denotes that the three nucleotides 77 to 79 are duplicated (present twice)
#		hgvsc = "c.38_40dupAAT"							#dup coding multiple
#		vals = mafvariant().splitDuplicationHGVSc( hgvsc )
#		print( vals )
#		self.assertTrue( vals[0] == "-" )
#		self.assertTrue( vals[1] == "38" )
#		self.assertTrue( vals[2] == "AAT" )
#
#	def test_splitInversionHGVSc( self ):
#		"""
#		Inversions
#		c.203_506inv denotes that the 304 nucleotides from position 203 to 506 have been inverted
#		"""
#		print( "Inversion" )
#		hgvsc = "c.1374_1375invAG"						#inv coding multiple
#		vals = mafvariant().splitInversionHGVSc( hgvsc )
#		print( vals )
#		self.assertTrue( vals[0] == "GA" )
#		self.assertTrue( vals[1] == "1374" )
#		self.assertTrue( vals[2] == "AG" )
#
#		hgvsc = "c.3296+9_3296+10invCA"					#inv non-coding multiple
#		vals = mafvariant().splitInversionHGVSc( hgvsc )
#		print( vals )
#		self.assertTrue( vals[0] == "-" )
#		self.assertTrue( vals[1] == "38" )
#		self.assertTrue( vals[2] == "AAT" )
#
#		hgvsc = "c.*2288_*2289invTG"					#inv non-coding multiple
#		vals = mafvariant().splitInversionHGVSc( hgvsc )
#		print( vals )
#		self.assertTrue( vals[0] == "-" )
#		self.assertTrue( vals[1] == "38" )
#		self.assertTrue( vals[2] == "AAT" )
#
if __name__ == '__main__':
	unittest.main()
