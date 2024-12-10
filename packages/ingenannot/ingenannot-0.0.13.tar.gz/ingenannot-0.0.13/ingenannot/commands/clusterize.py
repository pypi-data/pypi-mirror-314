#!/usr/bin/env python3

import sys
import logging

from ingenannot.utils import Utils
from ingenannot.commands.command import Command


class Clusterize(Command):

    def __init__(self, args):

        self.gff_transcripts = args.Gff_transcripts
        self.gff_out = args.Gff_out
        self.gff_genes = args.Gff_genes
        self.keep_atts = args.keep_atts
        self.overlap_ratio = args.overlap_ratio

    def export(self, clusters):
        '''export  clusters in gff'''

        fh = open(self.gff_out, 'w')
        for idx,cl in enumerate(clusters):
            for gene in cl.genes:
                for tr in gene.lTranscripts:
                    atts = {}
                    if self.keep_atts:
                        atts = tr.dAttributes
                        atts["gene_id"] = ["GENE_{:05}".format(idx+1)]
                        atts["transcript_id"] = [tr.id]
                    else:
                        atts = {"gene_id":["GENE_{:05}".format(idx+1)],"transcript_id":[tr.id]}

                    fh.write(tr.to_gtf(atts))
                    for ex in tr.lExons:
                        fh.write(ex.to_gtf("GENE_{:05}".format(idx+1),tr.id))
        fh.close()


    def filter(self, tr_genes, annotations):
        '''filter transcripts overlapping multi genes'''


        filtered_genes = []
        for idx,gene in enumerate(tr_genes):
            validate = True
            for tr in gene.lTranscripts:
                nb_overlap = 0
                for annot in [a for a in annotations if a.seqid==tr.seqid and tr.start >= a.start-25000 and tr.end <= a.end+25000]:
                    start = annot.lTranscripts[0].get_min_cds_start()
                    end = annot.lTranscripts[0].get_max_cds_end()
                    if tr.coords_spanning_ratio(start,end) > self.overlap_ratio:
                        nb_overlap += 1
                if nb_overlap > 1:
                    validate = False
            if validate:
                filtered_genes.append(gene)

        return filtered_genes



    def run(self):
        '''run'''

        tr_genes = Utils.extract_genes(self.gff_transcripts)

        if self.gff_genes:
            annotations = Utils.extract_genes(self.gff_genes)

            tr_genes = self.filter(tr_genes, annotations)

        clusters = Utils.clusterize(tr_genes, 'gene', True, 10)

        self.export(clusters)

        return 0
