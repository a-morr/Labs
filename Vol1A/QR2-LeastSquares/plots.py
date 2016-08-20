# plots.py
"""Volume 1A: QR 2 (Least Squares and Computing Eigenvalues). Plotting file."""
from __future__ import print_function
import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../matplotlibrc')

from matplotlib import pyplot as plt
from functools import wraps
from sys import stdout
import os

def _save(filename):
    """Decorator for saving, clearing, and closing figures automatically."""
    try:
        name, extension = filename.split(".")
    except (ValueError, TypeError) as e:
        raise ValueError("Invalid file name '{}'".format(filename))
    if extension not in {"pdf", "png"}:
        raise ValueError("Invalid file extension '{}'".format(extension))
    if not os.path.isdir("figures"):
        os.mkdir("figures")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                print("{:.<40}".format(filename), end='')
                stdout.flush()
                plt.clf()
                out = func(*args, **kwargs)
                plt.savefig("figures/"+filename, format=extension)
                print("done.")
                return out
            except Exception as e:
                print("\n\t", e, sep='')
            finally:
                plt.clf()
                plt.close('all')
        return wrapper
    return decorator

# Figures =====================================================================

import numpy as np
from scipy import linalg as la
from scipy.stats import linregress

@_save("line_fit_example.pdf")
def line():
    x = np.linspace(0, 10, 20)
    y = .5*x - 3 + np.random.randn(20)
    a, b = linregress(x, y)[:2]

    plt.plot(x, y, 'k*', label="Data Points")
    plt.plot(x, a*x + b, 'b-', lw=2, label="Least Squares Fit")
    plt.legend(loc="upper left")

@_save("circle_fit_example.pdf")
def circle():
    """Load the data from circle.npy. Use least squares to calculate the circle
    that best fits the data.

    Plot the original data points the least squares circle together.
    """
    x, y = np.load("circle.npy").T
    A = np.column_stack((2*x, 2*y, np.ones_like(x)))
    b = x**2 + y**2
    c1, c2, c3 = la.lstsq(A, b)[0]
    r = np.sqrt(c1**2 + c2**2 + c3)

    theta = np.linspace(0, 2*np.pi, 200)
    plt.plot(r*np.cos(theta)+c1, r*np.sin(theta)+c2, '-', lw=2)
    plt.plot(x, y, 'k*')
    plt.axis("equal")

# =============================================================================

def draw_all():
    line()
    circle()

if __name__ == "__main__":
    draw_all()
