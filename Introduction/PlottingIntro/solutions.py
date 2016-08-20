# solutions.py
"""Introductory Labs: Intro to Matplotlib. Solutions file."""
import numpy as np
from matplotlib import pyplot as plt


def var_of_means(n):
    """Construct a random matrix A with values drawn from the standard normal
    distribution. Calculate the mean value of each row, then calculate the
    variance of these means. Return the variance.

    Inputs:
        n (int): The number of rows and columns in the matrix A.

    Returns:
        (float) The variance of the means of each row.
    """
    A = np.random.randn(n,n)
    return A.mean(axis=1).var()

def prob1():
    """Create an array of the results of var_of_means() with inputs
    n = 100, 200, ..., 1000. Plot and show the resulting array.
    """
    y = np.array([var_of_means(n) for n in xrange(100, 1100, 100)])
    plt.plot(y)
    plt.show()


def prob2():
    """Plot the functions sin(x), cos(x), and arctan(x) on the domain
    [-2pi, 2pi]. Make sure the domain is refined enough to produce a figure
    with good resolution.
    """
    x = np.linspace(-2*np.pi, 2*np.pi, 200)
    plt.plot(x, np.sin(x))
    plt.plot(x, np.cos(x))
    plt.plot(x, np.arctan(x))
    plt.show()


def prob3():
    """Plot the curve f(x) = 1/(x-1) on the domain [-2,6].
        1. Split the domain so that the curve looks discontinuous.
        2. Plot both curves with a thick, dashed magenta line.
        3. Change the range of the y-axis to [-6,6].
    """
    x1, x2 = np.split(np.linspace(-2, 6, 200), [75])
    # x1, x2 = np.linspace(-2, 1, 75), np.linspace(1, 6, 125)
    plt.plot(x1, 1/(x1 - 1), 'm--', lw=4)
    plt.plot(x2, 1/(x2 - 1), 'm--', lw=4)
    plt.ylim(-6, 6)
    plt.show()


def prob4():
    """Plot the functions sin(x), sin(2x), 2sin(x), and 2sin(2x) on the
    domain [0, 2pi].
        1. Arrange the plots in a square grid of four subplots.
        2. Set the limits of each subplot to [0, 2pi]x[-2, 2].
        3. Give each subplot an appropriate title.
        4. Give the overall figure a title.
        5. Use the following line colors and styles.
              sin(x): green solid line.
             sin(2x): red dashed line.
             2sin(x): blue dashed line.
            2sin(2x): magenta dotted line.
    """
    x = np.linspace(0, 2*np.pi, 200)

    plt.subplot(221)    # sin(x)
    plt.plot(x, np.sin(x), 'g-', lw=2)
    plt.axis([0, 2*np.pi, -2, 2])
    plt.title("sin(x)")

    plt.subplot(222)    # sin(2x)
    plt.plot(x, np.sin(2*x), 'r--', lw=2)
    plt.axis([0, 2*np.pi, -2, 2])
    plt.title("sin(2x)")

    plt.subplot(223)    # 2sin(x)
    plt.plot(x, 2*np.sin(x), 'b--', lw=2)
    plt.axis([0, 2*np.pi, -2, 2])
    plt.title("2sin(x)")

    plt.subplot(224)    # 2sin(2x)
    plt.plot(x, 2*np.sin(2*x), 'm:', lw=2)
    plt.axis([0, 2*np.pi, -2, 2])
    plt.title("2sin(2x)")

    plt.suptitle("Solution to Problem 4 (subplots)")
    plt.show()


def prob5():
    """Visualize the data in FARS.npy. Use np.load() to load the data, then
    create a single figure with two subplots:
        1. A scatter plot of longitudes against latitudes. Because of the
            large number of data points, use black pixel markers (use "k,"
            as the third argument to plt.plot()). Label both axes.
        2. A histogram of the hours of the day, with one bin per hour.
            Label and set the limits of the x-axis.
    """
    data = np.load("FARS.npy")

    plt.subplot(211)
    plt.plot(data[:,1], data[:,2], 'k,')
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.axis("equal")

    plt.subplot(212)
    plt.hist(data[:,0], bins=24, range=[-.5, 23.5])
    plt.xlim(-.5,23.5)
    plt.xlabel("Hour (Military Time)")

    plt.suptitle("Solution to Problem 5 (FARS data)")
    plt.show()

def prob6():
    """Plot the function f(x,y) = sin(x)sin(y)/xy on the domain
    [-2pi, 2pi]x[-2pi, 2pi].
        1. Create 2 subplots: one with a heat map of f, and one with a contour
            map of f. Choose an appropriate number of level curves, or specify
            the curves yourself.
        2. Set the limits of each subplot to [-2pi, 2pi]x[-2pi, 2pi].
        3. Choose a non-default color scheme.
        4. Add a colorbar to each subplot.
    """

    # Define the mesgrid and calculate f() on the grid.
    x = np.linspace(-2*np.pi, 2*np.pi, 200)
    y = np.copy(x)
    X, Y = np.meshgrid(x,y)
    Z = np.sin(X)*np.sin(Y)/(X*Y)

    plt.subplot(121)        # Heat map.
    plt.pcolormesh(X, Y, Z, cmap="Spectral")
    plt.axis([-2*np.pi, 2*np.pi, -2*np.pi, 2*np.pi])
    plt.colorbar()

    plt.subplot(122)        # Contour map.
    plt.contour(X, Y, Z, 10, cmap="Spectral")
    plt.axis([-2*np.pi, 2*np.pi, -2*np.pi, 2*np.pi])
    plt.colorbar()

    plt.suptitle("Solution to Problem 6 (meshgrids)")
    plt.show()
