# solutions.py
"""Volume 1, Lab 16: Importance Sampling and Monte Carlo Simulations.
Solutions file. Written by Tanner Christensen, Winter 2016.
"""

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

def prob1(n):
    """Approximate the probability that a random draw from the standard
    normal distribution will be greater than 3."""
    h = lambda x : x > 3
    X = np.random.randn(n)
    return 1/n * np.sum(h(X))

def prob2():
    """Answer the following question using importance sampling: 
            A tech support hotline receives an average of 2 calls per 
            minute. What is the probability that they will have to wait 
            at least 10 minutes to receive 9 calls?
    Returns:
        IS (array) - an array of estimates using 
            [5000, 10000, 15000, ..., 500000] as number of 
            sample points."""
    h = lambda y : y > 10
    f = lambda y : stats.gamma(a=9,scale=0.5).pdf(y)
    g = lambda y : stats.norm(loc=12,scale=2).pdf(y)
    num_samples = np.arange(5000,505000,5000)
    IS = []
    for n in num_samples:
        Y = np.random.normal(12,2,n)
        approx = 1./n*np.sum(h(Y)*f(Y)/g(Y))
        IS.append(approx)
    IS = np.array(IS)
    return IS

def prob3():
    """Plot the errors of Monte Carlo Simulation vs Importance Sampling
    for the prob2()."""
    h = lambda x : x > 10
    MC_estimates = []
    for N in xrange(5000,505000,5000):
        X = np.random.gamma(9,scale=0.5,size=N)
        MC = 1./N*np.sum(h(X))
        MC_estimates.append(MC)
    MC_estimates = np.array(MC_estimates)

    IS_estimates = prob2()
    
    actual = 1 - stats.gamma(a=9,scale=0.5).cdf(10)

    MC_errors = np.abs(MC_estimates - actual)
    IS_errors = np.abs(IS_estimates - actual)
    
    x = np.arange(5000,505000,5000)
    plt.plot(x, MC_errors, color='r', label="Monte Carlo")
    plt.plot(x, IS_errors, color='b', label="Importance Sampling")
    plt.legend()
    plt.show()
    
def prob4():
    """Approximate the probability that a random draw from the
    multivariate standard normal distribution will be less than -1 in 
    the x-direction and greater than 1 in the y-direction."""
    h = lambda y : y[0] < -1 and y[1] > 1
    f = lambda y : stats.multivariate_normal(np.zeros(2), np.eye(2)).pdf(y)
    g = lambda y : stats.multivariate_normal(np.array([-1,1]), np.eye(2)).pdf(y)
    
    n = 10**4
    Y = np.random.multivariate_normal(np.array([-1,1]), np.eye(2), size=n)
    hh = np.apply_along_axis(h, 1, Y)
    ff = np.apply_along_axis(f, 1, Y)
    gg = np.apply_along_axis(g, 1, Y)
    approx = 1./n*np.sum(hh*ff/gg)

    return approx
    
if __name__ == "__main__":
    import numpy as np
    print prob4()

    n = 10**6
    h = lambda y : y[0] < -1 and y[1] > 1
    X = np.random.multivariate_normal(np.zeros(2),np.eye(2),n)
    print 1/n * np.sum(np.apply_along_axis(h, 1, X))
    
    
