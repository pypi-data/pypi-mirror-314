#!/usr/bin/env python3

'''This module contains Select class'''

import logging
import copy

from ingenannot.utils import Utils
from ingenannot.utils.annot_edit_distance import AnnotEditDistance
from ingenannot.commands.command import Command
from ingenannot.utils.graphics import Graphics

class Select(Command):
    '''
    The Select is a Command running annotation selection.

    Attributes:
    -----------
    fof : list of files
    output : output file
    clutype : clustering type
    clustranded : clustering stranded
    noaed : do not perform aed
    nb_sources_filtering : nbsrc_filter
    nbsrc_absolute : nbsrc_absolute
    transcript_gff_file : evtr
    transcript_gff_file_source : evtr_source
    transcript_gff_file_stranded : evtrstranded
    protein_gff_file : evpr
    protein_gff_file_source : evpr_source
    protein_gff_file_stranded : evprstranded
    aed_tr_cds_only : aed_tr_cds_only
    penalty_overflow : penalty_overflow
    aedtr_filtering : aedtr
    aedpr_filtering : aedpr
    use_ev_lg : use_ev_lg
    min_CDS_length : min_cds_len
    no_partial : no_partial
    genome_fasta_file : genome
    longread_gff_file : longreads
    longread_gff_file_source : longreads_source
    longread_penalty_overflow : longread_penalty_overflow
    gaeval : use gaeval
    prefix : prefix
    no_export : export
    no_cds_overlap : do not export cds with overlap
    '''

    def __init__(self, args):

        self.fof = args.fof
        self.output = args.Output
        self.clutype = args.clutype
        self.clustranded = args.clustranded
        self.noaed = args.noaed
        self.nb_sources_filtering = args.nbsrc_filter
        self.nbsrc_absolute = args.nbsrc_absolute
        self.transcript_gff_file = args.evtr
        self.transcript_gff_file_source = args.evtr_source
        self.transcript_gff_file_stranded = args.evtrstranded
        self.protein_gff_file = args.evpr
        self.protein_gff_file_source = args.evpr_source
        self.protein_gff_file_stranded = args.evprstranded
        self.aed_tr_cds_only = args.aed_tr_cds_only
        self.penalty_overflow = args.penalty_overflow
        self.aedtr_filtering = args.aedtr
        self.aedpr_filtering = args.aedpr
        self.use_ev_lg = args.use_ev_lg
        self.min_CDS_length = args.min_cds_len
        self.no_partial = args.no_partial
        self.genome_fasta_file = args.genome
        self.longread_gff_file = args.longreads
        self.longread_gff_file_source = args.longreads_source
        self.longread_penalty_overflow = args.longreads_penalty_overflow
        self.gaeval = args.gaeval
        self.prefix = args.prefix
        self.no_export = args.no_export
        self.no_cds_overlap = args.no_cds_overlap

        if self.no_partial and not self.genome_fasta_file:
            raise Exception("genome in fasta format required with no_partial genes")


    def filter_metagenes_required_number_sources(self, metagenes):
        '''filter metagenes with a minimum nb of sources'''

        logging.info("## Filtering metagenes for a required number of sources")
        logging.info(f"## required number of sources at least : {self.nbsrc_absolute}")
        logging.info(f"## number of metagenes before filtering of nb sources: {len(metagenes)}")

        filtered_metagenes = []
        for mg in metagenes:
            if mg.get_number_of_src() >= self.nbsrc_absolute:
                filtered_metagenes.append(mg)

        logging.info(f"## number of metagenes after filtering of nb sources: \
                {len(filtered_metagenes)}")

        return filtered_metagenes


    def _remove_small_cds_included(self, ltr):
        '''
        In some cases, a small CDS was defined
        when a longer one was predicted by another method
        This could be due to a very small fragmented transcript
        So, in case where no protein evidence support this,
        we remove the small CDS and keep the longest, if
        no penalty CDS structure
        By default only the next tr is analyzed. This prevent
        multi deletion of protein well supported by other method
        Remove orphan model
        '''

        new_tr = []
        for i, tr in enumerate(ltr[:-1]):
            to_keep = True
            if tr.best_bx_evidence[1] == 1.0 and (tr.tr_penalty != 'yes' \
                and tr.lg_penalty != 'yes') and (tr.best_tr_evidence[1] != 1.0 \
                or tr.best_lg_evidence[1] != 1.0):
                for tr2 in ltr[i+1:i+2]:
                    if tr2.best_bx_evidence[1] == 1.0 and (tr2.tr_penalty != 'yes' \
                        and tr2.lg_penalty != 'yes') and (tr2.best_tr_evidence[1] != 1.0 \
                        or tr2.best_lg_evidence[1] != 1.0):
                        if tr2.get_min_cds_start() < tr.get_min_cds_start() \
                            or tr2.get_max_cds_end() > tr.get_max_cds_end():
                            if tr.is_cds_included_in_other_cds(tr2):
                                if self.no_partial:
                                    if not tr2.is_cds_partial(self.genome_fasta_file):
                                        logging.debug(f"CDS of TR: {tr.id}, {tr.seqid}, \
                                        {tr.start} is in CDS of TR2: {tr2.id}, {tr2.seqid}, \
                                        {tr2.start}, removed")
                                        to_keep = False
                                else:
                                    logging.debug("CDS of TR: {tr.id}, {tr.seqid}, {tr.start} \
                                    is in CDS of TR2: {tr2.id}, {tr2.seqid}, {tr2.start}, removed")
                                    to_keep = False
            if to_keep:
                new_tr.append(tr)
        # add last tr
        new_tr.append(ltr[-1])
        return new_tr


    def filter(self, metagenes, nb_not_exported, coords=None):
        '''filter '''

        export_tr = []
        not_exported_tr = []

        for nb, mg in enumerate(metagenes):

            if nb%1000 == 0:
                logging.info(f"{nb} metagenes analyzed on {len(metagenes)}")

            current_mg_export_tr = []
            current_mg_not_export_tr = []
            lsorted_tmp = Utils.rank_transcripts(mg.lTranscripts, self.gaeval)

            # limit potential transcripts to coordinates (use for rescue overlapping CDS)
            lsorted = []
            if coords:
                for tr in lsorted_tmp:
                    if tr.get_min_cds_start() > coords[0] and tr.get_max_cds_end() < coords[1]:
                        lsorted.append(tr)
                lsorted_tmp = lsorted

            # new to validate
            post_filter = True
            if post_filter:
                lsorted_tmp = self._remove_small_cds_included(lsorted_tmp)


            lfilteredlen = []
            for tr in lsorted_tmp:
                if tr.getCDSTotalLength() >= self.min_CDS_length:
                    lfilteredlen.append(tr)


            lsorted = []
            if self.no_partial:
                #for tr in lsorted_tmp:
                for tr in lfilteredlen:
                    if not tr.is_cds_partial(self.genome_fasta_file):
                        lsorted.append(tr)
                    else:
                        logging.debug(f"Partial CDS for {tr.id}")
            else:
                lsorted = lfilteredlen


            if len(lsorted) == 0:
                logging.debug(f"No complete CDS for MetaGene {mg.id}, not exported")
                nb_not_exported += 1
                continue

            # keep first CDS (tr)
            tr = lsorted[0]
            if mg.get_number_of_src() < self.nb_sources_filtering:
                aed_tr = tr.best_tr_evidence[1]
                if self.use_ev_lg:
                    aed_tr = min(tr.best_tr_evidence[1],tr.best_lg_evidence[1])
                if aed_tr <= self.aedtr_filtering or tr.best_bx_evidence[1] <= self.aedpr_filtering:
                    export_tr.append(tr)
                    current_mg_export_tr.append(tr)
                else:
                    nb_not_exported += 1
                    not_exported_tr.append(tr)
                    current_mg_not_export_tr.append(tr)
                    continue
            else:
                export_tr.append(tr)
                current_mg_export_tr.append(tr)

            if len(current_mg_export_tr) > 0:
                # try to rescue other CDS  if no overlap
                for i,tr in enumerate(lsorted[1::]):
                    overlap = False
                    for j in current_mg_export_tr:
                        if tr.overlap_cds_with_other_transcript_cds(j):
                            overlap = True
                            break
                    if not overlap:
                        if mg.get_number_of_src_overlapping_tr(tr) < self.nb_sources_filtering:
                            aed_tr = tr.best_tr_evidence[1]
                            if self.use_ev_lg:
                                aed_tr = min(tr.best_tr_evidence[1],tr.best_lg_evidence[1])
                            if aed_tr <= self.aedtr_filtering \
                                or tr.best_bx_evidence[1] <= self.aedpr_filtering:
                                export_tr.append(tr)
                                current_mg_export_tr.append(tr)
                        else:
                            export_tr.append(tr)
                            current_mg_export_tr.append(tr)

        logging.debug(f"{nb_not_exported} metagenes not exported")

        return export_tr, not_exported_tr


    def export(self,allgenes, export_tr, fh):
        '''export selection in gff'''

        source = "ingenannot"
        references = list(set([x.seqid for x in allgenes]))
        Utils.natural_sort(references)

        with open(fh, 'w') as f:
            ID = 0
            for ref in references:
                seq_genes = [g for g in allgenes if g.seqid == ref]
                for tr in sorted([ t for t in export_tr if t.seqid == ref],
                        key=lambda x: x.get_min_cds_start()):
                    for gene in seq_genes:

                        if gene.gene_id == tr.gene_id and gene.source == tr.source:
                            ID += 1
                            atts = {'ID':[f'{self.prefix}_{ID:05}'],
                                    'gene_source':[gene.gene_id],
                                    'source':[f'{gene.source}']}

                            # change gene coordinates in case of selection of one isoform
                            gene.start = tr.start
                            gene.end = tr.end

                            f.write(gene.to_gff3(atts=atts, source=source))
                            if not tr.best_tr_evidence[0]:
                                ev_tr = "None"
                            else:
                                ev_tr = tr.best_tr_evidence[0]
                            if not tr.best_bx_evidence[0]:
                                ev_bx = "None"
                            else:
                                ev_bx = tr.best_bx_evidence[0]

                            atts = {'ID':[f'{self.prefix}_{ID:05}.1'],
                                    'transcript_source':[tr.id],'source':[gene.source],
                                    'Parent':[f'{self.prefix}_{ID:05}'],'ev_tr': [ev_tr],
                                    'aed_ev_tr':[f'{tr.best_tr_evidence[1]:.4f}'],
                                    'ev_tr_penalty': [tr.tr_penalty], 'ev_pr' : [ev_bx],
                                    'aed_ev_pr' : [f'{tr.best_bx_evidence[1]:.4f}']}

                            #if self.longread_gff_file:
                            if not tr.best_lg_evidence[0]:
                                ev_lg = "None"
                            else:
                                #ev_lg = tr.best_lg_evidence[0].id
                                ev_lg = tr.best_lg_evidence[0]
                            atts_lg = {'ev_lg': [ev_lg],
                                    'aed_ev_lg':[f'{tr.best_lg_evidence[1]:.4f}'],
                                    'ev_lg_penalty':[tr.lg_penalty]}
                            atts.update(atts_lg)

                            f.write(tr.to_gff3(atts=atts,source=source))

                            for i,exon in enumerate(tr.lExons):
                                atts = {'ID':[f'exon:{self.prefix}_{ID:05}.{i+1}'],
                                        'Parent':[f'{self.prefix}_{ID:05}.1']}
                                f.write(exon.to_gff3(atts=atts,source=source))
                            for i,cds in enumerate(tr.lCDS):
                                atts = { 'ID':[f'cds:{self.prefix}_{ID:05}.1'],
                                        'Parent':[f'{self.prefix}_{ID:05}.1']}
                                f.write(cds.to_gff3(atts=atts,source=source))
                            break
        f.close()


    def run(self):
        """"launch command"""

        genes = Utils.extract_genes_from_fof(self.fof)

        if self.noaed:
            Utils.get_aed_from_attributes(genes)
        else:
            if not self.transcript_gff_file:
                raise Exception("missing transcript evidence file: set --evtr parameter")
            if not self.protein_gff_file:
                raise Exception("missing protein evidence file: set --evpr parameter")

        if self.gaeval:
            gaeval_infos = Utils.extract_gaeval_from_fof(self.fof)
            Utils.add_gaeval_infos_to_transcripts(genes, gaeval_infos)

        clusters = Utils.clusterize(genes, cltype=self.clutype,
                stranded=self.clustranded, procs=Command.NB_CPUS)
        metagenes = Utils.get_metagenes_from_clusters(clusters)
        nb_metagenes = len(metagenes)
        ##debug
        if self.nbsrc_absolute > 1:
            metagenes = self.filter_metagenes_required_number_sources(metagenes)
        nb_removed_metagenes = nb_metagenes - len(metagenes)
        if not self.noaed:
            for metag in metagenes:
                metag.genes = AnnotEditDistance.compute_aed(metag.genes,
                        self.transcript_gff_file, self.transcript_gff_file_stranded,
                        self.transcript_gff_file_source, self.penalty_overflow, evtype="tr",
                        cds_only=self.aed_tr_cds_only, procs=Command.NB_CPUS)

                metag.genes = AnnotEditDistance.compute_aed(metag.genes,
                        self.protein_gff_file, self.protein_gff_file_stranded,
                        self.protein_gff_file_source, 0.0, evtype="pr", procs=Command.NB_CPUS)

                if self.longread_gff_file:
                    metag.genes = AnnotEditDistance.compute_aed(metag.genes,
                            self.longread_gff_file, True, self.longread_gff_file_source,
                            self.longread_penalty_overflow, evtype="lg",
                            cds_only=self.aed_tr_cds_only, procs=Command.NB_CPUS)

        transcripts, transcripts_not_exported = self.filter(metagenes, nb_removed_metagenes)
        if self.no_cds_overlap:
            logging.info("Analyzing CDS overlap")
            transcripts, strfr_transcripts_not_exported = self.aed_strand_filter(transcripts)
            nb_rescue = 0
            for strfr in strfr_transcripts_not_exported:
                rescue_tr = self.rescue_tr_overlapping_cds(strfr, metagenes, transcripts)
                if rescue_tr:
                    nb_rescue += 1
                    logging.debug("RESCUE {} instead of {}".format(rescue_tr[0].id, strfr.id))
                    transcripts.append(rescue_tr[0])
                else:

                    transcripts_not_exported.append(strfr)

            # rescue transcript if a non-overlapp

            logging.info(f"{nb_rescue} transcripts rescued after overlapping with other CDS")


        l_aed_tr, l_aed_tr_no_penalty, l_aed_pr, l_aed_pr_no_penalty = \
        Graphics.get_values_for_aed_scatter_hist(transcripts,self.use_ev_lg)

        graph_output = f"{self.output}.scatter_hist_aed.png"
        Graphics.plot_aed_scatter_hist([l_aed_tr, l_aed_pr, l_aed_tr_no_penalty,
            l_aed_pr_no_penalty], self.aedtr_filtering, self.aedpr_filtering,
            graph_output ,legend=['aed_tr','aed_pr'], title="all runs - density of aed")
        logging.info(f"Scatter plot exported in {graph_output}")

        self.export(genes,transcripts,self.output)
        if self.no_export :
            self.export(genes,transcripts_not_exported,"no-export.{}".format(self.output))

        return 0


    def aed_strand_filter(self, transcripts):
        '''filter overlapping CDS based on AED'''

        transcripts_not_exported = []

        list_to_remove = Utils.aed_strand_filter_transcripts(transcripts)

        new_transcripts = []
        for tr in transcripts:
            if tr not in list_to_remove:
                new_transcripts.append(tr)
            else:
                transcripts_not_exported.append(tr)

        logging.info(f"{len(transcripts_not_exported)} transcripts \
                removed due to overlapping with other CDS")

        return new_transcripts, transcripts_not_exported


    def rescue_tr_overlapping_cds(self, tr, metagenes, transcripts):
        '''rescue gene in case of overlaps '''

        tr_before = None
        tr_after = None

        transcripts_sorted = sorted([ tt for tt in transcripts if tt.seqid == tr.seqid ],
                                      key=lambda x: x.get_min_cds_start())

        for i,t in enumerate(transcripts_sorted[:-1]):
            if tr.get_min_cds_start() > transcripts_sorted[i].get_min_cds_start() \
                and tr.get_max_cds_end() < transcripts_sorted[i+1].get_max_cds_end():
                tr_before = transcripts_sorted[i]
                tr_after = transcripts_sorted[i+1]
        if not tr_before or not tr_after:
            return None
        meta = None
        for m in metagenes:
            if tr in m.lTranscripts:
                meta = copy.deepcopy(m)
                break
        filtered_tr = []
        for tran in meta.lTranscripts:
            if tran.get_min_cds_start() > tr_before.get_max_cds_end() \
                and tran.get_max_cds_end() < tr_after.get_min_cds_start():
                filtered_tr.append(tr)

        if len(filtered_tr) == 0:
            return None

        tr_filt, tr_filt_not_exported = self.filter([meta], 0,
                coords=(tr_before.get_max_cds_end(),tr_after.get_min_cds_start()))
        if tr_filt:
            return tr_filt

        return None
