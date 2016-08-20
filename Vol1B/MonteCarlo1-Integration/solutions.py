# solutions.py
"""Volume I: Monte Carlo Integration
Solutions file. Written by Tanner Christensen, Jan 2016
Edited by Jessica Morrise, May 2016
"""

import numpy as np
import scipy.stats as stats
from matplotlib import pyplot as plt
    
def prob1(N=10000):
    """Return an estimate of the volume of the unit sphere using Monte
    Carlo Integration.

    Input:
        N (int, optional) - The number of points to sample. Defaults
            to 10000.
    
    """
    points = np.random.rand(3, N)
    points = points*2 - 1
    radii = np.linalg.norm(points,axis=0)
    numInSphere = np.count_nonzero(radii <= 1)
    return 8.*numInSphere/N
    
def prob2(f, a, b, N=10000):
    """Use Monte-Carlo integration to approximate the integral of 
    1-D function f on the interval [a,b].
    
    Inputs:
        f (function) - Function to integrate. Should take scalar input.
        a (float) - Left-hand side of interval.
        b (float) - Right-hand side of interval.
        N (int, optional) - The number of points to sample in 
            the Monte-Carlo method. Defaults to 10000.
        
    Returns:
        estimate (float) - The result of the Monte-Carlo algorithm.
                
    Example:
        >>> f = lambda x: x**2
        >>> # Integral from 0 to 1. True value is 1/3.
        >>> prob2(f, 0, 1)
        0.3333057231764805
    """
    points = np.random.rand(1,N)
    V = b-a
    points = V*points + a
    fPoints = np.apply_along_axis(f,0,points)
    return V*np.sum(fPoints)/float(N)
    
def prob3(f, mins, maxs, N=10000):
    """Use Monte-Carlo integration to approximate the integral of f
    on the box defined by mins and maxs.
    
    Inputs:
        f (function) - The function to integrate. This function should 
            accept a 1-D NumPy array as input.
        mins (1-D np.ndarray) - Minimum bounds on integration.
        maxs (1-D np.ndarray) - Maximum bounds on integration.
        N (int, optional) - The number of points to sample in 
            the Monte-Carlo method. Defaults to 10000.
        
    Returns:
        estimate (float) - The result of the Monte-Carlo algorithm.
                
    Example:
        >>> f = lambda x: np.hypot(x[0], x[1]) <= 1
        >>> # Integral over the square [-1,1] x [-1,1]. True value is pi.
        >>> mc_int(f, np.array([-1,-1]), np.array([1,1]))
        3.1290400000000007
    """
    if len(mins) != len(maxs):
        raise ValueError("Dimension of mins and maxs must be the same")
    
    # create points
    dim = len(mins)
    side_lengths = maxs-mins
    points = np.random.rand(N,dim)
    points = side_lengths*points + mins

    # calculate Volume
    V = 1
    for i in xrange(dim):
        V *= maxs[i] - mins[i]

    # apply the function f along axis=1 and sum all the results
    estimate = V*np.sum(np.apply_along_axis(f,1,points))/float(N)
    
    return estimate
    
def prob4():
    
    #define the joint normal distribution
    joint_normal = lambda x: 1/(2*np.pi)**(len(x)/2.)*np.exp(-x.T.dot(x)/2.)    
    
    mins = np.array([-1.5,0,0,0])
    maxs = np.array([0.75,1,0.5,1])
    means = np.zeros(4)
    covs = np.eye(4)
    
    my_value = prob3(joint_normal,mins,maxs,50000)  
    scipy_value, inform = stats.mvn.mvnun(mins, maxs, means, covs)
    err = np.abs(my_value - scipy_value)/abs(scipy_value) # relative error
    return my_value, scipy_value, err  
    
def prob5(numEstimates=50):
    """Plot the error of Monte Carlo Integration.
    """

    # actual volume of the unit sphere
    actual = 4.1887902047863905
    
    # construct an array of values of N
    # use closer-spaced values near 50
    N = [i*1000 for i in xrange(1,51)]
    N = [50,100,500] + N
    errors = []    
    
    for n in N:
        meanErr = 0.
        for i in xrange(numEstimates):
            I = prob1(n) # estimate the integral
            err = np.abs(I - actual)/actual # compute the relative error
            meanErr += err
        errors.append(meanErr/float(numEstimates))
    
    # create the plot
    plt.plot(N,errors,label='Error')
    plt.plot(N,[1./n**0.5 for n in N],'r--',label=r'$1/\sqrt{N}$')
    plt.ylim([0,max(errors)])
    plt.xlim([0,max(N)])
    plt.xlabel(r'$N$')
    plt.ylabel('Relative error')
    plt.title('Sphere volume error vs. number of points used')
    plt.legend()
    plt.show()
    
if __name__ == "__main__":
    print prob1()
