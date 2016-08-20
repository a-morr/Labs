# name this file 'solutions.py'.
"""Volume II Lab 15: Line Search Algorithms
<name>
<class>
<date>
"""


# Problem 1
def newton1d(f, df, ddf, x, niter=10):
    """
    Perform Newton's method to minimize a function from R to R.

    Parameters:
        f (function): The twice-differentiable objective function.
        df (function): The first derivative of 'f'.
        ddf (function): The second derivative of 'f'.
        x (float): The initial guess.
        niter (int): The number of iterations. Defaults to 10.
    
    Returns:
        (float) The approximated minimizer.
    """
    raise NotImplementedError("Problem 1 Incomplete")

def test_newton():
    """Use the newton1d() function to minimixe f(x) = x^2 + sin(5x) with an
    initial guess of x_0 = 0. Also try other guesses farther away from the
    true minimizer, and note when the method fails to obtain the correct
    answer.

    Returns:
        (float) The true minimizer with an initial guess x_0 = 0.
        (float) The result of newton1d() with a bad initial guess.
    """
    raise NotImplementedError("Problem 1 Incomplete")


# Problem 2
def backtracking(f, slope, x, p, a=1, rho=.9, c=10e-4):
    """Perform a backtracking line search to satisfy the Armijo Conditions.

    Parameters:
        f (function): the twice-differentiable objective function.
        slope (float): The value of grad(f)^T p.
        x (ndarray of shape (n,)): The current iterate.
        p (ndarray of shape (n,)): The current search direction.
        a (float): The intial step length. (set to 1 in Newton and
            quasi-Newton methods)
        rho (float): A number in (0,1).
        c (float): A number in (0,1).
    
    Returns:
        (float) The computed step size satisfying the Armijo condition.
    """
    raise NotImplementedError("Problem 2 Incomplete")


# Problem 3    
def gradientDescent(f, df, x, niter=10):
    """Minimize a function using gradient descent.

    Parameters:
        f (function): The twice-differentiable objective function.
        df (function): The gradient of the function.
        x (ndarray of shape (n,)): The initial point.
        niter (int): The number of iterations to run.
    
    Returns:
        (list of ndarrays) The sequence of points generated.
    """
    raise NotImplementedError("Problem 3 Incomplete")

def newtonsMethod(f, df, ddf, x, niter=10):
    """Minimize a function using Newton's method.

    Parameters:
        f (function): The twice-differentiable objective function.
        df (function): The gradient of the function.
        ddf (function): The Hessian of the function.
        x (ndarray of shape (n,)): The initial point.
        niter (int): The number of iterations.
    
    Returns:
        (list of ndarrays) The sequence of points generated.
    """
    raise NotImplementedError("Problem 3 Incomplete")


# Problem 4
def gaussNewton(f, df, jac, r, x, niter=10):
    """Solve a nonlinear least squares problem with Gauss-Newton method.

    Parameters:
        f (function): The objective function.
        df (function): The gradient of f.
        jac (function): The jacobian of the residual vector.
        r (function): The residual vector.
        x (ndarray of shape (n,)): The initial point.
        niter (int): The number of iterations.
    
    Returns:
        (ndarray of shape (n,)) The minimizer.
    """
    raise NotImplementedError("Problem 4 Incomplete")


# Problem 5
def census():
    """Generate two plots: one that considers the first 8 decades of the US
    Census data (with the exponential model), and one that considers all 16
    decades of data (with the logistic model).
    """

    # Start with the first 8 decades of data.
    years1 = np.arange(8)
    pop1 = np.array([3.929,  5.308,  7.240,  9.638,
                    12.866, 17.069, 23.192, 31.443])

    # Now consider the first 16 decades.
    years2 = np.arange(16)
    pop2 = np.array([3.929,   5.308,   7.240,   9.638,
                    12.866,  17.069,  23.192,  31.443,
                    38.558,  50.156,  62.948,  75.996,
                    91.972, 105.711, 122.775, 131.669])

    raise NotImplementedError("Problem 5 Incomplete")
