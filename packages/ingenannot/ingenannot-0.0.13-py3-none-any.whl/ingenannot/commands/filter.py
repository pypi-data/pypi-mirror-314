#/usr/bin/env python3

import logging
import re

from  ingenannot.utils import Utils
from  ingenannot.entities.cds import CDS

class Filter(object):

    def __init__(self, args):

        self.gff_gene = args.Gff_genes
        self.gff_te = args.Gff_TEs
        self.gff_output = args.Output
        self.size_te = args.size
        self.feature = args.feature
        self.bed = args.bed
        self.fraction = args.fraction

    def extract_te_coords(self):
        """extract Transposable elements coordinates"""

        logging.info("reading {}".format(self.gff_te))

        coords = []
        with open(self.gff_te, 'r') as f:
            for line in f:
                if not re.match('^#', line):
                    val = line.rstrip().split("\t")
                    if self.bed:
                        if int(val[2])-int(val[1]) > self.size_te:
                            coords.append((val[0],int(val[1])+1,int(val[2])))
                    else:
                        if val[2] == self.feature and int(val[4])-int(val[3])+1 > self.size_te:
                            coords.append((val[0],int(val[3]),int(val[4])))

        logging.info("{} regions extracted from {}".format(len(coords),self.gff_te))

        return coords

    def overlap_te_features(self, genes, te_coords, fraction=0.1):
        """overlap between TE and specified feature"""

        logging.info("computing overlaps")

        lgenes = []
        for gene in genes:
            to_remove = False
            for co in te_coords:
                if gene.seqid != co[0]:
                    continue
                nb_overlapping_bases = 0
                for cds in gene.lTranscripts[0].lCDS:
                    if cds.start <= co[1] <= cds.end <= co[2]:
                        nb_overlapping_bases += cds.end-co[1]+1
                    if co[1] <= cds.start <= co[2] <= cds.end:
                        nb_overlapping_bases += co[2]-cds.start+1
                    if cds.start <= co[1] <= co[2] <= cds.end:
                        nb_overlapping_bases += co[2]-co[1]+1
                    if co[1] <= cds.start and co[2] >= cds.end:
                        nb_overlapping_bases += cds.end-cds.start+1
                if nb_overlapping_bases / gene.lTranscripts[0].getCDSTotalLength() > fraction:
                    to_remove = True
                    continue
            if to_remove:
                continue
            else:
                lgenes.append(gene)
        return lgenes

    def export(self, genes):
        """export to Gff3"""

        logging.info("exporting genes in {}".format(self.gff_output))

        references = set()
        for g in genes:
            references.add(g.seqid)
        references = list(references)
        Utils.natural_sort(references)

        with open(self.gff_output, 'w') as f:
            for ref in references:
                for gene in sorted([g for g in genes if g.seqid==ref], key=lambda x:x.start) :
                    atts = {'ID':[gene.gene_id],'source':[gene.source]}
                    f.write(gene.to_gff3(atts))

                    for tr in gene.lTranscripts:
                        #atts = {'ID':[tr.id], 'source':[gene.source],'Parent':[gene.gene_id]}
                        atts = tr.dAttributes
                        atts['ID'] = [tr.id]
                        #atts['source'] = [gene.source]
                        atts['Parent'] = [gene.gene_id]
                        f.write(tr.to_gff3(atts=atts))
                    #dedup exons
                    lExons = []
                    for tr in gene.lTranscripts:
                        for i,exon in enumerate(tr.lExons):
                            atts = {'ID':[exon.exon_id], 'source':[gene.source],'Parent':[",".join(exon.lTranscript_ids)]}
                            #tr.add_cds(CDS('cds:{}_{}-{}'.format(exon.seqid,exon.start,exon.end),exon.seqid,exon.start,exon.end,exon.strand,'.',tr.id))
                            if exon.exon_id not in lExons:
                                f.write(exon.to_gff3(atts=atts))
                                lExons.append(exon.exon_id)
                    for tr in gene.lTranscripts:
                        for i,cds in enumerate(tr.lCDS):
                            atts = {'ID':[cds.cds_id], 'source':[gene.source],'Parent':[tr.id]}
                            f.write(cds.to_gff3(atts=atts))
        f.close()

        logging.info("{} genes exported".format(len(genes)))



    def run(self):
        """"launch command"""

        genes = Utils.extract_genes(self.gff_gene)
        te_coords = self.extract_te_coords()
        filtered_genes = self.overlap_te_features(genes, te_coords, self.fraction)
        self.export(filtered_genes)

        return 0
