#!/usr/bin/env python3

'''This module contains IsoformRanking class'''

import logging
import re
import multiprocessing

from distutils.util import strtobool
from collections import OrderedDict
from collections import Counter
from pathlib import Path

import numpy as np
import pysam

from ingenannot.commands.command import Command
from ingenannot.utils import Utils

class IsoformRanking(Command):
    '''
    The AED is a Command running AED annotation.

    Attributes:
    -----------
    gff_transcripts : Gff_transcripts
    bam : bam
    prefix : prefix
    paired : paired
    stranded : stranded
    sj_threshold : sj_threshold
    cov_threshold : cov_threshold
    alt_threshold : alt_threshold
    rescue : rescue
    sj_full : sj_full
    bam_fof : fof
    '''

    def __init__(self, args):

        self.gff_transcripts = args.Gff_transcripts
        self.bam = args.bam
        self.prefix = args.prefix
        self.paired = args.paired
        self.stranded = args.stranded
        self.sj_threshold = args.sj_threshold
        self.cov_threshold = args.cov_threshold
        self.alt_threshold = args.alt_threshold
        self.rescue = args.rescue
        self.sj_full = args.sj_full
        self.bam_fof = args.fof

    def get_intron_coordinates(self, tr):
        '''Return intron coordinates'''

        introns = []
        for i,e in enumerate(tr.lExons[:-1]):
            introns.append((e.end+1,tr.lExons[i+1].start-1))

        return introns

    def get_support_junction(self,chrom,start,end,strand,bam_file,paired,stranded,transcripts):
        '''Get support of annotated junctions'''

        junctions = self.junction_counter(chrom,start,end,strand,bam_file,paired,stranded)
        junctions = self._remove_spurious_junctions_not_in_annotations(junctions,transcripts)
        for junc, counts in junctions.items():
            nb_start = self.base_counter(chrom,junc[0]-2,junc[0]-1,strand,bam_file,paired, stranded)
            nb_stop = self.base_counter(chrom,junc[1]+1,junc[1]+2,strand,bam_file,paired, stranded)
            ratio = (counts/nb_start + counts/nb_stop)/2
            junctions[junc] = (counts,ratio)
        return junctions

    def base_counter(self,chrom,start,end,strand, bam_file, paired, stranded):
        '''Get all reads crossing this position, in a SJ or not.'''

        reads = []
        sam_file = pysam.AlignmentFile(bam_file, "rb")

        if stranded:
            if paired:
                if strand == -1:
                    reads = [read for read in sam_file.fetch(chrom,start,end)
                            if (read.is_reverse and read.is_read2 and read.is_proper_pair
                                and not read.is_secondary and not read.is_supplementary)
                            or (not read.is_reverse and read.is_read1 and read.is_proper_pair
                                and not read.is_secondary and not read.is_supplementary)]
                else:
                    reads = [read for read in sam_file.fetch(chrom,start,end)
                            if (read.is_reverse and read.is_read1 and read.is_proper_pair
                                and not read.is_secondary and not read.is_supplementary)
                            or (not read.is_reverse and read.is_read2 and read.is_proper_pair
                                and not read.is_secondary and not read.is_supplementary)]
            else: #single
                if strand == -1:
                    reads = [read for read in sam_file.fetch(chrom,start,end)
                            if not read.is_reverse and not read.is_secondary
                            and not read.is_supplementary]
                else:
                    reads = [read for read in sam_file.fetch(chrom,start,end)
                            if read.is_reverse and not read.is_secondary
                            and not read.is_supplementary]
        else:
            if paired:
                reads = [read for read in sam_file.fetch(chrom,start,end)
                        if not read.is_secondary and not read.is_supplementary
                        and read.is_proper_pair]
            else:
                reads = [read for read in sam_file.fetch(chrom,start,end)
                        if not read.is_secondary and not read.is_supplementary]

        return len(reads)

    def junction_counter(self,chrom,start,end,strand, bam_file, paired, stranded):
        '''get count per junction'''

        junctions = None
        sam_file = pysam.AlignmentFile(bam_file, "rb")
        if stranded:
            if paired:
                if strand == -1:
                    junctions = sam_file.find_introns((
                        read for read in sam_file.fetch(chrom,start,end)
                        if (read.is_reverse and read.is_read2 and read.is_proper_pair
                            and not read.is_secondary and not read.is_supplementary)
                        or (not read.is_reverse and read.is_read1 and read.is_proper_pair
                            and not read.is_secondary and not read.is_supplementary) ))
                else:
                    junctions = sam_file.find_introns((
                        read for read in sam_file.fetch(chrom,start,end)
                        if (read.is_reverse and read.is_read1 and read.is_proper_pair
                            and not read.is_secondary and not read.is_supplementary)
                        or (not read.is_reverse and read.is_read2 and read.is_proper_pair
                            and not read.is_secondary and not read.is_supplementary) ))
            else: #single
                if strand == -1:
                    junctions = sam_file.find_introns((
                        read for read in sam_file.fetch(chrom,start,end)
                        if not read.is_reverse and not read.is_secondary
                        and not read.is_supplementary))
                else:
                    junctions = sam_file.find_introns((
                        read for read in sam_file.fetch(chrom,start,end)
                        if read.is_reverse and not read.is_secondary
                        and not read.is_supplementary))
        else:
            if paired:
                junctions = sam_file.find_introns((
                    read for read in sam_file.fetch(chrom,start,end)
                    if not read.is_secondary and not read.is_supplementary and read.is_proper_pair))
            else:
                junctions = sam_file.find_introns((
                    read for read in sam_file.fetch(chrom,start,end)
                    if not read.is_secondary and not read.is_supplementary))

        return junctions

    def rank_junctions(self, junctions):
        '''rank junction per coverage'''

        return OrderedDict({j[0]:j[1] for j in sorted(junctions.items(),
            key=lambda x: x[1][1], reverse=True) if j[1][1] > self.sj_threshold})

    def get_top_expressed_based_on_shared_SJ(self, transcripts, junctions):
        '''get expression level based on junction support'''

        scores_all = {tr.id:[] for tr in transcripts}
        nb_shared_junctions = 0
        for i,j in enumerate(junctions):
            shared_junction = True
            tr_validate = []

            for tr in transcripts:
                if self.sj_full:
                    if not (j[0] > tr.start and j[1] < tr.end):
                        shared_junction = False
                        break
                else:
                    if (j[0] > tr.start and j[1] < tr.end)\
                    or (j[0] > tr.start and j[0]<tr.end and j[1] > tr.end)\
                    or (j[0]< tr.start and j[1] > tr.start and j[1] < tr.end):
                        pass
                    else:
                        shared_junction = False
                        break

            if shared_junction:
                nb_shared_junctions += 1
                for tr in transcripts:
                    if (j[0]+1,j[1]) in self.get_intron_coordinates(tr):
                        logging.debug(f"intron {j} found in {tr.id}"
                        f"{self.get_intron_coordinates(tr)}")
                        scores_all[tr.id].append(junctions[j][1])
                    else:
                        logging.debug(f"intron {j} not found in {tr.id}"
                        f"{self.get_intron_coordinates(tr)}")
                        overlapping_junctions = []
                        for ju in junctions:
                            if (ju[0]!= j[0]) or (ju[1] != j[1]):
                                if (ju[0]<j[0] and ju[1]>j[1]) \
                                or (ju[0]>j[0] and ju[1]<j[1]) \
                                or (ju[0]>=j[0] and ju[0]<j[1]) \
                                or (ju[1]<=j[1] and ju[1]>j[0]):
                                    overlapping_junctions.append(ju)
                        if overlapping_junctions:
                            injunction = []
                            for jo in overlapping_junctions:
                                if (jo[0]+1, jo[1]) in self.get_intron_coordinates(tr):
                                    injunction.append(junctions[jo][1])
                            if not injunction:
                                total = sum(junctions[jo][1] for jo
                                    in overlapping_junctions) + junctions[j][1]
                                scores_all[tr.id].append(max(1-total,0))
                            else:
                                scores_all[tr.id].append(min(injunction))

                        if not overlapping_junctions:
                            scores_all[tr.id].append(1-junctions[j][1])
        if nb_shared_junctions:
            mean = {}
            max_mean = 0
            for tr_id in scores_all:
                mean[tr_id] = (min(scores_all[tr_id]),np.mean(scores_all[tr_id]))
            classif = []
            alternatives_filtered = []
            for m in sorted(set(mean.values()), reverse=True):
                classif_mean = []
                for tr in transcripts:
                    if mean[tr.id] == m:
                        classif_mean.append(tr)
                        if m[0] < self.alt_threshold:
                            alternatives_filtered.append(tr.id)
                classif.append(classif_mean)
            return classif, alternatives_filtered
        return [transcripts], []

    def new_get_exon_coverage(self, transcripts, bam):
        '''get exon coverage'''

        samfile = pysam.AlignmentFile(bam, "r")

         # get all exons to compute one time coverage
        exon_coverage = {}
        seqid = transcripts[0][0].seqid
        self.working_tr_strand = transcripts[0][0].strand
        min_start = []
        max_end = []
        for g_tr in transcripts:
            for tr in g_tr:
                min_start.append(tr.get_min_exon_start())
                max_end.append(tr.get_max_exon_end())
                for ex in sorted(tr.lExons,key=lambda x: x.start):
                    exon_coverage[(ex.start-1,ex.end)] = 0

        start = min(min_start)-1
        end = max(max_end)
        cov =  samfile.count_coverage(seqid,start, end, read_callback=self.callback_filter_read)
        pos_cov = list(map(sum, zip(cov[0],cov[1],cov[2],cov[3])))
        for ex in exon_coverage:
            exon_coverage[ex] = pos_cov[ex[0]-start:ex[1]-start]

        return exon_coverage

    def get_top_expressed_based_on_coverage(self, transcripts, exon_coverage, idx):
        '''get top expressed transcript based oncoverage'''

        ranked_tr = []
        unranked_tr = []

        start = min([x.get_min_exon_start() for x in transcripts])
        end = max([x.get_max_exon_end() for x in transcripts])
        tr_positions = []


        # get coverage for each transcript/exons
        for tr in transcripts:
            positions = {x:None for x in range(start-1,end)} # in 0-index base
            for ex in sorted(tr.lExons,key=lambda x: x.start):
                for i,j in enumerate(range(ex.start-1,ex.end)):
                    positions[j] = exon_coverage[(ex.start-1,ex.end)][i]
            tr_positions.append(positions)

        # compute mean coverage on shared bases
        shared_bases = []
        for pos in range(start-1,end):
            shared = True
            for i,tr in enumerate(transcripts):
                if tr_positions[i][pos] is None:
                    shared = False
                    break
            if shared:
                shared_bases.append(tr_positions[0][pos])

        # shared bases null if fragmented isoform, non overlaping
        if len(shared_bases) == 0:
            logging.debug(f"rescue shared bases for {transcripts[0].gene_id}")
            shared_bases = self.rescue_shared_bases_non_overlapping_isoforms(
                    transcripts, tr_positions, start, end)

        median = np.median(shared_bases)
        threshold = median * self.cov_threshold

        if median == 0:
            unranked_tr = transcripts
            return ranked_tr, unranked_tr

        scores = {}

        for i,tr in enumerate(transcripts):
            positions = []
            for ex in sorted(tr.lExons,key=lambda x: x.start):
                positions.extend(range(ex.start-1,ex.end))
            score = len([tr_positions[i][x] for x in positions \
                        if tr_positions[i][x] > threshold]) -  \
                    len([tr_positions[i][x] for x in positions \
                        if tr_positions[i][x] < threshold])
            scores[tr.id] = score


        for i,s in enumerate(sorted(set(scores.values()), reverse=True)):
            for tr in transcripts:
                if scores[tr.id] == s:
                    # add median cov for weigth sum in case multiple bam
                    # add idx + rank for weigh in case multiple bam
                    ranked_tr.append((tr,median,idx+i*0.01))

        return ranked_tr, unranked_tr

    def rescue_shared_bases_non_overlapping_isoforms(self, transcripts, tr_positions, start, end):
        '''todo'''

        shared_bases = [None]*(end-start+1)
        shared_nb_transcripts = [0]*(end-start+1)
        for i,pos in enumerate(range(start-1,end)):
            for j,tr in enumerate(transcripts):
                if tr_positions[j][pos] is not None:
                    shared_nb_transcripts[i] += 1
                    shared_bases[i] = tr_positions[j][pos]
        max_tr = max(shared_nb_transcripts)
        return [x for i,x in enumerate(shared_bases) if shared_nb_transcripts[i] == max_tr]

    def callback_filter_read(self,read):
        '''
           callback function to filter count_coverage
           pysam function. Take into account, pairing and
           strand specificity
        '''

        if self.working_bam_is_stranded:
            if self.working_bam_is_paired:
                if self.working_tr_strand == -1:
                    if (read.is_reverse and read.is_read2) \
                    or ((not read.is_reverse) and read.is_read1):
                        return True
                else:
                    if (read.is_reverse and read.is_read1) \
                    or ((not read.is_reverse) and read.is_read2):
                        return True
            else: #single
                if self.working_tr_strand == -1:
                    if not read.is_reverse :
                        return True
                else:
                    if read.is_reverse :
                        return True
        else:
            return True
        return False

    def get_bam_files_to_analyze(self):
        '''
        return the list of bam files
        to analyze
        '''

        bams = []

        if self.bam_fof:
            with open(self.bam_fof, 'r') as f:
                for line in f:
                    if not re.match("^#",line):
                        values = line.rstrip().split("\t")
                        fh = values[0]
                        if not Path(fh).is_file():
                            logging.error(f"Problem conf, Missing bam file: {fh}")
                            raise Exception(f"Missing bam file: {fh}")
                        if not Path(f"{fh}.bai").is_file():
                            logging.error(f"Problem conf, Missing index (.bai) of bam file: {fh}")
                            raise Exception(f"Missing index (.bai) of bam file: {fh}")
                        paired = bool(strtobool(values[1]))
                        stranded = bool(strtobool(values[2]))
                        bams.append((fh,paired,stranded))
        elif self.bam:
            if not Path(self.bam).is_file():
                logging.error(f"Problem conf, Missing bam file: {self.bam}")
                raise Exception(f"Missing bam file: {self.bam}")
            if not Path(f"{self.bam}.bai").is_file():
                logging.error(f"Problem conf, Missing index (.bai) of bam file: {self.bam}")
                raise Exception(f"Missing index (.bai) of bam file: {self.bam}")
            bams.append((self.bam,self.paired,self.stranded))
        else:
            raise Exception("Missing at least one bam file to analyze")

        logging.info(f"{len(bams)} bam files to analyze")

        return bams

    def _remove_spurious_junctions_not_in_annotations(self, junctions,transcripts):
        '''remove new annotations not in assembled transcripts'''

        introns = []
        selected_junctions = {}
        for tr in transcripts:
            introns.extend([(i[0]-1, i[1]) for i in self.get_intron_coordinates(tr)])
        for j in junctions:
            if j in introns:
                selected_junctions[j] = junctions[j]
        return selected_junctions

    def ranking_transcripts(self, genes, bam_file, paired, stranded):
        '''rank transcripts'''

        ranked_transcripts = []
        ranked_transcripts_raw = []
        unclassified_transcripts = []
        alternatives_transcripts_filtered = []
        for g in genes:
            logging.debug(f"ranking gene {g.gene_id}")
            junctions = self.get_support_junction(
                    g.seqid,g.start,g.end,g.strand,bam_file, paired, stranded,g.lTranscripts)
            # remove junctions without enough support
            junctions = self.rank_junctions(junctions)

            transcripts = [] # list of working transcripts
            untranscripts = [] # list of working unclassified transcripts
            # remove transcript if less supported than RNA-seq !!! bad iso !
            for tr in g.lTranscripts:
                introns = self.get_intron_coordinates(tr)
                introns_status_ok = True
                for i in introns:
                    if (i[0]-1, i[1]) not in junctions:
                        logging.debug(f"transcript {tr.id} not ranked,"
                        f"introns not supported with rna-seq data")
                        introns_status_ok = False
                if introns_status_ok:
                    transcripts.append(tr)
                else:
                    untranscripts.append(tr)

            # rescue transcripts if no transcripts selected
            # with introns (ex 2 introns, 1 not supported)
            if self.rescue and len(transcripts) == 0:
                logging.debug(f"No transcripts \"junction reliable\" for gene {g.gene_id},"
                              f"all transcripts rescued")
                transcripts = g.lTranscripts
                untranscripts = []

            if len(transcripts) == 0: # no reliable transcript and no rescue
                unclassified_transcripts.append(untranscripts)
                continue
            top_transcripts_intermediate, alternatives_filtered = \
                    self.get_top_expressed_based_on_shared_SJ(transcripts,junctions)
            alternatives_transcripts_filtered.extend(alternatives_filtered)
            alternatives_transcripts_filtered.extend([t.id for t in untranscripts])

            exon_coverage = self.new_get_exon_coverage(top_transcripts_intermediate, bam_file)

            g_ranked_tr = []
            g_ranked_tr_raw = []
            for idx,group_tr in enumerate(top_transcripts_intermediate):
                ranked_tr, unranked_tr = \
                        self.get_top_expressed_based_on_coverage(group_tr, exon_coverage, idx)
                g_ranked_tr.extend(ranked_tr)
                g_ranked_tr_raw.append(ranked_tr)
                untranscripts.extend(unranked_tr)
            if g_ranked_tr:
                logging.debug(f"selected {g_ranked_tr[0][0].id}"
                              f"as best transcript for gene {g.gene_id}")
            ranked_transcripts.append(g_ranked_tr)
            ranked_transcripts_raw.append(g_ranked_tr_raw)
            unclassified_transcripts.append(untranscripts)

        return ranked_transcripts, unclassified_transcripts,\
               ranked_transcripts_raw, alternatives_transcripts_filtered

    def run(self):

        '''
        Suppose file with gene_id and transcript_id
        no clustering. Selection /ranking at tr level for
        each gene
        '''

        bam_files = self.get_bam_files_to_analyze()

        genes = Utils.extract_genes(self.gff_transcripts)
        ranked_transcripts = []
        ranked_transcripts_raw = []
        unclassified_transcripts = []
        alternatives_transcripts_filtered = []
        for bam in bam_files:

            ranked_transcripts_bam = []
            ranked_transcripts_raw_bam = []
            unclassified_transcripts_bam = []
            alternatives_transcripts_filtered_bam = []
            self.working_bam_is_paired = bam[1]
            self.working_bam_is_stranded = bam[2]
            logging.info("Analyzing bam file: {bam[0]}, paired: {bam[1]}, stranded: {bam[2]}")

            if Command.NB_CPUS > 1:
                ratio = 100
                if len(genes) < 100:
                    ratio = 5
                logging.info(f"{len(range(0,len(genes),ratio))} subprocesses to run:")
                pool = multiprocessing.Pool(Command.NB_CPUS)
                results = [pool.apply_async(self.ranking_transcripts,\
                        (genes[i:i + ratio], bam[0], bam[1], bam[2]))\
                        for idx,i in enumerate(range(0, len(genes), ratio))]
                for i,r in enumerate(results):
                    r_ranking, r_unclassif, r_ranking_raw, r_alt_filtered = r.get()
                    logging.info(f"Analysis done: {i+1}/{len(results)}")
                    ranked_transcripts_bam.extend(r_ranking)
                    ranked_transcripts_raw_bam.extend(r_ranking_raw)
                    unclassified_transcripts_bam.extend(r_unclassif)
                    alternatives_transcripts_filtered_bam.extend(r_alt_filtered)
                pool.close()
                pool.join()
            else:
                ranked_transcripts_bam, unclassified_transcripts_bam,\
                ranked_transcripts_raw_bam, alternatives_transcripts_filtered_bam = \
                self.ranking_transcripts(genes, bam[0], bam[1], bam[2])

            ranked_transcripts.append(ranked_transcripts_bam)
            ranked_transcripts_raw.append(ranked_transcripts_raw_bam)
            unclassified_transcripts.append(unclassified_transcripts_bam)
            alternatives_transcripts_filtered.extend(alternatives_transcripts_filtered_bam)

        # deduplicate alternatives_transcripts_filtered and keep only if filtered in all bam
        dedup_alternatives_transcripts_filtered = \
                self._dedup_alt_tr(alternatives_transcripts_filtered, len(bam_files))

        if len(bam_files) > 1:
            ranked_bam_results = self.rank_separate_bam_results(genes, ranked_transcripts)
            self.export(ranked_bam_results, f"{self.prefix}.ranking.gff",True)
            self.export(ranked_bam_results, f"{self.prefix}.top.gff",True, True)
            alt_iso = self.get_best_alternative_isoform(genes,\
                    ranked_transcripts_raw, dedup_alternatives_transcripts_filtered)
            self.export(alt_iso, f"{self.prefix}.alternatives.gff",True)

            unclassif_bam_results = self.unclassif_separate_bam_results(genes,\
                    ranked_bam_results, unclassified_transcripts)
            self.export(unclassif_bam_results, f"{self.prefix}.unclassif.gff",False)
        else: #direct export
            self.export(ranked_transcripts[0], f"{self.prefix}.ranking.gff",True)
            self.export(ranked_transcripts[0], f"{self.prefix}.top.gff",True, True)
            self.export(unclassified_transcripts[0], f"{self.prefix}.unclassif.gff",False)
            alt_iso = self.get_best_alternative_isoform(genes, ranked_transcripts_raw,\
                    dedup_alternatives_transcripts_filtered)
            self.export(alt_iso, f"{self.prefix}.alternatives.gff",True)

        return 0

    def _dedup_alt_tr(self, transcripts, nb_bam):
        '''dedup transcripts'''

        c = Counter(transcripts)
        return [tr for tr in c if c[tr] == nb_bam]

    def get_best_alternative_isoform(self, genes, ranked_transcripts, \
            alternatives_transcripts_filtered):
        '''return ranked best isoforms'''

        transcripts = []
        if len(ranked_transcripts) == 1:
            for bam in ranked_transcripts:
                for g in bam:
                    group = []
                    for g_tr in g:
                        if g_tr and g_tr[0][0].id not in alternatives_transcripts_filtered:
                            group.append(g_tr[0])
                    transcripts.append(group)
            return transcripts

        select_ranked = []
        rank = {g.gene_id:[] for g in genes}
        for bam in ranked_transcripts:
            for ltrs in bam:
                if ltrs:
                    if ltrs[0]:
                        rank[ltrs[0][0][0].gene_id].append(ltrs)
        s_ranked = {}
        # select most supported
        for g in rank:
            max_coverage = -1
            selected_ranking = None
            for i,ltr in enumerate(rank[g]):
                median_max_cov = -1
                tmp_select = []
                for u in ltr:
                    if u:
                        median_max_cov = max(median_max_cov,max(j[1] for j in u))
                        tmp_select.append(u[0])
                if median_max_cov > max_coverage and median_max_cov > -1:
                    max_coverage = median_max_cov
                    selected_ranking = tmp_select
            if selected_ranking:
                s_ranked[g] = selected_ranking

        # add new iso (need to be implemented)
        for g in rank:
            l_selected_tr = []
            for i,ltr in enumerate(rank[g]):
                for u in ltr:
                    if g in s_ranked:
                        l_selected_tr = [t[0] for t in s_ranked[g]]
                    find = False
                    for tr in u:
                        if tr[0].id in [t.id for t in l_selected_tr]:
                            find = True
                            break
                    if find is False and len(u) > 0:
                        if g in s_ranked:
                            s_ranked[g].append(u[0])
                        else:
                            s_ranked[g] = [u[0]]
            if g in s_ranked:
                select_ranked.append(s_ranked[g])

        select_ranked_filtered = []
        for ltr in select_ranked:
            l = []
            for tr in ltr:
                if tr[0].id not in alternatives_transcripts_filtered:
                    l.append(tr)
            select_ranked_filtered.append(l)
        return select_ranked_filtered

    def unclassif_separate_bam_results(self, genes, ranked_transcripts, unclassified_transcripts):
        """
        return unclassified transcripts if unclassified in all
        bam files
        """

        ranked_tr = []
        for g in ranked_transcripts:
            for tr in g:
                ranked_tr.append(tr[0].id)
        ranked_tr_id = list(set(ranked_tr))

        select_unclassified = set()
        rank = {g.gene_id:[] for g in genes}

        l = []
        for i,bam in enumerate(unclassified_transcripts):
            for ltrs in bam:
                for tr in ltrs:
                    l.append(tr.id)

        select_unclassified = set(l)
        unclassified = []

        for g in genes:
            l_tr = []
            for tr in g.lTranscripts:
                if tr.id in select_unclassified and tr.id not in ranked_tr_id:
                    l_tr.append(tr)
            unclassified.append(l_tr)

        return unclassified

    def rank_separate_bam_results(self, genes, ranked_transcripts):
        """
        rank the expression level based on the highest coverage
        level
        need to implement weigth based on position (available in
        ranked_transcripts, third row for each bam)
        WARNING: need to deal with missing isoforms
        in some bams.
        """

        select_ranked = []
        rank = {g.gene_id:[] for g in genes}

        for bam in ranked_transcripts:
            for ltrs in bam:
                if ltrs:
                    rank[ltrs[0][0].gene_id].append(ltrs)


        for g in rank:
            max_coverage = -1
            selected_ranking = None
            for i,ltr in enumerate(rank[g]):
                median_max_cov = (max(j[1] for j in ltr))
                if median_max_cov > max_coverage:
                    max_coverage = median_max_cov
                    selected_ranking = ltr
            if selected_ranking:
                select_ranked.append(selected_ranking)
        return select_ranked

    def export(self, g_transcripts, fname, classified=True, top=False):
        '''export isoforms'''

        # export same CDS
        with open(fname, 'w') as f:
            logging.info(f"Writing: {fname}")
            source = "ingenannot-isoform-ranking"
            for g_tr in g_transcripts:
                for idx,tr_median in enumerate(g_tr):
                    if top and idx > 0:
                        break
                    if classified:
                        tr = tr_median[0] # tr and median in tuple
                        tr.source = source
                        f.write(tr.to_gtf(atts={"gene_id":[tr.gene_id],
                            "transcript_id":[tr.id], "rank":[str(idx+1)]}))
                    else:
                        tr = tr_median # only tr
                        tr.source = source
                        f.write(tr.to_gtf(atts={"gene_id":[tr.gene_id],
                            "transcript_id":[tr.id], "rank":["unclassifed"]}))
                    for i, exon in enumerate(tr.lExons):
                        exon.source = source
                        f.write(exon.to_gtf(tr.gene_id, tr.id))
        f.close()
