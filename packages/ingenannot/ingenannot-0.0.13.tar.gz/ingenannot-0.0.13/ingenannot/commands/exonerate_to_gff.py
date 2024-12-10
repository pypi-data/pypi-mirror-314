#/usr/bin/env python3

import logging
import multiprocessing
import math
import pysam
import sys
from ingenannot.utils import Utils
from ingenannot.utils.gff_reader import GFF3Reader, GTFReader
from ingenannot.utils.gene_builder import GeneBuilder
from ingenannot.utils.annot_edit_distance import AnnotEditDistance
from ingenannot.commands.command import Command
import numpy as np
import matplotlib
import pandas as pd
import re

import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg


class ExonerateToGff(Command):

    def __init__(self, args):

        self.input = args.Input
        self.mode = args.mode
        self.prefix = args.prefix

    def build_entry(self,idx, contig, target, strand, segments, percentage, rel_coords, mode, prefix):

        min_match = int(segments[0][0])
        max_match = int(segments[0][1])
        match_parts = []
        for i,seg in enumerate(segments):
            min_match = min(int(seg[0]),min_match)
            max_match = max(int(seg[1]),max_match)
            rel_lend = int(rel_coords[i][0])
            rel_rend = int(rel_coords[i][0]) + int(rel_coords[i][1])
            if mode == 'prot':
                rel_rend = int(rel_coords[i][0]) + int(int(rel_coords[i][1])/3)

            match_parts.append("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(contig,"exonerate_to_gff","match_part",seg[0],seg[1],percentage,strand,".","ID={}match.{}.{};Parent={}match.{};Dbxref=exonerate:{};Target={} {} {}".format(prefix,idx,i,prefix,idx,target,target,rel_lend,rel_rend)))

        print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(contig,"exonerate_to_gff","match",min_match,max_match,percentage,strand,".","ID={}match.{};Dbxref=exonerate:{};Name={}".format(prefix, idx,i,target,target)))

        # sort in place start
        match_parts.sort(key=lambda mp: int(mp.split("\t")[3]))

        for mp in match_parts:
            print(mp)


    def run(self):
        """"launch command"""

        idx = 0
        contig = ""
        target = ""
        strand = ""
        segments = []
        percentage = "."
        rel_coords = []

        fh = open(self.input,'r')

        # skip first lines
        for line in fh:
            if re.match(".*START OF GFF DUMP.*", line):
                break

        for line in fh:
            l = line.rstrip()
            m = re.match(".*AveragePercentIdentity: (\S+).*", line)
            if m:
                percentage = m.group(1)
                #continue
            m1 = re.match("^\#\#gff-version",line)
            m2 = re.match(".*Command.*",line)
            if m or m2:
                if segments:
                    idx += 1
                    self.build_entry(idx, contig, target, strand, segments, percentage, rel_coords, self.mode, self.prefix)
                contig = ""
                target = ""
                strand = ""
                segments = []
                percentage = "."
                rel_coords = []
            m3 = re.match("^(\S+)\t(\S+)\t(\S+)\t(\d+)\t(\d+)\t(\S+)\t(\S+)\t(\S+)\t(.*)", line)
            if m3:
                if m3.group(3) == "gene":
                    m4 = re.match(".* sequence (\S+) .*", m3.group(9))
                    #print(m.group(9))
                    if m4:
                        target = m4.group(1)
                     #   print(target)
                        continue
                    else:
                        print("Error cannot read target line --")
                        sys.exit(1)
                if m3.group(3) == "exon":
                    contig = m3.group(1)
                    strand = m3.group(7)
                    segments.append([min(int(m3.group(4)),int(m3.group(5))),max(int(m3.group(4)),int(m3.group(5)))])
                    #print(segments)
                    continue
                if m3.group(3) == "similarity":
                    r=re.compile("Align \d+ (\d+) (\d+)")
                    m4 = r.findall(m3.group(9))
                    rel_coords = m4
                    continue

        if segments:
            idx += 1
            self.build_entry(idx, contig, target, strand, segments, percentage, rel_coords, self.mode, self.prefix)

        fh.close()

        return 0
