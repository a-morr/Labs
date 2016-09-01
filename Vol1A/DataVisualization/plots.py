# newplots.py
"""Volume 1A: Data Visualization. Plotting file."""

from __future__ import print_function
import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../matplotlibrc')

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

# Problem 1 (Anscombe's Quartet) ----------------------------------------------

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

# Problem 2 (Line Plots / Small Multiples) ------------------------------------

@_save("chebyshev_bad.pdf")
def line_bad():
    x = np.linspace(-1, 1, 200)
    for n in range(9):
        plt.plot(x, np.polynomial.Chebyshev.basis(n)(x), lw=1,
                                                label= "n = {}".format(n))
    plt.axis([-1.1, 1.1, -1.1, 1.1])
    plt.legend()

@_save("chebyshev_good.pdf")
def line_good():
    x = np.linspace(-1, 1, 200)
    for n in range(9):
        plt.subplot(3,3,n+1)
        plt.plot(x, np.polynomial.Chebyshev.basis(n)(x))
        plt.axis([-1.1, 1.1, -1.1, 1.1])

        # Turn off extra tick marks and axis labels.
        plt.tick_params(which="both", top="off", right="off")
        if n < 6:
            plt.tick_params(labelbottom="off")
        if n % 3:
            plt.tick_params(labelleft="off")
        plt.title("n = {}".format(n))

def prob2():
    line_bad()
    line_good()

# Problem 3 (Scatter Plots) ---------------------------------------------------

@_save("scatter_1.pdf")
def scatter_1():
    length, width, height = np.random.randint(1, 20, (3,50))
    plt.scatter(length, width, s=100)

    plt.grid()
    plt.xlabel("Length (inches)", fontsize=18, color="white")
    plt.ylabel("Width (inches)", fontsize=18)
    plt.tick_params(labelbottom="off")

    return length, width, height

@_save("scatter_2.pdf")
def scatter_2(length, width, height):
    plt.scatter(length, width, c=height, s=100)

    plt.grid()
    plt.xlabel("Length (inches)", fontsize=18, color="white")
    plt.ylabel("Width (inches)", fontsize=18, color="white")
    plt.tick_params(labelbottom="off", labelleft="off")
    cbar = plt.colorbar()
    cbar.set_label("Height (inches)", fontsize=18)

@_save("scatter_3.pdf")
def scatter_3(length, width, height):
    plt.scatter(length, width, s=length*width*height/2., alpha=.7)

    plt.grid()
    plt.xlabel("Length (inches)", fontsize=18)
    plt.ylabel("Width (inches)", fontsize=18)

@_save("scatter_4.pdf")
def scatter_4(length, width, height):
    plt.scatter(length, width, c=height, s=length*width*height/2., alpha=.7)

    plt.grid()
    plt.xlabel("Length (inches)", fontsize=18)
    plt.ylabel("Width (inches)", fontsize=18, color="white")
    plt.tick_params(labelleft="off")
    cbar = plt.colorbar()
    cbar.set_label("Height (inches)", fontsize=18)

def prob3():
    l,w,h = scatter_1()
    scatter_2(l,w,h)
    scatter_3(l,w,h)
    scatter_4(l,w,h)

# Problem 4 (Histograms) ------------------------------------------------------

@_save("histogram_1_bad.pdf")
def histogram_1_bad(N):
    data = np.random.normal(size=N)
    plt.plot(data)
    return data

@_save("histogram_1_good.pdf")
def histogram_1_good(data):
    plt.hist(data, bins=30)

@_save("histogram_2.pdf")
def histogram_2(N):
    data = np.random.beta(a=5, b=2, size=N)
    plt.hist(data, bins=30)
    return data

@_save("histogram_3.pdf")
def histogram_3(data):
    plt.hist(data, bins=30, lw=0, histtype="stepfilled")
    plt.tick_params(axis="y", labelcolor='white')
    plt.tick_params(left="off", top="off", right="off")

@_save("histogram_4.pdf")
def histogram_4(data):
    freq, bin_edges = np.histogram(data, bins=30)
    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2.
    plt.plot(bin_centers, freq, 'k-', lw=4)
    plt.tick_params(axis="y", labelcolor="white")
    plt.tick_params(left="off", top="off", right="off")

    # plt.tick_params(left="off", top="off", right="off", labelleft="off")

@_save("earthquake.pdf")
def earthquake():
    years, magnitudes, longitude, latitude = np.load("earthquakes.npy").T
    plt.plot(years, magnitudes, '.')
    plt.xlabel("Year")
    plt.ylabel("Magnitude")

def prob4():

    histogram_1_good(histogram_1_bad(1000))
    data = histogram_2(10000)
    histogram_3(data)
    histogram_4(data)

    earthquake()

# Problem 5 -------------------------------------------------------------------

@_save("heatmap_1.png")
def heatmap_1(N):
    x = np.linspace(-1.5, 1.5, N)
    X, Y = np.meshgrid(x, x.copy())
    Z = Y**2 - X**3 + X**2

    plt.pcolormesh(X, Y, Z, cmap="viridis")
    plt.colorbar()

    return X, Y, Z

@_save("heatmap_2.png")
def heatmap_2(X, Y, Z):
    plt.contour(X, Y, Z, [-1, -.25, 0, .25, 1, 4], colors="white")
    plt.pcolormesh(X, Y, Z, cmap="viridis")
    plt.colorbar()

@_save("contour_1.pdf")
def contour_1(X, Y, Z):
    plt.contour(X, Y, Z, 6, cmap="viridis")
    plt.colorbar()

@_save("contour_2.pdf")
def contour_2(X, Y, Z):
    plt.contourf(X, Y, Z, 12, cmap="viridis")
    plt.colorbar()

@_save("heatmap_3.png")
def heatmap_3(N):
    x = np.linspace(-6, 6, N)
    X, Y = np.meshgrid(x, x.copy())
    Z = np.abs(Y**2 - X**3 + X**2)

    plt.pcolormesh(X, Y, Z, cmap="plasma")
    plt.colorbar()

    return X, Y, Z

@_save("contour_3.pdf")
def contour_3(X, Y, Z):
    plt.contourf(X, Y, Z, 6, cmap="plasma", norm=colors.LogNorm())
    plt.colorbar()

def prob5():
    x,y,z = heatmap_1(200)
    heatmap_2(x,y,z)
    contour_1(x,y,z)
    contour_2(x,y,z)

    x,y,z = heatmap_3(200)
    contour_3(x,y,z)

# Problem 6 -------------------------------------------------------------------

@_save("bar_1.pdf")
def bar_1():
    labels = ["Lobster Thermador", "Baked Beans", "Crispy Bacon",
                "Smoked Sausage", "Hannibal Ham", "Eggs", "Spam"]
    values = [10, 11, 18, 19, 20, 21, 22]
    positions = np.arange(len(labels))

    plt.bar(positions, values, align="center")
    plt.xticks(positions, labels)

    return labels, values, positions

@_save("bar_2.pdf")
def bar_2(labels, values, positions):
    plt.barh(positions, values, align="center")
    plt.yticks(positions, labels)
    plt.gcf().subplots_adjust(left=0.2)

@_save("pie.pdf")
def pie(labels, values, positions):
    explode = np.zeros(len(values))
    explode[np.random.randint(0,explode.size)] = .2
    plt.pie(values, explode, labels, shadow=True,
                            startangle=np.random.randint(0,360,1))
    plt.gca().set_aspect("equal")

@_save("dishonest_1.pdf")
def dishonest_1(N):
    x = np.linspace(5, 10, N) + np.random.normal(size=N)/3.
    y = .5*x + 4 + np.random.normal(size=N)/2.
    plt.plot(x, y, 'o', ms=10)

    return x, y

@_save("dishonest_2.pdf")
def dishonest_2(x, y):
    plt.plot(x, y, 'o', ms=10)
    plt.xlim(-5,20)

@_save("dishonest_3.pdf")
def dishonest_3(x, y):
    plt.semilogy(x, y, 'o', ms=10)

@_save("honest.pdf")
def honest(x, y):
    plt.plot(x, y, 'o', ms=10)
    plt.xlim([0, x.max()+.2])
    plt.ylim([0, x.max()+.2])

def country_data(save=True):
    data = np.array([
                    [   8.742, 374.056, 179.2, 167.6],
                    [  10.985, 33.197, 160.0, 142.2],
                    [ 206.553, 1774.725, 173.1, 158.8],
                    [1378.36, 10866.444, 167  , 158.6],
                    [  5.495, 229.810, 178.9, 165.3],
                    [ 81.771, 3355.772, 178  , 165  ],
                    [  9.823, 120.687, 176  , 164  ],
                    [1330.09, 2073.543, 164.7, 161.2],
                    [ 127.00, 4123.258, 172.5, 158  ],
                    [ 24.214, 17.396, 165.6, 154.9],
                    [  0.622, 4.588, 183.2, 168.4],
                    [  5.237, 388.315, 182.4, 168  ],
                    [ 31.489, 192.084, 164  , 151  ],
                    [ 50.617, 1377.873, 170.8, 157.4],
                    [ 20.966, 82.316, 163.6, 151.4],
                    [  8.342, 664.738, 175.4, 164  ],
                    [ 78.742, 718.221, 174  , 158.9],
                    [ 65.110, 2848.755, 177.8, 164.5],
                    [324.311, 17946.996, 176.1, 162.1],
                    [ 92.700, 193.599, 165.7, 155.2]
                                                            ])
    if save:
        np.save("countries.npy", data)
    return data

def prob6():
    l,v,p = bar_1()
    bar_2(l,v,p)
    pie(l,v,p)

    x,y = dishonest_1(20)
    dishonest_2(x,y)
    dishonest_3(x,y)
    honest(x,y)

# =============================================================================

def save_all():
    prob2()
    prob3()
    prob4()
    prob5()
    prob6()


if __name__ == '__main__':
    save_all()
