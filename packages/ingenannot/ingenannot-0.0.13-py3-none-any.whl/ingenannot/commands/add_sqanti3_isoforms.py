#!/usr/bin/env python3

import logging
import sys
import copy

from ingenannot.utils import Utils
from ingenannot.commands.command import Command

class AddSqanti3Isoforms(Command):

    def __init__(self, args):

        self.gff_genes = args.Gff_genes
        self.gff_transcripts = args.Gff_transcripts
        self.lIDs = args.IDs
        self.output = args.output
        self.no_identicals = args.no_identicals # if same mRNA either same CDS or not


    def _is_identical(self,tr,ltrs):

        for t in ltrs:
            if t.has_same_exons(tr):
                logging.info("transcript {} is identical to {} in annotation, no new isoform".format(tr.id,t.id))
                return True
        return False


    def run(self):
        """launch command"""

        genes = Utils.extract_genes(self.gff_genes)
        transcripts = Utils.extract_genes(self.gff_transcripts)
        dtrs = {}
        for g in transcripts:
            dtrs[g.gene_id] = g
        IDs = []
        with open(self.lIDs, 'r') as fh:
            for line in fh:
                IDs.append(line.rstrip())

        fout = None
        if self.output:
            fout = open(self.output, 'w')

        gff3 =""
        for gene in genes:
            tr_idx =len(gene.lTranscripts)
            if gene.gene_id in dtrs:
                for tr in dtrs[gene.gene_id].lTranscripts:
                    if tr.id in IDs:
                        if not tr.is_feature_spanning(gene):
                            logging.error("WARNING !!!, your new isoform {} not spanning the associated gene {}, are you sure ?".format(tr.id, gene.gene_id))

                        if self.no_identicals:
                            if self._is_identical(tr,gene.lTranscripts):
                                continue
                        t = copy.deepcopy(tr)
                        tr_idx += 1
                        t.id = "{}.{}".format(gene.gene_id,tr_idx)
                        t.dAttributes = {'ID':["{}.{}".format(gene.gene_id,tr_idx)], 'Parent':[gene.gene_id], 'transcript_source':[tr.id]}
                        for exon in sorted(t.lExons, key=lambda x : x.start):
#                            exon.exon_id = "exon_tochange:{}:{}_exon{.3}".format(exon.exon_id)
                            exon.lTranscript_ids = [t.id]
                        for cds in sorted(t.lCDS, key=lambda x : x.start):
                            cds.cds_id = "cds:{}".format(t.id)
                            cds.transcript_id = t.id
                            #cds.dAttributes = {'ID':["cds:{}".format(t.id)], 'Parent':[t.id]}
                        gene.add_transcript_with_update(t)


            lExs = {}
            gff3 += gene.to_gff3()
            for tr in gene.lTranscripts:
                gff3 += tr.to_gff3(atts=tr.dAttributes)

                for ex in sorted(tr.lExons, key=lambda x : x.start):
                    #gff3 += ex.to_gff3(atts={"ID":[ex.exon_id],"Parent":[tr.id]})
                    #gff3 += ex.to_gff3()
                    if (ex.seqid, ex.start, ex.end) not in lExs:
                        lExs[(ex.seqid, ex.start, ex.end)] = ex

            for i,ex in enumerate(sorted(lExs.values(), key=lambda x: x.start)):
                # rename exon
                ex.exon_id = 'exon:{}.{}'.format(gene.gene_id,i)
                # print
                gff3 += ex.to_gff3()

            for tr in gene.lTranscripts:
                for cds in sorted(tr.lCDS, key=lambda x : x.start):
                    #gff3 += cds.to_gff3(atts={"ID":[cds.cds_id],"Parent":[tr.id]})
                    gff3 += cds.to_gff3()

            for tr in gene.lTranscripts:
                strand = '+'
                if tr.strand == -1:
                   strand = '-'
                five_prime_utrs = tr.infer_five_prime_utrs()
                for i,utr in enumerate(five_prime_utrs):
                    atts = {'ID':['five_prime_UTR_{}_{:03}'.format(tr.id,i+1)], 'source':[gene.source],'Parent':[tr.id]}
                    str_atts = ''
                    for att in atts:
                        str_atts += '{}={};'.format(att,",".join(atts[att]))
                    #f.write("{}\t{}\tfive_prime_UTR\t{}\t{}\t.\t{}\t.\t{}\n".format(tr.seqid,'ingenannot',utr[0],utr[1],strand,str_atts))
                    gff3 += "{}\t{}\tfive_prime_UTR\t{}\t{}\t.\t{}\t.\t{}\n".format(tr.seqid,'ingenannot',utr[0],utr[1],strand,str_atts)
                three_prime_utrs = tr.infer_three_prime_utrs()
                for i,utr in enumerate(three_prime_utrs):
                    atts = {'ID':['three_prime_UTR_{}_{:03}'.format(tr.id,i+1)], 'source':[gene.source],'Parent':[tr.id]}
                    str_atts = ''
                    for att in atts:
                        str_atts += '{}={};'.format(att,",".join(atts[att]))
                    #f.write("{}\t{}\tthree_prime_UTR\t{}\t{}\t.\t{}\t.\t{}\n".format(tr.seqid,'ingenannot',utr[0],utr[1],strand,str_atts))
                    gff3 += "{}\t{}\tthree_prime_UTR\t{}\t{}\t.\t{}\t.\t{}\n".format(tr.seqid,'ingenannot',utr[0],utr[1],strand,str_atts)



#            if gene.gene_id in dtrs:
#                for tr in dtrs[gene.gene_id].lTranscripts:
#                    if tr.id in IDs:
#                        gff3 += tr.to_gff3(atts=tr.dAttributes)
#                        for ex in sorted(tr.lExons, key=lambda x : x.start):
#                             #gff3 += ex.to_gff3(atts={"ID":[ex.exon_id],"Parent":[tr.id]})
#                            gff3 += ex.to_gff3()
#                        for cds in sorted(tr.lCDS, key=lambda x : x.start):
#                            #gff3 += cds.to_gff3(atts={"ID":[cds.cds_id],"Parent":[tr.id]})
#                            gff3 += cds.to_gff3()


        if fout:
            fout.write(gff3)
            fout.close()
        else:
            print(gff3)

        return 0
