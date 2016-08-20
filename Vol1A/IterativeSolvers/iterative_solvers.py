# iterative_solvers.py
"""Volume 1A: Iterative Solvers.
<Name>
<Class>
<Date>
"""
import numpy as np
import scipy.sparse as spar

# Helper functions
def diag_dom(n, vals=[-4,4], num_entries=None):
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
    for _ in xrange(num_entries):
        i = np.random.randint(0,n)
        j = np.random.randint(0,n)
        A[i,j] = np.random.randint(vals[0],vals[1])
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
        A (spar.coo_matrix) - strictly diagonally dominantn sparse nxn matrix.
    """
    if num_entries is None:
        num_entries = int(n**1.5) - n

    rows = np.random.random_integers(0,n-1,num_entries)
    cols = np.random.random_integers(0,n-1,num_entries)
    values = np.random.random_integers(-4,4,num_entries)
    A = spar.coo_matrix((values, (rows,cols)), shape=(n, n))

    A = A.todok()
    Acsr = A.tocsr()
    for i in xrange(n):
        A[i,i] = np.abs(Acsr[i,:]).sum() + 1
    return A.tocsr()

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
    raise NotImplemented("Problem 1 not complete!")

# Problem 2
def plot_convergence(A, b, maxiters=100, tol=1e-8):
    """Plot the rate of convergence for solving the system Ax = b.

    Inputs:
        A (array) - 2D NumPy array
        b (array) - 1D NumPy array
        maxiters (int, optional) - maximum iterations for algorithm to perform.
        tol (float) - tolerance for convergence
    """
    raise NotImplemented("Problem 2 not complete!")

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
    raise NotImplemented("Problem 3 not complete!")


# Problem 4
def compare_times():
    """For a 5000 parameter system, compare the runtimes of the Gauss-Seidel
    method and la.solve. Print an explanation of why Gauss-Seidel is so much
    faster.
    """
    raise NotImplemented("Problem 4 not complete!")


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
    raise NotImplemented("Problem 5 not complete!")

# Problem 6

####### --- TO BE DETERMINED --- ########

# Problem 7 (Optional)
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
    raise NotImplemented("Problem 7 not complete!")
