# Name this file 'solutions.py'.
"""Volume II: Compressed Sensing.
<Name>
<Class>
<Date>
"""


# Problem 1
def l1Min(A, b):
    """Calculate the solution to the optimization problem

        minimize    ||x||_1
        subject to  Ax = b

    Return only the solution x (not any slack variable), as a flat NumPy array.

    Parameters:
        A ((m,n) ndarray)
        b ((m, ) ndarray)

    Returns:
        x ((n, ) ndarray): The solution to the minimization problem.
    """
    raise NotImplementedError("Problem 1 Incomplete")


# Problem 2
def prob2(filename='ACME.png'):
    """Reconstruct the image in the indicated file using 100, 200, 250,
    and 275 measurements. Seed NumPy's random number generator with
    np.random.seed(1337) before each measurement to obtain consistent
    results.

    Resize and plot each reconstruction in a single figure with several
    subplots (use plt.imshow() instead of plt.plot()). Return a list
    containing the Euclidean distance between each reconstruction and the
    original image.
    """
    raise NotImplementedError("Problem 2 Incomplete")


# Problem 3
def prob3(filename="StudentEarthData.npz"):
    """Reconstruct single-pixel camera color data in StudentEarthData.npz
    using 450, 650, and 850 measurements. Seed NumPy's random number generator
    with np.random.seed(1337) before each measurement to obtain consistent
    results.

    Return a list containing the Euclidean distance between each
    reconstruction and the color array.
    """
    raise NotImplementedError("Problem 3 Incomplete")

