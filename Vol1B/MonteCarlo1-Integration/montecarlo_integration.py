# montecarlo_integration.py
"""Volume 1B: Monte Carlo 1 (Integration).
<Name>
<Class>
<Date>
"""


# Problem 1
def prob1():
    """Return an estimate of the volume of the unit sphere using Monte
    Carlo Integration.

    Inputs:
        numPoints (int, optional) - Number of points to sample. Defaults
            to 10^5.
    Returns:
        volume (int) - Approximate value of the area of the unit sphere.
    """
    raise NotImplementedError("Problem 1 Incomplete")


# Problem 2
def prob2():
    """Return an estimate of the area under the curve,
    f(x) = |sin(10x)cos(10x) + sqrt(x)*sin(3x)| from 1 to 5.

    Inputs:
        numPoints (int, optional) - Number of points to sample. Defautls
            to 10^5.
    Returns:
        area (int) - Apprimate value of the area under the
            specified curve.
    """
    raise NotImplementedError("Problem 2 Incomplete")


# Problem 3
def mc_int(f, mins, maxs, numPoints=500, numIters=100):
    """Use Monte-Carlo integration to approximate the integral of f
    on the box defined by mins and maxs.

    Inputs:
        f (function) - The function to integrate. This function should
            accept a 1-D NumPy array as input.
        mins (1-D np.ndarray) - Minimum bounds on integration.
        maxs (1-D np.ndarray) - Maximum bounds on integration.
        numPoints (int, optional) - The number of points to sample in
            the Monte-Carlo method. Defaults to 500.
        numIters (int, optional) - An integer specifying the number of
            times to run the Monte Carlo algorithm. Defaults to 100.

    Returns:
        estimate (int) - The average of 'numIters' runs of the
            Monte-Carlo algorithm.

    Example:
        >>> f = lambda x: np.hypot(x[0], x[1]) <= 1
        >>> # Integral over the square [-1,1] x [-1,1]. Should be pi.
        >>> mc_int(f, np.array([-1,-1]), np.array([1,1]))
        3.1290400000000007
    """
    raise NotImplementedError("Problem 3 Incomplete")


# Problem 4
def prob4(numPoints=[500]):
    """Calculates an estimate of the integral of
    f(x,y,z,w) = sin(x)y^5 - y^5 + zw + yz^3

    Inputs:
        numPoints (list, optional) - a list of the number of points to
            use the approximation. Defaults to [500].
    Returns:
        errors (list) - a list of the errors when calculating the
            approximation using 'numPoints' points.
    Example:
    >>> prob4([100,200,300])
    [-0.061492011289160729, 0.016174426377108819, -0.0014292910207835802]
    """
    raise NotImplementedError("Problem 4 Incomplete")
