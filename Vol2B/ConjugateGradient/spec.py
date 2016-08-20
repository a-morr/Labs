# Name this file 'solutions.py'.
"""Volume II Lab 18: Conjugate Gradient
<Name>
<Class>
<Date>
"""

# Problem 1
def conjugateGradient(b, x0, Q, tol=1e-4):
    """Use the Conjugate Gradient Method to find the solution to the linear
    system Qx = b.
    
    Parameters:
        b  ((n, ) ndarray)
        x0 ((n, ) ndarray): An initial guess for x.
        Q  ((n,n) ndarray): A positive-definite square matrix.
        tol (float)
    
    Returns:
        x ((n, ) ndarray): The solution to the linear systm Qx = b, according
            to the Conjugate Gradient Method.
    """
    raise NotImplementedError("Problem 1 Incomplete")

# Problem 2
def prob2(filename='linregression.txt'):
    """Use conjugateGradient() to solve the linear regression problem with
    the data from linregression.txt.
    Return the solution x*.
    """
    raise NotImplementedError("Problem 2 Incomplete")

# Problem 3
def prob3(filename='logregression.txt'):
    """Use scipy.optimize.fmin_cg() to find the maximum likelihood estimate
    for the data in logregression.txt.
    """
    raise NotImplementedError("Problem 3 Incomplete")