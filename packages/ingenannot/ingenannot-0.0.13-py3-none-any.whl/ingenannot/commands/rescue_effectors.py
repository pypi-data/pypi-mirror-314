#!/usr/bin/env python3

import os
import sys
import logging
import math
import re
import pysam
import multiprocessing
import pandas as pd

from ingenannot.commands.command import Command
from ingenannot.utils import Utils
from ingenannot.utils.effector_predictor import EffectorPredictor

from ingenannot.utils.gene_builder import GeneBuilder
from ingenannot.utils.gff_reader import GTFReader, GFF3Reader

from ingenannot.entities.gene import Gene
from ingenannot.entities.transcript import Transcript
from ingenannot.entities.exon import Exon
from ingenannot.entities.cds import CDS


class RescueEffectors(Command):

    def __init__(self, args):

        self.gff_genes = args.Gff_genes
        self.gff_transcripts = args.Gff_transcripts
        self.genome = args.Genome

        EffectorPredictor.TMHMM = args.tmhmm
        EffectorPredictor.SIGNALP = args.signalp
        EffectorPredictor.EFFECTORP = args.effectorp
        EffectorPredictor.TARGETP = args.targetp
        EffectorPredictor.SIGNALP_CPOS = args.signalp_cpos
        EffectorPredictor.EFFECTORP_THRESHOLD = args.effectorp_score
        EffectorPredictor.MAX_LENGTH = args.max_len
        EffectorPredictor.MIN_LENGTH = args.min_len

        self.min_intergenic_len = args.min_intergenic_len
        self.size_ratio = args.size_ratio
        self.tr_stranded = not(args.unstranded)
        self.gff3_output = args.output

    def extract_transcripts_overlapping_inter_genes(self, intergenes):

        source = "unknown"
        fraction = 0.99
        all_tr_to_remove = []
        all_tr_to_keep = []

        tbx = pysam.TabixFile(self.gff_transcripts)
        # default gtf (tr and lg type)
        builder = GeneBuilder('gtf')
        for ig in intergenes:
            features = []

            if ig[0] not in tbx.contigs:
                continue

            min_start = [ig[1]-1]
            max_end = [ig[2]]
            for row in tbx.fetch(ig[0],ig[1]-1,ig[2]):
                min_start.append(int(row.split("\t")[3]))
                max_end.append(int(row.split("\t")[4]))
            for row in tbx.fetch(ig[0], min(min_start), max(max_end)):
                features.append(GTFReader.convertRowToFeature(str(row)))
            if len(features) > 0:
                evidences_genes_to_remove = []
                evidences_genes_to_keep = []
                evidence_genes = builder.build_all_genes(features, coding_only=True, source=source)
                for g_tr in evidence_genes:
                    to_remove = False
                    nb_overlapping_bases = 0
                    if ig[1] <= g_tr.start <= ig[2] <= g_tr.end:
                        nb_overlapping_bases += ig[2]-g_tr.start+1
                    if g_tr.start <= ig[1] <= g_tr.end <= ig[2]:
                        nb_overlapping_bases += g_tr.end-ig[1]+1
                    if ig[1] <= g_tr.start <= g_tr.end <= ig[2]:
                        nb_overlapping_bases += g_tr.end-g_tr.start+1
                    if g_tr.start <= ig[1] and g_tr.end >= ig[2]:
                        nb_overlapping_bases += ig[2]-ig[1] +1
                    if nb_overlapping_bases / (g_tr.end-g_tr.start+1) < fraction:
                        to_remove = True
                    if to_remove:
                        evidences_genes_to_remove.append(g_tr)
                    else:
                        evidences_genes_to_keep.append(g_tr)

                all_tr_to_remove.extend(evidences_genes_to_remove)
                all_tr_to_keep.extend(evidences_genes_to_keep)

        logging.info("Keep {} transcripts overlapping intergenic regions".format(len(all_tr_to_keep)))
        return all_tr_to_keep



    def get_usefull_pro_from_translations(self, seq, tr_length, stranded):

        min_size = EffectorPredictor.MIN_LENGTH
        max_size = EffectorPredictor.MAX_LENGTH
        prots = set()


        translations = self.extract_prot_from_seq(seq, stranded)
#        if stranded == False:
#            raise Exception("Error cannot deal with non-stranded data, ask for implementation if needed")
#
#        frame_1 = ''
#        frame_2 = ''
#        frame_3 = ''
#        for i in range(0,len(seq),3):
#            frame_1 += Utils.translate(seq[i:i+3].upper())
#            frame_2 += Utils.translate(seq[i+1:i+4].upper())
#            frame_3 += Utils.translate(seq[i+2:i+5].upper())
#
#        for trans in [frame_1, frame_2, frame_3]:
        for trans in translations:
            for i,aa in enumerate(trans):
                if aa == 'M':
                    prot = 'M'
                    idx = 1
                    if i+idx == len(trans):
                        continue
                    aa_end = trans[i+idx]
                    while aa_end != '*':
                        prot += trans[i+idx]
                        idx += 1
                        if i+idx == len(trans):
                            prot = ''
                            break
                        aa_end = trans[i+idx]
                    if max_size >= len(prot) >= min_size and aa_end == "*" and len(prot)*3 / tr_length >= self.size_ratio :
                        prots.add(prot)
        return prots

    def extract_prot_from_seq(self, seq, stranded):

        if stranded == False:
            raise Exception("Error cannot deal with non-stranded data, ask for implementation if needed")

        frame_1 = ''
        frame_2 = ''
        frame_3 = ''
        for i in range(0,len(seq),3):
            frame_1 += Utils.translate(seq[i:i+3].upper())
            frame_2 += Utils.translate(seq[i+1:i+4].upper())
            frame_3 += Utils.translate(seq[i+2:i+5].upper())

        return [frame_1, frame_2, frame_3]

#    def get_usefull_pro_from_translations(self, translations):
#
#        min_size = EffectorPredictor.MIN_LENGTH
#        max_size = EffectorPredictor.MAX_LENGTH
#        prots = set()
#        for trans in translations:
#            for i,aa in enumerate(trans):
#                if aa == 'M':
#                    prot = 'M'
#                    idx = 1
#                    if i+idx == len(trans):
#                        continue
#                    aa_end = trans[i+idx]
#                    while aa_end != '*':
#                        prot += trans[i+idx]
#                        idx += 1
#                        if i+idx == len(trans):
#                            prot = ''
#                            break
#                        aa_end = trans[i+idx]
#                    if max_size >= len(prot) >= min_size and aa_end == "*":
#                        prots.add(prot)
#        return prots
#

    def validate_prot_in_tr(self,tr,prot,stranded):

        fasta = pysam.FastaFile(self.genome)
        seq = ''
        for ex in tr.lExons:
            seq += fasta.fetch(ex.seqid, ex.start-1, ex.end)
        if tr.strand == -1:
            seq = Utils.reverse_complement(seq)
        prots = self.extract_prot_from_seq(seq, stranded)
        for i, p in enumerate(prots):
            index = p.find("{}*".format(prot))
            if index != -1:
                start_prot = index * 3 + i
                end_prot = start_prot + len(prot *3) + 3 -1
                lpos = []
                for e in tr.lExons:
                    for x in range(e.start,e.end+1):
                        lpos.append(x)
                if tr.strand == 1:
                    start = lpos[start_prot]
                    end = lpos[end_prot]
                    return (tr, tr.seqid, start, end)
                else:
                    end = lpos[-(start_prot+1)]
                    start = lpos[-(end_prot+1)]
                    return (tr, tr.seqid, start, end)
        return None




    def run(self):

        genes = Utils.extract_genes(self.gff_genes)

        references = Utils.get_seq_length_from_fasta(self.genome)

        inter_genes = Utils.get_intergenic_coordinates(genes,references,self.min_intergenic_len)

        selected_genes = self.extract_transcripts_overlapping_inter_genes(inter_genes)

        clusters = Utils.clusterize(selected_genes, cltype="gene", stranded=self.tr_stranded)

        fasta = pysam.FastaFile(self.genome)
        all_prots = []
        for i,cl in enumerate(clusters):
            translations = []
            for g in cl.genes:
                for tr in g.lTranscripts:
                    seq = ''
                    for ex in tr.lExons:
                        seq += fasta.fetch(ex.seqid, ex.start-1, ex.end)
                    if tr.strand == -1:
                        seq = Utils.reverse_complement(seq)
                        # faire reverse comp
                    translations.extend(self.get_usefull_pro_from_translations(seq, (tr.end-tr.start+1),self.tr_stranded))

            prots = set(translations)
            all_prots.append((list(prots),i))

        # write fasta file
        nb_prots = 0
        fasta_prot = "rescue_eff_prot.fasta"
        with open(fasta_prot, "w") as fh:
            for i,cl in enumerate(all_prots):
                for j,p in enumerate(cl[0]):
                    fh.write(">cl_{}_{}\n{}\n".format(cl[1],j,p))
                    nb_prots += 1
        fh.close()
        logging.info("{} proteins written in {} ready for analysis".format(nb_prots,fasta_prot))


        self.effpred = EffectorPredictor(os.path.abspath(fasta_prot))

        df = self.effpred.run(export=False)
        selected_proteins = df['Seq']
        df = df.set_index('Seq')

        logging.info("{} proteins selected as potential effectors".format(len(selected_proteins)))

        if logging.getLogger().getEffectiveLevel() > 0:
            pd.set_option('display.max_rows', df.shape[0]+1)
            print(df)

        prots_to_validate = {}
        for j in selected_proteins:
            m = re.match("cl_(\d+)_(\d+)", j)

            if m:
                cl = int(m.group(1))
                idx = int(m.group(2))
                if cl not in prots_to_validate:
                    prots_to_validate[cl] = [(j,all_prots[cl][0][idx])]
                else:
                    prots_to_validate[cl].append((j,all_prots[cl][0][idx]))


        # reduce cluster to only one prot, best effectorP score
        logging.info("Select best candidate per cluster if necessary")
        for cl in prots_to_validate:

            if len(prots_to_validate[cl]) > 1:
                logging.debug("Selecting best candidate for cluster {}".format(cl))
                top = None
                top_effectP_score = 0.0
                for p in prots_to_validate[cl]:
                    if df.loc[p[0],('effectorp','probability')] > top_effectP_score:
                        top_effectP_score = df.loc[p[0],('effectorp','probability')]
                        top = p
                prots_to_validate[cl] = [top]

        transcripts = []
        for cl in prots_to_validate:
            for p in prots_to_validate[cl]:
                validate = False
                for g in clusters[cl].genes:
                    for tr in g.lTranscripts:

                        res = self.validate_prot_in_tr(tr,p[1],self.tr_stranded)
                        if res:
                            validate = True
                            res[0].infer_cds_parts_from_start_end(res[2], res[3])
                            res[0].dAttributes['signalp'] = ['Y']
                            res[0].dAttributes['signalp_pos'] = ['{}'.format(df.loc[p[0],('signalp','Cpos')])]
                            res[0].dAttributes['effectorp_score'] = ['{:.3f}'.format(df.loc[p[0],('effectorp','probability')])]
                            res[0].dAttributes['tmhmm'] = ['{}'.format(df.loc[p[0],('tmhmm','domains')])]
                            res[0].dAttributes['targetp'] = ['{}'.format(df.loc[p[0],('targetp','Localization')])]
                            res[0].dAttributes['len_aa'] = ['{}'.format(df.loc[p[0],('length','')])]

                            transcripts.append((res[0],df.loc[p[0],('effectorp','probability')]))
                            break
                    if validate:
                        break

        transcripts = self.strand_filter(transcripts)

        self.export(transcripts, self.gff3_output)

        return 0



    def export(self, g_transcripts, fname):

        genes = []

        source = "ingenannot-effector-rescue"
        for idx,tr in enumerate(g_transcripts):

            t = Transcript("mRNA::effector_{}".format(idx+1),tr.seqid,tr.get_min_cds_start(),tr.get_max_cds_end(),tr.strand, "gene:effector_{}".format(idx+1), source)
            t.dAttributes = tr.dAttributes
            t.dAttributes['ID'] = ["mRNA::effector_{}".format(idx+1)]
            t.dAttributes['Parent'] = ["gene:effector_{}".format(idx+1)]

            g = Gene("gene:effector_{}".format(idx+1),tr.seqid,tr.get_min_cds_start(),tr.get_max_cds_end(),tr.strand,source)
            g.add_transcript(t)

            for i, exon in enumerate(tr.lExons):
                if exon.end >= tr.get_min_cds_start() and exon.start <= tr.get_max_cds_end():
                    exon.source = source
#                    f.write(exon.to_gtf(tr.gene_id, tr.id))
                    ex = Exon("exon:effector_{}_{}".format(idx+1,i+1),tr.seqid,max(tr.get_min_cds_start(),exon.start),min(tr.get_max_cds_end(),exon.end),tr.strand,[t.id],source)
                    t.add_exon(ex)
            for i, cds in enumerate(tr.lCDS):
                c = CDS("cds:effector_{}".format(idx+1),cds.seqid,cds.start,cds.end,cds.strand,cds.frame,t.id,source)
                t.add_cds(c)

            genes.append(g)

       # genes = self.fix_frame(genes)
        for gene in genes:
            for tr in gene.lTranscripts:
                tr.fix_frame()


        references = list(set([x.seqid for x in genes]))
        Utils.natural_sort(references)
        # export limited to CDS 
        with open(fname, 'w') as f:
            logging.info("Writing: {}".format(fname))

            for ref in references:
                seq_genes = [g for g in genes if g.seqid == ref]
                for g in sorted(seq_genes, key=lambda x: x.start):

#            for g in genes:
                    f.write(g.to_gff3())
                    for t in g.lTranscripts:
                        f.write(t.to_gff3(atts=t.dAttributes))
                        for i, ex in enumerate(t.lExons):
                            f.write(ex.to_gff3())
                        for i, c in enumerate(t.lCDS):
                            f.write(c.to_gff3())


        f.close()


    def strand_filter(self, transcripts):

        conflict_list = []
        transcripts_not_exported = []

        tr_dict = {}
        references = set([tr[0].seqid for tr in transcripts])
        for ref in references:
            ref_tr = sorted([tr for tr in transcripts if tr[0].seqid == ref], key=lambda x: x[0].get_min_cds_start())
            for i,tr in enumerate(ref_tr[:-1]):
                    tr_dict[(tr[0].id,tr[0].source)] = tr[0]
                    for tr2 in ref_tr[i+1:]:
                      if tr[0].is_feature_spanning(tr2[0]):
                        if tr[0].overlap_cds_with_other_transcript_cds(tr2[0]):
                            conflict_list.append((tr, tr2))

            # add last tr in dict
            tr_dict[(ref_tr[-1][0].id,ref_tr[-1][0].source)] = ref_tr[-1]

        logging.info("{} potential conflicts to resolved".format(len(conflict_list)))

        list_to_remove = []
        for cf in conflict_list:
            l = sorted(cf, key=lambda i:i[1], reverse=True)
            if l[0] not in list_to_remove:
                list_to_remove.append(l[1])

        new_transcripts = []
        for tr in transcripts:
            if tr not in list_to_remove:
                new_transcripts.append(tr[0])
            else:
                transcripts_not_exported.append(tr)

        logging.info("{} transcripts removed due to overlapping with other CDS".format(len(transcripts_not_exported)))

        return new_transcripts



