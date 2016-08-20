# differentiation.py
"""Volume 1B: Differentiation.
<Name>
<Class>
<Date>
"""

# Problem 1
def centered_difference_quotient(f, pts, h=1e-5):
    """Compute the centered difference quotient for function (f)
    given points (pts).

    Inputs:
        f (function): the function for which the derivative will be approximated
        pts (array): array of values to calculate the derivative

    Returns:
        centered difference quotient (array): array of the centered difference
            quotient
    """
    raise NotImplementedError("Problem 1 Incomplete")


# Problem 2
def jacobian(f, n, m, pt, h=1e-5):
    """Compute the approximate Jacobian matrix of f at pt using the centered
    difference quotient.

    Inputs:
        f (function): the multidimensional function for which the derivative
            will be approximated
        n (int): dimension of the domain of f
        m (int): dimension of the range of f
        pt (array): an n-dimensional array representing a point in R^n
        h (float): a float to use in the centered difference approximation

    Returns:
        Jacobian matrix of f at pt using the centered difference quotient.
    """
    raise NotImplementedError("Problem 2 Incomplete")


# Problem 3
def findError():
    """Compute the maximum error of jacobian() for the function
    f(x,y)=[(e^x)*sin(y)+y^3,3y-cos(x)] on the square [-1,1]x[-1,1].

    Returns:
        Maximum error of your jacobian function.
    """
    raise NotImplementedError("Problem 3 Incomplete")


# Problem 4
def Filter(image, F):
    """Applies the filter to the image.

    Inputs:
        image (ndarray): an array of the image
        F (ndarray): an nxn array of the filter to be applied.

    Returns:
        The filtered image.
    """
    raise NotImplementedError("Problem 4 Incomplete")


# Problem 5
def sobelFilter(image):
    """Apply the Sobel filter to the image.

    Inputs:
        image (ndarray): an array of the image in grayscale

    Returns:
        The filtered image.
    """
    raise NotImplementedError("Problem 5 Incomplete")
