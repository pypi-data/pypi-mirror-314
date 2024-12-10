#!/usr/bin/env python3
'''
Module with reader classes
'''
import re
import sys
import logging

class Feature():
    '''
    Feature: store feature fields
    '''

    def __init__(self, id, seqid, source, type, start, end, score, strand, frame, attributes):
        """Feature constructor"""

        self.id = id
        self.seqid = seqid
        self.source = source
        self.type = type
        self.start = start
        self.end = end
        self.score = score
        self.strand = strand
        self.frame = frame
        self.attributes = attributes

    def __eq__(self, other):
        """Equality on all args"""

        return ((self.id,self.seqid,self.source,self.type,self.start,self.end,self.score,self.strand,self.frame,self.attributes) == (other.id, other.seqid, other.source,other.type, other.start, other.end, other.score,other.strand, other.frame,other.attributes))

    def __repr__(self):
        """Feature representation"""

        return 'Feature: {}-{}-{}-{}-{}-{}-{}-{}-{}-{}'.format(self.type,self.id,self.seqid,self.source,self.start,self.end,self.score, self.strand,self.frame,self.attributes)

class GFF3Reader():
    '''
    GFF3Reader: read gff3 file
    '''

    def __init__(self, fh, loglevel='ERROR'):

        self.fh = fh
        self.loglevel = loglevel
        logging.basicConfig(level=self.loglevel)
        self.nbFeatures = 0
        self.sReferences = set()

        try:
            self.filehandle = open(self.fh, 'r')
        except Exception as e:
            logging.error(e)
            sys.exit(1)

    def __del__(self):
        """..."""

        self.filehandle.close()

    @staticmethod
    def _stringToDict(string):
        """convert field 9 from string to dict"""

        dAttributes = {}
        for att in string.split(";"):
            if att and att.split():
                values = att.split("=")
                #fix errors in GFF
                if len(values) == 2:
                    tag,val = att.split("=")
                    dAttributes[tag] = val.split(",")
        return dAttributes

    def read(self, downgraded=False):
        """Iterator on feature"""

        currentLine = None
        for idx, line in enumerate(self.filehandle):
            currentLine = line.strip()
            if not currentLine:
                pass
            elif re.match('^#', currentLine):
                pass
            else:
                m = re.search(r"^\s*(\S+)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)\s+([+-.])\s+(\S+)\s+(\S.*)$", currentLine)
                if m == None:
                    print(line)
                    raise Exception("Error GFF format line:{}".format(idx))

                id = GFF3Reader._getFeatureTagValue('ID',m.group(9),downgraded)
                dAttributes = GFF3Reader._stringToDict(m.group(9))
                score = None
                try:
                    score = float(m.group(6))
                except ValueError:
                    logging.debug("No score to cast as float")
                strand = GFF3Reader._getStrand(m.group(7))
                frame = None
                if m.group(8).isdigit():
                    frame = int(m.group(8))
                self.sReferences.add(m.group(1))
                f = Feature(id,m.group(1),m.group(2),m.group(3),int(m.group(4)),int(m.group(5)),score,strand, frame, dAttributes)
                self.nbFeatures += 1

                yield f

    @staticmethod
    def convertRowToFeature(row, idx=None, downgraded=False):

        m = re.search(r"^\s*(\S+)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)\s+([+-.])\s+(\S+)\s+(\S.*)$", row)
        if m == None:
            raise Exception("Error GFF format line:{}".format(idx))

        id = GFF3Reader._getFeatureTagValue('ID',m.group(9),downgraded=downgraded)
        dAttributes = GFF3Reader._stringToDict(m.group(9))
        score = None
        try:
            score = float(m.group(6))
        except ValueError:
            logging.debug("No score to cast as float")

        strand = GFF3Reader._getStrand(m.group(7))
        frame = None
        if m.group(8).isdigit():
            frame = int(m.group(8))
        #f = Feature(id,m.group(1),m.group(2),m.group(3),int(m.group(4))+1,int(m.group(5)),score,strand, frame, dAttributes)
        f = Feature(id,m.group(1),m.group(2),m.group(3),int(m.group(4)),int(m.group(5)),score,strand, frame, dAttributes)
        return f



    @staticmethod
    def _getFeatureTagValue(tag, line, downgraded=False):
        """Return the fist value of the tag property"""
        m = re.search(r".*{mytag}=([^;]*);{{0,1}}.*".format(mytag = tag),line)
        if m:
            return m.group(1).split(',')[0]
        elif downgraded:
            return None 
        else:
            raise Exception('Cannot find tag {} in string \'{}\''.format(tag, line))


    @staticmethod
    def _getStrand(strand):
        """Return strand as integer(1,-1) instead of +,- """

        if strand == '+':
            return 1
        elif strand == '-':
            return -1
        elif strand == '.':
            return None
        else:
            raise Exception('Cannot defined strand for feature')

    def getsReferences(self):
        """getter set of references"""

        return self.sReferences

        with open(self.fh, 'r') as input:
            for line in input:
                if not re.match('^#', line):
                    line = line.rstrip('\n')
                    values = line.split('\t')

    @staticmethod
    def _getFeatureTagValues(tag, line):
        """Return the list of values of the tag property"""
        m = re.search(r".*{mytag}=([^;]*);{{0,1}}.*".format(mytag = tag),line)
        if m:
            return m.group(1).split(',')
        else:
            raise Exception('Cannot find tag {} in string \'{}\''.format(tag, line))



class GTFReader():
    '''
    GTFReader: read gtf files
    '''

    def __init__(self, fh, loglevel='ERROR'):

        self.fh = fh
        self.loglevel = loglevel
        logging.basicConfig(level=self.loglevel)
        self.nbFeatures = 0
        self.sReferences = set()

        try:
            self.filehandle = open(self.fh, 'r')
        except Exception as e:
            logging.error(e)
            sys.exit(1)

    def __del__(self):
        """..."""

        self.filehandle.close()

    @staticmethod
    def _stringToDict(string):
        """convert field 9 from string to dict"""

        dAttributes = {}
        for att in string.split(";"):
            if att and  att.strip():
         #       print(att)
                tag,val = att.strip().split(" ")
                dAttributes[tag] = val.replace('"','').split(",")
        return dAttributes

    @staticmethod
    def convertRowToFeature(row, idx=None):

        m = re.search(r"^\s*(\S+)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)\s+([+-.])\s+(\S+)\s+(\S.*)$", row)
        if m == None:
            raise Exception("Error GTF format line:{}".format(idx))

        #id = self._getFeatureTagValue('ID',m.group(9))
        id = "feature-{}".format(idx)
        dAttributes = GTFReader._stringToDict(m.group(9))
        score = None
        try:
            score = float(m.group(6))
        except ValueError:
            logging.debug("No score to cast as float")
        strand = GTFReader._getStrand(m.group(7))
        frame = None
        if m.group(8).isdigit():
            frame = int(m.group(8))
        #f = Feature(id,m.group(1),m.group(2),m.group(3),int(m.group(4))+1,int(m.group(5)),score,strand, frame, dAttributes)
        f = Feature(id,m.group(1),m.group(2),m.group(3),int(m.group(4)),int(m.group(5)),score,strand, frame, dAttributes)

        return f

    def read(self, downgraded=False):
        """Iterator on feature"""

        currentLine = None
        for idx, line in enumerate(self.filehandle):
            currentLine = line.strip()
            if not currentLine:
                pass
            elif re.match('^#', currentLine):
                pass
            else:
                m = re.search(r"^\s*(\S+)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)\s+([+-.])\s+(\S+)\s+(\S.*)$", currentLine)
                if m == None:
                    raise Exception("Error GTF format line:{}".format(idx))

                #id = self._getFeatureTagValue('ID',m.group(9))
                id = "feature-{}".format(idx)
                dAttributes = self._stringToDict(m.group(9))
                score = None
                try:
                    score = float(m.group(6))
                except ValueError:
                    logging.debug("No score to cast as float")
                strand = self._getStrand(m.group(7))
                frame = None
                if m.group(8).isdigit():
                    frame = int(m.group(8))
                self.sReferences.add(m.group(1))
                f = Feature(id,m.group(1),m.group(2),m.group(3),int(m.group(4)),int(m.group(5)),score,strand, frame, dAttributes)
                self.nbFeatures += 1

                yield f

    @staticmethod
    def _getStrand(strand):
        """Return strand as integer(1,-1) instead of +,- """

        if strand == '+':
            return 1
        elif strand == '-':
            return -1
        elif strand == '.':
            return None
        else:
            raise Exception('Cannot defined strand for feature')

    def getsReferences(self):
        """getter set of references"""

        return self.sReferences

        with open(self.fh, 'r') as input:
            for line in input:
                if not re.match('^#', line):
                    line = line.rstrip('\n')
                    values = line.split('\t')


class GFFReader():
    '''
    GFFReader: factory
    '''

    __readers = {'gff3':GFF3Reader,
                 'gtf':GTFReader}


    def __init__(self, fh):
        """todo"""

        self.fh = fh
        with open(fh, 'r') as input:
            for line in input:
                if not re.match('^#', line):
                    self.fmt = GFFReader.guess_format(line)
                    break
        input.close()
        logging.info("parsing %s as format:%s",self.fh, self.fmt)
        self.reader = GFFReader.__readers[self.fmt](self.fh)

    @staticmethod
    def get_reader_type(fmt):
        if fmt not in  GFFReader.__readers:
            return None
        else:
            return GFFReader.__readers[fmt]

    @staticmethod
    def guess_format(line):
        """try to guess GFF/GTF format"""

        fields = line.rstrip('\n').split("\t")
        if len(fields) != 9:
            raise Exception("9 fields required to respect the GFF format {}".format(line))
        #first test split on ;
        all_tags = fields[8].split(";")
        #second test split on =
        tag1 = all_tags[0].split("=")
        if len(tag1) == 2:
            return "gff3"
        #third test split on " "
        tag1 = all_tags[0].split(" ")
        if len(tag1) == 2:
            if tag1[0] in ["gene_id", "transcript_id"]:
                return "gtf"
        else:
            return "gff2"


    def read(self, downgraded=False):
        """return dedicated reader feature generator"""

        yield from self.reader.read(downgraded=downgraded)

    @staticmethod
    def convertRowToFeature(row, idx=None):
        """return"""

        fmt = GFFReader.guess_format(row)
        return GFFReader.__readers[fmt].convertRowToFeature(row, idx)
