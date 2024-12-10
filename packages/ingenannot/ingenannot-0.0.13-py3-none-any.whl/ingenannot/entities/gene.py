#!/usr/bin/env python3

class Gene(object):

    def __init__(self, gene_id, seqid, start, end, strand, source=None):
        """init"""

        self.gene_id = gene_id
        self.seqid = seqid
        self.start = start
        self.end = end
        self.strand = strand
        self.source = source
        self.type = None
        self.lTranscripts = []

    def isOnReverseStrand(self):
        """return True if strand -"""

        if self.strand == -1:
            return True
        else:
            return False

    def add_transcript(self, transcript):
        """add transcript"""

        ## TODO WARNING NO UPDATE OF GENE COORDINATES
        self.lTranscripts.append(transcript)
        self.lTranscripts.sort(key=lambda x: (x.start,x.id))

    def add_transcript_with_update(self, tr):
        """ add transcript and:
        - update coordinates of gene
        - update exons if shared between transcripts
        """

        # update gene coordinates:
        self.start = min(self.start,tr.start)
        self.end = max(self.end, tr.end)
        # add transcript
        self.lTranscripts.append(tr)
        self.lTranscripts.sort(key=lambda x: (x.start,x.id))
        # update exons for all transcripts
        exs = {}
        for t in self.lTranscripts:
            for ex in t.lExons:
                if (ex.seqid, ex.start, ex.end) not in exs:
                    exs[(ex.seqid, ex.start, ex.end)] = ex
                    if t.id not in exs[(ex.seqid, ex.start, ex.end)].lTranscript_ids:
                        exs[(ex.seqid, ex.start, ex.end)].add_transcript(t.id)
                else:
                    if t.id not in exs[(ex.seqid, ex.start, ex.end)].lTranscript_ids:
                        exs[(ex.seqid, ex.start, ex.end)].add_transcript(t.id)

        for t in self.lTranscripts:
            t.lExons = []
            for ex in exs:
                if t.id in exs[ex].lTranscript_ids:
                    t.add_exon(exs[ex])

        return


    def remove_transcript(self, tr_id):
        """remove transcript"""

        ## TODO WARNING NO UPDATE OF GENE COORDINATES
        for tr in self.lTranscripts:
            if tr.id == tr_id:
                self.lTranscripts.remove(tr)
                break
        self.lTranscripts.sort(key=lambda x: (x.start,x.id))

    def is_coding(self):

        if self.type == "coding":
            return True
        else:
            False

    def get_min_cds_start(self):

        return min([tr.get_min_cds_start() for tr in self.lTranscripts])

    def get_max_cds_end(self):

        return max([tr.get_max_cds_end() for tr in self.lTranscripts])

    def get_min_exon_start(self):

        return min([tr.get_min_exon_start() for tr in self.lTranscripts])

    def get_max_exon_end(self):

        return max([tr.get_max_exon_end() for tr in self.lTranscripts])

    def is_feature_spanning(self, feature):
        """TODO refactor to add in a Feature class"""

        if self.start <= feature.start <= self.end:
            return True
        if self.start <= feature.end <= self.end:
            return True
        if feature.start <= self.start and feature.end >= self.end:
            return True
        return False

    def to_gff3(self,atts=None, source=None):

        strand = '+'
        if self.strand == -1:
            strand = '-'
        str_atts = ''
        src = self.source
        if source:
            src = source
        if atts:
            for att in atts:
                str_atts += '{}={};'.format(att,",".join(atts[att]))
            return "{}\t{}\tgene\t{}\t{}\t.\t{}\t.\t{}\n".format(self.seqid,src,self.start,self.end,strand,str_atts)
        else:
            return "{}\t{}\tgene\t{}\t{}\t.\t{}\t.\tID={};\n".format(self.seqid,src,self.start,self.end,strand,self.gene_id)

    def __hash__(self):

        return hash(self.gene_id)

    def __eq__(self, other):
        """Equality on all args"""

        return ((self.gene_id,self.seqid,self.start,self.end,self.strand, self.lTranscripts) == (other.gene_id, other.seqid, other.start, other.end, other.strand, other.lTranscripts))

    def __ne__(self, other):

        return not self == other

    def __repr__(self):
        """Gene representation"""

        return 'Gene: {}-{}-{}-{}-{}-{}'.format(self.gene_id,self.seqid,self.start,self.end,self.strand, self.lTranscripts)

    def __gt__(self, other):

        return ((self.seqid, self.start) > (other.seqid, other.start))

