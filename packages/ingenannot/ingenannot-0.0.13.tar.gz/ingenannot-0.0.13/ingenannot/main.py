#!/usr/bin/env python3

"""This module parse arguments and launch commands"""

import sys
import argparse
import logging
import multiprocessing
import shutil
import ingenannot.commands as cmd

class ArgParse():
    '''
    The ArgParse object is the shared argument parser for all subcommands
    of ingenannot.

    Attributes:
    -----------
    parser : ArgumentParser
        The ArgumentParser of argparse
    subparsers: List of subparsers
        List to store subparsers
    '''


    def __init__(self):

        # ingenannot shared args
        self.parser = argparse.ArgumentParser(prog='ingenannot')
        self.parser.add_argument(
                "-p","--procs",
                help='Number of procs to use, default=1',
                type=int, default=1
        )
        self.parser.add_argument(
                "-v", "--verbosity",
                type=int, choices=[1,2,3],
                help="increase output verbosity 1=error, 2=info, 3=debug"
        )
        self.subparsers = self.parser.add_subparsers(help="sub-command help")


    def load_all_subparsers(self):
        """Load all subparsers"""

        self.subparser_add_sqanti3_isoforms()
        self.subparser_aed()
        self.subparser_aed_compare() # code and test to do and validate
        self.subparser_aed_strand_annotation_filter()
        self.subparser_clusterize()
        self.subparser_compare()
        self.subparser_curation()
        self.subparser_effector_predictor() # code
        self.subparser_exonerate_to_gff()
        self.subparser_filter() # code
        self.subparser_isoform_ranking() # coverage test
        self.subparser_rename()
        self.subparser_rescue_effectors() # code
        self.subparser_select()
        self.subparser_soclassif()
        self.subparser_utr_refine()
        self.subparser_validate()


    def subparser_aed(self):
        """Add subparser for AED cmd"""

        sbp = self.subparsers.add_parser(
                'aed',
                help='Compute AED'
        )
        sbp.add_argument(
                "Input",
                help="GFF/GTF File",
                type=str
        )
        sbp.add_argument(
                "Output",
                help="Output Annotation file in GFF file format with AED",
                type=str
        )
        sbp.add_argument(
                "source",
                help="Source of Annotation (eugene, maker, braker3, helixer...)",
                type=str
        )
        sbp.add_argument(
                "evtr",
                help="Gff file of transcript evidence, compressed with bgzip \
                      and indexed with tabix",
                type=str
        )
        sbp.add_argument(
                "evpr",
                help="Gff file protein evidence, compressed with bgzip and \
                      indexed with tabix",
                type=str
        )
        sbp.add_argument(
                "--evtr_source",
                help='Source for Gff file transcript evidence ex \
                      "stringtie", default=undefined',
                default="undefined",
                type=str
        )
        sbp.add_argument(
                "--evpr_source",
                help='Source for Gff file protein evidence ex \
                     "blastx, diamond, exonerate, miniprot", default=undefined',
                default="undefined",
                type=str
        )
        sbp.add_argument(
                "--evtrstranded",
                help='Same strand orientation required to consider match \
                      with evidence, default=False',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--evprstranded",
                help='Same strand orientation required to consider match with \
                      evidence, default=False',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--penalty_overflow",
                help='In the event that a Coding DNA Sequence (CDS) exceeds \
                      the expected length or violates intron constraints based \
                      on transcript evidence, a penalty should be applied to \
                      computation of the Annotation Edit Distance (AED) score. \
                      The penalty value ranges from 0.0 to 1.0, default=0.0, \
                      no penalty',
                default=0.0,
                type=float
        )
        sbp.add_argument(
                "--longreads",
                help="Gff file longread based transcript evidence, compressed \
                      and indexed with tabix",
                type=str
        )
        sbp.add_argument(
                "--longreads_source",
                help='Source for Gff file longread based evidence ex \
                      "Iso-Seq", default=undefined',
                default="undefined",
                type=str
        )
        sbp.add_argument(
                "--longreads_penalty_overflow",
                help='In the event that a Coding DNA Sequence (CDS) \
                      exceeds the expected length or violates intron \
                      constraints based on transcript evidence, a penalty \
                      should be applied to computation of the Annotation Edit \
                      Distance (AED) score. The penalty value ranges from \
                      0.0 to 1.0, default=0.25',
                default=0.25,
                type=float
        )
        sbp.add_argument(
                "--aedtr",
                help='Transcript AED value for graph limits, default=0.5',
                default=0.5,
                type=float
        )
        sbp.add_argument(
                "--aedpr",
                help='protein AED value for graph limit, default=0.2',
                default=0.2,
                type=float
        )
        sbp.add_argument(
                "--aed_tr_cds_only",
                help='For transcripts (short-reads and longreads), compute \
                      AED on CDS only, instead of Exon and CDS, with best \
                      score selection, default=False',
                default=False,
                action='store_true'
        )
        sbp.set_defaults(command=cmd.AED)

        return sbp
   

    def subparser_aed_compare(self):
        """Add subparser for AEDCompare cmd"""

        sbp = self.subparsers.add_parser(
                'aed_compare',
                help='Compare annotation sets based on their AED scores'
        )
        sbp.add_argument(
                "fof",
                help="File of files, <GFF with AED tags>TAB<source>",
                type=str
        )
        sbp.add_argument(
                "-s","--statistics",
                help='Perform statistics on AED scores between sources \
                      , default=False',
                action="store_true",
                default=False
        )
        sbp.set_defaults(command=cmd.AEDCompare)

        return sbp


    def subparser_aed_strand_annotation_filter(self):
        """Add subparser for StrandAnnotationFilter cmd"""

        sbp = self.subparsers.add_parser(
                'aed_strand_annotation_filter',
                help='Remove opposite overlapping annotations based on AED scores'
        )
        sbp.add_argument(
                "Input",
                help="GFF File with AED tags",
                type=str
        )
        sbp.add_argument(
                "Output",
                help="Filtered output annotation file",
                type=str
        )
        sbp.set_defaults(command=cmd.StrandAnnotationFilter)

        return sbp


    def subparser_add_sqanti3_isoforms(self):
        """Add subparser for AddSqanti3Isoforms cmd"""

        sbp = self.subparsers.add_parser(
                'add_sqanti3_isoforms',
                help='Add Isoforms from sqanti3 outputs'
        )
        sbp.add_argument(
                "Gff_genes",
                help="Gene Annotation file in GFF/GTF file format",
                type=str
        )
        sbp.add_argument(
                "Gff_transcripts",
                help="Gff file of transcript in Sqanti3 format",
                type=str
        )
        sbp.add_argument(
                "IDs",
                help="File with list of transcript IDs to add",
                type=str
        )
        sbp.add_argument(
                "-o","--output",
                help="Output Annotation file in GFF file format",
                type=str
        )
        sbp.add_argument(
                "--no_identicals",
                help="Do not add new isoform if the same mRNA with same exons \
                      is in the annotation, even the CDS is different",
                action="store_true",
                default=False
        )
        sbp.set_defaults(command=cmd.AddSqanti3Isoforms)

        return sbp


    def subparser_clusterize(self):
        """Add subparser for Clusterize cmd"""

        sbp = self.subparsers.add_parser(
                'clusterize',
                help='clusterize transcripts with genes, transcripts\
                      from differents runs must have different names\
                      -l option with StringTie'
        )
        sbp.add_argument(
                "Gff_transcripts",
                help="Transcripts file in GFF/GTF file",
                type=str
        )
        sbp.add_argument(
                "Gff_out",
                help="Output GFF file with transcripts clusterized per gene",
                type=str
        )
        sbp.add_argument(
                "-g","--Gff_genes",
                help="Gene Annotation file in GFF/GTF file uses to remove \
                      transcripts overlapping several CDS",
                type=str
        )
        sbp.add_argument(
                "--keep_atts",
                help='Keep attributes on transcript features',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "-r","--overlap_ratio",
                help='Overlap ratio between transcripts and CDS from \
                      annotations to consider an overlap \
                      range[0.0-1.0], default=0.6',
                default=0.6,
                type=float
        )
        sbp.set_defaults(command=cmd.Clusterize)

        return sbp


    def subparser_compare(self):
        """Add subparser for Compare cmd"""

        sbp = self.subparsers.add_parser(
                'compare',
                help='Compare gene content between several annotations'
        )
        sbp.add_argument(
                "fof",
                help="File of files, <GFF/GTF>TAB<source>",
                type=str
        )
        sbp.add_argument(
                "--clutype",
                help='Feature type used to clusterize: [gene, cds], \
                      default=cds',
                default='cds'
        )
        sbp.add_argument(
                "--clustranded",
                help='Same strand orientation required to cluster features, \
                      default=False',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--export_same_cds",
                help='Export identical shared CDS by all annotations in \
                      same_cds.gff3 file, default=False',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--export_specific",
                help='Export specific CDS for each annotation, locus and \
                      CDS specific in separate files, default=False',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--export_list_specific",
                help='Export specific CDS common to a list of sources, list \
                      the source with a sbpace',
                nargs='*'
        )
        sbp.add_argument(
                "--export_venn",
                help='Export CDS in with metagene code to perform venn \
                      diagrams, default=False',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--export_upsetplot",
                help='Export upsetplot of CDS, default=False',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--graphout",
                help="output filename of the graph, default=upsetplot.png",
                type=str,
                default='upsetplot.png'
        )
        sbp.add_argument(
                "--graphtitle",
                help="output title of the graph, default=Intersecting sets \
                      of CDS",
                type=str,
                default='Intersecting sets of CDS'
        )
        sbp.set_defaults(command=cmd.Compare)

        return sbp


    def subparser_curation(self):
        """Add subparser for Curation cmd"""

        sbp = self.subparsers.add_parser(
                'curation',
                help='Define priorities, classify genes for manual \
                        control or modification'
        )
        sbp.add_argument(
                "Input",
                help="GFF File with AED tags",
                type=str
        )
        sbp.add_argument(
                "Output",
                help="GFF File with new curation tag",
                type=str
        )
        sbp.add_argument(
                "--graphout",
                help="output filename of the graph, default=curation.png",
                type=str,
                default='curation.png'
        )
        sbp.add_argument(
                "--graphtitle",
                help="output title of the graph, default=AED categories \
                      for manual curation",
                type=str,
                default='AED categories for manual curation'
        )
        sbp.set_defaults(command=cmd.Curation)

        return sbp


    def subparser_effector_predictor(self):
        """Add subparser for EffectorPredictor cmd"""

        sbp = self.subparsers.add_parser(
                'effector_predictor',
                help='Predict effector genes'
        )
        sbp.add_argument(
                "fasta",
                help="Fasta file of proteins",
                type=str
        )
        sbp.add_argument(
                "--signalp",
                help=f"Path to signalp, default={shutil.which('signalp')} \
                        (from system lookup)",
                type=str,
                default=shutil.which('signalp')
        )
        sbp.add_argument(
                "--tmhmm",
                help=f"Path to tmhmm, default={shutil.which('tmhmm')} \
                        (from system lookup)",
                type=str,
                default=shutil.which('tmhmm')
        )
        sbp.add_argument(
                "--targetp",
                help=f"Path to targetp, default={shutil.which('targetp')} \
                        (from system lookup)",
                type=str,
                default=shutil.which('targetp')
             )
        sbp.add_argument(
                "--effectorp",
                help=f"Path to effectorp, default={shutil.which('EffectorP.py')} \
                        (from system lookup)",
                type=str, default=shutil.which('EffectorP.py')
        )
        sbp.add_argument(
                "--signalp_cpos",
                help="Maximal position of signal peptide cleavage site, \
                      default=25",
                default=25, type=int
        )
        sbp.add_argument(
                "--effectorp_score",
                help="Minimal effectorp score, default=0.7",
                default=0.7,
                type=float
        )
        sbp.add_argument(
                "--max_len",
                help="Maximal length of protein, default=300",
                default=300,
                type=int
        )
        sbp.add_argument(
                "--min_len",
                help="Minimal length of protein, default=30",
                default=30,
                type=int
        )
        sbp.set_defaults(command=cmd.EffectorPredictorCmd)

        return sbp


    def subparser_exonerate_to_gff(self):
        """Add subparser for ExonerateToGff cmd"""

        sbp = self.subparsers.add_parser(
                'exonerate_to_gff',
                help='Transform exonerate output to gff format',
                description="RUN exonerate with:\
                             exonerate --model p2g --showvulgar no \
                             --showalignment no --showquerygff no \
                             --showtargetgff yes --percent 80 --ryo \
                             \"AveragePercentIdentity: %pi\n\" \
                             protein_db.pep target_genome.fasta"
        )
        sbp.add_argument(
                "Input",
                help="Output of exonerate",
                type=str
        )
        sbp.add_argument(
                "-m", "--mode",
                help="Mode: [prot, nuc], default=prot",
                type=str,
                default="prot",
                choices=['prot', 'nuc']
        )
        sbp.add_argument(
                "-p", "--prefix",
                help="Add a prefix to the feature name, usefull if \
                      you ran exonerate in a split mode",
                type=str,
                default=""
        )
        sbp.set_defaults(command=cmd.ExonerateToGff)

        return sbp


    def subparser_filter(self):
        """Add subparser for Filter cmd"""

        sbp = self.subparsers.add_parser(
                'filter',
                help='Filter annotations'
        )
        sbp.add_argument(
                "Gff_genes",
                help="Gene Annotation file in GFF/GTF file format",
                type=str
        )
        sbp.add_argument(
                "Gff_TEs",
                help="Annotation file in GFF/GTF file format",
                type=str
        )
        sbp.add_argument(
                "Output",
                help="Output Annotation file in GFF file format",
                type=str
        )
        sbp.add_argument(
                "-s", "--size",
                help="Minimum required size of feature for filtering, \
                      default=300bp",
                type=int,
                default=300
        )
        sbp.add_argument(
                "-f", "--feature",
                help="Feature type expected for filtering, default=match_part",
                type=str,
                default="match_part"
        )
        sbp.add_argument(
                "--bed",
                help="Bed file expected instead of GFF/GTF file",
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "-r", "--fraction",
                help="Minimum fraction of CDS overlapped for filtering, \
                      default=0.1 (10 percent)",
                type=float,
                default=0.1
        )
        sbp.set_defaults(command=cmd.Filter)

        return sbp


    def subparser_isoform_ranking(self):
        """Add subparser for IsoformRanking cmd"""

        sbp = self.subparsers.add_parser(
                'isoform_ranking',
                help='Rank isoform based on junction and read coverages'
        )
        sbp.add_argument(
                "Gff_transcripts",
                help="Gff file of transcripts",
                type=str
        )
        sbp.add_argument(
                "-p", "--prefix",
                help="Prefix for output annotation files in GFF file format, \
                      default=isoforms",
                type=str,
                default="isoforms"
        )
        sbp.add_argument(
                "-b","--bam",
                help="bam file to analyze",
                type=str
        )
        sbp.add_argument(
                "--paired",
                help='The bam file is paired or not, default=False',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--stranded",
                help='The bam file is stranded or not, default=False',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "-f","--fof",
                help="File of bam files, <bam>TAB<type>TAB<stranded>",
                type=str
        )
        sbp.add_argument(
                "--sj_threshold",
                help="threshold used as ratio of coverage to keep a junction \
                      for ranking, default=0.05",
                default=0.05,
                type=float
        )
        sbp.add_argument(
                "--cov_threshold",
                help="threshold of the median use to excluded bases in \
                      coverage count , default=0.05",
                default=0.05,
                type=float
        )
        sbp.add_argument(
                "--alt_threshold",
                help="threshold of the isoform to keep it in the \
                      isoform.alternatives.gff, based on junction coverage, \
                      default=0.1",
                default=0.1,
                type=float
        )
        sbp.add_argument(
                "--rescue",
                help='If set, in case of no transcript was selected due to \
                      unsupported junctions, keep at least one based on the \
                      coverage, default=False',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--sj_full",
                help='Junctions supported by only one side will be analyzed \
                      as shared junction, if set both sides need to overlap \
                      all transcript to be considered in ranking, \
                      default=False',
                action="store_true",
                default=False
        )
        sbp.set_defaults(command=cmd.IsoformRanking)

        return sbp


    def subparser_rename(self):
        """Add subparser for Rename cmd"""

        sbp = self.subparsers.add_parser(
                'rename',
                help='Rename gene name with pattern'
        )
        sbp.add_argument(
                "Gff_genes",
                help="Gene Annotation file in GFF/GTF file",
                type=str
        )
        sbp.add_argument(
                "pattern",
                help="Pattern to use for renaming gene, {ref}=sequence, \
                     {geneidx}=gene index whole genome, {geneidxref}= gene \
                     index on the sequence",
                type=str
        )
        sbp.add_argument(
                "--mapping",
                help='Export mapping file to keep track of changes',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--locus_tag",
                help='Add gene Id as Locus_tag for ENA submission',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--name",
                help='Replace the tag Name in Gene and mRNA feature \
                      with new ID',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--tr_ranking_ID",
                help='In cases of multi-mRNA, try to keep the order \
                      based on name ex T001.1 then T001.2 when renaming',
                action="store_true",
                default=False
        )
        sbp.set_defaults(command=cmd.Rename)

        return sbp


    def subparser_rescue_effectors(self):
        """Add subparser for RescueEffectors cmd"""

        sbp = self.subparsers.add_parser(
                'rescue_effectors',
                help='Perform rescue of effector genes'
        )
        sbp.add_argument(
                "Gff_genes",
                help="Gene Annotation file in GFF/GTF file format",
                type=str
        )
        sbp.add_argument(
                "Gff_transcripts",
                help="Gff file of transcript evidence, compressed with bgzip \
                      and indexed with tabix",
                type=str
        )
        sbp.add_argument(
                "Genome",
                help="Genome in fasta format or compressed in bgzip format",
                type=str
        )
        sbp.add_argument(
                "--signalp",
                help=f"Path to signalp, default={shutil.which('signalp')} \
                        (from system lookup)",
                type=str,
                default=shutil.which('signalp')
        )
        sbp.add_argument(
                "--tmhmm",
                help=f"Path to tmhmm, default={shutil.which('tmhmm')} \
                        (from system lookup)",
                type=str,
                default=shutil.which('tmhmm')
        )
        sbp.add_argument(
                "--targetp",
                help=f"Path to targetp, default={shutil.which('targetp')} \
                        (from system lookup)",
                type=str,
                default=shutil.which('targetp')
        )
        sbp.add_argument(
                "--effectorp",
                help=f"Path to signalp, default={shutil.which('EffectorP.py')} \
                        (from system lookup)",
                type=str,
                default=shutil.which('EffectorP.py')
        )
        sbp.add_argument(
                "--signalp_cpos",
                help="Maximal position of signal peptide cleavage site, \
                      default=25",
                default=25,
                type=int
        )
        sbp.add_argument(
                "--effectorp_score",
                help="Minimal effectorp score, default=0.7",
                default=0.7,
                type=float
        )
        sbp.add_argument(
                "--max_len",
                help="Maximal length of protein in aa, default=300",
                default=300,
                type=int
        )
        sbp.add_argument(
                "--min_len",
                help="Minimal length of protein in aa, default=30",
                default=30,
                type=int
        )
        sbp.add_argument(
                "--min_intergenic_len",
                help="Minimal intergenic length to consider, default=100",
                default=100
        )
        sbp.add_argument(
                "--size_ratio",
                help="Minimal ratio length of CDS/mRNA, default=0.2",
                default=0.2,
                type=float
        )
        sbp.add_argument(
                "--unstranded",
                help='The transcripts are stranded or not, default=False',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "-o","--output",
                help="Output Annotation file in GFF file format, \
                      default=effectors.gff3",
                type=str,
                default="effectors.gff3"
        )
        sbp.set_defaults(command=cmd.RescueEffectors)

        return sbp


    def subparser_soclassif(self):
        """Add subparser for SOClassification cmd"""

        sbp = self.subparsers.add_parser(
                'soclassif',
                help='Classify transcripts based on SO classification'
        )
        sbp.add_argument(
                "fof",
                help="File of files, <GFF/GTF>TAB<source>",
                type=str
        )
        sbp.add_argument(
                "--clutype",
                help='Feature type used to clusterize: [gene, cds], \
                      default=cds',
                default='cds'
        )
        sbp.add_argument(
                "--clustranded",
                help='Same strand orientation required to cluster features, \
                      default=False',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--clatype",
                help='Feature type used to classify: [gene, cds], \
                      default=cds',
                default='cds'
        )
        sbp.set_defaults(command=cmd.SOClassification)

        return sbp


    def subparser_select(self):
        """Add subparser for Select cmd"""

        sbp = self.subparsers.add_parser(
                'select',
                help='Select best gene model'
        )
        sbp.add_argument(
                "fof",
                help="File of files, <GFF/GTF>TAB<source>",
                type=str
        )
        sbp.add_argument(
                "Output",
                help="Output Annotation file in GFF file format",
                type=str
        )
        sbp.add_argument(
                "--noaed",
                help='If set, use precompute aed info available in gff file, \
                      no aed computation',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--clutype",
                help='Feature type used to clusterize: [gene, cds], \
                      default=cds',
                default='cds'
        )
        sbp.add_argument(
                "--clustranded",
                help='Same strand orientation required to cluster features, \
                      default=False',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--evtr",
                help="Gff file of transcript evidence",
                type=str
        )
        sbp.add_argument(
                "--evpr",
                help="Gff file protein evidence, compressed and indexed \
                      with tabix",
                type=str
        )
        sbp.add_argument(
                "--evtr_source",
                help='Specify source for Gff file transcript evidence ex \
                      "stringtie", default=undefined',
                default="undefined",
                type=str
        )
        sbp.add_argument(
                "--evpr_source",
                help='Specify source for Gff file protein evidence ex \
                      "blastx, miniprot", default=undefined',
                default="undefined",
                type=str
        )
        sbp.add_argument(
                "--evtrstranded",
                help='Same strand orientation required to consider match \
                      with evidence, default=False',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--evprstranded",
                help='Same strand orientation required to consider match \
                      with evidence, default=False',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--penalty_overflow",
                help='In case of a CDS is longer or violate constraint of \
                      intron with the tr evidence, add a penalty to the \
                      computation of the aed score range[0.0-1.0], \
                      default=0.0, no penalty',
                default=0.0,
                type=float
        )
        sbp.add_argument(
                "--nbsrc_filter",
                help='Number of sources required to bypass aedtr and aedpr \
                      filtering, default=max number of source + 1',
                type=int,
                default=10000
        )
        sbp.add_argument(
                "--aedtr",
                help='Minimum aedtr required when filtering default=1.0, ',
                default=1.0,
                type=float
        )
        sbp.add_argument(
                "--aedpr",
                help='Minimum aedpr required when filtering default=1.0, ',
                default=1.0,
                type=float
        )
        sbp.add_argument(
                "--aed_tr_cds_only",
                help='For transscripts (short-reads and longreads), compute \
                      aed on CDS only, instead of Exon and CDS, with best \
                      score selection, default=False',
                default=False,
                action='store_true'
        )
        sbp.add_argument(
                "--use_ev_lg",
                help='Use aed of long-read instead of aed_tr if better, \
                      default=False',
                default=False,
                action='store_true'
        )
        sbp.add_argument(
                "--nbsrc_absolute",
                help='Number of sources required to keep a gene, default=1',
                type=int,
                default=1
        )
        sbp.add_argument(
                "--min_cds_len",
                help='Minimum CDS len required default=90, prot with 30AA ',
                default=90,
                type=int
        )
        sbp.add_argument(
                "--no_partial",
                help='In case of the best selected CDS is partial \
                      (no CDS nor STOP codon), export another CDS if possible, \
                      default=False',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--genome",
                help="Genome in fasta format required with no_partial",
                type=str
        )
        sbp.add_argument(
                "--longreads",
                help="Gff file longread based transcript evidence, compressed \
                      and indexed with tabix",
                type=str
        )
        sbp.add_argument(
                "--longreads_source",
                help='Specify source for Gff file longread based evidence \
                      ex "Iso-Seq", default=undefined',
                default="undefined",
                type=str
        )
        sbp.add_argument(
                "--longreads_penalty_overflow",
                help='In case of a CDS is longer or violate constraint of \
                      intron with the longread based transcript evidence, \
                      add a penalty to the computation of the aed score \
                      range[0.0-1.0], default=0.25',
                default=0.25,
                type=float
        )
        sbp.add_argument(
                "--gaeval",
                help="expect gaeval tsv file for each annotation file, \
                      File of files: <GFF/GTF>TAB<source>TAB<gaeval>",
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--prefix",
                help='prefix for gene name, default=G',
                default='G',
                type=str
        )
        sbp.add_argument(
                "--no_export",
                help='export gff file containing the un-exported best genes',
                default=False,
                action='store_true'
        )
        sbp.add_argument(
                "--no_cds_overlap",
                help='post process filter to remove worst CDS if overlapping \
                      with other CDS',
                default=False,
                action='store_true'
        )
        sbp.set_defaults(command=cmd.Select)

        return sbp


    def subparser_utr_refine(self):
        """Add subparser for UTRREfine cmd"""

        sbp = self.subparsers.add_parser(
                'utr_refine',
                help='Refine UTR boundaries'
        )
        sbp.add_argument(
                "Gff_genes",
                help="Gene Annotation file in GFF/GTF file format to \
                      add/correct UTRs",
                type=str
        )
        sbp.add_argument(
                "Gff_transcripts",
                help="Transcript Annotation file in GFF/GTF file format used \
                      to add/correct UTRs",
                type=str
        )
        sbp.add_argument(
                "Output",
                help="Output Annotation file in GFF file format",
                type=str
        )
        sbp.add_argument(
                "--utr_mode",
                help="In case of several transcripts match the ORFs to extend, \
                      select the mode to add UTR [longest, shortest, rank, \
                      all], default=longest",
                type=str,
                default='longest',
                choices=['longest','shortest', 'rank', 'all']
        )
        sbp.add_argument(
                "--erase",
                help='Previous annotated UTRs will be deleted, instead of to \
                      be elongated, and so possibly reduced, default=False',
                action="store_true",
                default=False
        )
        sbp.add_argument(
                "--onlynew",
                help='Add only new UTR on genes without UTR, keep previous if \
                      available, default=False',
                action="store_true",
                default=False
        )
        sbp.set_defaults(command=cmd.UTRRefine)

        return sbp


    def subparser_validate(self):
        """Add subparser for Validate cmd"""

        parser_validate = self.subparsers.add_parser(
                'validate',
                help='Validate expected GTF/GFF file formats'
        )
        parser_validate.add_argument(
                "Gff_genes",
                help="Gene Annotation file in GFF/GTF file format",
                type=str
        )
        parser_validate.add_argument(
                "-s","--statistics",
                help="Statistics of annotations",
                action="store_true",
                default=False
        )
        parser_validate.add_argument(
                "-g","--genome",
                help="Genome in Fasta file, more statistics metrics \
                      if provided",
                type=str,
                default=None
        )
        parser_validate.add_argument(
                "-a","--addseqs",
                help="Export file in GFF3 with ##sequence-region  \
                      pragma",
                action="store_true",
                default=False
        )
        parser_validate.add_argument(
                "--fixframe",
                help="fix error in CDS frame and log warning",
                action="store_true",
                default=False
        )
        parser_validate.add_argument(
                "--gaeval",
                help="Perform required control and transform to run \
                      with gaeval",
                action="store_true",
                default=False
        )
        parser_validate.add_argument(
                "-o","--output",
                help="Output Annotation file in GFF file format",
                type=str
        )
        parser_validate.set_defaults(command=cmd.Validate)

        return parser_validate


def main():
    """script entry point"""

    i = ArgParse()
    i.load_all_subparsers()
    args = i.parser.parse_args()

    log_level='ERROR'
    if args.verbosity == 1:
        log_level = 'ERROR'
    if args.verbosity == 2:
        log_level = 'INFO'
    if args.verbosity == 3:
        log_level = 'DEBUG'
    logging.getLogger().setLevel(log_level)

    if args.procs > 1:
        cmd.Command.NB_CPUS = min(args.procs, multiprocessing.cpu_count()-1)
        logging.info("Multi-processs requested: %s procs will be used",
                     cmd.Command.NB_CPUS)

    if 'command' not in args:
        i.parser.print_help()
        sys.exit(1)

    try:
        command = args.command(args)
        command.run()
    except RuntimeError as error:
        #print(error)
        i.parser.print_help()
        sys.exit(1)


def exe():
    """Delegate to script or class"""

    if __name__ == "__main__":
        sys.exit(main())

exe()
