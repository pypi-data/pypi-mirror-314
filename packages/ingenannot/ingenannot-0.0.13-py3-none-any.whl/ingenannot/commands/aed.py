#/usr/bin/env python3

'''This module contains AED class'''

import logging
from ingenannot.utils import Utils
from ingenannot.utils.annot_edit_distance import AnnotEditDistance
from ingenannot.utils.graphics import Graphics
from ingenannot.commands.command import Command

class AED(Command):
    '''
    The AED is a Command running AED annotation.

    Attributes:
    -----------
    input : input file
    output : output file
    source : source
    transcript_gff_file : transcript_gff_file
    transcript_gff_file_source : transcript_gff_file_source
    transcript_gff_file_stranded : transcript_gff_file_stranded
    protein_gff_file : protein_gff_file
    protein_gff_file_source : protein_gff_file_source
    protein_gff_file_stranded : protein_gff_file_stranded
    penalty_overflow : penalty_overflow
    longread_gff_file : longread_gff_file
    longread_gff_file_source : longread_gff_file_source
    longread_penalty_overflow : longread_penalty_overflow
    aedtr : aedtr
    aedpr : aedpr
    aed_tr_cds_only : aed_tr_cds_only
    '''

    def __init__(self, args):

        self.input = args.Input
        self.output = args.Output
        self.source = args.source
        self.transcript_gff_file = args.evtr
        self.transcript_gff_file_source = args.evtr_source
        self.transcript_gff_file_stranded = args.evtrstranded
        self.protein_gff_file = args.evpr
        self.protein_gff_file_source = args.evpr_source
        self.protein_gff_file_stranded = args.evprstranded
        self.penalty_overflow = args.penalty_overflow
        self.longread_gff_file = args.longreads
        self.longread_gff_file_source = args.longreads_source
        self.longread_penalty_overflow = args.longreads_penalty_overflow
        self.aedtr = args.aedtr
        self.aedpr = args.aedpr
        self.aed_tr_cds_only = args.aed_tr_cds_only

    def export(self, allgenes):
        '''export in gff'''

        with open(self.output, 'w') as f:
            for gene in allgenes:
                atts = {'ID':[gene.gene_id],'source':[gene.source]}
                f.write(gene.to_gff3(atts=atts))
                for tr in gene.lTranscripts:
                    if not tr.best_tr_evidence[0]:
                        ev_tr = "None"
                    else:
                        ev_tr = tr.best_tr_evidence[0]
                    if not tr.best_bx_evidence[0]:
                        ev_bx = "None"
                    else:
                        ev_bx = tr.best_bx_evidence[0]

                    atts = {'ID':[tr.id], 'source':[gene.source],
                            'Parent':[gene.gene_id], 'ev_tr': [ev_tr],
                           # 'aed_ev_tr':['{:.4f}'.format(tr.best_tr_evidence[1])],
                            'aed_ev_tr':[f"{tr.best_tr_evidence[1]:.4f}"],
                            'ev_tr_penalty': [tr.tr_penalty], 'ev_pr' : [ev_bx],
                            'aed_ev_pr' : [f'{tr.best_bx_evidence[1]:.4f}']}

                    if self.longread_gff_file:
                        if not tr.best_lg_evidence[0]:
                            ev_lg = "None"
                        else:
                            ev_lg = tr.best_lg_evidence[0]
                        atts_lg = {'ev_lg': [ev_lg],
                                'aed_ev_lg':[f'{tr.best_lg_evidence[1]:.4f}'],
                                'ev_lg_penalty':[tr.lg_penalty]}
                        atts.update(atts_lg)

                    f.write(tr.to_gff3(atts=atts))
                    for exon in tr.lExons:
                        atts = {'ID':[exon.exon_id], 'source':[gene.source],
                                'Parent':[",".join(exon.lTranscript_ids)]}
                        f.write(exon.to_gff3(atts=atts))
                    for i,cds in enumerate(tr.lCDS):
                        atts = {'ID':[cds.cds_id], 'source':[gene.source],'Parent':[tr.id]}
                        f.write(cds.to_gff3(atts=atts))
        f.close()

    def run(self):
        '''launch command'''

        genes = Utils.extract_genes(self.input, True, self.source)

        genes = AnnotEditDistance.compute_aed(genes, self.transcript_gff_file,
                self.transcript_gff_file_stranded, self.transcript_gff_file_source,
                self.penalty_overflow, evtype="tr", cds_only=self.aed_tr_cds_only,
                procs=Command.NB_CPUS)

        genes = AnnotEditDistance.compute_aed(genes, self.protein_gff_file,
                self.protein_gff_file_stranded, self.protein_gff_file_source,
                0.0, evtype="pr",cds_only=True, procs=Command.NB_CPUS)

        if self.longread_gff_file:
            genes = AnnotEditDistance.compute_aed(genes, self.longread_gff_file,
                    True, self.longread_gff_file_source,
                    self.longread_penalty_overflow, evtype="lg",
                    cds_only=self.aed_tr_cds_only, procs=Command.NB_CPUS)

        self.export(genes)

        transcripts = []
        for g in genes:
            transcripts.extend(g.lTranscripts)

        use_ev_lg = False
        if self.longread_gff_file:
            use_ev_lg = True

        l_aed_tr, l_aed_tr_no_penalty, l_aed_pr, l_aed_pr_no_penalty = \
                Graphics.get_values_for_aed_scatter_hist(transcripts,use_ev_lg)

        graph_output = f"scatter_hist_aed.{self.source}.png"
        Graphics.plot_aed_scatter_hist([l_aed_tr, l_aed_pr, l_aed_tr_no_penalty,
            l_aed_pr_no_penalty], self.aedtr, self.aedpr, graph_output,
            legend=['aed_tr','aed_pr'], title="None")
        logging.info(f"Scatter plot exported in {graph_output}")

        return 0
