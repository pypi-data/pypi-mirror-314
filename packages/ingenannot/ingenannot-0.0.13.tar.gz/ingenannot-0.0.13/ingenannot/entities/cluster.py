#!/usr/bin/env python3
"""
entity class: Cluster
"""

class Cluster():
    """entity class: Cluster"""

    def __init__(self, seqid, start, end, strand=None, genes=None):
        """init"""

        self.seqid = seqid
        self.start = start
        self.end = end
        self.strand = strand
        if genes is None:
            self.genes = []
        else:
            self.genes = genes
            self.genes.sort(key=lambda x: (x.start, x.gene_id))

    @classmethod
    def merge(cls,clusters, stranded=False):
        """merge list of clusters"""

        if stranded:
            for i,clu in enumerate(clusters[:-1]):
                if clusters[i].strand != clusters[i+1].strand:
                    raise Exception("Cannot merge clusters, same strand required")
        seqid = clusters[0].seqid
        start = min([clu.start for clu in clusters])
        end = max([clu.end for clu in clusters])
        strand = clusters[0].strand
        genes = []
        for clu in clusters:
            genes.extend(clu.genes)
        genes.sort(key=lambda x: (x.start, x.gene_id))
        return cls(seqid,start,end,strand, list(genes))

    def add_gene(self, gene, stranded=False):
        """add gene"""

        if stranded and gene.strand != self.strand:
            raise Exception("Cannot add a gene to a cluster with a \
                    different strand, when stranded required")
        self.genes.append(gene)
        self.genes.sort(key=lambda x: (x.start, x.gene_id))

    def is_cluster_spanning(self, cluster, stranded=False):
        """test if 2 clusters overlap"""

        if stranded is True and self.strand != cluster.strand:
            return False
        if self.start <= cluster.start <= self.end:
            return True
        if self.start <= cluster.end <= self.end:
            return True
        if cluster.start <= self.start and cluster.end >= self.end:
            return True
        return False

    def is_cluster_spanning_min_cov(self, cluster, stranded=False, cov=0.5):
        """
           test if 2 clusters overlap
           if the fraction of overlap equal at least
           the "cov" parameter of the param "cluster"
           and not the reference cluster.
        """

        if stranded is True and self.strand != cluster.strand:
            return False
        overlap = self.end - cluster.start
        if self.start <= cluster.start <= self.end:
            if overlap / (cluster.end-cluster.start) >= cov:
                return True
        overlap = cluster.end - self.start
        if self.start <= cluster.end <= self.end:
            if overlap / (cluster.end-cluster.start) >= cov:
                return True
        if cluster.start <= self.start and cluster.end >= self.end:
            return True
        return False

    def is_gene_spanning(self, gene):
        """test if a CDS overlap the cluster"""

        if self.start <= gene.get_min_cds_start() <= self.end:
            return True
        if self.start <= gene.get_max_cds_end() <= self.end:
            return True
        if gene.get_min_cds_start() <= self.start and gene.get_max_cds_end() >= self.end:
            return True
        return False

    def __eq__(self, other):
        """Equality on all args"""

        return (self.seqid,self.start,self.end, self.genes) == \
                (other.seqid, other.start, other.end, other.genes)

    def __ne__(self, other):

        return not self == other

    def __str__(self):
        """Cluster representation"""

        return 'Cluster: {}-{}-{}-{}-{}'.format(self.seqid,self.start,
                self.end,self.strand, [gene.gene_id for gene in self.genes])
