#!/usr/bin/env python3

import logging
import sys

from  ingenannot.utils import Utils

class Validate(object):

    def __init__(self, args):

        self.gff_gene = args.Gff_genes
        self.statistics = args.statistics
        self.genome = args.genome
        self.addseqs = args.addseqs
        self.fixframe = args.fixframe
        self.gaeval = args.gaeval
        self.output = args.output


    def export_gff3_gaeval(self, genes, fout):

        gff3 =""
        for gene in genes:
            gff3 += gene.to_gff3()
            for tr in gene.lTranscripts:
                gff3 += tr.to_gff3()
                for ex in sorted(tr.lExons + tr.lCDS, key=lambda x : x.start):
                    gff3 += ex.to_gff3(atts={"Parent":[tr.id]})
        if fout:
            fout.write(gff3)
        else:
            print(gff3)

    def export_gff3(self, genes, fout):

        gff3 =""
        for gene in genes:
            gff3 += gene.to_gff3()
            for tr in gene.lTranscripts:
                atts=tr.dAttributes
                atts["ID"]=[tr.id]
                atts["Parent"]=[tr.gene_id]
                gff3 += tr.to_gff3(atts=atts)
                for ex in sorted(tr.lExons, key=lambda x : x.start):
                    gff3 += ex.to_gff3(atts={"ID":[ex.exon_id],"Parent":[tr.id]})
                for cds in sorted(tr.lCDS, key=lambda x : x.start):
                    gff3 += cds.to_gff3(atts={"ID":[cds.cds_id],"Parent":[tr.id]})
        if fout:
            fout.write(gff3)
        else:
            print(gff3)


    def fix_frame(self, genes):

        for gene in genes:
            for tr in gene.lTranscripts:
                next_frame = None
                prev_delta_bases = None
                if tr.strand == 1:
                    lCDS = sorted(tr.lCDS, key=lambda x : x.start)
                if tr.strand == -1:
                    lCDS = sorted(tr.lCDS, key=lambda x : x.start, reverse=True)
                for cds in lCDS:
        #            for cds in sorted(tr.lCDS, key=lambda x : x.start):
                        if next_frame == None:
                            next_frame = 0
                            if cds.frame != next_frame:
                                logging.info("Warning change frame {} to {}".format(cds.frame, next_frame))
                                cds.frame = 0
                            delta_bases = ((cds.end - cds.start + 1) - next_frame) % 3
                            next_frame = (3 - delta_bases) % 3
                        else:
                            if cds.frame != next_frame:
                                logging.info("Warning change frame {} to {}".format(cds.frame, next_frame))
                                cds.frame = next_frame
                            delta_bases = ((cds.end - cds.start + 1) - next_frame) % 3
                            next_frame = (3 - delta_bases) % 3
 
        return genes


    def run(self):
        """"launch command"""


        genes = []
        printout = False
        fout = None
        if self.output:
            fout = open(self.output, 'w')

        try:
            genes = Utils.extract_genes(self.gff_gene)
            logging.info("Validation OK")
        except Exception as e:
            logging.info("Validation Not OK")
            logging.error(e)

        if self.addseqs or self.gaeval:
            printout = True
            refs = {}
            for gene in genes:
                if gene.seqid not in refs:
                    refs[gene.seqid] = (gene.start, gene.end)
                else:
                    refs[gene.seqid] = (min(gene.start,refs[gene.seqid][0]),max(gene.end,refs[gene.seqid][1]))
            for ref in refs:
                if fout:
                    fout.write("##sequence-region   {} {} {}\n".format(ref, refs[ref][0], refs[ref][1]))
                else:
                    print("##sequence-region   {} {} {}".format(ref, refs[ref][0], refs[ref][1]))

        if self.fixframe or self.gaeval:
            printout = True
            genes = self.fix_frame(genes)


        if printout or self.output:
            if self.gaeval:
                self.export_gff3_gaeval(genes, fout)
            else:
                self.export_gff3(genes, fout)

        if self.output:
            fout.close()

        if self.statistics:
            metrics = Utils.statistics(genes, self.genome)
            print('## Statistics ##')
            for metric in metrics:
                print('{};{}'.format(metric,metrics[metric]))
            print('################')

        return 0
