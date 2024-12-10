#!/usr/bin/env python3


class EMOperators(object):

    @staticmethod
    def overlap(x, y, type):
        """
           x and y are overlapping if they share
           at least one part in common
        """
        x_lparts = []
        y_lparts = []
        if type == 'exon':
            x_lparts = x.lExons
            y_lparts = y.lExons
        elif type == 'cds':
            x_lparts = x.lCDS
            y_lparts = y.lCDS
        else:
            raise Exception('part: {} not valid, use exon or cds'.format(type))

        for x_part in x_lparts:
            for y_part in y_lparts:
                if (x_part.start, x_part.end) == \
                   (y_part.start, y_part.end):
                    return True
        return False

    @staticmethod
    def disjoint(x, y, type):
        """
           x and y are disjoint if they share
           no parts in common
        """

        return not EMOperators.overlap(x, y, type)

    @staticmethod
    def part_overlap(x, y, type):
        """
           x and y have part overlappping
           if at least one base is shared
           between 2 parts"
        """

        x_lparts = []
        y_lparts = []
        if type == 'exon':
            x_lparts = x.lExons
            y_lparts = y.lExons
        elif type == 'cds':
            x_lparts = x.lCDS
            y_lparts = y.lCDS
        else:
            raise Exception('part: {} not valid, use exon or cds'.format(type))

        for x_part in x_lparts:
            for y_part in y_lparts:
                if EMOperators.__sequence_part_overlap(x_part, y_part):
                    return True
        return False

    @staticmethod
    def __sequence_part_overlap(x, y):
        """
           x and y sequence overlapping
        """

        if x.start > y.end or x.end < y.start:
            return False
        return True

    @staticmethod
    def binary_product(s1, s2):
        """todo"""

        pass

    @staticmethod
    def difference(s1, s2):
        """todo"""

        pass

    @staticmethod
    def binary_sum(s1, s2):
        """todo"""

        pass

