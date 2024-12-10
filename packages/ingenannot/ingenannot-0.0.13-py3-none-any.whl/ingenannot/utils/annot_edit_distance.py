#!/usr/bin/env python3
'''
AnnotEditDistance
'''
import logging
import multiprocessing
import pysam

from ingenannot.utils.gene_builder import GeneBuilder
from ingenannot.utils.gff_reader import GTFReader, GFF3Reader


class AnnotEditDistance():
    """
    utility class computing necessary
    methods to provide AED between genes
    or transcipts
    """

    def __init__(self):
        """pass"""

    @staticmethod
    def sensitivity(tr1, tr2, tr1_no_utr=False, tr2_no_utr=False):
        """
        Compute sensitivity between 2 transcripts
        """
        sensitivity = 0
        tr1_tr2_shared = tr1.get_nb_shared_bases_with_another_transcript(tr2, tr1_no_utr, tr2_no_utr)
        tr2_specific = tr2.get_nb_specific_bases_vs_another_transcript(tr1, tr2_no_utr, tr1_no_utr)
        if (tr1_tr2_shared + tr2_specific) != 0:
            sensitivity = tr1_tr2_shared / (tr1_tr2_shared + tr2_specific)

        return sensitivity

    @staticmethod
    def specificity(tr1, tr2, tr1_no_utr=False, tr2_no_utr=False):
        """
        Compute specificity between 2 transcripts
        """
        tr1_tr2_shared = tr1.get_nb_shared_bases_with_another_transcript(tr2, tr1_no_utr, tr2_no_utr)
        tr1_specific = tr1.get_nb_specific_bases_vs_another_transcript(tr2, tr1_no_utr, tr2_no_utr)

        return tr1_tr2_shared / (tr1_tr2_shared + tr1_specific) 

    @staticmethod
    def accuracy(tr1, tr2, tr1_no_utr=False, tr2_no_utr=False):
        """
        Compute accuracy
        """
         
        sensitivity = 0
        tr1_tr2_shared = tr1.get_nb_shared_bases_with_another_transcript(tr2, tr1_no_utr, tr2_no_utr)
        tr1_specific = tr1.get_nb_specific_bases_vs_another_transcript(tr2, tr1_no_utr, tr2_no_utr)
        tr2_specific = tr2.get_nb_specific_bases_vs_another_transcript(tr1, tr2_no_utr, tr1_no_utr)
        if (tr1_tr2_shared + tr2_specific) != 0:
            sensitivity = tr1_tr2_shared / (tr1_tr2_shared + tr2_specific)

        specificity = tr1_tr2_shared / (tr1_tr2_shared + tr1_specific) 

        return (sensitivity + specificity) / 2 

    @staticmethod
    def incongruence(tr1, tr2, tr1_no_utr=False, tr2_no_utr=False):
        """
        Compute incongruence/distance between 2 transcripts
        """

        return 1 - AnnotEditDistance.accuracy(tr1,tr2,tr1_no_utr,tr2_no_utr)

    @staticmethod
    def annot_edit_distance_between_2_gene_releases(gn1, gn2):
        """
        Compute AED for 2 annotation releases
        It takes into account alternative transcripts
        and the AED is computed based on closest
        distance/incongruence between transcripts
        """

        distances = []
        for tr1 in gn1.lTranscripts:
            distance = 1.0
            for tr2 in gn2.lTranscripts:
                distance = min(distance, AnnotEditDistance.incongruence(tr1,tr2))
            distances.append(distance)

        if distances:
            return sum(distances) / len(distances)
        return 1.0

    @staticmethod
    def compute_aed(genes, gff_file, stranded, source, penalty_overflow, evtype="tr",
            cds_only=False, procs=1):
        '''compute aedpr'''

        if procs > 1:
            ratio = 100
            pool = multiprocessing.Pool(procs)
            results = [pool.apply_async(AnnotEditDistance._aed_job, (genes[i:i + ratio],
                gff_file,stranded, source, penalty_overflow, evtype, cds_only, idx+1,
                len(range(0, len(genes), ratio))))
                for idx,i in enumerate(range(0, len(genes), ratio))]
            new_genes = []
            for i,res in enumerate(results):
                r_genes = res.get()
                new_genes.extend(r_genes)
            genes = new_genes
            pool.close()
            pool.join()

        else:
            genes = AnnotEditDistance._aed_job(genes,gff_file, stranded, source,
                    penalty_overflow, evtype, cds_only, 1,1)

        return genes

    @classmethod
    def _aed_job(cls, genes, transcript_file, stranded=False, source="unknown",
            penalty_overflow=0.0, evtype="tr", cds_only=False, idx=1, tot=1):

        message_type = {"tr":"Transcriptomic", "lg":"Long reads based transcriptomic",
                "pr":"Proteomic"}
        logging.info("Starting %s evidence analysis %d/%d",message_type[evtype],idx, tot)
        tbx = pysam.TabixFile(transcript_file)
        # default gtf (tr and lg type)
        builder = GeneBuilder('gtf')
        if evtype == "pr":
            builder = GeneBuilder('gff3-blastx')
            if source == "miniprot":
                builder = GeneBuilder('gff3-miniprot')

        for idx_g,gene in enumerate(genes):
            features = []

            if gene.seqid not in tbx.contigs:
                continue

            min_start = [gene.start-1]
            max_end = [gene.end]
            for row in tbx.fetch(gene.seqid, gene.start-1, gene.end):
                min_start.append(int(row.split("\t")[3]))
                max_end.append(int(row.split("\t")[4]))
            rows = []
            for row in tbx.fetch(gene.seqid, min(min_start), max(max_end)):
                if gene.strand == 1 and row.split("\t")[6] == "+":
                    rows.append(row)
                elif gene.strand == -1 and row.split("\t")[6] == "-":
                    rows.append(row)
                else:
                    pass

            if evtype == "pr":
                if source == "miniprot":
                    for row in rows:
                        features.append(GFF3Reader.convertRowToFeature(str(row), downgraded=True))
                else:
                    for row in rows:
                        features.append(GFF3Reader.convertRowToFeature(str(row)))
            else:
                for row in rows:
                    features.append(GTFReader.convertRowToFeature(str(row)))
            
            if len(features) > 0:
                evidence_genes = builder.build_all_genes(features, coding_only=True, source=source)
                if len(evidence_genes) >1:
                    evidence_genes = builder.deduplicate_genes(evidence_genes) 
                
                for trans in gene.lTranscripts :
                    best_aed = 1.0
                    for egene in evidence_genes:
                        if stranded:
                            if trans.strand != egene.strand:
                                continue
                        for gtr in egene.lTranscripts:
                            flag_penalty = False
                            if evtype == "pr":

                                aed = AnnotEditDistance.incongruence(trans,gtr, tr1_no_utr=True, tr2_no_utr=True)
                                if aed < best_aed:
                                    trans.best_bx_evidence = (gtr.id,aed)
                                    best_aed = aed
                            else:
                                aed = 1.0
                                if evtype in ("tr","lg"):
                                    if cds_only:
                                        aed = AnnotEditDistance.incongruence(trans,gtr, tr1_no_utr=True, tr2_no_utr=False)
                                    else:
                                        aed = min(AnnotEditDistance.incongruence(trans,gtr, tr1_no_utr=True, tr2_no_utr=False),
                                        AnnotEditDistance.incongruence(trans,gtr, tr1_no_utr=False, tr2_no_utr=False))
                                if penalty_overflow > 0.0 and aed < 1.0:
                                    if trans.get_nb_specific_bases_vs_another_transcript(gtr,self_no_utr=True) > 0 \
                                    or gtr.get_nb_specific_bases_vs_another_transcript_specific_positions(
                                            trans,trans.get_min_cds_start(),trans.get_max_cds_end(), other_no_utr=True) > 0:
                                        aed += penalty_overflow
                                        flag_penalty = True
                                if aed < best_aed:
                                    penalty = "undef"
                                    if penalty_overflow > 0.0:
                                        if flag_penalty :
                                            penalty = "yes"
                                        else:
                                            penalty = "no"
                                    if evtype == "tr":
                                        trans.best_tr_evidence = (gtr.id,aed)
                                        trans.tr_penalty = penalty
                                    if evtype == "lg":
                                        trans.best_lg_evidence = (gtr.id,aed)
                                        trans.lg_penalty = penalty
                                    best_aed = aed

        logging.info("%s evidence analyzed %d/%d",message_type[evtype],idx,tot)
        return genes
