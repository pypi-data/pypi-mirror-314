#!usr/bin/env python3

import logging
import copy
import pandas as pd
import numpy as np
import sys

from ingenannot.utils import Utils
from ingenannot.commands.command import Command

from ingenannot.utils.graphics import Graphics

from ingenannot.entities.transcript import Transcript
from ingenannot.entities.gene import Gene
from ingenannot.entities.exon import Exon

class Compare(Command):

    def __init__(self, args):

        self.fof = args.fof
        self.clutype = args.clutype
        self.clustranded = args.clustranded
        self.graph_out = args.graphout
        self.graph_title = args.graphtitle
        self.export_same_cds = args.export_same_cds
        self.export_specific = args.export_specific
        self.export_list_specific = args.export_list_specific
        self.export_venn = args.export_venn
        self.export_upsetplot = args.export_upsetplot
        self.source = "ingenannot_compare"


    def __get_number_of_unique_sources_from_transcripts(self,trs):
        """return the number of different sources"""

        sources = set()
        for tr in trs:
            sources.add(tr.source)
        return len(sources)

    def export_same_cds_files(self, same_CDS, filename):

        # export same CDS
        with open(filename, 'w') as f:
            logging.info("Writing: {} with {} CDS".format(filename, len(same_CDS)))
            for g in same_CDS:
                g.source = self.source
                f.write(g.to_gff3())
                tr = g.lTranscripts[0]
                tr.source = self.source
                f.write(tr.to_gff3(atts={"raw_transcripts":tr.dAttributes['raw_transcripts']}))
                for i, exon in enumerate(tr.lExons):
                    exon.source = self.source
                    f.write(exon.to_gff3())
                for i, cds in enumerate(tr.lCDS):
                    cds.source = self.source
                    f.write(cds.to_gff3())
        f.close()



#    def export_same_cds_files(self, same_CDS):
#
#        # export same CDS
#        with open("same_cds.gff3", 'w') as f:
#            logging.info("Writing: same_cds.gff3")
#            for g in same_CDS:
#                g.source = self.source
#                f.write(g.to_gff3())
#                tr = g.lTranscripts[0]
#                tr.source = self.source
#                f.write(tr.to_gff3(atts={"raw_transcripts":tr.dAttributes['raw_transcripts']}))
#                for i, exon in enumerate(tr.lExons):
#                    exon.source = self.source
#                    f.write(exon.to_gff3())
#                for i, cds in enumerate(tr.lCDS):
#                    cds.source = self.source
#                    f.write(cds.to_gff3())
#        f.close()
#
    def export_specific_files(self, specific_loci, specific_CDS_not_loci):

        # export specific loci
        self._export_from_dict(specific_loci,prefix="specific_loci")
        # export specific CDS not loci
        self._export_from_dict(specific_CDS_not_loci,prefix="specific_CDS_not_loci")

    def _export_from_dict(self,d,prefix):

        for k in d:
            with open("{}.{}.gff".format(k,prefix), 'w') as f:
                logging.info("Writing: {}.{}.gff".format(k,prefix))
                for tr in d[k]:
                    tr.source = self.source
                    f.write(tr.to_gff3())
                    for i, exon in enumerate(tr.lExons):
                        exon.source = self.source
                        f.write(exon.to_gff3())
                    for i, cds in enumerate(tr.lCDS):
                        cds.source = self.source
                        f.write(cds.to_gff3())
            f.close()


    def __prepare_same_CDS_for_export(self,m,i,ltr_CDS):
        """TODO"""

        tr_template = ltr_CDS[0]
        all_tr = [x.id for x in  ltr_CDS]
        seqid = tr_template.seqid
        start = tr_template.get_min_cds_start()
        end = tr_template.get_max_cds_end()
        strand = tr_template.strand
        g = Gene('gene-{}.{}'.format(m.id,i),seqid, start, end, strand)
        tr = Transcript('mRNA-{}.{}'.format(m.id,i),seqid, start, end, strand, g.gene_id)
        tr.dAttributes['raw_transcripts'] = all_tr
        lCDS = copy.deepcopy(tr_template.lCDS)
        lExons = []
        for cds_part in lCDS:
            cds_part.cds_id = 'cds.{}.{}'.format(m.id,i)
            cds_part.transcript_id = tr.id
            lExons.append(Exon('exon.{}.{}'.format(m.id,i),cds_part.seqid,cds_part.start,cds_part.end,cds_part.strand,[tr.id]))

        tr.lCDS = lCDS
        tr.lExons = lExons
        g.lTranscripts = [tr]

        return(g)


    def compare(self, metagenes, sources):
        '''compare genes'''

        metrics = {}
        all_CDS = set()
        CDS_clu_sources = {}
        for src in sources:
            CDS_clu_sources[src] = []
        metagenes_same_cds = []
        metagenes_different_cds = []

        nb_total_CDS = 0
        nb_same_cds = 0
        nb_same_cds_list_specific = 0
        same_CDS = []
        same_CDS_list_specific = []

        shared_CDS = {}
        shared_CDS_debug = {}
        for x,src in enumerate(sources):
            shared_CDS[x+1] = 0
            shared_CDS_debug[x+1] = []

        for m in metagenes:

            if m.have_transcripts_same_cds():
                metagenes_same_cds.append(m)
            else:
                metagenes_different_cds.append(m)
            CDS_transcripts = m.get_CDS_transcript_association()

            for i,cds in enumerate(CDS_transcripts):
                nb_total_CDS += 1

                # clean if same CDS from same source
                cds_sources = {}
                multiple = False
                to_remove = []
                for ti in list(CDS_transcripts.values())[i]:
                    if ti.source in cds_sources:
                        cds_sources[ti.source] += 1
                        multiple = True
                        to_remove.append(ti)
                    else:
                        cds_sources[ti.source] = 1
                if multiple:
                    for tr_r in to_remove:
                        CDS_transcripts[cds].remove(tr_r)
                        logging.error("WARNING, Source: {} have multiple same CDS for metagene {}, removing transcript: {}".format(tr_r.source,m.id,tr_r.id))


                if self.__get_number_of_unique_sources_from_transcripts(CDS_transcripts[cds]) == len(sources):
                    nb_same_cds += 1
                    if self.export_same_cds:
                        same_CDS.append(self.__prepare_same_CDS_for_export(m,i,CDS_transcripts[cds]))


                if self.export_list_specific:
                    if sorted(self.export_list_specific) == sorted([tr.source for tr in CDS_transcripts[cds]]):
                        nb_same_cds_list_specific += 1
                        same_CDS_list_specific.append(self.__prepare_same_CDS_for_export(m,i,CDS_transcripts[cds]))


                shared_CDS[self.__get_number_of_unique_sources_from_transcripts(CDS_transcripts[cds])] += 1

                for tr in CDS_transcripts[cds]:
                   CDS_clu_sources[tr.source].append("m{}.{}.{}.{}".format(m.id,i,m.seqid,m.start))
                   all_CDS.add("m{}.{}.{}.{}".format(m.id,i,m.seqid,m.start))


        metrics["Number of Metagenes"] = len(metagenes)
        metrics["Number of different CDS"] = nb_total_CDS
        metrics["Number of sources per CDS"] = shared_CDS
        metrics["Number of CDS shared by all sources"] =  nb_same_cds
        metrics["Number of MetaGenes with unique CDS"] = len(metagenes_same_cds)

        nbsrc_metag_same_cds = dict.fromkeys(range(1,len(sources)+1),0)
        nbsrc_metag_same_cds_debug = dict.fromkeys(range(1,len(sources)+1),[])
        for metagene in metagenes_same_cds:
            nbsrc_metag_same_cds[self.__get_number_of_unique_sources_from_transcripts(metagene.lTranscripts)] += 1
            nbsrc_metag_same_cds_debug[self.__get_number_of_unique_sources_from_transcripts(metagene.lTranscripts)].append(metagene.id)
        metrics["Number of MetaGenes with unique CDS (nb sources)"] = nbsrc_metag_same_cds
        metrics["Number of MetaGenes with multiple CDS"] = len(metagenes_different_cds)
        nbcds_metag_different_cds = {}
        for metagene in metagenes_different_cds:
            if len(metagene.lCDS) in nbcds_metag_different_cds:
                nbcds_metag_different_cds[len(metagene.lCDS)] += 1
            else:
                nbcds_metag_different_cds[len(metagene.lCDS)] = 1
        metrics["Number of MetaGenes with multiple CDS (nb different CDS)"] = nbcds_metag_different_cds

        metrics["shared same CDS"] = []
        for i, src1 in enumerate(sources):
            for src2 in sources[i::]:
                nb = 0
                for cds in CDS_clu_sources[src1]:
                    if cds in CDS_clu_sources[src2]:
                        nb += 1
                metrics["shared same CDS"].append("{} - {}: {}".format(src1, src2, nb))

        lMetagenes_for_filtering = copy.deepcopy(metagenes)

        # remove less representative CDS of each clusters
        transcripts_same_cds_2 = []
        for m in lMetagenes_for_filtering:
            CDS_tr = m.get_CDS_transcript_association()
            if (len(CDS_tr) > 1):
                max_nb = 0
                trToKeep = []
                for i,cds in enumerate(CDS_tr):
                    if len(list(CDS_tr.values())[i]) > max_nb:
                        trToKeep = list(CDS_tr.values())[i]
                        max_nb = len(list(CDS_tr.values())[i])
                m.lTranscripts = trToKeep

            if m.have_transcripts_same_cds():
                transcripts_same_cds_2.append(m)
        nbsrc_metag_same_cds_2 = {}
        nbsrc_metag_same_cds_2_debug = {}
        for x,src in enumerate(sources):
            nbsrc_metag_same_cds_2[x+1] = 0
            nbsrc_metag_same_cds_2_debug[x+1] = []
        for metagene in transcripts_same_cds_2:
            nbsrc_metag_same_cds_2[len(set([t.source for t in metagene.lTranscripts]))] += 1
            nbsrc_metag_same_cds_2_debug[len(set([t.source for t in metagene.lTranscripts]))].append(metagene.id)

        specific_CDS = {src:[] for src in sources}
        specific_loci = {src:0 for src in sources}
        specific_loci_CDS = {src:[] for src in sources}
        specific_CDS_not_loci = {src:[] for src in sources}
        for m in metagenes:
            asso = m.get_CDS_transcript_association()
            sources = []
            for cds in asso:
                sources.extend([t.source for t in asso[cds]])
            sources = set(sources)
            if len(sources) == 1:
                specific_loci[list(sources)[0]] += 1
                for cds in asso:
                    specific_loci_CDS[asso[cds][0].source].append(asso[cds][0])
                    specific_CDS[asso[cds][0].source].append(asso[cds][0])
            else:
                for cds in asso:
                    if len(asso[cds]) == 1:
                        specific_CDS_not_loci[asso[cds][0].source].append(asso[cds][0])
                        specific_CDS[asso[cds][0].source].append(asso[cds][0])

        metrics["Number of specific CDS per source"] = {key:len(specific_CDS[key]) for key in specific_CDS}
        metrics["Number of specific CDS, with other CDS from other source at the same locus/metagene"] = {key:len(specific_CDS_not_loci[key]) for key in specific_CDS_not_loci}
        metrics["Number of specific loci/Metagene per source"] = {key:specific_loci[key] for key in specific_loci}
        metrics["Number of sources of most representative CDS per Metagene"] = nbsrc_metag_same_cds_2

        if self.export_same_cds:
            self.export_same_cds_files(same_CDS, "same_cds.gff3")

        if self.export_specific:
            self.export_specific_files(specific_loci_CDS, specific_CDS_not_loci)

        if self.export_list_specific:
            self.export_same_cds_files(same_CDS_list_specific, "same_cds.{}.gff3".format("_".join(self.export_list_specific)))

        return all_CDS, CDS_clu_sources, metrics


    def venn_list(self, CDS_clu_sources, sources):
        """
        Export list for Venn Diagrams
        """

        for src in sources:
            with open("venn_{}.list".format(src), 'w') as f:
                logging.info("Writing: venn_{}.list".format(src))
                for cds in CDS_clu_sources[src]:
                    f.write("{}\n".format(cds))
            f.close()

        with open("all_sources_venn.list", 'w') as f:
            logging.info("Writing: all_sources_venn.list")
            f.write("{}\n".format("\t".join(sources)))
            end = max([len(CDS_clu_sources[src]) for src in sources])
            for i in range(0,end):
                val = []
                for src in sources:
                    if len(CDS_clu_sources[src]) > i:
                        val.append(CDS_clu_sources[src][i])
                    else:
                        val.append("")
                f.write("{}\n".format("\t".join(val)))
            f.close()



    def upsetplot(self, all_CDS, CDS_clu_sources, sources):
        """
        Draw upsetplot of shared/specific CDS
        """

        df = pd.DataFrame()
        for src in sources:
            val = []
            for cds in all_CDS:
                if cds in CDS_clu_sources[src]:
                    val.append(True)
                else:
                    val.append(False)
            df[src] = val
        df.reset_index(inplace=True)
        df.set_index(sources,inplace=True)
        Graphics.plot_upsetplot(df,self.graph_out,self.graph_title)
        logging.info("Upsetplot exported in {}".format(self.graph_out))

    def print_metrics(self, metrics):
        """print metrics"""

        for key in metrics:
            if type(metrics[key]) == list:
                print("{}:".format(key))
                for val in metrics[key]:
                    print(val)
            else:
                print("{}: {}".format(key,metrics[key]))


    def run(self):
        """"launch command"""

        sources = Utils.get_sources_from_fof(self.fof)

        if self.export_list_specific:
            for src in self.export_list_specific:
                if src not in sources:
                    raise Exception("One source specified in --export_list_specific is not available")

        genes = Utils.extract_genes_from_fof(self.fof)
        clusters = Utils.clusterize(genes, cltype=self.clutype, stranded=self.clustranded, procs=Command.NB_CPUS)
        metagenes = Utils.get_metagenes_from_clusters(clusters)
        all_CDS, CDS_clu_sources, metrics =  self.compare(metagenes, sources)
        self.print_metrics(metrics)
        if self.export_venn:
            self.venn_list(CDS_clu_sources,sources)
        if self.export_upsetplot:
            self.upsetplot(all_CDS,CDS_clu_sources,sources)

        return 0
