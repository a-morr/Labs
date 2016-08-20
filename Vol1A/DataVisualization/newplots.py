# newplots.py
"""Volume 1A: Data Visualization. Plotting file."""

from __future__ import print_function
import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../../matplotlibrc')

# Decorator ===================================================================

from matplotlib import colors, pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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

# Plots =======================================================================

import numpy as np

# Problem 1 -------------------------------------------------------------------

def anscombe_data(save=False):
    data = np.array([[10.0,  8.04, 10.0, 9.14, 10.0,  7.46,  8.0,  6.58],
                     [ 8.0,  6.95,  8.0, 8.14,  8.0,  6.77,  8.0,  5.76],
                     [13.0,  7.58, 13.0, 8.74, 13.0, 12.74,  8.0,  7.71],
                     [ 9.0,  8.81,  9.0, 8.77,  9.0,  7.11,  8.0,  8.84],
                     [11.0,  8.33, 11.0, 9.26, 11.0,  7.81,  8.0,  8.47],
                     [14.0,  9.96, 14.0, 8.10, 14.0,  8.84,  8.0,  7.04],
                     [ 6.0,  7.24,  6.0, 6.13,  6.0,  6.08,  8.0,  5.25],
                     [ 4.0,  4.26,  4.0, 3.10,  4.0,  5.39, 19.0, 12.50],
                     [12.0, 10.84, 12.0, 9.13, 12.0,  8.15,  8.0,  5.56],
                     [ 7.0,  4.82,  7.0, 7.26,  7.0,  6.42,  8.0,  7.91],
                     [ 5.0,  5.68,  5.0, 4.74,  5.0,  5.73,  8.0,  6.89]])
    if save:
        np.save("anscombe.npy", data)
    return data

# Problem 2 -------------------------------------------------------------------

# Line Plots - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@_save("line_vs_scatter_line.pdf")
def line_vs_scatter_line():
    x = np.linspace(0, 4, 8)
    data = x**2
    plt.plot(x, data, 'b-', linewidth=2)
    return x, data

@_save("line_vs_scatter_scat.pdf")
def line_vs_scatter_scat(x, data):
    plt.plot(x, data, 'g.', markersize=15)

@_save("line_vs_scatter_both.pdf")
def line_vs_scatter_both(x, data):
    plt.plot(x, data, 'r.-', linewidth=2, markersize=15)

# Scatter Plots - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@_save("scatter_1_bad.pdf")
def scat_1_bad():
    data = anscombe_data()
    x, y = data[:,2], data[:,3]
    plt.scatter(x, y, c='b', s=500)
    return x, y

@_save("scatter_1_good.pdf")
def scat_1_good(x, y):
    plt.scatter(x, y, s=.5*y**4, alpha=.8)
    return x, y

@_save("scatter_2_bad.pdf")
def scat_2_bad():
    data = anscombe_data()
    x, y = data[:,4], data[:,5]
    plt.scatter(x, y, c='b', s=500)
    return x, y

@_save("scatter_2_good.pdf")
def scat_2_good(x, y):
    plt.scatter(x, y, s=500, c=y, alpha=.8)
    cbar = plt.colorbar()
    cbar.set_label("y")

def prob2():
    # x, data = line_vs_scatter_line()
    # line_vs_scatter_scat(x, data)
    # line_vs_scatter_both(x, data)

    scat_1_good(*scat_1_bad())
    scat_2_good(*scat_2_bad())

# Problem 3 -------------------------------------------------------------------

@_save("hist_1_bad.pdf")
def hist_1_bad(N):
    data = np.random.normal(size=N)
    plt.plot(data)
    return data

@_save("hist_1_good.pdf")
def hist_1_good(data):
    plt.hist(data, bins=30)

@_save("hist_2_bad.pdf")
def hist_2_bad(N):
    data = np.random.exponential(size=N)
    plt.hist(data, bins=30)
    return data

@_save("hist_2_good.pdf")
def hist_2_good(data):
    plt.hist(data, bins=30, lw=0, histtype="stepfilled")
    plt.tick_params(axis="y", which="both", labelcolor='white', left='off',
                                                                right="off")
    plt.tick_params(axis="x", which="both", top='off')

def hist_3(N):
    data = np.random.beta(a=5, b=2, size=N)
    freq, bin_edges = np.histogram(data, bins=50)
    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2.
    plt.plot(bin_centers, freq, 'b-', lw=4)
    plt.hist(data, bins=50, alpha=.1)
    plt.tick_params(axis="both", which="both", labelleft='off',
                                left="off", top="off", right="off")

# Problem Statement - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@_save("earthquake.pdf")
def earthquake():
    years, magnitudes, longitude, latitude = np.load("earthquakes.npy").T
    plt.plot(years, magnitudes, '.')
    plt.xlabel("Year")
    plt.ylabel("Magnitude")

def prob3():

    hist_1_good(hist_1_bad(10000))
    hist_2_good(hist_2_bad(10000))
    _save("hist_3_bad.pdf")(hist_3)(10000)
    _save("hist_3_good.pdf")(hist_3)(10000000)

    earthquake()

# Problem 4 -------------------------------------------------------------------

@_save("rosenbrock.pdf")
def rosenbrock():
    fig = plt.figure()
    ax = Axes3D(fig, azim = -128, elev = 43)
    x = np.linspace(-2, 2, 50)
    y = np.linspace(-1, 3, 50)
    X, Y = np.meshgrid(x, y)
    Z = (1.-X)**2 + 100.*(Y-X**2)**2
    ax.plot_surface(X, Y, Z, rstride = 1, cstride = 1, cmap="viridis", linewidth=0, edgecolor='none', norm=colors.LogNorm())

    ax.set_xlim([-2, 2.0])
    ax.set_ylim([-1, 3.0])
    ax.set_zlim([0, 2500])

    plt.xlabel("x")
    plt.ylabel("y")

def save_all():
    prob2()
    prob3()
    rosenbrock()

if __name__ == '__main__':
    # prob2()
    save_all()
