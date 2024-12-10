#!/usr/bin/env python3

import logging
import re
import multiprocessing
import numpy as np
import pysam
import gzip

from ingenannot.utils.gff_reader import GFFReader
from ingenannot.utils.gene_builder import GeneBuilder

from ingenannot.entities.cluster import Cluster
from ingenannot.entities.metagene import MetaGene
from ingenannot.entities.gene import Gene

class Utils(object):


    @staticmethod
    def get_aed_from_attributes(genes):

        logging.info("Retrieving aed annotations")

        for g in genes:
            for tr in g.lTranscripts:
                tr.set_evidence_aed_info_from_attributes()


    @staticmethod
    def get_sources_from_fof(fof):
        """get sources from fof"""

        files = Utils._read_inputfile(fof)
        sources = [source[1] for source in files]
        return sources

    @staticmethod
    def extract_genes_from_fof(fof, coding_only=True):
        """gene extraction from fof"""

        files = Utils._read_inputfile(fof)
        sources = [source[1] for source in files]
        allgenes = []

        for fh in files:
            genes = Utils.extract_genes(fh[0], coding_only, fh[1])
            allgenes.extend(genes)
        logging.info("{} genes extracted from {} sources".format(len(allgenes), len(sources)))
        logging.info("{} transcripts extracted from {} sources".format(sum([len(x.lTranscripts) for x in allgenes]), len(sources)))
        return allgenes

    @staticmethod
    def extract_gaeval_from_fof(fof):
        """extract gaeval information for all files"""

        files = Utils._read_inputfile(fof)
        all_gaeval_infos = {}

        for fh in files:
            try:
                gaeval_infos = Utils.extract_gaeval_infos(fh[2],fh[1])
                all_gaeval_infos.update(gaeval_infos)
            except Exception as  e:
                logging.error(str(e))
        logging.info("Gaeval infos extracted from {} transcripts".format(len(all_gaeval_infos)))
        return all_gaeval_infos


    @staticmethod
    def extract_gaeval_infos(tsv_file, source="undefined"):
        """gaeval tsv extraction"""

        gaeval_infos = {}
        logging.info("reading {}".format(tsv_file))
        with open(tsv_file, 'r') as f:
            #read header
            header = f.readline()
            #read values
            for line in f:
                values = line.rstrip().split("\t")
                gaeval_infos[(values[0],source)] = values[2:]

        return gaeval_infos

    @staticmethod
    def add_gaeval_infos_to_transcripts(genes, gaeval_infos):
        """add gaeval info to transcript"""

        for g in genes:
            for tr in g.lTranscripts:
                if (tr.id,tr.source) in gaeval_infos:
                    tr.add_gaeval_infos(gaeval_infos[(tr.id,tr.source)])
                else:
                    logging.error("Missing gaeval infos for transcript: {}, source: {}".format(tr.id,tr.source))

    @staticmethod
    def extract_genes(gff_file, coding_only=True, source="undefined"):
        """gene extraction"""

        logging.info("reading {}".format(gff_file))

        allgenes = []
        reader = GFFReader(gff_file)
        features = []
        genes = []
        prevfeat = None
        builder = GeneBuilder(reader.fmt)
        for feat in reader.read():
            if not prevfeat:
                pass
            elif prevfeat.seqid != feat.seqid:
                genes.extend(builder.build_all_genes(features, coding_only=coding_only, source=source))
                features = []
            features.append(feat)
            prevfeat = feat
        genes.extend(builder.build_all_genes(features, coding_only=coding_only, source=source))
        # control model
        for g in genes:
            for tr in g.lTranscripts:
                if tr.start != tr.get_min_exon_start():
                    logging.debug("fixing transcript coordinates {}".format(tr.id))
                    tr.start = tr.get_min_exon_start()
                if tr.end != tr.get_max_exon_end():
                    logging.debug("fixing transcript coordinates {}".format(tr.id))
                    tr.end = tr.get_max_exon_end()
            g.start = g.get_min_exon_start()
            g.end = g.get_max_exon_end()


        allgenes.extend(genes)

        logging.info("{} genes extracted from {} - source: {}".format(len(allgenes), gff_file, source))


        return allgenes

    def _read_inputfile(fof):

        files = []
        with open(fof, 'r') as f:
            for line in f:
                if not re.match("^#",line):
                    files.append(line.rstrip().split("\t"))
        return files


    @staticmethod
    def clusterize(genes, cltype='cds', stranded=False, procs=1):
        '''clusterize genes from the same locus
        '''

        logging.info("Clustering genes based on '{}' coordinates, strand orientation: '{}'".format(cltype, stranded))

        references = []
        clusters = []
        for gene in genes:
                cl = None
                if cltype == 'cds':
                    cl = Cluster(gene.seqid, gene.get_min_cds_start(), gene.get_max_cds_end(), gene.strand)
                elif cltype == 'gene':
                    cl = Cluster(gene.seqid, gene.get_min_exon_start(), gene.get_max_exon_end(), gene.strand)

                cl.add_gene(gene, stranded=stranded)
                clusters.append(cl)
                references.append(gene.seqid)
        references = list(set(references))
        Utils.natural_sort(references)
        # join spanning clusters
        merged_clusters = []

        PROCS = procs

        if PROCS > 1:
            TASKS = []
            for ref in references:
                TASKS.append((Utils._clusterize_per_seq,(ref, [x for x in clusters if x.seqid == ref],stranded)))
            pool = multiprocessing.Pool(PROCS)
            results = [pool.apply_async(Utils.working_process,t) for t in TASKS]
            for i,r in enumerate(results):
                r_clusters = r.get()
                merged_clusters.extend(r_clusters)
            pool.close()
            pool.join()
        else:
            for ref in references:
                clusters_ref = [x for x in clusters if x.seqid == ref]
                merged_clusters_ref = Utils._clusterize_per_seq(ref, clusters_ref, stranded)
                merged_clusters.extend(merged_clusters_ref)
        logging.info("{} clusters generated".format(len(merged_clusters)))

        return merged_clusters

    @staticmethod
    def clusterize_transcripts(transcripts, stranded=False, procs=1):
        '''clusterize transcripts from the same locus
        '''

        logging.info("Clustering trasncripts based on exon coordinates, strand orientation: '{}'".format(stranded))

        references = []
        clusters = []
        for tr in transcripts:
                cl = Cluster(tr.seqid, tr.get_min_exon_start(), tr.get_max_exon_end(), tr.strand)

                #cl.add_gene(gene, stranded=stranded)
                # create virtual gene for each tr
                g = Gene('gene_{}'.format(tr.id),tr.seqid,tr.start, tr.end, strand=tr.strand)
                g.add_transcript(tr)
                cl.add_gene(g, stranded=stranded)
                clusters.append(cl)
                references.append(tr.seqid)
        references = list(set(references))
        Utils.natural_sort(references)
        # join spanning clusters
        merged_clusters = []

        PROCS = procs

        if PROCS > 1:
            TASKS = []
            for ref in references:
                TASKS.append((Utils._clusterize_per_seq,(ref, [x for x in clusters if x.seqid == ref],stranded)))
            pool = multiprocessing.Pool(PROCS)
            results = [pool.apply_async(Utils.working_process,t) for t in TASKS]
            for i,r in enumerate(results):
                r_clusters = r.get()
                merged_clusters.extend(r_clusters)
            pool.close()
            pool.join()
        else:
            for ref in references:
                clusters_ref = [x for x in clusters if x.seqid == ref]
                merged_clusters_ref = Utils._clusterize_per_seq(ref, clusters_ref, stranded)
                merged_clusters.extend(merged_clusters_ref)
        logging.info("{} clusters generated".format(len(merged_clusters)))

        return merged_clusters

    def _clusterize_per_seq_recursive(ref,clusters_ref, stranded):

        merged_clusters_ref = []
        clusters_ref.sort(key=lambda x: x.start)
        for cl in clusters_ref:
            merge = False
            for i,cl2 in enumerate(merged_clusters_ref):
#                if cl2.is_cluster_spanning(cl, stranded=stranded):
                if cl2.is_cluster_spanning_min_cov(cl, stranded=stranded, cov=0.1):
                    merged_clusters_ref[i] = Cluster.merge([cl2,cl], stranded=stranded)
                    merge = True
                    break
            if not merge:
                merged_clusters_ref.append(cl)

        # recursive
        if len(merged_clusters_ref) != len(clusters_ref):
            merged_clusters_ref = Utils._clusterize_per_seq_recursive(ref, merged_clusters_ref,stranded)

        return merged_clusters_ref


    def _clusterize_per_seq(ref,clusters_ref, stranded):

        merged_clusters_ref = Utils._clusterize_per_seq_recursive(ref, clusters_ref,stranded)

        logging.info("{} clusters for sequence: {}".format(len(merged_clusters_ref), ref))
        return merged_clusters_ref

    def _atoi(text):
        return int(text) if text.isdigit() else text

    def _natural_keys(text):
        '''
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        '''
        return [ Utils._atoi(c) for c in re.split('(\d+)', text) ]

    def natural_sort(ls):

        ls.sort(key=Utils._natural_keys)

    def working_process(func, args):
        result = func(*args)
        return result

    def get_metagenes_from_clusters(clusters):

        lMetagenes = []
        for i,cl in enumerate(clusters):
            seqid = cl.seqid
            start = min([gene.start for gene in cl.genes])
            end = max([gene.end for gene in cl.genes])
            transcripts = []
            for gene in cl.genes:
                transcripts.extend(gene.lTranscripts)
            m = MetaGene(i,seqid, start, end, transcripts)
            # DEBUG add for comapre (test recursif !!!)
            m.genes = cl.genes
            lMetagenes.append(m)
        logging.info(f"{len(lMetagenes)} metagenes built")
        return lMetagenes



    @staticmethod
    def statistics(genes, genome=''):
        '''Compute gene metrics'''

        metrics = {}
        metrics['nb_genes'] = len(genes)
        len_genes = sorted([g.end -g.start +1 for g in genes])
        metrics['average_gene_length'] = sum(len_genes)/len(len_genes)
        metrics['median_gene_length'] = len_genes[int(len(len_genes)/2)]
        metrics['min_gene_length'] = len_genes[0]
        metrics['max_gene_length'] =  len_genes[-1]
        len_transcripts = []
        transcripts_per_gene = []
        for g in genes:
            for tr in g.lTranscripts:
                len_transcripts.append(tr.end-tr.start + 1)
            transcripts_per_gene.append(len(g.lTranscripts))
        len_transcripts.sort()

        metrics['nb_transcripts'] = len(len_transcripts)
        metrics['average_transcripts_per_gene'] = sum(transcripts_per_gene)/len(transcripts_per_gene)
        metrics['average_transcript_length'] = sum(len_transcripts)/len(len_transcripts)
        metrics['median_transcript_length'] = len_transcripts[int(len(len_transcripts)/2)]
        metrics['min_transcript_length'] = len_transcripts[0]
        metrics['max_transcript_length'] = len_transcripts[-1]
        len_exons = []
        exons_per_transcript = []
        for g in genes:
            for tr in g.lTranscripts:
                for ex in tr.lExons:
                    len_exons.append(ex.end-ex.start + 1)
                exons_per_transcript.append(len(tr.lExons))
        len_exons.sort()
        metrics['nb_exons'] = len(len_exons)
        metrics['average_exons_per_transcript'] = sum(exons_per_transcript)/len(exons_per_transcript)
        metrics['average_exon_length'] = sum(len_exons)/len(len_exons)
        metrics['median_exon_length'] = len_exons[int(len(len_exons)/2)]
        metrics['min_exon_length'] = len_exons[0]
        metrics['max_exon_length'] = len_exons[-1]
        metrics['nb_transcript_mono_exon'] = exons_per_transcript.count(1)
        len_introns = []
        introns_per_transcript = []
        for g in genes:
            for tr in g.lTranscripts:
                for intron in tr.getlIntrons():
                    len_introns.append(intron.end-intron.start + 1)
                introns_per_transcript.append(len(tr.getlIntrons()))
        len_introns.sort()

        metrics['nb_introns'] = len(len_introns)
        metrics['average_introns_per_transcript'] = sum(introns_per_transcript)/len(introns_per_transcript)
        metrics['average_intron_length'] = sum(len_introns)/len(len_introns)
        metrics['median_intron_length'] = len_introns[int(len(len_introns)/2)]
        metrics['min_intron_length'] = len_introns[0]
        metrics['max_intron_length'] = len_introns[-1]
        len_CDS = []
        CDS_completness = []
        for g in genes:
            for tr in g.lTranscripts:
                len_CDS.append(tr.getCDSTotalLength())
                if genome:
                    CDS_completness.append(tr.is_cds_partial(genome))
        len_CDS.sort()
        metrics['nb_CDS'] = len(len_CDS)
        if genome:
            metrics['nb_complete_CDS'] = CDS_completness.count(False)
            metrics['nb_partial_CDS'] = CDS_completness.count(True)
        metrics['average_CDS_length'] = sum(len_CDS)/len(len_CDS)
        metrics['median_CDS_length'] = len_CDS[int(len(len_CDS)/2)]
        metrics['min_CDS_length'] = len_CDS[0]
        metrics['max_CDS_length'] = len_CDS[-1]

        nb_tr_utrs = 0
        five_utrs = []
        three_utrs = []
        for g in genes:
            for tr in g.lTranscripts:
                five_utr = tr.infer_five_prime_utrs()
                three_utr = tr.infer_three_prime_utrs()
                len_five_utr = 0
                len_three_utr = 0
                len_five_utr = sum([i[1]-i[0]+1 for i in five_utr])
                len_three_utr = sum([i[1]-i[0]+1 for i in three_utr])
                if len_five_utr or len_three_utr:
                    nb_tr_utrs += 1
                    if len_five_utr:
                        five_utrs.append(len_five_utr)
                    if len_three_utr:
                        three_utrs.append(len_three_utr)

        five_utrs.sort()
        three_utrs.sort()
        metrics['nb_transcripts_with_utr'] = nb_tr_utrs
        if len(five_utrs) > 0:
            metrics['average_five_prime_utr_length'] = sum(five_utrs)/len(five_utrs)
            metrics['median_five_prime_utr_length'] = five_utrs[int(len(five_utrs)/2)]
            metrics['min_five_prime_utr_length'] = five_utrs[0]
            metrics['max_five_prime_utr_length'] = five_utrs[-1]
        if len(three_utrs) > 0:
            metrics['average_three_prime_utr_length'] = sum(three_utrs)/len(three_utrs)
            metrics['median_three_prime_utr_length'] = three_utrs[int(len(three_utrs)/2)]
            metrics['min_three_prime_utr_length'] = three_utrs[0]
            metrics['max_three_prime_utr_length'] = three_utrs[-1]

        return metrics


    @staticmethod
    def reverse_complement(seq):
        """reverse complement table"""

        table = { 'a':'t',
                  't':'a',
                  'c':'g',
                  'g':'c',
                  'A':'T',
                  'T':'A',
                  'C':'G',
                  'G':'C',
                  'N':'N',
                  'n':'n',
                  '-':'-'}
        Rev = []
        for base in seq[::-1]:
            Rev.append(table[base])

        return ''.join(Rev)

    @staticmethod
    def translate(codon):
            """codon translation table"""
 
            table = { 'TTT' : 'F',
                      'TTC' : 'F',
                      'TTA' : 'L',
                      'TTG' : 'L',
                      'TCT' : 'S',
                      'TCC' : 'S',
                      'TCA' : 'S',
                      'TCG' : 'S',
                      'TAT' : 'Y',
                      'TAC' : 'Y',
                      'TAA' : '*',
                      'TAG' : '*',
                      'TGT' : 'C',
                      'TGC' : 'C',
                      'TGA' : '*',
                      'TGG' : 'W',
                      'CTT' : 'L',
                      'CTC' : 'L',
                      'CTA' : 'L',
                      'CTG' : 'L',
                      'CCT' : 'P',
                      'CCC' : 'P',
                      'CCA' : 'P',
                      'CCG' : 'P',
                      'CAT' : 'H',
                      'CAC' : 'H',
                      'CAA' : 'Q',
                      'CAG' : 'Q',
                      'CGT' : 'R',
                      'CGC' : 'R',
                      'CGA' : 'R',
                      'CGG' : 'R',
                      'ATT' : 'I',
                      'ATC' : 'I',
                      'ATA' : 'I',
                      'ATG' : 'M',
                      'ACT' : 'T',
                      'ACC' : 'T',
                      'ACA' : 'T',
                      'ACG' : 'T',
                      'AAT' : 'N',
                      'AAC' : 'N',
                      'AAA' : 'K',
                      'AAG' : 'K',
                      'AGT' : 'S',
                      'AGC' : 'S',
                      'AGA' : 'R',
                      'AGG' : 'R',
                      'GTT' : 'V',
                      'GTC' : 'V',
                      'GTA' : 'V',
                      'GTG' : 'V',
                      'GCT' : 'A',
                      'GCC' : 'A',
                      'GCA' : 'A',
                      'GCG' : 'A',
                      'GAT' : 'D',
                      'GAC' : 'D',
                      'GAA' : 'E',
                      'GAG' : 'E',
                      'GGT' : 'G',
                      'GGC' : 'G',
                      'GGA' : 'G',
                      'GGG' : 'G'}

            if codon not in table:
                return ''

            return table[codon]

    @staticmethod
    def get_seq_length_from_fasta(fasta_path):

        seqs = {}
        fasta = pysam.FastaFile(fasta_path)
        for seq in fasta.references:
            seqs[seq] = fasta.get_reference_length(seq)
        return seqs

    @staticmethod
    def get_intergenic_coordinates(genes, seqs, min_len=0):

        references = list(set([g.seqid for g in genes]))
        Utils.natural_sort(references)
        intergenic_regions = []
        for ref in references:
            if ref not in seqs:
                raise Exception("Error genes on unknown sequence")

            start = 1
            for g in sorted([g for g in genes if g.seqid == ref], key=lambda x: x.get_min_cds_start()):
                if g.get_min_cds_start()-1 > start:
                    if g.get_min_cds_start() - start > min_len:
                        intergenic_regions.append((g.seqid, start, g.get_min_cds_start()-1))
                start = g.get_max_cds_end() + 1
            if start < seqs[ref] and seqs[ref] - start > min_len:
                intergenic_regions.append((ref, start, seqs[ref]))
        logging.info("{} intergenic regions extracted".format(len(intergenic_regions)))
        return intergenic_regions



    def atoi(text):
        return int(text) if text.isdigit() else text
    
    def natural_keys(text):
        '''
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        '''
        return [ Utils.atoi(c) for c in re.split('(\d+)', text) ]
   
    @staticmethod
    def natural_sort(ls):
    
        ls.sort(key=Utils.natural_keys)

    @staticmethod
    def rank_transcripts(transcripts, gaeval):
        """double sort tr and pr, compare list, when
           discrepency, use distances"""

        l_sorted = []
        l_tr_rank = sorted(transcripts, key=lambda tr: (min(tr.best_tr_evidence[1],tr.best_lg_evidence[1]), tr.best_bx_evidence[1]))
        l_pr_rank = sorted(transcripts, key=lambda tr: (tr.best_bx_evidence[1], min(tr.best_tr_evidence[1],tr.best_lg_evidence[1])))
        for idx in range(0,len(transcripts)):
            tr_to_remove = None
            if l_tr_rank[0] == l_pr_rank[0]:
                tr_to_remove = l_tr_rank[0]
            elif l_tr_rank[0].best_bx_evidence[1] == l_pr_rank[0].best_bx_evidence[1]:
                tr_to_remove = l_tr_rank[0]
            else:
                if gaeval:
                    if l_pr_rank[0].gaeval_infos['int'] > l_tr_rank[0].gaeval_infos['int']:
                        tr_to_remove = l_pr_rank[0]
                    else:
                        tr_to_remove = l_tr_rank[0]
                else:
                    tr_delta = l_pr_rank[0].best_tr_evidence[1] - l_tr_rank[0].best_tr_evidence[1]
                    # add stronger weigth on protein distance 
#                    pr_delta = (l_tr_rank[0].best_bx_evidence[1] - l_pr_rank[0].best_bx_evidence[1]) * 1.5
                    pr_delta = l_tr_rank[0].best_bx_evidence[1] - l_pr_rank[0].best_bx_evidence[1]

                    # To validate BUG ? order
                    if tr_delta >= pr_delta:
                        tr_to_remove = l_tr_rank[0]
                    else:
                        tr_to_remove = l_pr_rank[0]
            l_sorted.append(tr_to_remove)
            l_tr_rank.remove(tr_to_remove)
            l_pr_rank.remove(tr_to_remove)

        return l_sorted

    @staticmethod
    def aed_strand_filter_transcripts(transcripts):

        conflict_list = []
        tr_dict = {}
        references = set([tr.seqid for tr in transcripts])
        for ref in references:
            ref_tr = sorted([tr for tr in transcripts if tr.seqid == ref], key=lambda x: x.get_min_cds_start())
            for i,tr in enumerate(ref_tr[:-1]):
                    tr_dict[(tr.id,tr.source)] = tr
                    for tr2 in ref_tr[i+1:]:
                      if tr.is_feature_spanning(tr2):
                        if tr.overlap_cds_with_other_transcript_cds(tr2):
                            conflict_list.append(((tr.id,tr.source), (tr2.id,tr2.source)))

            # add last tr in dict
            tr_dict[(ref_tr[-1].id,ref_tr[-1].source)] = ref_tr[-1]

        logging.info("{} potential conflicts to resolved".format(len(conflict_list)))

        list_to_remove = []
        for cf in conflict_list:
            l = Utils.rank_transcripts([tr_dict[cf[0]],tr_dict[cf[1]]],False)
            if l[0] not in list_to_remove:
                list_to_remove.append(l[1])

        return list_to_remove
