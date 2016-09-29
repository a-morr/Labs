# solutions.py
"""Volume 1A: Linear Systems. Solutions file."""

import numpy as np
from time import time
from scipy import sparse
from scipy import linalg as la
from scipy.sparse import linalg as spla
from matplotlib import pyplot as plt


# Problem 1
def ref(A):
    """Reduce the square matrix A to REF. You may assume that A is invertible
    and that a 0 will never appear on the main diagonal. Avoid operating on
    entries that you know will be 0 before and after a row operation.
    """
    A = np.array(A, dtype=np.float, copy=True)
    m,n = A.shape
    for j in xrange(n):
        for i in xrange(j+1, m):
            A[i,j:] -= A[j,j:] * A[i,j] / A[j,j]
    return A


# Problem 2
def lu(A):
    """Compute the LU decomposition of the square matrix A. You may assume the
    decomposition exists and requires no row swaps.

    Returns:
        L ((n,n) ndarray): The lower-triangular part of the decomposition.
        U ((n,n) ndarray): The upper-triangular part of the decomposition.
    """
    m, n = A.shape
    U = np.array(A, dtype=np.float, copy=True)
    L = np.eye(n)
    for j in xrange(n):
        for i in xrange(j+1, m):
            L[i,j] = U[i,j]/U[j,j]
            U[i,j:] -= L[i,j]*U[j,j:]
    return L,U


# Problem 3
def solve(A, b):
    """Use the LU decomposition and back substitution to solve the linear
    system Ax = b. You may assume that A is invertible (hence square).
    """
    m, n = A.shape
    L, U = lu(A)

    # First solve Ly = Pb (assume P = I).
    y = np.zeros(n)
    for k in xrange(n):
        y[k] = b[k] - np.dot(L[k,:k], y[:k])

    # Now solve Ux = y.
    x = np.zeros(n)
    for k in reversed(xrange(n)):
        x[k] = (y[k] - np.dot(U[k,k:], x[k:])) / U[k,k]

    return x


# Problem 4
def prob4(N=11):
    """Time different scipy.linalg functions for solving square linear systems.
    Plot the system size versus the execution times. Use log scales if needed.
    """
    domain = 2**np.arange(1,N+1)
    inv, solve, lu_factor, lu_solve = [], [], [], []

    for n in domain:
        A = np.random.random((n,n))
        b = np.random.random(n)

        start = time()
        la.inv(A).dot(b)
        inv.append(time()-start)

        start = time()
        la.solve(A, b)
        solve.append(time()-start)

        start = time()
        x = la.lu_factor(A)
        la.lu_solve(x, b)
        lu_factor.append(time()-start)

        start = time()
        la.lu_solve(x, b)
        lu_solve.append(time()-start)

    plt.subplot(121)
    plt.plot(domain, inv, '.-', lw=2, label="la.inv()")
    plt.plot(domain, solve, '.-', lw=2, label="la.solve()")
    plt.plot(domain, lu_factor, '.-', lw=2,
                                    label="la.lu_factor() and la.lu_solve()")
    plt.plot(domain, lu_solve, '.-', lw=2, label="la.lu_solve() alone")
    plt.xlabel("n"); plt.ylabel("Seconds")
    plt.legend(loc="upper left")

    plt.subplot(122)
    plt.loglog(domain, inv, '.-', basex=2, basey=2, lw=2)
    plt.loglog(domain, solve, '.-', basex=2, basey=2, lw=2)
    plt.loglog(domain, lu_factor, '.-', basex=2, basey=2, lw=2)
    plt.loglog(domain, lu_solve, '.-', basex=2, basey=2, lw=2)
    plt.xlabel("n")

    plt.suptitle("Problem 4 Solution")
    plt.show()


# Problem 5
def prob5(n):
    """Return a sparse n x n tridiagonal matrix with 2's along the main
    diagonal and -1's along the first sub- and super-diagonals.
    """
    return sparse.diags([-1,2,-1], [-1,0,1], shape=(n,n))


# Problem 6
def prob6(N=10):
    """Time regular and sparse linear system solvers. Plot the system size
    versus the execution times. As always, use log scales where appropriate.
    """
    domain = 2**np.arange(2,N+1)
    solve, spsolve = [], []

    for n in domain:
        A = prob5(n).tocsr()
        b = np.random.random(n)

        start = time()
        spla.spsolve(A, b)
        spsolve.append(time()-start)

        A = A.toarray()
        start = time()
        la.solve(A, b)
        solve.append(time()-start)

    plt.subplot(121)
    plt.plot(domain, spsolve, '.-', lw=2, label="spla.spsolve()")
    plt.plot(domain, solve, '.-', lw=2, label="la.solve()")
    plt.xlabel("n"); plt.ylabel("Seconds")
    plt.legend(loc="upper left")

    plt.subplot(122)
    plt.loglog(domain, spsolve, '.-', basex=2, basey=2, lw=2)
    plt.loglog(domain, solve, '.-', basex=2, basey=2, lw=2)
    plt.xlabel("n")

    plt.suptitle("Problem 6 Solution")
    plt.show()


# Additional Material =========================================================

def ref_fast(A):
    """Alternate REF using an outer product. Fast, but not very intuitive."""
    for i in xrange(A.shape[0]):
        A[i+1:,i:] -= np.outer(A[i+1:,i]/A[i,i], A[i,i:])

def lu2_fast(A):
    """Alternative LU decomposition using an outer product."""
    U = A.copy()
    L = np.eye(A.shape[0])
    for i in xrange(A.shape[0]-1):
        L[i+1:,i] = U[i+1:,i] / U[i,i]
        U[i+1:,i:] -= np.outer(L[i+1:,i], U[i,i:])
    return L, U

def lu_inplace(A):
    """Compute the LU decomposition of the square matrix A *IN PLACE*."""
    for j in xrange(A.shape[0]-1):
        for i in xrange(j+1, A.shape[0]):
            A[i,j] /= A[j,j]
            A[i,j+1:] -= A[i,j] * A[j,j+1:]

def lu_det(A):
    """Compute det(A) using the LU decomposition (via la.lu_factor())."""
    lu, piv = la.lu_factor(A)

    # Determine if there were an even or odd number of row swaps.
    s = (piv != np.arange(A.shape[0])).sum() % 2
    return ((-1)**s) * lu.diagonal().prod()

def cholesky(A):
    L = np.zeros_like(A)
    for i in xrange(A.shape[0]):
        for j in xrange(i):
            L[i,j]=(A[i,j] - np.inner(L[i,:j], L[j,:j])) / L[j,j]
        sl = L[i,:i]
        L[i,i] = sqrt(A[i,i] - np.inner(sl, sl))
    return L

def cholesky_inplace(A):
    for i in xrange(A.shape[0]):
        A[i,i+1:] = 0.
        for j in range(i):
            A[i,j] = (A[i,j] - np.inner(A[i,:j],A[j,:j])) / A[j,j]
        sl = A[i,:i]
        A[i,i] = sqrt(A[i,i] - np.inner(sl, sl))

def cholesky_solve(A, B):
    for j in xrange(A.shape[0]):
        B[j] /= A[j,j]
        for i in xrange(j+1, A.shape[0]):
            B[i] -= A[i,j] * B[j]
    for j in xrange(A.shape[0]-1, -1, -1):
        B[j] /= A[j,j]
        for i in xrange(j):
            B[i] -= A[j,i] * B[j]


