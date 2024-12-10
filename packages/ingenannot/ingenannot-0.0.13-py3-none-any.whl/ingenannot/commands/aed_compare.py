#!/usr/bin/env python3

'''This module contains AEDCompare class'''

import logging
import numpy as np
import pandas as pd
from ingenannot.utils import Utils
from ingenannot.utils.graphics import Graphics
from ingenannot.utils.statistics import Statistics
from ingenannot.commands.command import Command


class AEDCompare(Command):
    '''
    The AEDCompare is a Command running AED comparison.

    Attributes:
    -----------
    fof : list of files to compare
    statistics : perfom statistics
    ncol : number of columns in graph legend
    '''

    def __init__(self, args):

        self.fof = args.fof
        self.statistics = args.statistics
        self.ncol = 6

    def run(self):
        """"launch command"""

        sources = Utils.get_sources_from_fof(self.fof)
        genes = Utils.extract_genes_from_fof(self.fof)
        Utils.get_aed_from_attributes(genes)
        Graphics.plot_cumulative_aed(sources, genes, "tr","cumulative_tr_AED.png",self.ncol)
        Graphics.plot_cumulative_aed(sources, genes, "pr","cumulative_pr_AED.png",self.ncol)
        Graphics.plot_cumulative_aed(sources, genes, "best","cumulative_best_AED.png",self.ncol)

        if self.statistics:
            print(self.perform_stats(sources, genes).to_csv(sep="\t"))

        return 0

    def perform_stats(self, sources, genes):
        """run statistics"""

        logging.info("Running statistics")

        dfstats = pd.DataFrame(columns=['mean (tr)','median (tr)','stdev (tr)',
            'mean (pr)','median (pr)','stdev (pr)', 'median_geom_x','median_geom_y',
            'mean_distance', 'mean_distance_to_0','median_distance',
            'median_distance_to_0'],index=sources, dtype='float64')
        for src in sources:
            # extract data
            aed_scores_tmp = []
            for gene in [x for x in genes if x.source == src]:
                for trans in gene.lTranscripts:
                    aed_scores_tmp.append((trans.best_tr_evidence[1],trans.best_bx_evidence[1]))
            aed_scores = np.array([[i[0] for i in aed_scores_tmp],[i[1] for i in aed_scores_tmp]])

            # mean / median/ stdev
            means = np.mean(aed_scores,axis=1)
            median = np.median(aed_scores,axis=1)
            std = np.std(aed_scores,axis=1)
            dfstats['mean (tr)'][src] = round(means[0],3)
            dfstats['mean (pr)'][src] = round(means[1],3)
            dfstats['median (tr)'][src] = round(median[0],3)
            dfstats['median (pr)'][src] = round(median[1],3)
            dfstats['stdev (tr)'][src] = round(std[0],3)
            dfstats['stdev (pr)'][src] = round(std[1],3)

            # geometric median
            geom_median = Statistics.geometric_median(aed_scores)
            dfstats['median_geom_x'][src] = round(geom_median[0],3)
            dfstats['median_geom_y'][src] = round(geom_median[1],3)
            dfstats['mean_distance'][src] = round(Statistics.mean_median_distance(aed_scores,
                geom_median)[0],3)
            dfstats['mean_distance_to_0'][src] = round(Statistics.mean_median_distance(aed_scores,
                [0,0])[0],3)
            dfstats['median_distance'][src] = round(Statistics.mean_median_distance(aed_scores,
                geom_median)[1],3)
            dfstats['median_distance_to_0'][src] = round(Statistics.mean_median_distance(aed_scores,
                [0,0])[1],3)

        return dfstats
