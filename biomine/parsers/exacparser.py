#!/usr/bin/python
# ExAC Parser - 
# author: Adam D Scott (adamscott@wustl.edu)
# version: v0.0 - 2016*05*18
# AC=38,2;AC_AFR=1,0;AC_AMR=0,0;AC_Adj=5,0;AC_EAS=0,0;AC_FIN=0,0;AC_Het=5,0,0;AC_Hom=0,0;AC_NFE=3,0;AC_OTH=0,0;AC_SAS=1,0;AF=3.200e-04,1.684e-05;AN=118764;AN_AFR=2366;AN_AMR=2222;AN_Adj=28902;AN_EAS=1822;AN_FIN=600;AN_NFE=13932;AN_OTH=268;AN_SAS=7692;

from biomine.variant.clinvarvariant import clinvarvariant
from biomine.variant.vepvariant import vepvariant
from biomine.variant.vepconsequencevariant import vepconsequencevariant
from biomine.variant.mafvariant import mafvariant
from biomine.variant.variant import variant
from biomine.variant.exacvariant import exacvariant
import vcf
import re

class exacparser(object):
	''' Example usage:
			vars = exacvariants()
			vars.getInputData( vcf=file )
	'''
	def __init__( self , **kwargs ):
		self.variants = kwargs.get( 'variants' , [] )
		#self.clinvarVariants = kwargs.get( 'clinvarVariants' , {} )
		self.vcfHeaderInfo = kwargs.get( 'vcfHeaderInfo' , [] )
		self.vcfKeyIndex = kwargs.get( 'vcfKeyIndex' , {} )

### Retrieve input data from user ###
	def getInputData( self  , **kwargs ):
		vcfFile = kwargs.get( 'vcf' , "" )
		preVEP = []
		vepDone = False
		exacDone = False
		if vcfFile:
			vepDone = self.readVCF( vcfFile , **kwargs )
			exacDone=False # currently only has 1000G

	def readVCF( self , inputFile , **kwargs ):
		writeToFile = kwargs.get( 'writeToFile' , "" )
		splitByChromosome = kwargs.get( 'splitByChromosome' , True )
		outFH = None
		inFile = None;
		if ( re.match( "\.gz" , inputFile ) ):
			inFile = vcf.Reader( open( inputFile , 'r' ) , compressed=True )
		else:
			inFile = vcf.Reader( open( inputFile , 'r' ) )
		preVEP = []
		vepDone = False
		#vepInfo = OD()
		self.vcfHeaderInfo = []
		metadata = inFile.metadata
		for pairs in metadata:
			if pairs == 'VEP':
				print "This .vcf has VEP annotations!"
				infos = inFile.infos
				for info_ID in infos.items():
					if info_ID[0] == "CSQ": #CSQ tag the VEP annotation, probably means consequence
						csq = info_ID
						Info = csq[1] #Info(...)
						if Info:
							desc = Info[3] #Consequence type...Format: Allele|Gene|...
							keysString = desc.split( "Format: " )[1]
							self.vcfHeaderInfo = keysString.split( "|" )
							self.vcfKeyIndex = {}
							i = 0
							for key in self.vcfHeaderInfo:
								#print str(i) + " => " + key
								#vepInfo[key] = None
								self.vcfKeyIndex[key] = i
								i = i + 1
		for record in inFile:
			chrom = record.CHROM
			reference = record.REF
			alternates = record.ALT
			start = record.start + 1 #1-base beginning of ref
			stop = record.end #0-base ending of ref
			info = record.INFO
			alti = -1
			for alternate in alternates:
				alti += 1
				alt = str( alternate )
				if alt == "None":
					alt = None
				if record.is_indel and not record.is_deletion: #insertion
					reference = "-"
					alt = alt[1:len(alt)]
					stop = stop + 1
				elif record.is_deletion:
					reference = reference[1:len(reference)] #assumes only one base overlap
					alt = "-"
					start = start + 1
					stop = stop

				parentVar = variant( \
					chromosome = chrom , \
					start = start , \
					stop = stop , \
					dbsnp = record.ID , \
					reference = reference , \
					alternate = alt , \
				)

				var = exacvariant( \
					parentVariant=parentVar
				)
				#"""
				csq = info.get( 'CSQ' , "noCSQ" )
				if not csq == "noCSQ":
					vepDone = True
					exacDone = True
					var.vepVariant = vepvariant()
					for thisCSQ in csq:
						values = thisCSQ.split( "|" )
						var.vcfInfo = values
						aas = [None , None] 
						if self.getVCFKeyIndex( values , "Amino_acids" ): #8 => Amino_acids
							aas = self.getVCFKeyIndex( values , "Amino_acids" ).split("/") 
							if len( aas ) > 1:
								aas[0] = mafvariant().convertAA( aas[0] )
								aas[1] = mafvariant().convertAA( aas[1] )
							else:
								#28 => HGVSc
								#29 => HGVSp
								hgvsp = self.getVCFKeyIndex( values , "HGVSp" ).split( ":" )
								changep = None
								if len( hgvsp ) > 1:
									changep = re.match( "p\." , hgvsp[1] )
								if changep:
									aas = mafvariant().splitHGVSp( hgvsp[1] )
									aas[0] = mafvariant().convertAA( aas[0] )
									aas[2] = mafvariant().convertAA( aas[2] )
								else:
									aas.append( None )
									needVEP = True
									preVEP.append( var )
						exons = [None , None]
						if self.getVCFKeyIndex( values , "EXON" ): #25 => EXON
							exons = self.getVCFKeyIndex( values , "EXON" ).split( "/" )
							if len( exons ) == 1:
								exons.append(None)
						introns = [None , None]
						if self.getVCFKeyIndex( values , "INTRON" ): #26 => INTRON
							introns = self.getVCFKeyIndex( values , "INTRON" ).split( "/" )
							if len( introns ) == 1:
								introns.append(None)
						siftStuff = [None , None]
						if self.getVCFKeyIndex( values , "SIFT" ):
							siftStuff = self.getVCFKeyIndex( values , "SIFT" ).split( "(" ) 
							if len( siftStuff ) == 1:
								siftStuff.append( None )
							else:
								siftStuff[1] = siftStuff[1].rstrip( ")" )
						polyPhenStuff = [None , None]
						if self.getVCFKeyIndex( values , "PolyPhen" ):
							polyPhenStuff = self.getVCFKeyIndex( values , "PolyPhen" ).split( "(" ) 
							if len( polyPhenStuff ) == 1:
								polyPhenStuff.append( None )
							else:
								polyPhenStuff[1] = polyPhenStuff[1].rstrip( ")" )

						vcv = vepconsequencevariant( \
							chromosome = chrom , \
							start = start , \
							stop = stop , \
							dbsnp = record.ID , \
							reference = reference , \
							alternate = alt , \
							gene_id=self.getVCFKeyIndex( values , "Gene" ) , \
							transcriptCodon=self.getVCFKeyIndex( values , "Feature" ) , \
							consequence_terms=self.getVCFKeyIndex( values , "Consequence" ).split( "&" ) , \
							positionCodon=self.getVCFKeyIndex( values , "cDNA_position" ) , \
							positionPeptide=self.getVCFKeyIndex( values , "Protein_position" ) , \
							referencePeptide=aas[0] , \
							alternatePeptide=aas[1] , \
							strand=self.getVCFKeyIndex( values , "STRAND" ) , \
							gene=self.getVCFKeyIndex( values , "SYMBOL" ) , \
							gene_symbol_source=self.getVCFKeyIndex( values , "SYMBOL_SOURCE" ) , \
							hgnc_id=self.getVCFKeyIndex( values , "HGNC_ID" ) , \
							biotype=self.getVCFKeyIndex( values , "BIOTYPE" ) , \
							canonical=self.getVCFKeyIndex( values , "CANONICAL" ) , \
							ccds=self.getVCFKeyIndex( values , "CCDS" ) , \
							transcriptPeptide=self.getVCFKeyIndex( values , "ENSP" ) , \
							predictionSIFT=siftStuff[0] , \
							scoreSIFT=siftStuff[1] , \
							predictionPolyphen=polyPhenStuff[0] , \
							scorePolyphen=polyPhenStuff[1] , \
							exon=exons[0] , \
							totalExons=exons[1] , \
							intron=introns[0] , \
							totalIntrons=introns[1] , \
						)

						var.alleleFrequency = self.getVCFKeyIndex( values , "GMAF" )
						var.vepVariant.consequences.append( vcv )

				severeRank = [ 	"transcript_ablation" , \
								"splice_acceptor_variant" , \
								"splice_donor_variant" , \
								"stop_gained" , \
								"frameshift_variant" , \
								"stop_lost" , \
								"start_lost" , \
								"transcript_amplification" , \
								"inframe_insertion" , \
								"inframe_deletion" , \
								"missense_variant" , \
								"protein_altering_variant" , \
								"splice_region_variant" , \
								"incomplete_terminal_codon_variant" , \
								"stop_retained_variant" , \
								"synonymous_variant" , \
								"coding_sequence_variant" , \
								"mature_miRNA_variant" , \
								"5_prime_UTR_variant" , \
								"3_prime_UTR_variant" , \
								"non_coding_transcript_exon_variant" , \
								"intron_variant" , \
								"NMD_transcript_variant" , \
								"non_coding_transcript_variant" , \
								"upstream_gene_variant" , \
								"downstream_gene_variant" , \
								"TFBS_ablation" , \
								"TFBS_amplification" , \
								"TF_binding_site_variant" , \
								"regulatory_region_ablation" , \
								"regulatory_region_amplification" , \
								"feature_elongation" , \
								"regulatory_region_variant" , \
								"feature_truncation" , \
								"intergenic_variant" ]

				mostSevere = None
				rankMostSevere = 10000
				mostSevereCons = severeRank[-1]
				for cons in var.vepVariant.consequences:
					for term in cons.terms:
						if term in severeRank:
							rank = severeRank.index( term )
						else:
							rank = 10000
						if rank < rankMostSevere:
							mostSevere = cons
							rankMostSevere = rank
							mostSevereCons = term
						elif rank == rankMostSevere:
							if cons.canonical:
								mostSevere = cons

				self.setMostSevere( var , mostSevere , mostSevereCons )
				#"""
				self.setAlleleMeasures( var , info , alti = alti , **kwargs )
			
				if ( writeToFile ):
					if ( splitByChromosome ):
						outFH = open( writeToFile + ".chr" + str( var.chromosome ) + ".tsv" , 'w' )
					else:
						outFH = open( writeToFile + ".tsv" , 'w' )
					outFH.write( "Chromosome\tStart\tStop\tReference\tAlternate\t" \
						+ "Frequency\t" \
						+ "AC_AFR\tAC_AMR\tAC_EAS\tAC_FIN\tAC_NFE\tAC_OTH\tAC_SAS\t" \
						+ "AC_Adj\tAC_Het\tAC_Hom\t" \
						+ "AN_AFR\tAN_AMR\tAN_EAS\tAN_FIN\tAN_NFE\tAN_OTH\tAN_SAS\tAN_Adj\t" \
						+ "Gene\tENST_ID\tENSP_ID\tReference_Peptide\tPosition_Peptide\tAlternate_Peptide\n" )
					self.writeField( outFH , var.chromosome )
					self.writeField( outFH , var.start )
					self.writeField( outFH , var.stop )
					self.writeField( outFH , var.reference )
					self.writeField( outFH , var.alternate )
					self.writeField( outFH , var.frequency )
					self.writeField( outFH , var.counts.afr )
					self.writeField( outFH , var.counts.amr )
					self.writeField( outFH , var.counts.eas )
					self.writeField( outFH , var.counts.fin )
					self.writeField( outFH , var.counts.nfe )
					self.writeField( outFH , var.counts.oth )
					self.writeField( outFH , var.counts.sas )
					self.writeField( outFH , var.counts.adj )
					self.writeField( outFH , var.counts.het )
					self.writeField( outFH , var.counts.hom )
					self.writeField( outFH , var.numbers.afr )
					self.writeField( outFH , var.numbers.amr )
					self.writeField( outFH , var.numbers.eas )
					self.writeField( outFH , var.numbers.fin )
					self.writeField( outFH , var.numbers.nfe )
					self.writeField( outFH , var.numbers.oth )
					self.writeField( outFH , var.numbers.sas , last=True )
				else:
					self.variants.append( var )

		if ( outFH ):
			outFH.close()
		return None

	def getVCFKeyIndex( self , values , field ):
		if field in self.vcfKeyIndex:
			return values[self.vcfKeyIndex[field]]
		return None

	def setAlleleMeasures( self , var , info , **kwargs ):
		self.setCounts( var , info , **kwargs )
		self.setNumbers( var , info , **kwargs )
		self.setFrequency( var , info , **kwargs )

	@staticmethod
	def setMostSevere( var , mostSevere , mostSevereCons , **kwargs ):
		if mostSevere:
			var.gene = mostSevere.gene
			var.referencePeptide = mostSevere.referencePeptide
			var.positionPeptide = mostSevere.positionPeptide
			var.alternatePeptide = mostSevere.alternatePeptide
			var.transcriptPeptide = mostSevere.transcriptPeptide
			var.transcriptCodon = mostSevere.transcriptCodon
			var.positionCodon = mostSevere.positionCodon
			var.vepVariant.mostSevereConsequence = mostSevereCons
			var.variantClass = mostSevereCons
		return var
	
	@staticmethod
	def setCounts( var , info , **kwargs ):
		var.setCounts( info , **kwargs )
	
	@staticmethod
	def setNumbers( var , info , **kwargs ):
		var.setNumbers( info , **kwargs )
	
	@staticmethod
	def setFrequency( var , info , **kwargs ):
		var.setFrequency( info , **kwargs )

	@staticmethod
	def writeField( out , value , last=False ):
		if ( last ):
			out.write( str( value ) + "\n" )
		else:
			out.write( str( value ) + "\t" )

