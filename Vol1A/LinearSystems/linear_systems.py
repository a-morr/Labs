# linear_systems.py
"""Volume 1A: Linear Systems.
<Name>
<Class>
<Date>
"""


# Problem 1
def ref(A):
    """Reduce the square matrix A to REF. You may assume that A is invertible
    and that a 0 will never appear on the main diagonal. Avoid operating on
    entries that you know will be 0 before and after a row operation.
    """
    raise NotImplementedError("Problem 1 Incomplete")


# Problem 2
def lu(A):
    """Compute the LU decomposition of the square matrix A. You may assume the
    decomposition exists and requires no row swaps.

    Returns:
        L ((n,n) ndarray): The lower-triangular part of the decomposition.
        U ((n,n) ndarray): The upper-triangular part of the decomposition.
    """
    raise NotImplementedError("Problem 2 Incomplete")


# Problem 3
def solve(A, b):
    """Use the LU decomposition and back substitution to solve the linear
    system Ax = b. You may assume that A is invertible (hence square).
    """
    raise NotImplementedError("Problem 3 Incomplete")


# Problem 4
def prob4():
    """Time different scipy.linalg functions for solving square linear systems.
    Plot the system size versus the execution times. Use log scales if needed.
    """
    raise NotImplementedError("Problem 4 Incomplete")


# Problem 5
def prob5(n):
    """Return a sparse n x n tridiagonal matrix with 2's along the main
    diagonal and -1's along the first sub- and super-diagonals.
    """
    raise NotImplementedError("Problem 5 Incomplete")


# Problem 6
def prob6():
    """Time regular and sparse linear system solvers. Plot the system size
    versus the execution times. As always, use log scales where appropriate.
    """
    raise NotImplementedError("Problem 6 Incomplete")

