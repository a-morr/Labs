#This solutions file is incomplete.
import numpy as np
from scipy import linalg as la
from scipy import sparse as sp
from matplotlib import pyplot as plt

def ps_scatter_plot(A, epsilon=.001, num_pts=20):
    n = A.shape[0]
    eigs = np.empty((num_pts+1,n),dtype=complex)
    for i in xrange(1,num_pts+1):
        E = np.random.random((n,n))
        E *= epsilon/la.norm(E)
        es = la.eigvals(A+E)
        eigs[i,:] = es
        plt.plot(np.real(eigs[i]),np.imag(eigs[i]),'b*')
    eigs[0] = la.eigvals(A.todense())
    plt.plot(np.real(eigs[0]),np.imag(eigs[0]),'r*')
    plt.show()
    return eigs
        
def problem1(n=120,epsilon=.001,num_pts=20):
    A = sp.diags([np.ones(n-1)*1j,np.ones(n-1)*-1j,-np.ones(n-2),np.ones(n-2)],[1,-1,2,-2])
    ps_scatter_plot(A,epsilon,num_pts)

def problem3(n=120,epsilon=.001,num_pts=20):
    AH = sp.diags([np.ones(n-1)*1j,np.ones(n-1)*-1j,-np.ones(n-2),-np.ones(n-2)],[1,-1,2,-2])
    ps_scatter_plot(AH,epsilon,num_pts)
    
    AN = sp.diags([np.ones(n-1)*1j,-np.ones(n-2),(np.random.rand(n)+np.random.rand(n)*1j)],[1,2,0])
    ps_scatter_plot(AN,epsilon,num_pts)

problem3(n=5,epsilon=.001,num_pts=200)