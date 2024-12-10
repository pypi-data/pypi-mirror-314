#/usr/bin/env python3

import logging

from ingenannot.utils import Utils
from ingenannot.utils.so_splicing_classifier import SOSplicingClassifier
from ingenannot.commands.command import Command

class SOClassification(Command):

    def __init__(self, args):

        self.fof = args.fof
        self.clutype = args.clutype
        self.clustranded = args.clustranded
        self.clatype = args.clatype

    def classify(self, metagenes):

        classification = { "N:O:O" : [],
                    "N:N:O" : [],
                    "N:O:N" : [],
                    "N:N:N" : [],
                    "O:N:O" : [],
                    "O:N:N" : [],
                    "O:O:N" : [],
                    "unclassified" : []}

        transcripts_same_cds = []
    #    not_analyzed_metagenes = []

        for m in metagenes:

            if len(m.lTranscripts) == 1:
         #       not_analyzed_metagenes.append(m)
                classification["unclassified"].append(m)
                continue

            if m.have_transcripts_same_cds():
                transcripts_same_cds.append(m)

            classif = SOSplicingClassifier.classify_gene(m, self.clatype.lower())
            if (classif[0]>0 and classif[1]== 0 and classif[2] == 0):
                classification["N:O:O"].append(m)
            if (classif[0]>0 and classif[1]> 0 and classif[2] == 0):
                classification["N:N:O"].append(m)
            if (classif[0]>0 and classif[1]== 0 and classif[2] > 0):
                classification["N:O:N"].append(m)
            if (classif[0]>0 and classif[1]> 0 and classif[2] > 0):
                classification["N:N:N"].append(m)
            if (classif[0]==0 and classif[1]> 0 and classif[2] ==0):
                classification["O:N:O"].append(m)
            if (classif[0]==0 and classif[1]> 0 and classif[2] > 0):
                classification["O:N:N"].append(m)
            if (classif[0]==0 and classif[1]==0 and classif[2] >0):
                classification["O:O:N"].append(m)

        print("{} metagenes with only one transcript, not analyzed".format(len(classification['unclassified'])))

        print("Classification:")
        for k in classification.keys():
            print('{}:{}'.format(k, len(classification[k])))

        print("nb classified metagenes with all transcripts sharing the same CDS: {}".format(len(transcripts_same_cds)))

        return classification

    def export_classification(self, classification):

        for clas, metagenes in classification.items():
            logging.info("classification: {} in classification_{}.gff3".format(clas,clas))
            with open("classification_{}.gff3".format(clas), 'w') as f:
                for m in metagenes:
                    f.write("{}\tclassification\tregion\t{}\t{}\t.\t.\t.\tID={};classif={}\n".format(m.seqid,m.start, m.end,m.id,clas))


    def run(self):
        """"launch command"""

        genes = Utils.extract_genes_from_fof(self.fof)
        clusters = Utils.clusterize(genes, cltype=self.clutype, stranded=self.clustranded, procs=Command.NB_CPUS)
        metagenes = Utils.get_metagenes_from_clusters(clusters)
        classification = self.classify(metagenes)
        self.export_classification(classification)

        return 0
