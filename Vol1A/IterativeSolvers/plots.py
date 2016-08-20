# plots.py
"""Volume 1A: Iterative Solvers. Plotting file."""
from __future__ import print_function
import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../matplotlibrc')

# Decorator ===================================================================

from matplotlib import pyplot as plt
from functools import wraps
from sys import stdout

def _save(filename):
    """Decorator for saving, clearing, and closing figures automatically."""
    try:
        name, extension = filename.split(".")
    except (ValueError, TypeError) as e:
        raise ValueError("Invalid file name '{}'".format(filename))
    if extension not in {"pdf", "png"}:
        raise ValueError("Invalid file extension '{}'".format(extension))

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                print("{:.<25}".format(func.__name__+'()'), end='')
                stdout.flush()
                plt.clf()
                out = func(*args, **kwargs)
                if extension == "pdf":
                    plt.savefig(filename, format='pdf')
                elif extension == "png":
                    plt.savefig(filename, format='png')
                print("done.")
                return out
            except Exception as e:
                print("\n", e, sep='')
            finally:
                plt.clf()
                plt.close('all')
        return wrapper
    return decorator

# Plots =======================================================================

import numpy as np
from scipy import linalg as la
from solutions import jacobi_method
import matplotlib.pyplot as plt

def jacobi(n=100, tol=1e-8):
    """Solve Laplace's Equation using the Jacobi method and array slicing."""
    # Initialize the plate.
    U = np.zeros((n,n))

    # Set boundary conditions.
    U[:, 0] = 100                   # West boundary condition.
    U[:,-1] = 100                   # East boundary condition.
    U[ 0,:] = 0                     # North boundary condition.
    U[-1,:] = 0                     # South boundary condition.

    # Make a copy and initialize a difference variable.
    V = np.copy(U)
    diff = tol

    # Perform the iteration.
    while diff >= tol:
        V[1:-1,1:-1] = (U[:-2,1:-1] + U[2:,1:-1] + U[1:-1,:-2] + U[1:-1,2:])/4.
        diff = np.max(np.abs(U-V))
        U[1:-1,1:-1] = V[1:-1,1:-1]

    return U

@_save("jacobi_small.pdf")
def jacobi_small_plate():
    U1 = jacobi(10)
    plt.tick_params(axis='both', which='both',
                    labelleft='off', labelbottom='off',
                    bottom='off', top='off', left='off', right='off')
    plt.imshow(U1)


@_save("jacobi_big.pdf")
def jacobi_big_plate():
    U2 = jacobi(100)
    plt.tick_params(axis='both', which='both',
                    labelleft='off', labelbottom='off',
                    bottom='off', top='off', left='off', right='off')
    plt.imshow(U2)


@_save("jacobi_convergence.pdf")
def jacobi_convergence():
    A = np.array([[2,0,-1],[-1,3,2],[0,1,3]])
    b = np.array([3,3,-1])

    x, x_approx = jacobi_method(A,b)

    x_approx = np.array(x_approx)
    dom = np.arange(x_approx.shape[0])
    norms = []
    for i in xrange(x_approx.shape[0]):
        norms.append(la.norm(A.dot(x_approx[i]) - b))

    plt.semilogy(dom, norms)
    plt.ylabel("Absolute Error of Approximation")
    plt.xlabel("Iteration #")
    plt.title("Convergence of Jacobi Method")


def all_plots():
    jacobi_small_plate()
    jacobi_big_plate()
    jacobi_convergence()


if __name__ == '__main__':
    all_plots()
