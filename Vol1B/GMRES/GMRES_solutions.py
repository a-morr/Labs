import numpy as np
import math
from scipy import linalg as la

def gmres(A,b, k=100, tol=1e-8):
    """
    Calculate approximate solution of Ax = b using GMRES algorithm.
    Inputs:
        A -- callable function that calculates Ax for any input vector x.
        b -- numpy array of length m
        k -- Maximum number of iterations of the GMRES algorithm. Defaults to 100.
        tol -- Stop iterating if the residual is less than `tol'. Defaults to 1e-8.
    Returns:
        Return (y, res) where 'y' is an approximate solution to Ax=b and 'res'
    is the residual.
    """
    # initialization steps
    m = b.size
    Q = np.empty((m,k))
    H = np.zeros((k+1,k))
    bnorm = la.norm(b,2)
    rhs = np.zeros(k+1)
    rhs[0] = bnorm
    Q[:,0] = b/bnorm

    for j in xrange(k-1):
        # Arnoldi iteration
        q = A(Q[:,j])
        for i in xrange(j+1):
            H[i,j] = np.inner(Q[:,i],q)
            q -= H[i,j]*Q[:,i]
        H[j+1,j] = la.norm(q,2)
        if H[j+1,j] > 1e-10:
            # don't divide by zero!
            q /= H[j+1,j]
        Q[:,j+1] = q

        # solve the least squares problem
        y, r = la.lstsq(H[:j+2,:j+1], rhs[:j+2])[:2]

        # compute the residual.
        r = math.sqrt(r)/bnorm
        if r < tol:
            # if we are sufficiently close to solution, return
            return Q[:,:j+1].dot(y), r
    return Q[:,:j+1].dot(y.flatten()), r
