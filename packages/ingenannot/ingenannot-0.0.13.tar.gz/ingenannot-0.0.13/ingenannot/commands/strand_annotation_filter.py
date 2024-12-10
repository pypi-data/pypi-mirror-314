#/usr/bin/env python3

import logging
import sys
from  ingenannot.utils import Utils
from ingenannot.commands.command import Command

class StrandAnnotationFilter(Command):

    def __init__(self, args):

        self.input = args.Input
        self.output = args.Output


    def export(self, allgenes, list_to_remove):

        with open(self.output, 'w') as f:

            for gene in allgenes:
                flag_remove = False
                for tr in gene.lTranscripts:
                    if tr in list_to_remove:
                        # TODO: need to implement removing only the bad transcript if
                        # isoforms, and recompute gene coords
                        # for instance one bad CDS imply removing of the whole gene
                        logging.info("removing gene {} and all transcripts".format(gene.gene_id))
                        flag_remove = True
                        break
                if not flag_remove:
                    #atts = {'ID':['gene:{}'.format(gene.gene_id)],'source':[gene.source]}
                    atts = {'ID':[gene.gene_id],'source':[gene.source]}
                    f.write(gene.to_gff3(atts=atts))
                    #print(gene.gene_id, gene.start, gene.end)
                    for tr in gene.lTranscripts:
                        if not tr.best_tr_evidence[0]:
                            ev_tr = "None"
                        else:
                            ev_tr = tr.best_tr_evidence[0]
                        if not tr.best_bx_evidence[0]:
                            ev_bx = "None"
                        else:
                            ev_bx = tr.best_bx_evidence[0]
                        atts = tr.dAttributes
                        #atts_id = {'ID': ['mRNA:{}'.format(tr.id)],'Parent':['gene:{}'.format(gene.gene_id)]}
                        atts_id = {'ID': [tr.id],'Parent':[gene.gene_id]}
                        atts.update(atts_id)
                        #atts = {'ID':['mRNA:{}'.format(tr.id)], 'source':[gene.source],'Parent':['gene:{}'.format(gene.gene_id)], 'ev_tr': [ev_tr], 'aed_ev_tr':['{:.4f}'.format(tr.best_tr_evidence[1])], 'ev_tr_penalty': [tr.tr_penalty], 'ev_pr' : [ev_bx], 'aed_ev_pr' : ['{:.4f}'.format(tr.best_bx_evidence[1])]}

                        if not tr.best_lg_evidence[0]:
                            ev_lg = "None"
                        else:
                            ev_lg = tr.best_lg_evidence[0]
                        atts_lg = {'ev_lg': [ev_lg], 'aed_ev_lg':['{:.4f}'.format(tr.best_lg_evidence[1])],'ev_lg_penalty':[tr.lg_penalty]}
                        atts.update(atts_lg)

                        f.write(tr.to_gff3(atts=atts))
                        for i,exon in enumerate(tr.lExons):
                            #atts = {'ID':['exon:{}.{}'.format(gene.gene_id,i+1)], 'source':[gene.source],'Parent':['mRNA:{}'.format(tr.id)]}
                            #atts = {'ID':['exon:{}.{}'.format(tr.id,i+1)], 'source':[gene.source],'Parent':['mRNA:{}'.format(tr.id)]}
                            #atts = {'ID':['exon:{}.{}'.format(tr.id,i+1)], 'source':[gene.source],'Parent':['{}'.format(tr.id)]}
                            atts = {'ID':[exon.exon_id], 'source':[gene.source],'Parent':[tr.id]}
                            f.write(exon.to_gff3(atts=atts))
                        for i,cds in enumerate(tr.lCDS):
                            #atts = {'ID':['cds:{}'.format(tr.id)], 'source':[gene.source],'Parent':['mRNA:{}'.format(tr.id)]}
                            #atts = {'ID':['cds:{}'.format(tr.id)], 'source':[gene.source],'Parent':['{}'.format(tr.id)]}
                            atts = {'ID':[cds.cds_id], 'source':[gene.source],'Parent':[tr.id]}
                            f.write(cds.to_gff3(atts=atts))
        f.close()

    def run(self):
        """"launch command"""

        genes = Utils.extract_genes(self.input)

        Utils.get_aed_from_attributes(genes)
        
        transcripts = []
        for g in genes:
            transcripts.extend([tr for tr in g.lTranscripts])

        list_to_remove = Utils.aed_strand_filter_transcripts(transcripts)

        self.export(genes, list_to_remove)

        return 0
