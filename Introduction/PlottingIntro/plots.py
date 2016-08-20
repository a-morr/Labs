# plots.py
"""Introductory Labs: Matploblib and Mayavi. Plotting file."""
from __future__ import print_function
import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../matplotlibrc')

# Decorator ===================================================================

from matplotlib import pyplot as plt, widgets as wg
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
                print("{:.<30}".format(filename), end='')
                stdout.flush()
                plt.clf()
                out = func(*args, **kwargs)
                if extension == "pdf":
                    plt.savefig("figures/"+filename, format='pdf')
                elif extension == "png":
                    plt.savefig("figures/"+filename, format='png',
                                                    size=(1024,768))
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
from mpl_toolkits.mplot3d import Axes3D

# Problem 1 -------------------------------------------------------------------

@_save("basic1.pdf")
def basic1():
    y = np.array([i**2 for i in xrange(-5,6)])
    plt.plot(y)

@_save("basic2.pdf")
def basic2(N):
    x = np.linspace(-5, 5, N)
    y = x**2
    plt.plot(x, y)

def prob1():
    basic1()
    basic2(50)

# Problem 3 -------------------------------------------------------------------

@_save("custom1.pdf")
def custom1(N):
    x = np.linspace(-2, 4, N)
    plt.plot(x, np.exp(x), 'g:', linewidth=6, label="Exponential")
    plt.xlabel("The x axis.", color='white')
    plt.title("This is the title.", fontsize=18)
    plt.legend(loc="upper left")

@_save("custom2.pdf")
def custom2(N):
    x = np.linspace(1, 4, N)
    plt.plot(x, np.log(x), 'r+', markersize=4)
    # plt.grid()
    plt.xlim(0, 5)
    plt.xlabel("The x axis")
    plt.title("This is the title.", fontsize=18, color='w')

@_save("discontinuousProblem.pdf")
def prob3_solution():
    x1, x2 = np.split(np.linspace(-2, 6, 200), [75])
    plt.plot(x1, 1/(x1 - 1), 'm--', lw=6)
    plt.plot(x2, 1/(x2 - 1), 'm--', lw=6)
    plt.ylim(-6, 6)

def prob3():
    custom1(100)
    custom2(100)
    prob3_solution()

# Problem 4 -------------------------------------------------------------------

def layout():
    for i in xrange(1,7):
        @_save("layout_{}.pdf".format(i))
        def box():
            plt.axis([-1,1,-1,1])
            plt.text(-.1,-.14,str(i),fontsize=72)
            plt.tick_params(
                axis='both',       # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom='off', top='off', left='off', right='off',
                labelbottom='off', labelleft='off')
        box()

@_save("subplots_1.pdf")
def subplots_1(N):
    x = np.linspace(.1, 2, N)
    plt.plot(x, np.exp(x), 'k', lw=2)
    plt.plot(x, np.exp(2*x), 'b', lw=2)
    plt.title("Exponential", fontsize=18)

@_save("subplots_2.pdf")
def subplots_2(N):
    x = np.linspace(.1, 2, N)
    plt.plot(x, np.log(x), 'k', lw=2)
    plt.plot(x, np.log(2*x), 'b', lw=2)
    plt.title("Logarithmic", fontsize=18)

def prob4(N=200):
    layout()
    subplots_1(N)
    subplots_2(N)

# Problem 5 -------------------------------------------------------------------

@_save("scatterplot.pdf")
def scatter():
    x = np.random.normal(scale=1.5, size=500)
    y = np.random.normal(scale=0.5, size=500)
    plt.plot(x, y, 'o', ms=10)
    return x

@_save("histogram.pdf")
def hist(x):
    plt.hist(x, bins=9, range=[-4.5, 4.5])
    # plt.hist(x, bins=np.arange(-4.5, 5.5))

def prob5():
    x = scatter()
    hist(x)

# Problem 6 -------------------------------------------------------------------

@_save("heatmap.png")
def heatmap(N):
    x = np.linspace(-np.pi, np.pi, N)
    y = x.copy()
    X, Y = np.meshgrid(x, y)

    plt.pcolormesh(X, Y, np.sin(X) * np.sin(Y), cmap="viridis")
                        # edgecolors='face', shading='flat')
    plt.axis([-np.pi, np.pi, -np.pi, np.pi])
    plt.colorbar()

    return X, Y

@_save("contour.pdf")
def contour(X, Y):
    plt.contour(X, Y, np.sin(X) * np.sin(Y), 10, cmap="Spectral")
    plt.colorbar()

@_save("contourf.pdf")
def contourf(X, Y):
    plt.contourf(X, Y, np.sin(X) * np.sin(Y), [-1, -.8, -.5, 0, .5, .8, 1],
                 cmap="magma")
    plt.colorbar()

def prob6():
    x, y = heatmap(200)
    contour(x, y)
    contourf(x, y)

# Additional Material ---------------------------------------------------------

@_save("surface_plot.pdf")
def surface_plot():
    x = np.linspace(-np.pi, np.pi, 200)
    y = np.copy(x)
    X, Y = np.meshgrid(x, y)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.view_init(elev=26, azim=-76)
    ax.plot_surface(X, Y, np.sin(X)*np.sin(Y))


@_save("interactive_plot.pdf")
def widget_plot():
    ax = plt.subplot(111)
    plt.subplots_adjust(bottom=.25)

    t = np.arange(0., 1., .001)
    a0, f0 = 5, 3
    s = a0 * np.sin(2 * np.pi * f0 * t)
    l = plt.plot(t, s)[0]

    plt.axis([0, 1, -10, 10])
    axfreq = plt.axes([.25, .05, .65, .03])
    axamp = plt.axes([.25, .1, .65, .03])
    sfreq = wg.Slider(axfreq, 'Freq', .1, 30., valinit=f0)
    samp = wg.Slider(axamp, 'Amp', .1, 10., valinit=a0)

    def update(val):
        amp = samp.val
        freq = sfreq.val
        l.set_ydata(amp * np.sin(2 * np.pi * freq * t))
        plt.draw()

    sfreq.on_changed(update)
    samp.on_changed(update)


def additional_material():
    surface_plot()
    widget_plot()

# Main Routine ================================================================

def save_all():
    prob1()
    prob3()
    prob4()
    prob5()
    prob6()
    additional_material()

if __name__ == '__main__':
    save_all()
