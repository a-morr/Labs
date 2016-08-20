# arnoldi.py
"""Volume 1B: The Arnoldi Iteration.
<Name>
<Class>
<Date>
"""


# Problem 1
def arnoldi(b, Amul, k, tol=1E-8):
    """Perform `k' steps of the Arnoldi iteration on the linear operator
    defined by `Amul', starting with the vector 'b'.

    Inputs:
        b (ndarray): The starting vector for the iteration.
        Amul (function): A function handle that describes a linear operator.
        k (int): The number of times to perform the iteration.
        tol (float): Stop iterating if the next vector in the iteration has
            norm less than `tol'. Defaults to 1e-8.

    Returns:
        H_n (ndarray)
        Q_n (ndarray)
            The number n will equal k, unless the algorithm terminated early,
            in which case n will be less than k.

    Examples:
        >>> A = np.array([[1,0,0],[0,2,0],[0,0,3]])
        >>> Amul = lambda x: A.dot(x)
        >>> H, Q = arnoldi(np.array([1,1,1]), Amul, 3)
        >>> np.allclose(H, np.conjugate(Q.T).dot(A).dot(Q) )
        True

        >>> H, Q = arnoldi(np.array([1,0,0]), Amul, 3)
        >>> H
        array([[ 1.+0.j]])
        >>> np.conjugate(Q.T).dot(A).dot(Q)
        array([[ 1.+0.j]])
    """
    raise NotImplementedError("Problem 1 Incomplete")


# Problem 2
def ritz(Amul, dim, k, iters):
    """Find `k' Ritz values of the linear operator defined by `Amul'.

    Inputs:
        Amul (function): A function describing a linear operator on R^(dim).
        dim (int): The dimension of the space on which `Amul' acts.
        k (int): The number of Ritz values to return.
        iters (int): The number of times to perform the Arnoldi iteration.
            Must be between `k' and `dim'.

    Returns:
        ((k,) ndarray): `k' Ritz values of the operator defined by `Amul.'
    """
    raise NotImplementedError("Problem 2 Incomplete")


# Problem 3
def fft_eigs(dim=2**20, k=4):
    """Return the largest `k' Ritz values of the Fast Fourier transform
    operating on a space of dimension `dim'.
    """
    raise NotImplementedError("Problem 3 Incomplete")


# Problem 4
def plot_ritz(A, n, iters):
    """Plot the relative error of the Ritz values of `A'. Use the number of
    iterations as the x-axis and the relative error of the Ritz values of H_k
    a approximations to the eigenvalues of A as the y-axis.

    Inputs:
        A (ndarray)
        n (int): The number of Ritz values to plot.
        iters (int): The number of times to perform the Arnoldi iteration.
    """
    raise NotImplementedError("Problem 4 Incomplete")
