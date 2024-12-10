#!/usr/bin/env python3
"""
Class entity: Transcript
"""

import pysam
import logging
import numpy as np
from ingenannot.entities.intron import Intron
from ingenannot.entities.cds import CDS


class Transcript():
    """Class entity: Transcript"""

    def __init__(self, id, seqid, start, end, strand, gene_id, source=None):
        """Transcript constructor"""

        self.id = id
        self.seqid = seqid
        self.start = start
        self.end = end
        self.strand = strand
        self.gene_id = gene_id
        self.source = source
        self.coding = True
        self.lCDS = []
        self.lExons = []
        self.dAttributes = {}
        self.best_tr_evidence = (None, 1.0)
        self.best_bx_evidence = (None, 1.0)
        self.best_lg_evidence = (None, 1.0)
        self.tr_penalty = "undef"
        self.lg_penalty = "undef"
        self.gaeval_infos = {}

    def is_feature_spanning(self, feature):
        """
        check if the feature spans the transcript
        TODO refactor to add in a Feature class
        """

        if self.start <= feature.start <= self.end:
            return True
        if self.start <= feature.end <= self.end:
            return True
        if feature.start <= self.start and feature.end >= self.end:
            return True
        return False


    def is_overlapping_feature(self, feature):
        """
        check if the feature fully , 100% overlaps the transcript
        TODO refactor to add in a Feature class
        """

        if self.start <= feature.start and self.end >= feature.end:
            return True
        return False

    def is_overlapping_coords(self,start, end):
        """
        check if the coords fully , 100% overlap the transcript
        TODO refactor to add in a Feature class
        """

        if self.start <= start and self.end >= end:
            return True
        return False

    def coords_spanning_ratio(self,start,end):
        """
        check if the coords fully , 100% overlap the transcript
        TODO refactor to add in a Feature class
        """

        if self.start <= start <= self.end <= end:
            return (self.end-start) / (end-start)
        elif start <= self.start <= end <= self.end:
            return (end-self.start) / (end-start)
        elif start <= self.start and self.end <= end:
            return (self.end-self.start) / (end-start)
        elif self.start <= start and end <= self.end:
            return 1.0
        else:
            return 0.0

    def is_on_reverse_strand(self):
        """return True if strand -"""

        if self.strand == -1:
            return True
        else:
            return False

    def is_partial_cds(self, seq):
        """return true if partial cds"""

        if seq[0] != 'M':
            return True
        elif seq[-1] != '*':
            return True
        else:
            return False

    def add_exon(self, exon):
        """add an exon"""

        self.lExons.append(exon)
        self.lExons.sort(key=lambda x: x.start)

    def add_cds(self, cds):
        """add a cds"""

        self.lCDS.append(cds)
        self.lCDS.sort(key=lambda x: x.start)

    def infer_cds_parts_from_start_end(self, start, end):
        """add a CDS from start and end exon"""

        for e in self.lExons:
            if start > e.end:
                continue
            if end < e.start:
                break
            cds_start = max(e.start,start)
            cds_end = min(e.end,end)
            self.add_cds(CDS("cds:{}".format(self.id),self.seqid,cds_start,
                cds_end,self.strand,None,self.source,self.id))

    def infer_five_prime_utrs(self):
        """infer five prime utrs"""

        utrs = []
        if self.strand == 1:
            pos_max = self.get_min_cds_start()
            for e in self.lExons:
                if e.end < pos_max:
                    utrs.append((e.start, e.end))
                if e.start < pos_max < e.end:
                    utrs.append((e.start, pos_max-1))
        else:
            pos_min = self.get_max_cds_end()
            for e in self.lExons:
                if e.start > pos_min:
                    utrs.append((e.start, e.end))
                if e.start < pos_min < e.end:
                    utrs.append((pos_min+1, e.end))
        return utrs

    def infer_three_prime_utrs(self):
        """infer three prime utrs"""

        utrs = []
        if self.strand == 1:
            pos_min = self.get_max_cds_end()
            for e in self.lExons:
                if e.start > pos_min:
                    utrs.append((e.start, e.end))
                if e.start < pos_min < e.end:
                    utrs.append((pos_min+1, e.end))
        else:
            pos_max = self.get_min_cds_start()
            for e in self.lExons:
                if e.end < pos_max:
                    utrs.append((e.start, e.end))
                if e.start < pos_max < e.end:
                    utrs.append((e.start, pos_max-1))
        return utrs

    def has_UTRs(self):
        """test if has UTRs"""

        if self.get_min_exon_start() < self.get_min_cds_start():
            return True
        if self.get_max_exon_end() > self.get_max_cds_end():
            return True
        return False


    def getSortedExons(self):
        """return sorted exons"""

        return self.lExons.sort(key=lambda x: x.start)

    def getLength(self):
        """return total length introns+exons"""

        return self.end-self.start+1

    def getExonTotalLength(self):
        """return the sum of Exon lengths"""

        return sum([exon.end-exon.start+1 for exon in self.lExons])

    def getCDSTotalLength(self):
        """return the length of CDS"""

        return sum([cds.end-cds.start+1 for cds in self.lCDS])

    def getlIntrons(self):
        '''return list of introns'''

        lIntrons =[]
        for i,ex in enumerate(self.lExons[:-1]):
            lIntrons.append(Intron("intron:{}.{}".format(self.id,i),self.seqid,self.lExons[i].end+1,self.lExons[i+1].start-1))

        return lIntrons

    def get_min_cds_start(self):
        """return min cds start"""

        return min([cds.start for cds in self.lCDS])

    def get_max_cds_end(self):
        """return max cds end"""

        return max([cds.end for cds in self.lCDS])

    def get_min_exon_start(self):
        """return min exon start"""

        return min([exon.start for exon in self.lExons])

    def get_max_exon_end(self):
        """return max exon end"""

        return max([exon.end for exon in self.lExons])

    def get_diff_vs_another_transcript(self, other):
        """return diff with another transcript"""

        if self.seqid != other.seqid:
            raise Exception("Error comparing {} and {}, not localized on same sequence".format(self.id, other.id))

        self_no_utr = False
        other_no_utr = False
        min_pos, max_pos = self.__get_boundaries_for_comparison(other,self_no_utr, other_no_utr)


        self_codes = self.get_nb_repr_for_comparison(min_pos, max_pos, self_no_utr, 1)
        other_codes = other.get_nb_repr_for_comparison(min_pos, max_pos, other_no_utr, 2)

        return np.add(self_codes,other_codes),min_pos,max_pos


    def get_nb_shared_bases_with_another_transcript(self, other, self_no_utr=False, other_no_utr=False):
        """get nb of shared bases between transcipts"""

        if self.seqid != other.seqid:
            return 0
        min_pos, max_pos = self.__get_boundaries_for_comparison(other,self_no_utr, other_no_utr)
        self_bits = self.get_bit_repr_for_comparison(min_pos, max_pos, self_no_utr)
        other_bits = other.get_bit_repr_for_comparison(min_pos, max_pos, other_no_utr)

        return bin(self_bits & other_bits).count("1")

    def get_nb_specific_bases_vs_another_transcript(self, other, self_no_utr=False, other_no_utr=False):
        """get nb of specific bases with another transcipt"""

        if self.seqid != other.seqid:
            if self_no_utr:
                return self.getCDSTotalLength()
            else:
                return self.getExonTotalLength()

        min_pos, max_pos = self.__get_boundaries_for_comparison(other, self_no_utr, other_no_utr)

        self_bits = self.get_bit_repr_for_comparison(min_pos, max_pos, self_no_utr)
        other_bits = other.get_bit_repr_for_comparison(min_pos, max_pos, other_no_utr)

        return bin(self_bits & (~ other_bits)).count("1")

    def get_nb_specific_bases_vs_another_transcript_specific_positions(self, other, start, end, self_no_utr=False, other_no_utr=False):
        """get nb of specific bases with another transcipt with specific start and end"""

        if self.seqid != other.seqid:
            if self_no_utr:
                return self.getCDSTotalLength()
            else:
                return self.getExonTotalLength()
        self_bits = self.get_bit_repr_for_comparison_spe(start, end, self_no_utr)
        other_bits = other.get_bit_repr_for_comparison_spe(start, end, other_no_utr)

        return bin(self_bits & (~ other_bits)).count("1")


    def __get_boundaries_for_comparison(self, other, self_no_utr=False, other_no_utr=False):
        """get coords to use depending of UTRs or not"""

        min_pos = None
        max_pos = None
        if self_no_utr and other_no_utr:
            min_pos = min(self.get_min_cds_start(), other.get_min_cds_start())
            max_pos = max(self.get_max_cds_end(), other.get_max_cds_end())
        elif self_no_utr and not other_no_utr:
            min_pos = min(self.get_min_cds_start(), other.get_min_exon_start())
            max_pos = max(self.get_max_cds_end(), other.get_max_exon_end())
        elif not self_no_utr and other_no_utr:
            min_pos = min(self.get_min_exon_start(), other.get_min_cds_start())
            max_pos = max(self.get_max_exon_end(), other.get_max_cds_end())
        else:
            min_pos = min(self.get_min_exon_start(), other.get_min_exon_start())
            max_pos = max(self.get_max_exon_end(), other.get_max_exon_end())

        return min_pos, max_pos


    def is_cds_included_in_other_cds(self, tr):
        """test if a CDS is included in another CDS"""

        for cds in self.lCDS:
            if self.get_bit_repr_for_comparison_spe(cds.start, cds.end, True) != \
               tr.get_bit_repr_for_comparison_spe(cds.start, cds.end, True):
                return False
        return True


    def get_nb_repr_for_comparison(self,min_pos, max_pos, no_utr, code=1):

        bitarray = [0]*(max_pos-min_pos+1)

        if no_utr:
            lFeatures = self.lCDS
        else:
            lFeatures = self.lExons
        for feat in lFeatures:
            for pos in range(feat.start,feat.end+1):
                    bitarray[pos-min_pos] = code

        return bitarray


    def get_bit_repr_for_comparison(self,min_pos, max_pos, no_utr, code=1):

        bitarray = 0

        if no_utr:
            lFeatures = self.lCDS
        else:
            lFeatures = self.lExons

        for feat in lFeatures:
            for pos in range(feat.start,feat.end+1):
                    #bitarray[pos-min_pos] = code
                    bitarray = bitarray | (1 << pos-min_pos) 
        
        return bitarray


    def get_bit_repr_for_comparison_spe(self,min_pos, max_pos, no_utr):

        bitarray = 0

        if no_utr:
            lFeatures = self.lCDS
        else:
            lFeatures = self.lExons

        for feat in lFeatures:
            for pos in range(feat.start,feat.end+1):
                if (pos >= min_pos) & (pos <= max_pos):
                    bitarray = bitarray | (1 << pos-min_pos) 

        return bitarray 


    def has_same_exons(self, other):
        """compare exons with exons from another transcript"""

        return sorted([(ex.start,ex.end) for ex in self.lExons]) == \
                sorted([(ex.start, ex.end) for ex in other.lExons])


    def overlap_cds_with_other_transcript_cds(self, other, stranded=False):
        """todo"""

        if stranded == True and self.strand != other.strand:
            return False
        if self.get_min_cds_start() <= other.get_min_cds_start() <= self.get_max_cds_end():
            return True
        if self.get_min_cds_start() <= other.get_max_cds_end() <= self.get_max_cds_end():
            return True
        if other.get_min_cds_start() <= self.get_min_cds_start() and other.get_max_cds_end() >= self.get_max_cds_end():
            return True
        return False


    def is_cds_partial(self, genome):
        """test if CDS partial"""

        from ingenannot.utils import Utils

        fh = pysam.FastaFile(genome)
        cds_seq = ''
        for cds in sorted(self.lCDS, key=lambda x : x.start):
           cds_seq +=  fh.fetch(cds.seqid, cds.start-1, cds.end)
        if self.strand == -1:
            cds_seq = Utils.reverse_complement(cds_seq)

        protein = ''
        for pos in range(0,len(cds_seq),3):
            protein += Utils.translate(cds_seq[pos:pos+3].upper())

        if len(cds_seq) % 3 != 0:
            return True
        if protein[0] != 'M':
            return True
        if protein[-1] != '*':
            return True
        if '*' in protein[1:-1]:
            return True
        return False


    def set_evidence_aed_info_from_attributes(self):
        """usefull when transcript intanciate from gff file"""

        if "aed_ev_tr" in self.dAttributes and "ev_tr" in self.dAttributes:
            self.best_tr_evidence = (self.dAttributes["ev_tr"][0],float(self.dAttributes["aed_ev_tr"][0]))
        else:
            logging.error("Problem: transcript [{}] of gene [{}], source [{}], missing aed_tr annotations".format(self.id, self.gene_id, self.source))
        if "aed_ev_pr" in self.dAttributes and "ev_pr" in self.dAttributes:
            self.best_bx_evidence = (self.dAttributes["ev_pr"][0],float(self.dAttributes["aed_ev_pr"][0]))
        else:
            logging.error("Problem: transcript [{}] of gene [{}], source [{}], missing aed_pr annotations".format(self.id, self.gene_id, self.source))
        if "aed_ev_lg" in self.dAttributes and "ev_lg" in self.dAttributes:
            self.best_lg_evidence = (self.dAttributes["ev_lg"][0],float(self.dAttributes["aed_ev_lg"][0]))

        if "ev_lg_penalty" in self.dAttributes:
            self.lg_penalty = self.dAttributes["ev_lg_penalty"][0]
        if "ev_tr_penalty" in self.dAttributes:
            self.tr_penalty = self.dAttributes["ev_tr_penalty"][0]


    def is_penalized(self):
        """
           identify if transcriptomic evidence with penalty
           A transcript is penalized if all available 
           transcriptomic evidence have a penalty status equals
           to yes. If one is missing, undef status, the penalty 
           is only required for the other.
        """

        #case 1: tr and lg with penalty
        if self.tr_penalty == 'yes' and self.lg_penalty == 'yes':
            return True
        #case 2: tr penalty and lg not defined (no support)
        if self.tr_penalty == 'yes' and self.lg_penalty == 'undef':
            return True
        #case 3: tr penalty not defined (no support) and lg  with penalty
        if self.tr_penalty == 'undef' and self.lg_penalty == 'yes':
            return True

        return False


    def add_gaeval_infos(self, infos):
        """add gaeval infos to the transcript"""

        if len(infos) != 7:
            raise Exception("Error in number of values when importing gaeval infos, for transcript: {} source: {}".format(self.id, self.source))
        self.gaeval_infos = dict(zip(['int','cov','numin','alpha','beta','gamma','epsilon'],infos))


    def fix_frame(self):
        """add/change frame if missing or false"""

        next_frame = None
        if self.strand == 1:
            lCDS = sorted(self.lCDS, key=lambda x : x.start)
        if self.strand == -1:
            lCDS = sorted(self.lCDS, key=lambda x : x.start, reverse=True)
        for cds in lCDS:
            if next_frame is None:
                next_frame = 0
                if cds.frame != next_frame:
                    logging.debug("Warning change frame {} to {}".format(cds.frame, next_frame))
                    cds.frame = 0
                delta_bases = ((cds.end - cds.start + 1) - next_frame) % 3
                next_frame = (3 - delta_bases) % 3
            else:
                if cds.frame != next_frame:
                    logging.debug("Warning change frame {} to {}".format(cds.frame, next_frame))
                    cds.frame = next_frame
                delta_bases = ((cds.end - cds.start + 1) - next_frame) % 3
                next_frame = (3 - delta_bases) % 3

    def to_gff3(self,atts=None, source=None):

        strand = '+'
        if self.strand == -1:
            strand = '-'
        str_atts = ''
        src=self.source
        if source:
            src=source
        if atts:
            for att in atts:
                str_atts += '{}={};'.format(att,",".join(atts[att]))
            return "{}\t{}\tmRNA\t{}\t{}\t.\t{}\t.\t{}\n".format(self.seqid,
                    src,self.start,self.end,strand,str_atts)
        else:
            return "{}\t{}\tmRNA\t{}\t{}\t.\t{}\t.\tID={};Parent={}\n".format(self.seqid,
                    src,self.start,self.end,strand,self.id,self.gene_id)

    def to_gtf(self, atts=None):

        strand = '+'
        if self.strand == -1:
            strand = '-'
        str_atts = ''
        if atts:
            for att in atts:
                str_atts += '{} \"{}\";'.format(att,",".join(atts[att]))
            return "{}\t{}\ttranscript\t{}\t{}\t.\t{}\t.\t{}\n".format(self.seqid,
                    self.source,self.start,self.end,strand,str_atts)
        else:
            return "{}\t{}\ttranscript\t{}\t{}\t.\t{}\t.\tgene_id \"{}\"; transcript_id \
                    \"{}\"\n".format(self.seqid,self.source,self.start,self.end,strand,self.gene_id,self.id)

    def __eq__(self, other):
        """Equality on all args"""

        return ((self.id,self.seqid,self.start,self.end,self.strand,self.lCDS, self.lExons,self.gene_id, self.source) == (other.id, other.seqid, other.start, other.end, other.strand, other.lCDS, other.lExons,other.gene_id, other.source))

    def __ne__(self, other):

        return not self == other

    def __repr__(self):
        """Transcript representation"""

        return 'Transcript: {}-{}-{}-{}-{}-{}-{}-{}'.format(self.id,self.seqid,self.start,self.end,self.strand,self.lCDS, self.lExons,self.gene_id)
