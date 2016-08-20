import numpy as np
from scipy import linalg as la
from matplotlib import pyplot as plt
from scipy import sparse #Used to create test cases

def ps_grid(eig_vals, grid_dim):
    """ 
    Computes the grid on which to plot the pseudospectrum
    of a matrix. This is a helper function for plot_ps(),
    and does not need to be called directly.
    """
    x0, x1 = min(eig_vals.real), max(eig_vals.real)
    y0, y1 = min(eig_vals.imag), max(eig_vals.imag)
    xmid = (x0 + x1) /2.
    xlen1 = x1 - x0 +.01
    ymid = (y0 + y1) / 2.
    ylen1 = y1 - y0 + .01
    xlen = max(xlen1, ylen1/2.)
    ylen = max(xlen1/2., ylen1)
    x0 = xmid - xlen
    x1 = xmid + xlen
    y0 = ymid - ylen
    y1 = ymid + ylen
    x = np.linspace(x0, x1, grid_dim)
    y = np.linspace(y0, y1, grid_dim)
    return x,y

def plot_ps(A, m=150, epsilon_vals=None, plot_eig_vals=True, labels=False):
    """
    Plots the pseudospectrum of the matrix A on an
    mxm grid of points
    
    Parameters
    ----------
    A : square, 2D ndarray
        The matrix whose pseudospectrum is to be plotted
    m : int
        The dimension of the square grid used for plotting
        Defaults to 150
    epsilon_vals : list of floats
        If k is in epsilon_vals, then the epsilon-pseudospectrum
        is plotted for epsilon=10**-k
        If epsilon_vals=None, the defaults of plt.contour are used
        instead of any specified values.
    plot_eig_vals : bool
        If True, the eigenvalues of A will be plotted along
        with the pseudospectum of A
        Defaults to True
    labels : bool
        If True, the contours will be labelled with k,
        where epsilon = 10**-k
        Defaults to False
    
    """
    T = la.schur(A, 'complex')
    eigs_A = T[0].diagonal()
    N = A.shape[0]
    maxit = N-1
    x_vals,y_vals = ps_grid(eigs_A, m)
    sigmin = np.zeros((m,m))
    for k in xrange(m):
        for i in xrange(m):
            T1 = (x_vals[k]+y_vals[i]*1.j)*np.identity(N)-T[0]
            T2 = (T1.T).conj()
            sigold = 0
            qold = np.zeros((N,1))
            beta = 0
            H = np.zeros_like(A)
            q = np.random.randn(N,1)+1.j*np.random.randn(N,1)
            q = q/la.norm(q)
            for p in xrange(maxit):
                v = la.solve_triangular(T1,(la.solve_triangular(T2,q,lower=True)))-beta*qold
                alpha = np.dot((q.T).conj(),v)[0].real
                v = v - alpha*q
                beta = la.norm(v)
                qold = q
                q = v/beta
                H[p+1,p] = beta
                H[p, p+1] = beta
                H[p,p] = alpha
                eigs_H = la.eigvalsh(H[:p+1,:p+1])
                sig = np.amax(np.absolute(eigs_H))
                if np.absolute(sigold/sig-1) < 0.001:
                    break
                sigold = sig
            sigmin[i,k] = np.sqrt(sig)
    fig = plt.figure()
    if plot_eig_vals:
        eigs_real = eigs_A.real
        eigs_imag = eigs_A.imag
        plt.scatter(eigs_real,eigs_imag) 
    CS = plt.contour(x_vals,y_vals,np.log10(sigmin), levels=epsilon_vals)
    if labels:
        plt.clabel(CS)
    #plt.show()
    return fig

def ps_test_1():
    """
    This test case should result in an image similar to the
    image on the top of page 23 of 'Spectra and Pseudospectra'
    by Trefethen and Embree.
    """
    a = [.25]*63; b = [0]*64; c = [1]*63; diags = np.array([a,b,c])
    d = sparse.diags(diags, [-1, 0, 1])
    A  = np.array(d.todense())
    l = range(2,9)
    test_fig = plot_ps(A,epsilon_vals=l)
    plt.title("Pseudospectrum of a Matrix")
    plt.show()

def ps_test_2():
    """
    This test case should match the top left image on page 57
    of the same book.
    """
    a = [-2.j]*147; b = [-4.]*148; c = [2.j]*149; d = [-1]*148; e = [2]*147
    mat = sparse.diags([a,b,c,d,e],[-3,-2,1,2,3])
    A = np.array(mat.todense())
    l = range(2,11)
    test_fig = plot_ps(A,epsilon_vals=l)
    plt.title("Pseudospectrum of a Matrix")
    plt.show()

def ps_test_3():
    """
    This test is of an upper triangular matrix and is given
    to demonstrate the usage of some of the function parameters.
    """
    A = np.array([[-1.,3.,5.j],[0,2.-4.j, 8],[0,0,-1.+1j]])
    test_fig = plot_ps(A, plot_eig_vals=False,labels=True)
    plt.title("Psuedospectrum of a 3x3 Matrix")
    plt.show()


def ps_scatter_plot(A, epsilon=.001, num_pts=100, plot_spec=False):
    """
    Plots the 'poorman's pseudospectrum' of a matrix A
    
    Parameters
    ----------
    A : square, 2D ndarray
        the matrix whose pseudospectrum is to be plotted
    epsilon : float
        This float determines which epsilon-pseudospectrum
        will be plotted
    num_pts : int
        The number of matrices, E, that will be used in the
        algorithm
    plot_spec : bool
        if True, the eigenvalues of A will also be plotted
        Defaults to False
    
    Returns
    -------
    fig : matplotlib figure
        A scatter plot representing the pseudospectrum of A
        
    """
    n = A.shape[0]
    spec_A = la.eigvals(A)
    x_spec = spec_A.real
    y_spec = spec_A.imag
    x_coords = np.empty(shape=(0,))
    y_coords = np.empty(shape=(0,))
    fig = plt.figure()
    for i in xrange(num_pts):
        shifted_A = A + gen_rand_matrix(n,epsilon)
        eig_vals = la.eigvals(shifted_A)
        eig_real = eig_vals.real
        eig_imag = eig_vals.imag
        x_coords = np.hstack((x_coords, eig_real))
        y_coords = np.hstack((y_coords, eig_imag))
    plt.scatter(x_coords, y_coords,marker=".")
    x, y = ps_grid(spec_A,100)
    if plot_spec:c
        plt.scatter(x_spec,y_spec, marker="o",color='r')
    plt.axis([x[0],x[-1],y[0],y[-1]])
    return fig
    
def gen_rand_matrix(n, epsilon):
    """
    This is a helper function for ps_scatter_plot().
    It should not be called directly.
    """
    real_B = np.random.uniform(low=-1.0, high=1.0, size=(n,n))
    imag_B = np.random.uniform(low=-1.0, high=1.0, size=(n,n))
    B = real_B + imag_B*1.j
    scale = epsilon/la.norm(B,2)
    B = B*scale
    return B


    
