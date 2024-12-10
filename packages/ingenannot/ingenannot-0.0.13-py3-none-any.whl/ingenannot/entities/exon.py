#!/usr/bin/env python3

class Exon(object):

    def __init__(self,exon_id, seqid, start, end, strand, lTranscript_ids, source=None):
        """Exon constructor"""

        self.exon_id = exon_id
        self.seqid = seqid
        self.start = start
        self.end = end
        self.strand = strand
        self.lTranscript_ids = lTranscript_ids
        self.lTranscript_ids.sort()
        self.source = source

    def add_transcript(self, tr_id):

        self.lTranscript_ids.append(tr_id)
        self.lTranscript_ids.sort()
        return self.lTranscript_ids

    def add_transcripts(self, tr_ids):

        for tr_id in tr_ids:
            if tr_id not in self.lTranscript_ids:
                self.lTranscript_ids.append(tr_id)
        self.lTranscript_ids.sort()
        return self.lTranscript_ids

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
            return "{}\t{}\texon\t{}\t{}\t.\t{}\t.\t{}\n".format(self.seqid,src,self.start,self.end,strand,str_atts)
        else:
            return "{}\t{}\texon\t{}\t{}\t.\t{}\t.\tID={};Parent={}\n".format(self.seqid,src,self.start,self.end,strand,self.exon_id,",".join(self.lTranscript_ids))


    def to_gtf(self, gene_id, tr_id, atts=None):

        strand = '+'
        if self.strand == -1:
            strand = '-'
        str_atts = ''
        if atts:
            for att in atts:
                str_atts += '{} \"{}\";'.format(att,",".join(atts[att]))
            return "{}\t{}\texon\t{}\t{}\t.\t{}\t.\t{}\n".format(self.seqid,self.source,self.start,self.end,strand,str_atts)
        else:
            return "{}\t{}\texon\t{}\t{}\t.\t{}\t.\tgene_id \"{}\"; transcript_id \"{}\"\n".format(self.seqid,self.source,self.start,self.end,strand,gene_id,tr_id)




    def __eq__(self, other):
        """Equality on all args"""

        return ((self.exon_id,self.seqid,self.start,self.end,self.strand,self.lTranscript_ids) == (other.exon_id,other.seqid, other.start, other.end, other.strand, other.lTranscript_ids))

    def __ne__(self, other):

        return not self == other

    def __repr__(self):
        """Exon representation"""

        return 'Exon: {}-{}-{}-{}-{}-{}'.format(self.exon_id,self.seqid,self.start,self.end,self.strand,self.lTranscript_ids)


