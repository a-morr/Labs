# solutions.py
"""Introductory Labs: Intro to NumPy. Solutions file."""

import numpy as np


def prob1():
    """Define the matrices A and B as arrays. Return the matrix product AB."""
    A = np.array([[3,-1,4],[1,5,-9]])
    B = np.array([[2,6,-5,3],[5,-8,9,7],[9,-3,-2,-3]])
    return A.dot(B)


def prob2():
    """Define the matrix A as an array. Return the matrix -A^3 + 9A^2 - 15A."""
    A = np.array([[3,1,4],[1,5,9],[-5,3,1]])
    A2 = np.dot(A, A)
    return -np.dot(A, A2) + 9*A2 - 15*A


def prob3():
    """Define the matrices A and B as arrays. Calculate the matrix product ABA,
    change its data type to np.int64, and return it.
    """
    A = np.triu(np.ones((7,7)))
    B = np.full_like(A, 5) - np.tril(np.full_like(A, 6))
    return np.dot(np.dot(A, B), A).astype(np.int64)


def prob4(A):
    """Make a copy of 'A' and set all negative entries of the copy to 0.
    Return the copy.

    Example:
        >>> A = np.array([-3,-1,3])
        >>> prob4(A)
        array([0, 0, 3])
    """
    B = A.copy()
    B[A < 0] = 0
    return B


def prob5():
    """Define the matrices A, B, and C as arrays. Return the block matrix
                                | 0 A^T I |
                                | A  0  0 |,
                                | B  0  C |
    where I is the identity matrix of appropriate size and each 0 is a matrix
    of all zeros, also of appropriate sizes.
    """
    A = np.arange(6).reshape((3,2)).T
    m, n = A.shape
    B = np.tril(np.full((3,3), 3, dtype=np.float64))
    C = -2*np.eye(3)
    O = np.zeros_like(A)
    return np.vstack((  np.hstack((np.zeros((n,n)), A.T,     np.eye(n))),
                        np.hstack((A,               np.zeros((m,m)), O)),
                        np.hstack((B,               O.T,             C))  ))


def prob6(A):
    """Divide each row of 'A' by the row sum and return the resulting array.

    Example:
        >>> A = np.array([[1,1,0],[0,1,0],[1,1,1]])
        >>> prob6(A)
        array([[ 0.5       ,  0.5       ,  0.        ],
               [ 0.        ,  1.        ,  0.        ],
               [ 0.33333333,  0.33333333,  0.33333333]])
    """
    return A / A.sum(axis=1)[:,np.newaxis].astype(np.float64)
    # Or use np.vstack() or np.reshape().


def prob7():
    """Given the array stored in grid.npy, return the greatest product of four
    adjacent numbers in the same direction (up, down, left, right, or
    diagonally) in the grid.
    """
    grid = np.load("grid.npy")

    # Slicing method.
    return max(
        np.max(grid[:,:-3] * grid[:,1:-2] * grid[:,2:-1] * grid[:,3:]),
        np.max(grid[:-3,:] * grid[1:-2,:] * grid[2:-1,:] * grid[3:,:]),
        np.max(grid[:-3,:-3]* grid[1:-2,1:-2] * grid[2:-1,2:-1] *grid[3:,3:]),
        np.max(grid[:-3,3:] * grid[1:-2,2:-1] * grid[2:-1,1:-2] *grid[3:,:-3]))

    # Naive iterative method (much less efficient).
    high = 0
    m,n = grid.shape
    for i in xrange(m):
        for j in xrange(n):
            z, w = 0, 0
            x = np.prod(grid[i,j:j+4])          # Right
            y = np.prod(grid[i:i+4,j])          # Down
            if i < m-3 and j < n-3:             # Right diagonal
                z = np.prod([grid[i,j],
                             grid[i+1,j+1],
                             grid[i+2,j+2],
                             grid[i+3,j+3]])
            if i < m-3 and j > 3:               # Left diagonal
                w = np.prod([grid[i,j],
                             grid[i+1,j-1],
                             grid[i+2,j-2],
                             grid[i+3,j-3]])
            high = max(x, y, z, w, high)
    return high
