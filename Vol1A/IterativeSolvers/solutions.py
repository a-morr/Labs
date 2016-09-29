# solutions.py
"""Volume 1A: Iterative Solvers. Solutions File."""

import time
import numpy as np
from scipy import sparse
from scipy import linalg as la
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.sparse import linalg as spla


# Helper functions
def diag_dom(n, num_entries=None):
    """Generate a strictly diagonally dominant nxn matrix.

    Inputs:
        n (int): the dimension of the system.
        num_entries (int): the number of nonzero values. Defaults to n^(3/2)-n.

    Returns:
        A ((n,n) ndarray): An nxn strictly diagonally dominant matrix.
    """
    if num_entries is None:
        num_entries = int(n**1.5) - n
    A = np.zeros((n,n))
    rows = np.random.choice(np.arange(0,n), size=num_entries)
    cols = np.random.choice(np.arange(0,n), size=num_entries)
    data = np.random.randint(-4, 4, size=num_entries)
    for i in xrange(num_entries):
        A[rows[i], cols[i]] = data[i]
    for i in xrange(n):
        A[i,i] = np.sum(np.abs(A[i])) + 1
    return A


# Problems 1 and 2
def jacobi_method(A, b, tol=1e-8, maxiters=100, plot=False):
    """Calculate the solution to the system Ax = b voa the Jacobi Method.

    Inputs:
        A ((n,n) ndarray): A square matrix.
        b ((n,) ndarray): A vector of length n.
        tol (float, opt): the convergence tolerance.
        maxiters (int, opt): the maximum number of iterations to perform.
        plot (bool, opt): if True, plot the convergence rate of the algorithm.
            (this is for Problem 2).

    Returns:
        x ((n,) ndarray): the solution to system Ax = b.
    """
    m,n = A.shape
    d = np.diag(A)
    x0 = np.zeros(n)
    error = []

    for k in xrange(maxiters):
        x1 = x0 + (b - A.dot(x0))/d
        error.append(la.norm(A.dot(x1) - b, ord=np.inf))
        if la.norm(x0 - x1, ord=np.inf) < tol:
            break
        x0 = x1

    if plot:
        plt.semilogy(error, lw=2, label="Jacobi")
        plt.ylabel("Absolute Error of Approximation")
        plt.xlabel("Iteration #")
        plt.title("Convergence of Jacobi Method")
        plt.show()

    return x1


# Problem 3
def gauss_seidel(A, b, tol=1e-8, maxiters=100, plot=False):
    """Calculate the solution to the system Ax = b via the Gauss-Seidel Method.

    Inputs:
        A ((n,n) ndarray): A square matrix.
        b ((n,) ndarray): A vector of length n.
        tol (float, opt): the convergence tolerance.
        maxiters (int, opt): the maximum number of iterations to perform.
        plot (bool, opt): if True, plot the convergence rate of the algorithm.

    Returns:
        x ((n,) ndarray): the solution to system Ax = b.
    """
    m,n = A.shape
    x0 = np.zeros(n)
    error = []

    for k in xrange(maxiters):
        x1 = x0.copy()
        for i in xrange(n):
            a_ii = A[i,i]
            x1[i] = x1[i] + (b[i] - np.dot(A[i], x1))/float(a_ii)
        error.append(la.norm(A.dot(x1) - b, ord=np.inf))
        if la.norm(x0-x1, ord=np.inf) < tol:
            break
        x0 = x1

    if plot:
        plt.semilogy(error, lw=2, label="Gauss-Seidel")
        plt.ylabel("Absolute Error of Approximation")
        plt.xlabel("Iteration")
        plt.title("Convergence of Gauss-Seidel Method")
        plt.show()

    return x1


# Problem 4
def prob4():
    """For a 5000 parameter system, compare the runtimes of the Gauss-Seidel
    method and la.solve(). Print an explanation of why Gauss-Seidel is so much
    faster.
    """
    gs_times, solve_times = [], []
    domain = 2**np.arange(5,12)

    for n in domain:
        A = diag_dom(n)
        b = np.random.rand(n)

        start = time.time()
        gauss_seidel(A,b)
        gs_times.append(time.time() - start)

        start = time.time()
        la.solve(A,b)
        solve_times.append(time.time() - start)

    plt.loglog(domain, gs_times, '.-', basex=2, basey=2, lw=2, ms=10,
                                                        label="Gauss-Seidel")
    plt.loglog(domain, solve_times, '.-', basex=2, basey=2, lw=2, ms=10,
                                                        label="la.solve()")
    plt.xlabel("System Size")
    plt.ylabel("Time (seconds)")
    plt.legend(loc="upper left")
    plt.show()


# Problem 5
def sparse_gauss_seidel(A, b, tol=1e-8, maxiters=100):
    """Calculate the solution to the sparse system Ax = b via the Gauss-Seidel
    Method.

    Inputs:
        A ((n,n) csr_matrix): An nxn sparse CSR matrix.
        b ((n,) ndarray): A vector of length n.
        tol (float, opt): the convergence tolerance.
        maxiters (int, opt): the maximum number of iterations to perform.

    Returns:
        x ((n,) ndarray): the solution to system Ax = b.
    """
    if type(A) != sparse.csr_matrix:
        A = sparse.csr_matrix(A)
    m,n = A.shape
    x0 = np.zeros(n)
    error = []
    diag = A.diagonal()

    for k in xrange(maxiters):
        x1 = x0.copy()
        for i in xrange(n):
            # <A_i, x> as given in the problem.
            rowstart = A.indptr[i]
            rowend = A.indptr[i+1]
            Aix = np.dot(A.data[rowstart:rowend],
                        x1[A.indices[rowstart:rowend]])
            x1[i] += (b[i] - Aix)/float(diag[i])
        if la.norm(x0-x1, ord=np.inf) < tol:
            return x1
        x0 = x1

    return x1


# Problem 6
def sparse_sor(A, b, omega, tol=1e-8, maxiters=100):
    """Calculate the solution to the system Ax = b via Successive Over-
    Relaxation.

    Inputs:
        A ((n,n) csr_matrix): An nxn sparse matrix.
        b ((n,) ndarray): A vector of length n.
        omega (float in [0,1]): The relaxation factor.
        tol (float, opt): the convergence tolerance.
        maxiters (int, opt): the maximum number of iterations to perform.

    Returns:
        x ((n,) ndarray): the solution to system Ax = b.
    """
    if type(A) != sparse.csr_matrix:
        A = sparse.csr_matrix(A)
    m,n = A.shape
    x0 = np.zeros(n)
    error = []
    diag = A.diagonal()

    for k in xrange(maxiters):
        x1 = x0.copy()
        for i in xrange(n):
            # <A_i, x> as given in the problem.
            rowstart = A.indptr[i]
            rowend = A.indptr[i+1]
            Aix = np.dot(A.data[rowstart:rowend],
                        x1[A.indices[rowstart:rowend]])
            x1[i] += omega*(b[i] - Aix)/float(diag[i])  # This line changed.
        if la.norm(x0-x1, ord=np.inf) < tol:
            return x1
        x0 = x1

    return x1

# Problem 7
def finite_difference(n):
    """Return the A and b described in the finite difference problem that
    solves Laplace's equation.
    """

    data = [[-4]*n, [1]*n, [1]*n]
    diags = [0,1,-1]
    subA = sparse.spdiags(data, diags, n, n)
    A = sparse.block_diag((subA,)*n)
    A.setdiag(1, n)
    A.setdiag(1,-n)

    # CHECK THIS IS RIGHT
    b = np.zeros(n**2)
    left_bound = np.arange(0,n**2, n)
    right_bound = np.arange(n-1, n**2, n)

    b[left_bound] = -100
    b[right_bound] = -100

    return A.tocsr(), b

# Problem 8
def compare_omega():
    """Time sparse_sor() with omega = 1, 1.05, 1.1, ..., 1.9, 1.95, tol=1e-2,
    and maxiters = 1000 using the A and b generated by finite_difference()
    with n = 20. Plot the times as a function of omega.
    """
    # Find an approximation for the optimal omega
    n = 10
    A,b = finite_difference(n)
    timings = []
    domain = np.arange(1,2,.05)
    for o in domain:
        before = time.time()
        sparse_sor(A, b, o, tol=1e-2, maxiters=1000)
        after = time.time()
        timings.append(after - before)
    plt.plot(domain, timings, lw=2)
    plt.show()

# Problem 9
def hot_plate(n):
    """Use finite_difference() to generate the system Au = b, then solve the
    system using SciPy's sparse system solver, scipy.sparse.linalg.spsolve().
    Visualize the solution using a heatmap using np.meshgrid() and
    plt.pcolormesh() ("seismic" is a good color map in this case).
    """
    A,b = finite_difference(n)
    U = spla.spsolve(A,b).reshape((n,n))

    x,y = np.linspace(0,10,n), np.linspace(0,10,n)
    X,Y = np.meshgrid(x, y)
    plt.pcolormesh(X, Y, U, cmap='seismic')
    plt.colorbar()
    plt.show()

# Testing solutions file ======================================================
def test_jacobi():
    results = []
    for n in [5, 10, 50, 100]:
        A = diag_dom(n)
        b = np.random.rand(n)
        jacobi_sol = jacobi_method(A,b)
        sol = la.solve(A,b)
        results.append(np.allclose(jacobi_sol, sol))
    return np.alltrue(results)

def test_plot_convergence():
    A = np.array([[2,0,-1],[-1,3,2],[0,1,3]])
    b = np.array([3,3,-1])
    jacobi_method(A,b,plot=True)
    gauss_seidel(A,b,plot=True)
    plt.show()
    return True

def test_gauss_seidel():
    results = []
    for n in [5, 10, 50, 100]:
        A = diag_dom(n)
        b = np.random.rand(n)
        gs_sol = gauss_seidel(A,b)
        sol = la.solve(A,b)
        results.append(np.allclose(gs_sol, sol))
    return np.alltrue(results)

def test_compare_times():
    prob4()
    return True

def test_sparse_gauss_seidel():
    results = []
    for n in [5, 10, 50, 100]:
        A = diag_dom(n)
        b = np.random.rand(n)
        sgs_sol = sparse_gauss_seidel(A,b)
        sol = la.solve(A,b)
        results.append(np.allclose(sgs_sol, sol))
    return np.alltrue(results)

def test_sparse_sor():
    results = []
    for n in [5, 10, 50, 100]:
        A = diag_dom(n)
        b = np.random.rand(n)
        sor_sol = sparse_sor(A,b,0.8,maxiters=300)
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

    compare_omega()
    hot_plate(150)
    print "Passed All Tests!"
    return True

if __name__ == "__main__":
    test_all()
