#!/usr/bin/env python3
"""
Class entity: MetaGene
"""

import logging
import collections

class MetaGene():
    """Class entity: Metagene"""

    def __init__(self, id, seqid, start, end, transcripts = None):
        """init"""

        self.id = id
        self.seqid = seqid
        self.start = start
        self.end = end
        self.genes = []
        if transcripts is None:
            self.lTranscripts = []
            self.lCDS = [] # unique CDS
        else:
            self.lTranscripts = transcripts
            self.lCDS = self.get_CDS_transcript_association()

    def add_gene(self, gene):
        """add gene"""

        self.genes.append(gene)

    def remove_transcript(self, transcript):
        """remove a transcript from Metagene"""

        ltrs = self.lTranscripts
        for i,tr in enumerate(self.lTranscripts):
            if (tr.id == transcript.id) & (tr.source == transcript.source):
                del ltrs[i]
                self.lTranscripts == ltrs
                self.lCDS = self.get_CDS_transcript_association()
                return tr
        return None

    def have_transcripts_same_cds(self):
        """all transcsipts have same Protein"""

        for tr in self.lTranscripts:
            for tr2 in self.lTranscripts[1::]:
                if sorted([(x.start,x.end) for x in tr.lCDS]) != \
                   sorted([(y.start, y.end) for y in tr2.lCDS]):
                    return False
        return True

    def have_at_least_2_transcripts_same_cds(self):
        """2 transcripts at least have same CDS"""

        for tr in self.lTranscripts:
            for tr2 in self.lTranscripts[1::]:
                if sorted([(x.start,x.end) for x in tr.lCDS]) == \
                   sorted([(y.start, y.end) for y in tr2.lCDS]):
                    return True
        return False


    def get_CDS_transcript_association(self):
        """get list of CDS coords with associated transcripts"""

        CDS = collections.OrderedDict()
        for i,tr in enumerate(self.lTranscripts):
            to_add = True
            for cds in CDS.keys():
                if tuple(sorted([(x.start,x.end) for x in tr.lCDS])) == cds:
                    CDS[cds].append(tr)
                    to_add = False
            if to_add:
                CDS[tuple(sorted([(x.start,x.end) for x in tr.lCDS]))] = [tr]


        if len(CDS.keys()) >= 2 and self.have_transcripts_same_cds():
            logging.error("Error: CDS keys > 2")
            raise Exception

        return CDS

    def classify_score_per_cds(self, utr_type='random'):

        """ utr_type = "random", "shortest", "longest" if
             same CDS
        """

        best_score_cds = collections.OrderedDict()
        CDS = self.get_CDS_transcript_association()
        for cds in CDS.keys():
            best_score = CDS[cds][0].evidence_ratio
            best_score_cds[cds] = CDS[cds][0]
            for t in CDS[cds][1:]:
                if t.evidence_ratio <= best_score:
                    if utr_type == 'longest':
                        if t.getLength() > best_score_cds[cds].getLength():
                            best_score = t.evidence_ratio
                            best_score_cds[cds] = t
                    elif utr_type == 'shortest':
                        if t.getLength() < best_score_cds[cds].getLength():
                            best_score = t.evidence_ratio
                            best_score_cds[cds] = t
                    else:
                        best_score = t.evidence_ratio
                        best_score_cds[cds] = t

        return best_score_cds


    def is_gene_spanning(self, gene):
        """TODO """

        if self.start <= gene.start <= self.end:
            return True
        if self.start <= gene.end <= self.end:
            return True
        if gene.start <= self.start and gene.end >= self.end:
            return True
        return False

    def get_number_of_src(self):
        """return the number of sources in transcript list"""

        sources = set()
        for tra in self.lTranscripts:
            sources.add(tra.source)
        return len(sources)


    def get_number_of_src_overlapping_tr_with_tr_restrictions(self, tra, ltra):
        """
        In case of rescue CDS in metagene if overlapping CDS,
        we need to know the number of source with a potential tr,
        but not overalping previously selected tr. Avoid export of
        secondary CDS without evidence support, but inside a metagene with
        enough sources.
        """

        l = []
        for t in self.lTranscripts:
            if tra == t:
                continue
            if t.overlap_cds_with_other_transcript_cds(tra, True):
                l.append(t)

        l2 = []
        for t in l:
            overlap = False
            for t2 in ltra:
                if t.overlap_cds_with_other_transcript_cds(t2,True):
                    overlap = True
            if not overlap:
                l2.append(t)

        sources = set()
        for t in l2:
            sources.add(t.source)
        return len(sources)

    def get_number_of_src_overlapping_tr(self, tr):
        """
        In case of rescue CDS in metagene if overlapping CDS,
        we need to know the number of source with a potential tr,
        overlapping this tr.
        """

        l = []
        for t in self.lTranscripts:
            if tr == t:
                continue
            if t.overlap_cds_with_other_transcript_cds(tr, True):
                l.append(t)

        sources = set()
        # adding tr to add one more source if possible
        l.append(tr)
        for t in l:
            sources.add(t.source)
        return len(sources)


    def __str__(self):
        """MetaGene representation"""

        return 'MetaGene: {}-{}-{}-{}'.format(self.seqid,self.start,
                self.end,",".join([tr.id for tr in self.lTranscripts]))
