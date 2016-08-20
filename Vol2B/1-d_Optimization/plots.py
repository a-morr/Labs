# plots.py
import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../matplotlibrc')

from matplotlib import pyplot as plt
import numpy as np
from scipy import linalg as la
from scipy import optimize as opt

def newtonsMethod1d(f, df, ddf, x, niter=10):   # Keep!
    '''
    Perform Newton's method to minimize a function from R to R.
    Inputs:
        f -- objective function (twice differentiable)
        df -- first derivative
        ddf -- second derivative
        x -- initial guess
        niter -- integer, giving the number of iterations
    Returns:
        the approximated minimizer
    '''
    for i in xrange(niter):
        x = x-df(x)/ddf(x)
    return x, f(x)

def myFunc(x):   # Keep!
    return 4*x**2 - 13*x + 40 + 6*np.sin(4*x)
def myDFunc(x):   # Keep!
    return 8*x - 13+24*np.cos(4*x)
def myDDFunc(x):   # Keep!
    return 8-96*np.sin(4*x)

def newton():  # Keep!
    x1,f1 = newtonsMethod1d(myFunc, myDFunc, myDDFunc, 1, niter=200)
    x2,f2 = newtonsMethod1d(myFunc, myDFunc, myDDFunc, 4, niter=200)
    dom = np.linspace(-10,10,100)
    plt.plot(dom, myFunc(dom))
    plt.plot(x1, f1, '*')
    plt.plot(x2, f2, '*')
    plt.annotate('Global Minimum', xy=(x1, f1), xytext=(-4, 200),
                arrowprops=dict(facecolor='black', shrink=0.1),)
    plt.annotate('Local Minimum', xy=(x2,f2), xytext=(2, 175),
                    arrowprops=dict(facecolor='black', shrink=0.1),)
    plt.savefig('newton.pdf')
    plt.clf()

newton()
