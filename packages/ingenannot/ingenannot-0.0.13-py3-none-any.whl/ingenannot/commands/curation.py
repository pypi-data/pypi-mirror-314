#/usr/bin/env python3

'''This module contains Curation class'''

import logging
from ingenannot.utils import Utils
from ingenannot.commands.command import Command
from ingenannot.utils.graphics import Graphics

class Curation(Command):
    '''
    The Curation is a Command running prioritization of
    gene manual curation.

    Attributes:
    -----------
    input: input file
    output: output file
    graph_out: output graphics
    graph_title: graphics title
    '''

    def __init__(self, args):

        self.input = args.Input
        self.output = args.Output
        self.graph_out = args.graphout
        self.graph_title = args.graphtitle

    def _classify_transcripts(self, genes):
        '''
        classify transcripts in categories
        with level of confidence.
        7 categories expected:
        1: high confidence
        2: good confidence
        3: moderate confidence
        4: high to moderate confidence, with penalty on structure
        5: moderate confidence, supported by one evidence type
        6: bad confidence
        7: no support, only ab-initio prediction
        '''

        categories = [[] for i in range(7)]
        for gene in genes:
            for trans in gene.lTranscripts:
                aed_trans = trans.best_tr_evidence[1]
                penalty_trans = trans.tr_penalty
                if trans.best_lg_evidence[1] < trans.best_tr_evidence[1]:
                    aed_trans = trans.best_lg_evidence[1]
                    penalty_trans = trans.lg_penalty

                # category 7
                if aed_trans == 1.0 and trans.best_bx_evidence[1] == 1.0:
                    categories[6].append(trans)
                    trans.dAttributes['curation']=['cat7']
                # category 1
                elif aed_trans < 0.1 and trans.best_bx_evidence[1] < 0.01 \
                        and penalty_trans != 'yes':
                    categories[0].append(trans)
                    trans.dAttributes['curation']=['cat1']
                # category 2
                elif (aed_trans < 0.1 and trans.best_bx_evidence[1] < 0.1 ) \
                        or (aed_trans < 0.5 and trans.best_bx_evidence[1] < 0.01) \
                        and penalty_trans != 'yes':
                    categories[1].append(trans)
                    trans.dAttributes['curation']=['cat2']
                # category 3
                elif aed_trans < 0.5 and trans.best_bx_evidence[1] < 0.1 and penalty_trans != 'yes':
                    categories[2].append(trans)
                    trans.dAttributes['curation']=['cat3']
                # category 3 
                elif aed_trans < 0.5 and trans.best_bx_evidence[1] < 0.1 and penalty_trans == 'yes':
                    categories[3].append(trans)
                    trans.dAttributes['curation']=['cat4']
                # category 4
                elif (aed_trans <= 0.1 and trans.best_bx_evidence[1] >= 0.1) \
                        or (aed_trans >= 0.5 and trans.best_bx_evidence[1] <= 0.02): 
                    categories[4].append(trans)
                    trans.dAttributes['curation']=['cat5']
                # category 6
                elif aed_trans <= 1.0 and trans.best_bx_evidence[1] <= 1.0:
                    categories[5].append(trans)
                    trans.dAttributes['curation']=['cat6']

        return categories, genes

    def export(self, allgenes):
        '''export in gff'''

        with open(self.output, 'w') as f:
            for gene in allgenes:
                atts = {'ID':[gene.gene_id]}
                f.write(gene.to_gff3())
                for tr in gene.lTranscripts:
                    f.write(tr.to_gff3(atts=tr.dAttributes))
                #dedup exons
                lExons = []
                for tr in gene.lTranscripts:
                    for i,exon in enumerate(tr.lExons):
                        atts = {'ID':[exon.exon_id],
                                'Parent':[",".join(exon.lTranscript_ids)]}
                        if exon.exon_id not in lExons:
                            f.write(exon.to_gff3(atts=atts))
                            lExons.append(exon.exon_id)
                for tr in gene.lTranscripts:
                    for i,cds in enumerate(tr.lCDS):
                        atts = {'ID':[cds.cds_id],'Parent':[tr.id]}
                        f.write(cds.to_gff3(atts=atts))

                for tr in gene.lTranscripts:
                    strand = '+'
                    if tr.strand == -1:
                        strand = '-'
                    five_prime_utrs = tr.infer_five_prime_utrs()
                    for i,utr in enumerate(five_prime_utrs):
                        atts = {'ID':[f'five_prime_UTR_{tr.id}_{i+1:03}'],
                                'Parent':[tr.id]}
                        str_atts = ''
                        for att,values in atts.items():
                            str_atts += f"{att}={','.join(values)};"
                        f.write(f"{tr.seqid}\tingenannot\tfive_prime_UTR\t" \
                                f"{utr[0]}\t{utr[1]}\t.\t{strand}\t.\t{str_atts}\n")
                    three_prime_utrs = tr.infer_three_prime_utrs()
                    for i,utr in enumerate(three_prime_utrs):
                        atts = {'ID':[f'three_prime_UTR_{tr.id}_{i+1:03}'],
                                'Parent':[tr.id]}
                        str_atts = ''
                        for att,values in atts.items():
                            str_atts += f"{att}={','.join(values)};"
                        f.write(f"{tr.seqid}\tingenannot\tthree_prime_UTR\t" \
                                f"{utr[0]}\t{utr[1]}\t.\t{strand}\t.\t{str_atts}\n")

        f.close()


    def run(self):
        '''launch command'''

        genes = Utils.extract_genes(self.input, True)
        Utils.get_aed_from_attributes(genes)

        transcripts = []
        for g in genes:
            transcripts.extend(g.lTranscripts)

        categories, genes_categorized = self._classify_transcripts(genes)

        transcripts = []
        for trlist in categories:
            transcripts.extend(trlist)

        graph_cats = []
        for category in categories:
            l_aed_tr, l_aed_tr_no_penalty, l_aed_pr, l_aed_pr_no_penalty = \
            Graphics.get_values_for_aed_scatter_hist(category, True)
            graph_cats.append([l_aed_tr,l_aed_pr])

        Graphics.plot_curation_scatter_hist(graph_cats
            , self.graph_out,
            legend=[f'cat1: high confidence (# {len(categories[0])})',\
                    f'cat2: good confidence (# {len(categories[1])})',\
                    f'cat3: moderate confidence (# {len(categories[2])})',\
                    f'cat4: high to moderate confidence, with penalty on structure (# {len(categories[3])})',\
                    f'cat5: moderate confidence, supported by one evidence type (# {len(categories[4])})',\
                    f'cat6: bad confidence (# {len(categories[5])})',\
                    f'cat7: no support, only ab-initio prediction (# {len(categories[6])})'],\
                    title=self.graph_title)

        logging.info(f"Scatter plot exported in {self.graph_out}")

        # export
        self.export(genes_categorized)
        logging.info(f'curation categories added in {self.output}')

        # print stdout catgeories
        print(f'cat1: high confidence;{len(categories[0])}\n'
              f'cat2: good confidence;{len(categories[1])}\n'
              f'cat3: moderate confidence;{len(categories[2])}\n'
              f'cat4: high to moderate confidence, with penalty on structure;{len(categories[3])}\n'
              f'cat5: moderate confidence, supported by one evidence type;{len(categories[4])}\n'
              f'cat6: bad confidence;{len(categories[5])}\n'
              f'cat7: no support, only ab-initio prediction;{len(categories[6])}')

        return 0
