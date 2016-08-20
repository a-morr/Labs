# solutions.py
"""Volume 1A: QR 1 (Decomposition). Solutions file."""

import numpy as np
from scipy import linalg as la

# Problem 1
def qr_gram_schmidt(A):
    """Compute the reduced QR decomposition of A via Modified Gram-Schmidt.

    Inputs:
        A ((m,n) ndarray): A matrix of rank n.

    Returns:
        Q ((m,n) ndarray): An orthonormal matrix.
        R ((n,n) ndarray): An upper triangular matrix.
    """
    m,n = A.shape
    Q = np.copy(A).astype(np.float)
    R = np.zeros((n,n))
    for i in range(n):
        R[i,i] = la.norm(Q[:,i])
        Q[:,i] /= R[i,i]
        for j in range(i+1,n):
            R[i,j] = np.dot(Q[:,j].T, Q[:,i])
            Q[:,j] -= R[i,j]*Q[:,i]
    return Q, R


# Problem 2
def abs_det(A):
    """Use the QR decomposition to efficiently compute the absolute value of
    the determinant of A.

    Inputs:
        A ((n,n) ndarray): A square matrix.

    Returns:
        (float) the absolute value of the detetminant of A.
    """
    Q,R = la.qr(A)                 # or Q, R = qr_gram_schmidt(A)
    return abs(R.diagonal().prod())


# Problem 3
def solve(A, b):
    """Use the QR decomposition to efficiently solve the system Ax = b.

    Inputs:
        A ((n,n) ndarray): An invertible matrix.
        b ((n, ) ndarray): A vector of length n.

    Returns:
        x ((n, ) ndarray): The solution to the system Ax = b.
    """
    m,n = A.shape
    Q,R = la.qr(A)

    # QRx = b -> Rx = (Q^T)b.
    y = np.dot(Q.T, b)

    # Use back substitution to solve Rx = y.
    x = np.zeros(n)
    for k in reversed(range(n)):
        x[k] = (y[k] - np.dot(R[k,k:], x[k:])) / R[k,k]

    return x

# Use this since np.sign(0) -> 0.
sign = lambda x: 1 if x >= 0 else -1

# Problem 4
def qr_householder(A):
    """Compute the full QR decomposition of A via Householder reflections.

    Inputs:
        A ((m,n) ndarray): A matrix of rank n.

    Returns:
        Q ((m,m) ndarray): An orthonormal matrix.
        R ((m,n) ndarray): An upper triangular matrix.
    """
    m,n = A.shape
    R = np.copy(A).astype(np.float)
    Q = np.identity(m)
    for k in range(n):
        u = np.copy(R[k:,k])
        u[0] += sign(u[0])*la.norm(u)
        u /= la.norm(u)
        R[k:,k:] -= 2*np.outer(u, np.dot(u, R[k:,k:]))
        Q[k:] -= 2*np.outer(u, np.dot(u, Q[k:]))
    return Q.T, R


# Problem 5
def hessenberg(A):
    """Compute the Hessenberg form H of A, along with the orthonormal matrix Q
    such that A = QHQ^T.

    Inputs:
        A ((n,n) ndarray): An invertible matrix.

    Returns:
        H ((n,n) ndarray): The upper Hessenberg form of A.
        Q ((n,n) ndarray): An orthonormal matrix.
    """
    m,n = A.shape
    H = np.copy(A).astype(np.float)
    Q = np.identity(m)
    for k in range(n-2):
        u = np.copy(H[k+1:,k])
        u[0] += sign(u[0])*la.norm(u)
        u /= la.norm(u)
        H[k+1:,k:] -= 2*np.outer(u, np.dot(u, H[k+1:,k:]))
        H[:,k+1:] -= 2*np.outer(np.dot(H[:,k+1:], u), u)
        Q[k+1:] -= 2*np.outer(u, np.dot(u, Q[k+1:]))
    return H, Q.T


# Additional Material
def qr_givens(A):
    """Compute the QR decomposition of A via Givens triangularization,
    assuming that at the ijth stage of the algorithm, a_ij will be nonzero.

    Inputs:
        A ((m,n) ndarray): A matrix of rank n.

    Returns:
        Q ((m,n) ndarray): An orthonormal matrix.
        R ((n,n) ndarray): An upper triangular matrix.
    """
    m,n = A.shape
    R = np.copy(A).astype(np.float)
    Q = np.identity(m)
    for j in range(n):
        for i in reversed(range(j+1,m)):
            a,b = R[i-1,j], R[i,j]
            G = np.array([[a,b],[-b,a]]) / np.sqrt(a**2+b**2)
            R[i-1:i+1,j:] = np.dot(G, R[i-1:i+1,j:])
            Q[i-1:i+1] = np.dot(G, Q[i-1:i+1])
    return Q.T, R


def qr_givens_hessenberg(H):
    """Compute the QR decomposition of the upper Hessenberg matrix H via
    Givens triangularization.

    Inputs:
        H ((m,n) ndarray): A matrix of rank n in upper Hessenberg form.

    Returns:
        Q ((m,n) ndarray): An orthonormal matrix.
        R ((n,n) ndarray): An upper triangular matrix.
    """
    m,n = H.shape
    R = np.copy(H).astype(np.float)
    Q = np.identity(m)
    for j in xrange(min(n, m-1)):
        i = j+1
        a,b = R[i-1,j],R[i,j]
        G = np.array([[a,b],[-b,a]]) / np.sqrt(a**2+b**2)
        R[i-1:i+1,j:] = np.dot(G, R[i-1:i+1,j:])
        Q[i-1:i+1,:i+1] = np.dot(G, Q[i-1:i+1,:i+1])
    return Q.T, R
