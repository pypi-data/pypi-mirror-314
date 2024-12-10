#!/usr/bin/env python
"""
entity class CDS
"""

class CDS():
    """entity class CDS"""

    def __init__(self,cds_id, seqid, start, end, strand, frame, transcript_id, source=None):
        """Transcript constructor"""

        self.cds_id = cds_id
        self.seqid = seqid
        self.start = start
        self.end = end
        self.strand = strand
        self.frame = frame
        self.source = source
        self.transcript_id = transcript_id

        if self.frame is None:
            self.frame = "."

    def to_gff3(self,atts=None, source=None):
        """print to gff3 format"""

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
            return "{}\t{}\tCDS\t{}\t{}\t.\t{}\t{}\t{}\n".format(self.seqid,
                    src,self.start,self.end,strand,self.frame,str_atts)
        return "{}\t{}\tCDS\t{}\t{}\t.\t{}\t{}\tID={};Parent={}\n"\
                .format(self.seqid,src,self.start,self.end,strand,\
                self.frame,self.cds_id,self.transcript_id)


    def __eq__(self, other):
        """Equality on all args"""

        return ((self.cds_id,self.seqid,self.start,self.end,self.strand,
                self.frame,self.transcript_id) == (other.cds_id,other.seqid,
                other.start, other.end, other.strand, other.frame,
                other.transcript_id))

    def __ne__(self, other):

        return not self == other

    def __repr__(self):
        """CDS representation"""

        return 'CDS: {}-{}-{}-{}-{}-{}-{}'.format(self.cds_id,self.seqid,
                self.start,self.end,self.strand,self.frame,self.transcript_id)
