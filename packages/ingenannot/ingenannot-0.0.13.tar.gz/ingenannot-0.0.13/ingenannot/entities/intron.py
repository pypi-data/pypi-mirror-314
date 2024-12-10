#!/usr/bin/env python3

class Intron(object):

    def __init__(self,intron_id, seqid, start, end, source=None):
        """Intron constructor"""

        self.intron_id = intron_id
        self.seqid = seqid
        self.start = start
        self.end = end
        self.source = source


