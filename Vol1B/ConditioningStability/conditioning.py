# conditioning.py
"""Volume 1B: Conditioning.
<Name>
<Class>
<Date>
"""

import numpy as np
from numpy.random import normal
from matplotlib import pyplot as plt

# Problem 1
def prob1():
    """Randomly perturb w_coeff by replacing each coefficient a_i with
    a_i*r_i, where r_i is drawn from a normal distribution centered at 1 with
    varience 1e-10.

    Plot the roots of 100 such experiments in a single graphic, along with the
    roots of the unperturbed polynomial w(x).

    Using the final experiment only, estimate the relative and absolute
    condition number (in any norm you prefer).

    Returns:
        Display a graph of all 100 perturbations.
        Print the values of relative and absolute condition numbers.
    """
    w_roots = np.arange(1, 21)
    w_coeffs = np.array([1, -210, 20615, -1256850, 53327946, -1672280820,
                40171771630, -756111184500, 11310276995381,
                    -135585182899530, 1307535010540395,
                    -10142299865511450, 63030812099294896,
                    -311333643161390640, 1206647803780373360,
                    -3599979517947607200, 8037811822645051776,
                    -12870931245150988800, 13803759753640704000,
                    -8752948036761600000, 2432902008176640000])

    raise NotImplementedError("Problem 1 Incomplete")


# Problem 2
def eig_condit(M):
    """Approximate the condition number of the eigenvalue problem at M.

    Inputs:
        M - A 2-D square NumPy array, representing a square matrix.

    Returns:
        A tuple containing approximations to the absolute and
        relative condition numbers of the eigenvalue problem at M.
    """
    raise NotImplementedError("Problem 2 Incomplete")



# 1 pt extra credit
def plot_eig_condit(x0=-100, x1=100, y0=-100, y1=100, res=10):
    '''
    Create a grid of points. For each pair (x,y) in the grid, find the
    relative condition number of the eigenvalue problem, using the matrix
    [[1 x]
     [y 1]]
    as your input. You can use plt.pcolormesh to plot the condition number
    over the entire grid.

    INPUT:
    x0 - min x-value of the grid
    x1 - max x-value
    y0 - min y-value
    y1 - max y-value
    res - number of points along each edge of the grid
    '''
    raise NotImplementedError("plot_eig_condit() not implemented")


# Problem 3
def integral(n):
    """RETURN I(n)"""
    raise NotImplementedError("Problem 3 Incomplete")

def prob3():
    """For the values of n in the problem, compute integral(n). Compare
    the values to the actual values, and print your explanation of what
    is happening.
    """

    #actual values of the integral at specified n
    actual_values = [0.367879441171, 0.145532940573, 0.0838770701034,
                 0.0590175408793, 0.0455448840758, 0.0370862144237,
                 0.0312796739322, 0.0270462894091, 0.023822728669,
                 0.0212860390856, 0.0192377544343]
    raise NotImplementedError("Problem 3 Incomplete")
