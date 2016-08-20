# plots.py
"""Volume 1A: Linear Transformations. Plotting file."""
from __future__ import print_function
import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../matplotlibrc')

from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from functools import wraps
from timeit import timeit
from random import random
from sys import stdout
from time import time
import numpy as np
import solutions
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

# Horse Pictures ==============================================================

def pixel_picture(data, title, top=True):
    plt.plot(data[0], data[1], 'k,')
    if top:
        plt.title(title, fontsize=24)
    else:
        plt.xlabel(title, fontsize=24)
    plt.tick_params(
        axis='both',       # changes apply to both axes
        which='both',      # both major and minor ticks are affected
        bottom='off', top='off', left='off', right='off',
        labelbottom='off', labelleft='off')
    plt.axis([-1,1,-1,1])
    plt.gca().set_aspect("equal")

@_save("OriginalHorse.pdf")
def original(data):
    pixel_picture(data, "Original", top=True)

@_save("StretchHorse.pdf")
def stretched(data, a, b):
    pixel_picture(solutions.stretch(data, a, b), "Stretch", top=True)

@_save("ShearHorse.pdf")
def sheared(data, a, b):
    pixel_picture(solutions.shear(data, a, b), "Shear", top=True)

@_save("ReflectionHorse.pdf")
def reflected(data, a, b):
    pixel_picture(solutions.reflect(data, a, b), "Reflection", top=False)

@_save("RotationHorse.pdf")
def rotated(data, theta):
    pixel_picture(solutions.rotate(data, theta), "Rotation", top=False)

@_save("CompositionHorse.pdf")
def combo(data, a1, b1, a2, b2, a3, b3, theta):
    pixel_picture(
        solutions.rotate(
            solutions.reflect(
                solutions.shear(
                    solutions.stretch(data, a1, b1),
                a2, b2),
            a3, b3),
        theta),
    "Composition", top=False)

@_save("TranslationHorse.pdf")
def translated(data, a, b):
    pixel_picture(data + np.vstack([a, b]), "Translation", top=True)

@_save("SolarSystem.pdf")
def solar_system(T=3*np.pi/2, omega_e=1, omega_m=13, N=400):
    time = np.linspace(0, T, N)
    earth, moon = [np.array([10,0])], [np.array([11,0])]

    def rotation(theta):
        return np.array([[np.cos(theta),-np.sin(theta)],
                         [np.sin(theta),np.cos(theta)]])

    for t in time[1:]:
        earth.append(rotation(t*omega_e).dot(earth[0]))
        moon.append(rotation(t*omega_m).dot([1, 0]) + earth[-1])

    earth = np.transpose(earth)
    moon = np.transpose(moon)

    plt.plot(earth[0], earth[1], label="Earth", lw=2)
    plt.plot(moon[0], moon[1], label="Moon", lw=2)
    plt.xlabel("x"); plt.ylabel("y")
    plt.gca().set_aspect("equal")
    plt.legend(loc="upper left")

def horse_drawings(a1, b1, a2, b2, a3, b3, theta, a4, b4):
    horse = np.load("horse.npy")[:,::10]
    original(horse)
    stretched(horse, a1, b1)
    sheared(horse, a2, b2)
    reflected(horse, a3, b3)
    rotated(horse, theta)
    combo(horse, a1, b1, a2, b2, a3, b3, theta)
    translated(horse, a4, b4)
    solar_system()

# Timing Pictures =============================================================

@_save("time_random_matrix1.pdf")
def timing_demo1(N=12):
    domain = 2**np.arange(1,N+1)
    times = []

    for n in domain:
        start = time()
        solutions.random_matrix(n)
        times.append(time() - start)

    plt.plot(domain, times, 'g.-', linewidth=2, markersize=15)
    plt.xlabel("n", fontsize=14)
    plt.ylabel("Seconds", fontsize=14)

    return domain, times

@_save("time_random_matrix2.pdf")
def timing_demo2(N, domain, times):
    plt.plot(domain, times, 'g.-', linewidth=2, markersize=15)
    plt.xlabel("n", fontsize=14)
    plt.ylabel("Seconds", fontsize=14)

    # Plot the dotted blue line over the green line.
    def f(x, a, b):
        return a*x**2 + b
    a, b = curve_fit(f, domain, times)[0]

    refinement = np.linspace(1, 2**N, 200)
    plt.plot(refinement, f(refinement, a, b), 'b--', lw=5)
    plt.ylim(ymin=0)
    plt.ylabel("Seconds", fontsize=14, color="white")

@_save("matrixVectorMultiplication.pdf")
def prob1A(N=9):
    domain = 2**np.arange(1,N+1)
    vector_times, matrix_times = [], []

    for n in domain:
        A = solutions.random_matrix(n)
        x = solutions.random_vector(n)
        B = solutions.random_matrix(n)

        start = time()
        solutions.matrix_vector_product(A, x)
        vector_times.append(time() - start)

        start = time()
        solutions.matrix_matrix_product(A, B)
        matrix_times.append(time() - start)

    plt.plot(domain, vector_times, 'b.-', lw=2, ms=15)
    plt.xlabel("n", fontsize=14); plt.ylabel("Seconds", fontsize=14)
    plt.title("Matrix-Vector Multiplication")

    return domain, vector_times, matrix_times


@_save("matrixMatrixMultiplication.pdf")
def prob1B(domain, matrix_times):
    plt.plot(domain, matrix_times, 'g.-', lw=2, ms=15)
    plt.xlabel("n", fontsize=14); plt.ylabel("Seconds", fontsize=14, color="w")
    plt.title("Matrix-Matrix Multiplication")

@_save("loglogDemoBad.pdf")
def loglog_bad(domain, vector_times, matrix_times):
    plt.plot(domain, vector_times, 'b.-', lw=2, ms=15, label="Matrix-Vector")
    plt.plot(domain, matrix_times, 'g.-', lw=2, ms=15, label="Matrix-Matrix")
    plt.legend(loc="upper left")

@_save("loglogDemoGood.pdf")
def loglog_good(domain, vector_times, matrix_times):
    """Generate the two figures between Problem 1 and Problem 2."""
    plt.loglog(domain, vector_times, 'b.-', basex=2, basey=2, lw=2, ms=15)
    plt.loglog(domain, matrix_times, 'g.-', basex=2, basey=2, lw=2, ms=15)

@_save("cachingDemo.pdf")
def caching_demo():

    sizes = 2**np.arange(2,19,.2)
    times = []
    for size in sizes:
        A, B = np.random.random((2, size))
        def func():
            A + B
        times.append(timeit(func, number=50) / 50.)

    plt.loglog(sizes[1:], times[1:], basex=2, basey=2, lw=2, ms=15)
    plt.ylabel("Seconds")
    plt.xlabel("n")

def timing_drawings(N1, N2):
    dom, times = timing_demo1(N1)
    timing_demo2(N1, dom, times)
    dom, vt, mt = prob1A(N2)
    prob1B(dom, mt)
    loglog_bad(dom, vt, mt)
    loglog_good(dom, vt, mt)
    caching_demo()

# =============================================================================

def draw_all():
    horse_drawings(.5, 1.2, .5, 0., 0., 1., np.pi/2., .75, .5)
    timing_drawings(12, 8)

if __name__ == "__main__":
    draw_all()
