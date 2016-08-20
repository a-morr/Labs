#solutions.py
"""
Vol I Lab __: GMRES
January 8, 2016
"""
import numpy as np
import numpy.linalg as la
from matplotlib import pyplot as plt
import time

#Problem 1: Implement the following function
def gmres(A, b, x0, k=100, tol=1e-8):
    '''Calculate approximate solution of Ax=b using GMRES algorithm.
    
    INPUTS:
    A    - Callable function that calculates Ax for any input vector x.
    b    - A NumPy array of length m.
    x0   - An arbitrary initial guess.
    k    - Maximum number of iterations of the GMRES algorithm. Defaults to 100.
    tol  - Stop iterating if the residual is less than 'tol'. Defaults to 1e-8.
    
    RETURN:
    Return (y, res) where 'y' is an approximate solution to Ax=b and 'res' 
    is the residual.
    '''
    #initialize stuff
    Q = np.empty((b.size, k + 1))
    H = np.zeros((k + 1, k))
    r0 = b - A(x0)
    beta = la.norm(r0, 2)
    be1 = np.zeros(k + 1)
    be1[0] = beta
    
    Q[:,0] = r0/beta
    
    # arnoldi iteration
    for j in xrange(k):
        Q[:,j+1] = A(Q[:,j])
        for i in xrange(j+1):
            H[i,j] = np.inner(Q[:,i],Q[:,j+1])
            Q[:,j+1] -= H[i,j] * Q[:,i]
        H[j+1,j] = la.norm(Q[:,j+1],2)
        if H[j+1,j] > tol:  # Don't divide by 0
            Q[:,j+1] /= H[j+1,j]
            
        # least squares bit       
        y, r = la.lstsq(H[:j+2,:j+1], be1[:j+2])[:2]
        
        #residual is root of what lstsq returns
        res = np.sqrt(r[0])
        
        if res < tol:
            return Q[:,:j+1].dot(y) + x0, res
            
    return Q[:,:j+1].dot(y) + x0, res
    
    
#Problem 2: Implement the following two functions
def plot_gmres(A, b, x0, tol=1e-8):
    '''Use the GMRES algorithm to approximate the solution to Ax=b.  Plot the
    eigenvalues of A and the convergence of the algorithm.
    
    INPUTS:
    A   - A 2-D NumPy array of shape mxm.
    b   - A 1-D NumPy array of length m.
    x0  - An arbitrary initial guess.
    tol - Stop iterating and create the desired plots when the residual is
          less than 'tol'. Defaults to 1e-8.
    
    OUTPUT:
    Follow the GMRES algorithm until the residual is less than tol, for a 
    maximum of m iterations. Then create the two following plots (subplots
    of a single figure):
     
    1. Plot the eigenvalues of A in the complex plane.
    
    2. Plot the convergence of the GMRES algorithm by plotting the
    iteration number on the x-axis and the residual on the y-axis.
    Use a log scale on the y-axis.
    '''
    k = b.size
    Q = np.empty((k, k + 1))
    H = np.zeros((k+1, k))
    
    Amul = lambda x: np.dot(A, x)
    r0 = b - Amul(x0)
    beta = la.norm(r0, 2)
    Q[:,0] = r0 / beta
    be1 = np.zeros(k+1)
    be1[0] = beta
    
    residuals = []
    
    # arnoldi iteration
    for j in xrange(k-1):
        Q[:,j+1] = Amul(Q[:,j])
        for i in xrange(j+1):
            H[i,j] = np.inner(Q[:,i],Q[:,j+1])
            Q[:,j+1] -= H[i,j] * Q[:,i]
        H[j+1,j] = la.norm(Q[:,j+1],2)
        if H[j+1,j] > tol:  # Don't divide by 0
            Q[:,j+1] /= H[j+1,j]

        # least squares bit       
        y, r = la.lstsq(H[:j+2,:j+1], be1[:j+2])[:2]
        
        #compute residual and add to list
        res = np.sqrt(r[0])
        residuals.append(res)
        
        if res < tol or H[j+1,j] < tol:
            break
    
    eigs = la.eig(A)[0]
    l = len(residuals)
    x = np.linspace(0, l-1, l)
    
    plt.subplot(1,2,1)
    plt.scatter(np.real(eigs),np.imag(eigs))
    
    plt.subplot(1,2,2)
    plt.yscale('log')
    plt.plot(x,residuals)
    
    plt.show()

    
def make_plots(m=200):
    '''Create the matrix An defined in problem 2 in the manual 
    for n = -4, -2, -0, 2, 4.  Call plot_gmres on each, with b 
    a vector of ones, and an initial guess x0 a vector of zeros.
    Print a statement explaining how the convergence relates to 
    the eigenvalues.
    '''
    for n in (-4, -2, 0, 2, 4):
        P = np.random.normal(0, .5/np.sqrt(m), (m,m))
        An = n*np.eye(m) + P
        b = np.ones(m)
        x0 = 0 * b
        plot_gmres(An, b, x0)
    
    print "The algorithm converges more slowly when the eigenvalues are clustered around the origin."
    
    
#Problem 3: Implement the following two functions
def gmres_k(Amul, b, x0, k=5, tol=1E-8, restarts=50):
    '''Use the GMRES(k) algorithm to approximate the solution to Ax=b.
    
    INPUTS:
    A   - A Callable function that calculates Ax for any vector x.
    b   - A NumPy array.
    x0  - An arbitrary initial guess.
    k   - Maximum number of iterations of the GMRES algorithm before
        restarting. Defaults to 5.
    tol - Stop iterating if the residual is less than 'tol'. Defaults
        to 1E-8.
    restarts - Maximum number of restarts. Defaults to 50.
    
    OUTPUT:
    Return (y, res) where 'y' is an approximate solution to Ax=b and 'res'
    is the residual.
    '''
    r = 0
    
    while r <= restarts:
        # Perform GMRES
        y, res = gmres(Amul, b, x0, k, tol)
        if res < tol:
            return y, res
        else:
            # Update guess
            x0 = y
            r += 1
            
    return y, res
    
    
def time_gmres(m=200):
    '''Time the gmres and gmres_k functions on each of the matrices
    from problem 2.  Let x0 be a vector of zeros or anything you like.
    The results might be more dramatic with an x0 of larger magnitude.
    Print your results.  What do you observe?
    '''
    for n in (-4, -2, 0, 2, 4):
        P = np.random.normal(0, .5/np.sqrt(m), (m,m))
        An = n*np.eye(m) + P
        b = np.ones(m)
        Amul = lambda x: np.dot(An, x)
        x0 = 0 * b
        
        t1 = time.clock()
        y1, res = gmres(Amul, b, x0)
        t2 = time.clock()

        y2, res = gmres_k(Amul, b, x0)
        t3 = time.clock()
        
        print "n =",
        print n,
        print ":"
        
        print "GMRES:   ",
        print t2 - t1
        
        print "GMRES(k):",
        print t3 - t2
        print
    