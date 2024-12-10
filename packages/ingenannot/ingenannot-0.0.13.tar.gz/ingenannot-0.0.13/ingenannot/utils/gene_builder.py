#!/usr/bin/env python3

import sys
import copy
import logging
from collections import defaultdict

from ingenannot.entities.gene import Gene
from ingenannot.entities.transcript import Transcript
from ingenannot.entities.exon import Exon
from ingenannot.entities.cds import CDS

class GFF3BuilderFeature(object):

    def __init__(self):
        pass

    def _check_attribute(self, feat, tag, idx=""):
        '''check if atribute available to buid feature'''

        try:
            if idx:
                feat.attributes[tag][idx]
            else:
                feat.attributes[tag]
        except Exception as e:
            raise Exception("missing {} for feature ID: {}".format(tag, feat.id))

    def build_gene(self, feat, source):

        if source == "undefined":
            source = feat.source

        return Gene(feat.id, feat.seqid, feat.start, feat.end, feat.strand, source)

    def build_transcript(self, feat, source):
        if source == "undefined":
            source = feat.source
        self._check_attribute(feat,'Parent',0)    
        tr = Transcript(feat.id, feat.seqid, feat.start, feat.end, feat.strand, feat.attributes['Parent'][0],source)
        #new:
        tr.dAttributes = feat.attributes
        #new

        if feat.type == "ncRNA":
            tr.coding = False
        return tr

    def build_exon(self, feat,source):

        if source == "undefined":
            source = feat.source

        self._check_attribute(feat,'Parent',0)
        return Exon(feat.id, feat.seqid, feat.start, feat.end, feat.strand, feat.attributes['Parent'], source)

    def build_cds(self, feat, source):

        if source == "undefined":
            source = feat.source

        self._check_attribute(feat,'Parent',0)
        return CDS(feat.id, feat.seqid, feat.start, feat.end, feat.strand, feat.frame, feat.attributes['Parent'][0],source)


class GTFBuilderFeature(object):

    def __init__(self):
        pass

    def _check_attribute(self, feat, tag, idx=""):
        '''check if atribute available to buid feature'''

        try:
            if idx:
                feat.attributes[tag][idx]
            else:
                feat.attributes[tag]
        except Exception as e:
            raise Exception("missing {} for feature ID: {}".format(tag, feat.id))

    def build_gene(self, feat, source):

        if source == "undefined":
            source = feat.source

        self._check_attribute(feat,'gene_id',0)
        return Gene(feat.attributes['gene_id'][0], feat.seqid, feat.start, feat.end, feat.strand, source)

    def build_transcript(self, feat, source):

        if source == "undefined":
            source = feat.source

        self._check_attribute(feat,'gene_id',0)
        self._check_attribute(feat,'transcript_id',0)
        tr = Transcript(feat.attributes['transcript_id'][0], feat.seqid, feat.start, feat.end, feat.strand, feat.attributes['gene_id'][0],source)
        tr.dAttributes = feat.attributes
        if feat.type == "ncRNA":
            tr.coding = False
        return tr

    def build_exon(self, feat, source):

        if source == "undefined":
            source = feat.source

        self._check_attribute(feat,'transcript_id')
        return Exon('exon:{}-{}-{}'.format(feat.seqid,feat.start,feat.end), feat.seqid, feat.start, feat.end, feat.strand, feat.attributes['transcript_id'], source)

    def build_cds(self, feat,source):

        if source == "undefined":
            source = feat.source

        self._check_attribute(feat,'transcript_id', 0)
        return CDS('CDS:{}-{}-{}'.format(feat.seqid,feat.start,feat.end), feat.seqid, feat.start, feat.end, feat.strand, feat.frame, feat.attributes['transcript_id'][0],source)


class GFF3BlastxBuilderFeature(GFF3BuilderFeature):

    def convert_features(self, features):

        new_features = []
        for feat in features:
            if feat.type == 'match':
                feat.type = 'mRNA'
                #feat.id = 'mRNA-{}'.format(feat.id)
                feat.attributes['Parent'] = ['gene-{}'.format(feat.id)]
            if feat.type == 'match_part':
                feat_cp = copy.deepcopy(feat)
                feat_cp.type = 'exon'
                feat_cp.id = 'exon-{}'.format(feat.id)
                new_features.append(feat_cp)
                feat.type = 'CDS'
                feat.id = 'CDS-{}'.format(feat.id)
        features.extend(new_features)
        return features

class GFF3MiniprotBuilderFeature(GFF3BuilderFeature):

    def convert_features(self, features):
        '''convert features from miniprot gff to feat with expected values'''

        new_features = []
        #idx = 0
        idx = defaultdict(int)
        for feat in features:
            if feat.type == 'mRNA':
                feat.attributes['Parent'] = ['gene-{}'.format(feat.id)]
                #idx=0
            if feat.type == 'CDS':
                idx[feat.attributes['Parent'][0]] += 1
                feat.id = 'CDS-{}.{}'.format(feat.attributes['Parent'][0],idx[feat.attributes['Parent'][0]])
                feat.attributes['ID'] = [feat.id]
                # add exon missing in output
                feat_cp = copy.deepcopy(feat)
                feat_cp.type = 'exon'
                feat_cp.id = 'exon-{}.{}'.format(feat.attributes['Parent'][0],idx[feat.attributes['Parent'][0]])
                feat_cp.attributes['ID'] = [feat_cp.id]
                new_features.append(feat_cp)
        features.extend(new_features)
        return features


class GeneBuilder(object):

    __builders = {'gff3':GFF3BuilderFeature,
                  'gtf':GTFBuilderFeature,
                  'gff3-blastx':GFF3BlastxBuilderFeature,
                  'gff3-miniprot':GFF3MiniprotBuilderFeature}

    def __init__(self, fmt):

        self.fmt = fmt
        self.builder = GeneBuilder.__builders[self.fmt]()

    def build_all_genes(self, features, coding_only=False, source="undefined"):

        genes = {}
        transcripts = {}
        exons = {}
        cds = {}
        if self.fmt in ['gff3-blastx','gff3-miniprot']:
            features = self.builder.convert_features(features)
        #idx = 0
        for feat in features:
            if feat.type == "gene":
                gene = self.builder.build_gene(feat, source)
                genes[gene.gene_id] = gene
         #       idx +=1
            if feat.type == "mRNA" or feat.type == "ncRNA" or feat.type == "transcript":
                transcript = self.builder.build_transcript(feat, source)
                transcripts[transcript.id] = transcript
            if feat.type == "exon":
                exon = self.builder.build_exon(feat,source)
              #  exon_id = 'exon:{}-{}-{}'.format(feat.seqid,feat.start,feat.end)
                exon_id = exon.exon_id
                if exon_id in exons:
                    if self.fmt == 'gtf':
                        exons[exon_id].add_transcript(feat.attributes['transcript_id'][0])
                    if self.fmt == 'gff3':
                        exons[exon_id].add_transcripts(feat.attributes['Parent'])
                else:
                    exons[exon.exon_id] = exon
            if feat.type == "CDS":
                ccds = self.builder.build_cds(feat,source)
                if ccds.cds_id not in cds:
                    cds[ccds.cds_id] = [ccds]
                else:
                    cds[ccds.cds_id].append(ccds)


        #print(idx)

# Note: from https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md

#NOTE 2
#    "Orphan" exons CDSs, and other features. Ab initio gene prediction programs call hypothetical exons and CDS's that are attached to the genomic sequence and not necessarily to a known transcript. To handle these features, you may either (1) create a placeholder mRNA and use it as the parent for the exon and CDS subfeatures; or (2) attach the exons and CDSs directly to the gene. This is allowed by SO because of the transitive nature of the part_of relationship.

        if cds and not exons:
            transcripts = self.build_cds_transcript_relation(cds, transcripts, genes, source)
            transcripts = self.inferring_exon_transcript_relation_from_cds(transcripts)
        elif not cds and not exons:
            #logging.debug("ERROR no exons, no CDS for {}".format(source))
            print("ERROR no exons, no CDS for {}".format(source))
            #logging.debug(features)
        elif exons and not cds:
            transcripts = self.build_exon_transcript_relation(exons, transcripts, genes)
        else :
            transcripts = self.build_cds_transcript_relation(cds, transcripts, genes, source)
            transcripts = self.build_exon_transcript_relation(exons, transcripts, genes)

        genes = self.build_transcript_gene_relation(transcripts, genes, source)


        # remove gene if no exons/cds
        lToRemove = set()
        for gene_id in genes:
            for tr in genes[gene_id].lTranscripts:
                if not tr.lExons and not tr.lCDS:
                    lToRemove.add(gene_id)

        for gene_id in lToRemove:
            del genes[gene_id]

        if coding_only:
            return [ gene for gene in genes.values() if gene.is_coding() == True ]

        return genes.values()

    def inferring_exon_transcript_relation_from_cds(self, transcripts):
        for tr in transcripts.values():
            for i,cds in enumerate(sorted(tr.lCDS, key=lambda x:x.start)):
                exon = Exon("exon:{}.{}".format(cds.cds_id,i),cds.seqid,cds.start,cds.end, cds.strand, [tr.id])
                tr.add_exon(exon)
        return transcripts

    def build_cds_transcript_relation(self, cds, transcripts, genes, source):

        # CDS could have the same ID or not
        # ie eugene diff ID,
        # CodingQuarry same ID 

        cds_no_transcript = {}

        all_cds = []
        #lcds = []
        for lcds in cds.values():
            all_cds += lcds
        for cds in all_cds:
            # add this test to fit with NOTE 2
            # CDS Parent could be the gene in 
            # ab initio gene prediction program
            # ie CodingQuarry


            if cds.transcript_id not in transcripts:
                if cds.transcript_id not in genes:
                    #raise Exception("CDS: {} has a parent: {}, not a gene nor a transcript".format(cds.cds_id,cds.transcript_id))
                    logging.error("CDS: {} has a parent: {}, not a gene nor a transcript".format(cds.cds_id,cds.transcript_id))
                #    print("TODO LOG ERROR: CDS: {} has a parent: {}, not a gene nor a transcript".format(cds.cds_id,cds.transcript_id))

                    raise Exception("CDS: {} has a parent: {}, not a gene nor a transcript".format(cds.cds_id,cds.transcript_id))
                    next
                else:
                    if cds.cds_id not in cds_no_transcript:
                        cds_no_transcript[cds.cds_id] = [cds]
                    else:
                        cds_no_transcript[cds.cds_id].append(cds)
            else:
                transcripts[cds.transcript_id].add_cds(cds)
        # Infer transcript
        # CDS must have the same ID
        # and same Parent
        new_transcripts = {}
        for cds_id in cds_no_transcript:
            gene_id = cds_no_transcript[cds_id][0].transcript_id
            seqid = cds_no_transcript[cds_id][0].seqid
            start = min([cds.start for cds in cds_no_transcript[cds_id]])
            end = max([cds.end for cds in cds_no_transcript[cds_id]])
            strand = cds_no_transcript[cds_id][0].strand
            tr_id = "{}-{}".format(cds_id,gene_id)
            tr = Transcript(tr_id,seqid,start,end,strand,gene_id,source)
            tr.coding = True
            # change tr id in CDS:
            for cds in cds_no_transcript[cds_id]:
                cds.transcript_id = tr_id

            print("TODO log: inferring tr from CDS: {}".format(tr))
            new_transcripts[tr_id] = tr
        if new_transcripts:
            new_transcripts = self.build_cds_transcript_relation(cds_no_transcript, new_transcripts, genes, source)

            transcripts.update(new_transcripts)

        return transcripts

    def build_exon_transcript_relation(self, exons, transcripts, genes):

        for exon in exons.values():
            for transcript_id in exon.lTranscript_ids:
                if transcript_id not in transcripts:
                    if transcript_id not in genes:
                    #raise Exception("Exon: {} has a parent: {}, not a gene nor a transcript".format(exon.exon_id,transcript_id))
                        logging.error("Exon: {} has a parent: {}, not a gene nor a transcript".format(exon.exon_id,transcript_id))
                        raise Exception ("Exon: {} has a parent: {}, not a gene nor a transcript".format(exon.exon_id,transcript_id))
                        next
                else:
                    transcripts[transcript_id].add_exon(exon)
        return transcripts

    def build_transcript_gene_relation(self, transcripts, genes, source):

        transcript_no_gene = {}
        for transcript in transcripts.values():
            if transcript.gene_id not in genes:
                #raise Exception("CDS: {} has a parent: {}, not a gene nor a transcript".format(cds.cds_id,cds.transcript_id))
          #      print("TODO LOG : Transcript: {} has a parent: {}, not a feature gene ".format(transcript.id,transcript.gene_id))
                if transcript.gene_id not in transcript_no_gene:
                    transcript_no_gene[transcript.gene_id] = [transcript]
                else:
                    transcript_no_gene[transcript.gene_id].append(transcript)
            else:
                genes[transcript.gene_id].add_transcript(transcript)
                if transcript.coding:
                    genes[transcript.gene_id].type = "coding"
                else:
                    genes[transcript.gene_id].type = "non-coding"
#        return genes
        # Infer genes
        new_genes = {}
        for gene_id in transcript_no_gene:
            seqid = transcript_no_gene[gene_id][0].seqid
            start = min([tr.start for tr in transcript_no_gene[gene_id]])
            end = max([tr.end for tr in transcript_no_gene[gene_id]])
            strand = transcript_no_gene[gene_id][0].strand
            g = Gene(gene_id,seqid,start,end,strand,source)
#            for tr in transcript_no_gene[gene_id]:
#                g.add_transcript(tr)
            g.coding = True

#            print("TODO log: inferring gene from tr: {}".format(transcript_no_gene[gene_id][0].id))
            new_genes[gene_id] = g
        if new_genes:
            new_genes = self.build_transcript_gene_relation(transcripts, new_genes, source)
            #new_genes = self.build_cds_transcript_relation(cds_no_transcript, new_transcripts, genes, source)

            genes.update(new_genes)

        return genes

    def deduplicate_genes(self, genes):
        """deduplicate genes based on exon coordinates"""

        dgenes = {}
        for gene in genes:
            transcripts = []
            for tr in gene.lTranscripts:
                transcripts.append(tuple(sorted([(ex.start,ex.end) for ex in tr.lExons])))
            dgenes[tuple(transcripts)] = gene

        return list(dgenes.values())
            
 
