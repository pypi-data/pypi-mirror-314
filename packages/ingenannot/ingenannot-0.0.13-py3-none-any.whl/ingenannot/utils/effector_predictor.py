#!/usr/bin/env python3

import os
import sys
import re
import shutil
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
from subprocess import PIPE, run
import argparse
import logging
import multiprocessing
import pysam

from ingenannot.utils.tool_checker import ToolChecker

class EffectorPredictor(object):


    SIGNALP, SIGNALP_VERSION = ToolChecker.find_tool('signalp')
    SIGNALP_CPOS = 25
    TMHMM, TMHMM_VERSION = ToolChecker.find_tool('tmhmm')
    TARGETP, TARGETP_VERSION = ToolChecker.find_tool("targetp")
    EFFECTORP, EFFECTORP_VERSION = ToolChecker.find_tool("effectorp")
    EFFECTORP_THRESHOLD = 0.7
    MAX_LENGTH = 300
    MIN_LENGTH = 30


    def __init__(self, fasta):

        self.fasta = os.path.abspath(fasta)
        self.output = 'effectors.txt'
        self.directory = os.getcwd()
        self.wdirectory = os.path.abspath("effpred")
        self.tools = ["signalp","tmhmm","targetp", "effectorp"]
        #self.tools = ["effectorp"]

    def validate_tools_status(self):

        if "signalp" in self.tools:
            if EffectorPredictor.SIGNALP is None or not os.path.isfile(EffectorPredictor.SIGNALP):
                raise Exception("signalp not found in {}".format(EffectorPredictor.SIGNALP))
            if EffectorPredictor.SIGNALP_VERSION:
                result = run("{} -V".format(EffectorPredictor.SIGNALP), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
                if not re.fullmatch(result.stdout.rstrip(), "signalp {}".format(EffectorPredictor.SIGNALP_VERSION)):
                    raise Exception("bad signalp version: {}".format(result.stdout))

        if "tmhmm" in self.tools:
            if EffectorPredictor.TMHMM is None or not os.path.isfile(EffectorPredictor.TMHMM):
                raise Exception("tmhmm not found in {}".format(EffectorPredictor.TMHMM))

        if "targetp" in self.tools:
            if EffectorPredictor.TARGETP is None or not os.path.isfile(EffectorPredictor.TARGETP):
                raise Exception("targetp not found in {}".format(EffectorPredictor.TARGETP))
            if EffectorPredictor.TARGETP_VERSION:
                result = run("{} -v".format(EffectorPredictor.TARGETP), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
                if not re.match("targetp v{}.*".format(EffectorPredictor.TARGETP_VERSION),result.stdout.rstrip()):
                    raise Exception("bad targetp version: {}".format(result.stdout))

        if "effectorp" in self.tools:
            if EffectorPredictor.EFFECTORP is None or not os.path.isfile(EffectorPredictor.EFFECTORP):
                raise Exception("effectorp not found in {}".format(EffectorPredictor.EFFECTORP))
            if EffectorPredictor.EFFECTORP_VERSION:
                result = run("{}".format(EffectorPredictor.EFFECTORP), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
                if not re.findall("EffectorP {}".format(EffectorPredictor.EFFECTORP_VERSION),result.stdout):
                    raise Exception("bad effectorp version: {}".format(result.stdout))
        return 0


    def run_signalp(self):

        rdir = "{}/signalp".format(self.wdirectory)
        os.makedirs(rdir, exist_ok=True)
        os.chdir(rdir)
        signalp_out = open("signalp.out", "w")
        result = run("{} -t euk {}".format(EffectorPredictor.SIGNALP, self.fasta_size_reduce ), stdout=signalp_out, stderr=PIPE, universal_newlines=True, shell=True)
        signalp_out.close()
        os.chdir(self.directory)
        return os.path.abspath("{}/signalp.out".format(rdir))

    def collect_signalp(self, output):

        # avoid first line and multi escape sep
        df = pd.read_csv(output, sep=r"\s+", skiprows=2, names=['name','Cmax', 'Cpos', 'Ymax', 'Ypos','Smax', 'Spos', 'Smean', 'D', 'SP', 'Dmaxcut', 'network'])
        df = df.drop(['Cmax','Ymax','Ypos','Spos','Smean','D','Dmaxcut'], axis = 1)
        names=[('signalp',i) for i in ['Cpos', 'Smax', 'SP', 'network']]
        names[:0] = [('name','')]
        index = pd.MultiIndex.from_tuples(names)
        df.columns = index
        return df


    def run_tmhmm(self):

        rdir = "{}/tmhmm".format(self.wdirectory)
        os.makedirs(rdir, exist_ok=True)
        os.chdir(rdir)
        tmhmm_out = open("tmhmm.out", "w")
        result = run("{} --short {}".format(EffectorPredictor.TMHMM, self.fasta_size_reduce ), stdout=tmhmm_out, stderr=PIPE, universal_newlines=True, shell=True)
        tmhmm_out.close()
        os.chdir(self.directory)
        return os.path.abspath("{}/tmhmm.out".format(rdir))


    def collect_tmhmm(self, output):

        df = pd.read_csv(output, sep=r'\s+', names=['name','len','AA','First','TMHMM', 'Topology'])
        df['TMHMM'] = df['TMHMM'].str.extract(r'PredHel=([\d+])')
        df = df.drop(['len','AA','First','Topology'], axis=1)
        names = [('name',''),('tmhmm','domains')]
        index = pd.MultiIndex.from_tuples(names)
        df.columns = index
        return df

    def run_targetp(self):

        rdir = "{}/targetp".format(self.wdirectory)
        os.makedirs(rdir, exist_ok=True)
        os.chdir(rdir)
        lfiles = self.subset_fasta(self.fasta_size_reduce , chunk=1000)
        lout = []
        for f in lfiles:
            targetp_out = open("{}.targetp".format(f),"w")
            lout.append(os.path.abspath("{}.targetp".format(f)))
            result = run("{} --fasta {} -stdout".format(EffectorPredictor.TARGETP, f), stdout=targetp_out, stderr=PIPE, universal_newlines=True, shell=True)
            targetp_out.close()
        os.chdir(self.directory)
        return lout


    def collect_targetp(self, loutput):

        df = pd.DataFrame()
        for o in loutput:
            num_lines = sum(1 for line in open(o))
            df_tmp = pd.read_csv(o, sep='\t', names=['ID','Prediction','noTP','SP','mTP', 'CS Position'], skiprows=[0,1])
            df = pd.concat([df,df_tmp])
        df = df.drop(['noTP','mTP','SP','CS Position'], axis=1)
        names = [('ID',''),('targetp','Localization')]
        index = pd.MultiIndex.from_tuples(names)
        df.columns = index
        return df

    def run_effectorp(self):

        rdir = "{}/effectorp".format(self.wdirectory)
        os.makedirs(rdir, exist_ok=True)
        os.chdir(rdir)
        effectorp_out = "effectorp_out.tab"
        fasta_out = "effectorp_out.fasta"
        result = run("{} -s -o {} -E {} -i {}".format(EffectorPredictor.EFFECTORP, effectorp_out, fasta_out, self.fasta_size_reduce ), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        os.chdir(self.directory)
        return os.path.abspath("{}/{}".format(rdir,effectorp_out))

    def collect_effectorp(self,output):

        df = pd.read_csv(output, sep="\t")
        names = [('name',''),('effectorp','prediction'),('effectorp','probability')]
        index = pd.MultiIndex.from_tuples(names)
        df.columns = index
        return df

    def subset_fasta(self, fasta, directory=os.getcwd(), chunk=1000):

        lfiles = set()
        idx = 0
        fout = open("chunk_{}".format(idx), 'w')
        with open(fasta, "r") as fh:
            for line in fh:
                if idx%chunk:
                    fout.write(line)
                else:
                    fout.write(line)
                    fout.close()
                    fout = open("chunk_{}".format(int(idx)), 'w')
                    lfiles.add("chunk_{}".format(idx))
                    fout.write(line)
                if line.startswith(">"):
                    idx += 1
        fout.close()
        return list(lfiles)

    def seq_filter_len(self):
        '''remove sequence smaller/longer than threshold'''

        filtered_fasta = "{}/size_filtered.fasta".format(self.wdirectory)
        fout = open(filtered_fasta, 'w')
        df = pd.DataFrame(columns=['Seq','length'])

        with pysam.FastxFile(self.fasta) as fh:
            for entry in fh:
                if EffectorPredictor.MIN_LENGTH < len(entry.sequence) < EffectorPredictor.MAX_LENGTH:
                    fout.write(">{}\n{}\n".format(entry.name, entry.sequence))
                    df = df._append({'Seq': entry.name, 'length':len(entry.sequence)}, ignore_index=True)

        names = [('Seq',''), ('length','')]
        index = pd.MultiIndex.from_tuples(names)
        df.columns = index
        return filtered_fasta, df

    def run(self, export=True):

        try:
            self.validate_tools_status()
            logging.info("Tools availability OK")
        except Exception as e:
            logging.error("Problem with tools availability, please check log")
            logging.error(e)
            raise(e)

        os.makedirs(self.wdirectory, exist_ok=True)

        self.fasta_size_reduce, df = self.seq_filter_len()

        if os.path.getsize(self.fasta_size_reduce) > 0:
            for tool in self.tools:

                if tool == "signalp":
                    signalp_out = self.run_signalp()
                    df_signalp = self.collect_signalp(signalp_out)
                    df = df.merge(df_signalp, left_on=('Seq'), right_on=('name'))
                    df = df.drop([('name')], axis=1)
                    df = df.loc[(df.loc[:,('signalp','SP')] == 'Y') & (df.loc[:,('signalp','Cpos')] < EffectorPredictor.SIGNALP_CPOS)]

                if tool == "tmhmm":
                    tmhmm_out = self.run_tmhmm()
                    df_tmhmm = self.collect_tmhmm(tmhmm_out)
                    df = df.merge(df_tmhmm, left_on=('Seq'), right_on=('name'))
                    df = df.drop([('name')], axis=1)
                    df[('tmhmm','domains')] = pd.to_numeric(df[('tmhmm','domains')])
                    df = df.loc[(df.loc[:,('tmhmm','domains')] == 0)]

                if tool == "targetp":
                    ltargetp_out = self.run_targetp()
                    df_targetp = self.collect_targetp(ltargetp_out)
                    df = df.merge(df_targetp, left_on=('Seq'), right_on=('ID'))
                    df = df.drop([('ID')], axis=1)
                    df = df.loc[(df.loc[:,('targetp','Localization')] == 'SP')]

                if tool == "effectorp":
                    effectorp_out = self.run_effectorp()
                    df_effectorp = self.collect_effectorp(effectorp_out)
                    df = df.merge(df_effectorp, left_on=('Seq'), right_on=('name'))
                    df = df.drop([('name')], axis=1)
                    df = df.loc[(df.loc[:,('effectorp','prediction')] == 'Effector') & (df.loc[:,('effectorp','probability')] > EffectorPredictor.EFFECTORP_THRESHOLD)]
        else:
            names = [('Seq',''), ('length',''),('signalp','Cpos'), ('signalp','Smax'), ('signalp','SP'), ('signalp','network'),('tmhmm','domains'),('targetp','Localization'),('effectorp','prediction'),('effectorp','probability')]
            df = pd.DataFrame(columns=names)
            index = pd.MultiIndex.from_tuples(names)
            df.columns = index

        if export:
            df = df.set_index('Seq')
            df.to_csv('{}/{}'.format(self.directory,self.output), float_format="%.3f")
        return df
