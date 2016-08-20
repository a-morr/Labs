# blackbox_function.py
"""Volume 2: Optimization Packages I (scipy.optimize). Auxiliary File."""

import numpy as np
from scipy import linalg as la

def blackbox(y_free):
    """
    Finds the length of a curve approximated piece-wise by a set of points.
    Accepts:
        y_free (1xn ndarray): the non-endpoint y-values of the curve.

    Returns:
        total_length (float): the length of the approximated curve.
    """
    # Initialize local constants.
    m = len(y_free) + 2 # Number points: free variables, origin, and endpoint.
    a, b = 40, 30       # Coordinates of endpoint.

     # Generate the evenly-spaced x-values of the curve.
    x = np.linspace(0,a,m)

     # Pad the free variables with the fixed endpoint values, 0 and b.
    y = np.hstack((0,y_free, b))

     # Calculate and return the line integral of the approximated curve.
    partial_norms = []
    for i,item in enumerate(y[:-1]):
        partial_norms.append(la.norm(np.array([x[i+1]-x[i],y[i+1] - item])))
    return np.sum(partial_norms)
