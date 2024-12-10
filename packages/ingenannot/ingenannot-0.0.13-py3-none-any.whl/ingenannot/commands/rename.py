import logging
import sys

from ingenannot.utils import Utils
from ingenannot.commands.command import Command

class Rename(Command):

    def __init__(self, args):

        self.gff_gene = args.Gff_genes
        self.pattern = args.pattern
        self.mapping = args.mapping
        self.name = args.name
        self.locus_tag = args.locus_tag
        self.tr_ranking_ID = args.tr_ranking_ID

    def run(self):
        """"launch command"""

        genes = []
        mapping_gene_table = {}
        mapping_tr_table = {}

        try:
            genes = Utils.extract_genes(self.gff_gene)
            logging.info("Validation OK")
        except Exception as e:
            logging.info("Validation Not OK")
            logging.error(e)



        source = "ingenannot"
        references = list(set([x.seqid for x in genes]))
        Utils.natural_sort(references)

        # index
        dgenes = {g.gene_id:g for g in genes}

        geneidx = 0
        for ref in references:
            geneidxref = 0
            seq_genes = [g for g in genes if g.seqid == ref]
            # sort tr per cds start if case not
            seq_tr = []
            for g in seq_genes:
                seq_tr.extend([tr for tr in g.lTranscripts])

            # keep trace gene if multiple tr
            gene_ok = []

            for tr in sorted(seq_tr, key=lambda x: x.get_min_cds_start()):
                if tr.gene_id not in dgenes:
                    raise Exception("Transcript {} with missing gene parent: {}".format(tr.id, tr.gene_id))

                if tr.gene_id not in gene_ok:
                    geneidx += 1
                    geneidxref += 1

                    gene_id = self.pattern.format(ref=ref,geneidx=geneidx,geneidxref=geneidxref)
                    atts = {'ID':[gene_id]}
                    if self.name:
                        atts['Name'] = ["{}".format(gene_id)]
                    if self.locus_tag:
                        atts['locus_tag'] = ["{}".format(gene_id)]

                    print(dgenes[tr.gene_id].to_gff3(atts=atts, source=source))

                    lTrs = dgenes[tr.gene_id].lTranscripts

                    if self.tr_ranking_ID:
                        lTrs = []
                        lTr_IDs = [t.id for t in dgenes[tr.gene_id].lTranscripts]
                        Utils.natural_sort(lTr_IDs)
                        for t_id in lTr_IDs:
                            for t in dgenes[tr.gene_id].lTranscripts:
                                if t_id == t.id:
                                    lTrs.append(t)

                    lExs = {}
                    for i,t in enumerate(lTrs):

                        tatts = t.dAttributes
                        tatts['ID'] = ["{}.{}".format(gene_id,i+1)]
                        tatts['Parent'] = ["{}".format(gene_id)]
                        if self.name:
                            tatts['Name'] = ["{}.{}".format(gene_id,i+1)]
                        if self.locus_tag:
                            tatts['locus_tag'] = ["{}".format(gene_id)]
                        print(t.to_gff3(atts=tatts,source=source))
                        mapping_tr_table[t.id] = "{}.{}".format(gene_id,i+1)

                        for ex in sorted(t.lExons, key=lambda x : x.start):
                            if (ex.seqid, ex.start, ex.end) not in lExs:
                                lExs[(ex.seqid, ex.start, ex.end)] = ex

                    for i,ex in enumerate(sorted(lExs.values(), key=lambda x: x.start)):
                        # rename exon
                        ex.exon_id = 'exon:{}.{}'.format(gene_id,i+1)
                        ex.source = source
                        # rename parent
                        ex_parent_ids = []
                        for ex_tr in ex.lTranscript_ids:
                            ex_parent_ids.append(mapping_tr_table[ex_tr])
                        ex.lTranscript_ids = ex_parent_ids

                        eatts = {'ID':[ex.exon_id]}
                        eatts['Parent'] = ex.lTranscript_ids
                        if self.locus_tag:
                            eatts['locus_tag'] = ["{}".format(gene_id)]
                        print(ex.to_gff3(eatts))

                    for i,t in enumerate(lTrs):
                        for cds in sorted(t.lCDS, key=lambda x : x.start):
                            cds.cds_id = 'cds:{}.{}'.format(gene_id,i+1)
                            cds.transcript_id = "{}.{}".format(gene_id,i+1)
                            cds.source = source

                            catts = {'ID':[cds.cds_id]}
                            catts['Parent'] = [cds.transcript_id]
                            if self.locus_tag:
                                catts['locus_tag'] = ["{}".format(gene_id)]
                            print(cds.to_gff3(catts))

                    for i,t in enumerate(lTrs):
                        strand = '+'
                        if t.strand == -1:
                           strand = '-'
                        five_prime_utrs = t.infer_five_prime_utrs()
                        for j,utr in enumerate(five_prime_utrs):
                            uatts = {'ID':['five_prime_UTR_{}.{}_{:03}'.format(gene_id,i+1,j+1)], 'Parent':["{}.{}".format(gene_id,i+1)]}
                            if self.locus_tag:
                                uatts['locus_tag'] = ["{}".format(gene_id)]
                            str_atts = ''
                            for att in uatts:
                                str_atts += '{}={};'.format(att,",".join(uatts[att]))
                            print("{}\t{}\tfive_prime_UTR\t{}\t{}\t.\t{}\t.\t{}\n".format(t.seqid,source,utr[0],utr[1],strand,str_atts))
                        three_prime_utrs = tr.infer_three_prime_utrs()
                        for j,utr in enumerate(three_prime_utrs):
                            uatts = {'ID':['three_prime_UTR_{}.{}_{:03}'.format(gene_id,i+1,j+1)], 'Parent':["{}.{}".format(gene_id,i+1)]}
                            if self.locus_tag:
                                uatts['locus_tag'] = ["{}".format(gene_id)]
                            str_atts = ''
                            for att in uatts:
                                str_atts += '{}={};'.format(att,",".join(uatts[att]))
                            print("{}\t{}\tthree_prime_UTR\t{}\t{}\t.\t{}\t.\t{}\n".format(tr.seqid,source,utr[0],utr[1],strand,str_atts))


                    gene_ok.append(tr.gene_id)
                    mapping_gene_table[tr.gene_id] = gene_id

        if self.mapping:
            logging.info("Exporting gene mapping in mapping_gene.txt")
            with open("mapping_gene.txt", 'w') as fh:
                fh.write("oldID\tnewID\n")
                for k in mapping_gene_table:
                    fh.write("{}\t{}\n".format(k,mapping_gene_table[k]))

            logging.info("Exporting transcript mapping in mapping_transcript.txt")
            with open("mapping_transcript.txt", 'w') as fh:
                fh.write("oldID\tnewID\n")
                for k in mapping_tr_table:
                    fh.write("{}\t{}\n".format(k,mapping_tr_table[k]))

        return 0
