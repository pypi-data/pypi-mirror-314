#!/usr/bin/env python3

import os
import re
import pandas as pd
from subprocess import PIPE, run
import argparse
import logging
import multiprocessing
from  ingenannot.commands.command import Command
from  ingenannot.utils.effector_predictor import EffectorPredictor


class EffectorPredictorCmd(Command,EffectorPredictor):

    def __init__(self, args):

        EffectorPredictor.__init__(self,args.fasta)
        EffectorPredictor.TMHMM = args.tmhmm
        EffectorPredictor.SIGNALP = args.signalp
        EffectorPredictor.EFFECTORP = args.effectorp
        EffectorPredictor.TARGETP = args.targetp
        EffectorPredictor.SIGNALP_CPOS = args.signalp_cpos
        EffectorPredictor.EFFECTORP_THRESHOLD = args.effectorp_score
        EffectorPredictor.MAX_LENGTH = args.max_len
        EffectorPredictor.MIN_LENGTH = args.min_len


