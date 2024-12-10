#!/usr/bin/env python3

from ingenannot.utils.em_operators import EMOperators as EM

class SOSplicingClassifier(object):
    """
    Splicing Classifier
    with SO codes
    """

    @staticmethod
    def classify_gene(gene, part_type='exon'):
        """
            classify transcripts of a gene

            :param gene: gene to classify
            :type gene: Gene
            :return: a tuple of 3 integers, corresponding to EM-questions
            :rtype: tuple
        """

        classification=(0,0,0)
        if len(gene.lTranscripts) > 0:
            for i,t1 in enumerate(gene.lTranscripts):
                for t2 in gene.lTranscripts[i+1::]:
                    classification = tuple([sum(x) for x in zip(classification,SOSplicingClassifier.classify_pair_of_transcripts(t1,t2,part_type))])
        return classification

    @staticmethod
    def classify_pair_of_transcripts(t1, t2, part_type):
        """
            classify

            :param t1: Transcript 1
            :param t2: Transcript 2
            :type t1: type
            :type t2: type
            :return: desc
            :rtype: type

        """

        if SOSplicingClassifier.are_transcripts_overlapping(t1, t2, part_type):
            return (0,0,1)
        elif SOSplicingClassifier.are_transcripts_parts_disjoint(t1, t2, part_type):
            return (0,1,0)
        else:
            return (1,0,0)


    @staticmethod
    def are_transcripts_sequence_disjoint(t1, t2, part_type):
        """
           Test if 2 transcripts are sequence disjoint

           Two transcripts are sequence disjoint if
           None of their exons shares any sequence
           in common.

           :param t1: Transcript 1
           :param t2: Transcript 2
           :type t1: Transcript
           :type t2: Transcript
           :return: True/False
           :rtype: bool
        """

        return not EM.part_overlap(t1, t2, type=part_type)

    @staticmethod
    def are_transcripts_parts_disjoint(t1,t2, part_type):
        """
           Test if 2 transcripts are parts disjoint

           Two transcripts are part disjoint if
           At least one of their exons shares any sequence
           in common, but with different coordinates

           :param t1: Transcript 1
           :param t2: Transcript 2
           :type t1: Transcript
           :type t2: Transcript
           :return: True/False
           :rtype: bool
        """

        return EM.part_overlap(t1, t2, type=part_type)

    @staticmethod
    def are_transcripts_overlapping(t1,t2, part_type):
        """
           Test if 2 transcripts are overlapping 

           Two transcripts are overlapping if at least 
           one of their exons (parts) is shared with same
           boundaries

        """

        return EM.overlap(t1, t2, type=part_type)
