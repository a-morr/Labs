# solutions.py
"""Volume 1A: Iterative Solvers. Solutions File."""
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg as la
import scipy.sparse as spar
import scipy.sparse.linalg as sparla
from mpl_toolkits.mplot3d import Axes3D
import time

# Helper functions
def diag_dom(n, num_entries=None):
    """Generate a strictly diagonally dominant nxn matrix.

    Inputs:
        n (int) - dimension.
        vals (list) - range of values for off-diagonal entries.
        num_entries (int) - number of nonzero values. If None, num_entries
                    defaults to n^(1.5) - n.

    Returns:
        A (array) - nxn strictly diagonally dominant matrix.
    """
    if num_entries is None:
        num_entries = int(n**1.5) - n
    A = np.zeros((n,n))
    rows = np.random.choice(np.arange(0,n), size=num_entries)
    cols = np.random.choice(np.arange(0,n), size=num_entries)
    data = np.random.randint(-4,4,size=num_entries)
    for i in xrange(num_entries):
        A[ rows[i], cols[i] ] = data[i]
    for i in xrange(n):
        A[i,i] = np.sum(np.abs(A[i,:])) + 1
    return A

def spar_diag_dom(n, num_entries=None):
    """Generate a strictly diagonally dominant sparse nxn matrix.

    Inputs:
        n (int) - dimension
        num_entries (int) - number of nonzero values. If None, num_entries
                    defaults to n^(1.5) - n.

    Returns:
        A (spar.csr_matrix) - strictly diagonally dominantn sparse nxn matrix.
    """
    return spar.csr_matrix(diag_dom(n, num_entries=numm_entries))

# Problem 1
def jacobi_method(A,b,maxiters=100,tol=1e-8):
    """Returns the solution to the system Ax = b using the Jacobi Method.

    Inputs:
        A (array) - 2D NumPy array
        b (array) - 1D NumPy array
        maxiters (int, optional) - maximum iterations for algorithm to perform.
        tol (float) - tolerance for convergence
    Returns:
        x (array) - solution to system Ax = b.
        x_approx (list) - list of approximations at each iteration.
    """
    n = A.shape[0]
    x0 = np.zeros(n)
    x = np.zeros(n)
    diag = np.diag(A)
    x_approx = []
    for k in xrange(maxiters):
        x = (b + diag*x - A.dot(x0))/diag
        if np.max(np.abs(x0-x)) < tol:
            return x, x_approx
        x0 = x
        x_approx.append(x)
    print "Maxiters hit!"
    return x, x_approx

# Problem 2
def plot_convergence(A, b, maxiters=100, tol=1e-8):
    """Plot the rate of convergence for solving the system Ax = b.

    Inputs:
        A (array) - 2D NumPy array
        b (array) - 1D NumPy array
        maxiters (int, optional) - maximum iterations for algorithm to perform.
        tol (float) - tolerance for convergence
    """
    x, x_approx = jacobi_method(A,b,maxiters,tol)

    x_approx = np.array(x_approx)
    dom = np.arange(x_approx.shape[0])
    norms = []
    for i in xrange(x_approx.shape[0]):
        norms.append(la.norm(A.dot(x_approx[i]) - b))

    plt.semilogy(dom, norms)
    plt.ylabel("Absolute Error of Approximation")
    plt.xlabel("Iteration #")
    plt.title("Convergence of Jacobi Method")
    plt.show()

# Problem 3
def gauss_seidel(A,b,maxiters=100,tol=1e-8):
    """Returns the solution to the system Ax = b using the Gauss-Seidel Method.

    Inputs:
        A (array) - 2D NumPy array
        b (array) - 1D NumPy array
        maxiters (int, optional) - maximum iterations for algorithm to perform.
        tol (float) - tolerance for convergence
    Returns:
        x (array) - solution to system Ax = b.
        x_approx (list) - list of approximations at each iteration.
    """
    n = A.shape[0]
    x0 = np.zeros(n)
    x = np.zeros(n)
    k = 0
    x_approx = []
    for k in xrange(maxiters):
        k += 1
        x = x0.copy()
        for i in xrange(n):
            a_ii = A[i,i]
            x[i] = b[i]/a_ii + x[i] - np.dot(A[i],x)/a_ii
        if np.max(np.abs(x0-x)) < tol:
            return x, x_approx
        x0 = x
        x_approx.append(x)
    print "Maxiters hit!"
    return x, x_approx

# Problem 4
def compare_times():
    """For a 5000 parameter system, compare the runtimes of the Gauss-Seidel
    method and la.solve. Print an explanation of why Gauss-Seidel is so much
    faster.
    """
    A = diag_dom(5000)
    b = np.random.rand(5000)
    before = time.time()
    gauss_seidel(A,b)
    after = time.time()
    gauss_seidel_time = after - before

    before = time.time()
    la.solve(A,b)
    after = time.time()
    la_solve_time = after - before

    print "Gauss-Seidel: " + str(gauss_seidel_time)
    print "la.solve: " + str(la_solve_time)

# Problem 5
def sparse_gauss_seidel(A,b,maxiters=100,tol=1e-8):
    """Returns the solution to the system Ax = b using the Gauss-Seidel method.

    Inputs:
        A (array) - 2D scipy.sparse matrix
        b (array) - 1D NumPy array
        maxiters (int, optional) - maximum iterations for algorithm to perform.
        tol (float) - tolerance for convergence
    Returns:
        x (array) - solution to system Ax = b.
        x_approx (list) - list of approximations at each iteration.
    """

    if type(A) != spar.csr_matrix:
        A = spar.csr_matrix(A)
    n = A.shape[0]
    x0 = np.zeros(n)
    x = np.ones(n)
    x_approx = []
    for k in xrange(maxiters):
        x = x0.copy()
        diag = A.diagonal()
        for i in xrange(n):
            rowstart = A.indptr[i]
            rowend = A.indptr[i+1]
            Aix = np.dot(A.data[rowstart:rowend],
                        x[A.indices[rowstart:rowend]])
            x[i] += (b[i] - Aix)/diag[i]
        if np.max(np.abs(x0-x)) < tol:
            return x, x_approx
        x0 = x
        x_approx.append(x)
    print "Maxiters hit!"
    return x, x_approx

# Problem 6
def sparse_sor(A,b,omega,maxiters=100, tol=1e-8):
    """Returns the solution to the system Ax = b using Successive Over-Relaxation.

    Inputs:
        A (array) - 2D scipy.sparse matrix
        b (array) - 1D NumPy array
        maxiters (int, optional) - maximum iterations for algorithm to perform.
        tol (float) - tolerance for convergence
    Returns:
        x (array) - solution to system Ax = b.
        x_approx (list) - list of approximations at each iteration.

    """
    if type(A) != spar.csr_matrix:
        A = spar.csr_matrix(A)
    n = A.shape[0]
    x0 = np.zeros(n)
    x = np.ones(n)
    x_approx = []
    for k in xrange(maxiters):
        x = x0.copy()
        diag = A.diagonal()
        for i in xrange(n):
            rowstart = A.indptr[i]
            rowend = A.indptr[i+1]
            Aix = np.dot(A.data[rowstart:rowend],
                        x[A.indices[rowstart:rowend]])
            x[i] += omega*(b[i] - Aix)/diag[i]
        if np.max(np.abs(x0-x)) < tol:
            return x, x_approx
        x0 = x
        x_approx.append(x)
    print "Maxiters hit!"
    return x, x_approx

# Problem 6
def finite_difference(n):
    data = [[-4]*n, [1]*n, [1]*n]
    diags = [0,1,-1]
    subA = spar.spdiags(data, diags, n, n)
    A = spar.block_diag((subA,)*n)
    A.setdiag(1, n)
    A.setdiag(1,-n)

    # the vector b is still royally screwed up
    b = np.zeros(n**2)
    left_bound = np.arange(0,n**2, n)
    right_bound = np.arange(n-1, n**2, n)

    b[left_bound] = -100
    b[right_bound] = -100

    return A, b

def compare_omega():
    # Find an approximation for the optimal omega
    n = 20
    A,b = finite_difference(n)
    timings = []
    for o in np.arange(1,2,.05):
        before = time.time()
        x = sparse_sor(A,b,o,maxiters=10000,tol=10**-2)[0]
        after = time.time()
        timings.append(after - before)
    plt.plot(np.arange(1,2,.05), timings)
    plt.show()

# Testing solutions file.
def test_jacobi():
    results = []
    for n in [5, 10, 50, 100]:
        A = diag_dom(n)
        b = np.random.rand(n)
        jacobi_sol, jacobi_approx = jacobi_method(A,b)
        sol = la.solve(A,b)
        results.append(np.allclose(jacobi_sol, sol))
    return np.alltrue(results)

def test_plot_convergence():
    A = np.array([[2,0,-1],[-1,3,2],[0,1,3]])
    b = np.array([3,3,-1])
    plot_convergence(A,b)
    return True

def test_gauss_seidel():
    results = []
    for n in [5, 10, 50, 100]:
        A = diag_dom(n)
        b = np.random.rand(n)
        gs_sol, gs_approx = gauss_seidel(A,b)
        sol = la.solve(A,b)
        results.append(np.allclose(gs_sol, sol))
    return np.alltrue(results)

def test_compare_times():
    compare_times()
    return True

def test_sparse_gauss_seidel():
    results = []
    for n in [5, 10, 50, 100]:
        A = diag_dom(n)
        b = np.random.rand(n)
        sgs_sol, sgs_approx = sparse_gauss_seidel(A,b)
        sol = la.solve(A,b)
        results.append(np.allclose(sgs_sol, sol))
    return np.alltrue(results)

def test_sparse_sor():
    results = []
    for n in [5, 10, 50, 100]:
        A = diag_dom(n)
        b = np.random.rand(n)
        sor_sol, sor_approx = sparse_sor(A,b,0.8,maxiters=300)
        sol = la.solve(A,b)
        results.append(np.allclose(sor_sol, sol))
    return np.alltrue(results)

def test_all():
    if not test_jacobi():
        print "Failed Jacobi"
        return False
    test_plot_convergence()
    if not test_gauss_seidel():
        print "Failed Gauss-Seidel"
        return False

    test_compare_times()
    if not test_sparse_gauss_seidel():
        print "Failed Sparse Gauss-Seidel"
        return False

    if not test_sparse_sor():
        print "Failed SOR"
        return False

    print "Passed All Tests!"
    return True

if __name__ == "__main__":
    test_all()
