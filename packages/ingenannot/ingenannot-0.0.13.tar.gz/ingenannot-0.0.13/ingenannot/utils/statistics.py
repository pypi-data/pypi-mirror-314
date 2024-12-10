#!/usr/bin/env python3
'''
Statistics

shared statistics methods
'''

import math
import numpy as np


class Statistics():
    '''
    Statistics 
    '''

    @staticmethod
    def geometric_median(points, num_iter = 300):
        """
        Compute the geometric median of a set of sample points,
        with Weiszfeld's algorithm (http://en.wikipedia.org/wiki/Geometric_median)
        from stackoverflow implementation (https://stackoverflow.com/questions/30299267/geometric-median-of-multidimensional-points)

        Parameters
        ----------

        - points: 2D np.array with [x1,x2,..][y1,y2,...]
        - num_iter: number of max iterations to converge

        Return
        ------

        - 2D np.array with x,y median coordinates


        """

        # -- Initialising 'median' to the centroid
        y = np.mean(points,1)

        # -- If the init point is in the set of points, we shift it:
        while (y[0] in points[0]) and (y[1] in points[1]):
            y+=0.1
   
        convergence=False # boolean testing the convergence toward a global optimum
        dist=[] # list recording the distance evolution
    
        # -- Minimizing the sum of the squares of the distances between each points in 'X' and the median.
        i=0
        while ( (not convergence) and (i < num_iter) ):
            num_x, num_y = 0.0, 0.0
            denum = 0.0
            m = points.shape[1]
            d = 0
            for j in range(0,m):
                div = max(math.sqrt( (points[0,j]-y[0])**2 + (points[1,j]-y[1])**2 ),0.0001)
                num_x += points[0,j] / div
                num_y += points[1,j] / div
                denum += 1./div
                d += div**2 # distance (to the median) to miminize
            dist.append(d) # update of the distance evolution
    
            if denum == 0.:
                warnings.warn( "Couldn't compute a geometric median, please check your data!" )
                return [0,0]
    
            y = [num_x/denum, num_y/denum] # update to the new value of the median
            if i > 2:
                convergence=(abs(dist[i]-dist[i-2])<0.01) # we test the convergence over three steps for stability
            i += 1
        if i == num_iter:
            raise ValueError( "The Weiszfeld's algoritm did not converged after"+str(numIter)+"iterations !!!!!!!!!" )
        # -- When convergence or iterations limit is reached we assume that we found the median.
    
        return np.array(y)

    @staticmethod
    def mean_median_distance(points,center):

        d = [] 

        for i,x in enumerate(points[0]):
            d.append(math.sqrt(pow((points[0][i]-center[0]),2) + pow((points[1][i]-center[1]),2)))
        return np.mean(d), np.median(d)


