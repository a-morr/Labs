import pysg
import numpy as np
from matplotlib import pyplot as plt

def plotGrid(dim,level):
    sg = pysg.sparseGrid(dim=dim,level=level)
    sg.generatePoints()
    points = sg.indices
    pts = len(points)
    xpts = np.empty(pts)
    if dim==1:
        for i in xrange(pts):
            pt = tuple(points[i])
            xpts[i] = sg.gP[pt].pointPosition(pt)[0]
        plt.plot(xpts,np.ones_like(xpts),'*')
    elif dim==2:
        ypts = np.empty(pts)
        for i in xrange(pts):
            pt = tuple(points[i])
            xpts[i], ypts[i] = sg.gP[pt].pointPosition(pt)
        plt.plot(xpts,ypts,'*')
    else:
        if dim > 3:
            print "Showing first three dimensions only"
        from mpl_toolkits.mplot3d import Axes3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ypts = np.empty(pts)
        zpts = np.empty(pts)
        for i in xrange(pts):
            pt = tuple(points[i])
            xpts[i], ypts[i], zpts[i] = sg.gP[pt].pointPosition(pt)[:3]
        ax.scatter(xpts, ypts, zpts)    
    #plt.show()

def n_vol(length,dim,level):
    return length**dim/(2**(dim*(level-1))*(dim+1))

def example():
    # There is an error here. the coefficient for loc [0.25,0.5] should be 0.
    def f(x):
        return x[0]
    dim = 2
    level = 3
    sg = pysg.sparseGrid(dim=dim,level=level)
    sg.setFunctionValues(f)
    sg.nodal2Hier()
    sg.setCoefficients()
    total = 0
    for i in xrange(len(sg.indices)):
        total += sg.gP[tuple(sg.indices[i])].coeff
    total /= 2**((level-1)*dim)*(dim+1)
    print total
