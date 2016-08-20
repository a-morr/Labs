import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../../matplotlibrc')

import numpy as np
import numpy.linalg as la
from matplotlib import pyplot as plt


def mc_circle():
    np.random.seed(42)
    points = np.random.rand(2, 500).T
    points = 4*(points-.5)
    pointsNorm = np.hypot(points[:,0],points[:,1]) <= 1
    InCircle = points[pointsNorm]
    OutCircle = points[~pointsNorm]
    plt.plot(InCircle[:,0], InCircle[:,1], 'r.')
    plt.plot(OutCircle[:,0], OutCircle[:,1], 'b.')

    # Plot the circle
    theta = np.linspace(0, 2*np.pi, 50)
    plt.plot(np.cos(theta),np.sin(theta),'k')

    plt.axes().set_aspect('equal')
    plt.axis([-2, 2, -2, 2])

    plt.savefig("figures/MC_Circle.pdf")
    plt.clf()

def prob1(N=10000):
    """Return an estimate of the volume of the unit sphere using Monte
    Carlo Integration.

    Input:
        N (int, optional) - The number of points to sample. Defaults
            to 10000.

    """
    points = np.random.rand(3, N)
    points = points*2 - 1
    radiusMask = la.norm(points,axis=0)
    radiusMask[radiusMask>1] = 0
    numInSphere = np.count_nonzero(radiusMask)
    return 8.*numInSphere/N

def mc_error_plot(numIters=50):
    actual = 4.1887902047863905

    N = [i*1000 for i in xrange(1,51)]
    N = [50,100,500] + N
    errors = []

    for n in N:
        meanErr = 0.
        for i in xrange(numIters):
            I = prob1(n)
            err = np.abs(I - actual)/actual
            meanErr += err
        errors.append(meanErr/float(numIters))

    plt.plot(N,errors,label='Error')
    plt.plot(N,[1./n**0.5 for n in N],'r--',label=r'$1/\sqrt{N}$')
    plt.ylim([0,max(errors)])
    plt.xlim([0,max(N)])
    plt.xlabel(r'$N$')
    plt.ylabel('Relative error')
    plt.legend()

    plt.savefig("figures/MC_error_2.pdf")
    plt.clf()


if __name__ == "__main__":
    #mc_circle()
    mc_error_plot()
