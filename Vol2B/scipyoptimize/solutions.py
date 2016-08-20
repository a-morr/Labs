# solutions.py
"""Volume 2: Optimization Packages I (scipy.optimize) solutions file."""

import scipy.optimize as opt
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from blackbox_function import blackbox

# Problem 1: use scipy.optimize.minimize() with different methods and compare.
def prob1():
    """Use the minimize() function in the scipy.optimize package to find the
    minimum of the Rosenbrock function (scipy.optimize.rosen) using the
    following methods:
        Nelder-Mead
        CG
        BFGS
    Use x0 = np.array([4., -2.5]) for the initial guess for each test.
    
    For each method, print whether it converged, and if so, print how many 
        iterations it took.
    """
    # Set up the initial guess.
    x0 = np.array([4.0,-2.5])

    # Test each method.
    info = {}
    info["Nelder-Mead"] = opt.minimize(opt.rosen, x0, method='Nelder-Mead')
    info["CG"] = opt.minimize(opt.rosen, x0, method='CG')
    info["BFGS"] = opt.minimize(opt.rosen, x0, method='BFGS')

    # Report the info.
    for method in info:
        print("Method:\t{}\nConverged:\t{} "
                                    .format(method, info[method]['success']))
        if info[method]['success']:
            print "Number of Iterations:", info[method]['nit'], '\n'

# Problem 2: Minizize an unknown "blackbox" function.
def prob2():
    """Minimize the function blackbox() in the blackbox_function module, 
    selecting the appropriate method of scipy.optimize.minimize() for this
    problem.  Do not pass your method a derivative. You may need to test 
    several methods and determine which is most appropriate.

    The blackbox() function returns the length of a piecewise-linear curve
    between two fixed points: the origin, and the point (40,30). 
    It accepts a one-dimensional ndarray} of length m of y-values, where m
    is the number of points of the piecewise curve excluding endpoints.
    These points are spaced evenly along the x-axis, so only the y-values 
    of each point are passed into blackbox().

    Once you have selected a method, select an initial point with the 
    provided code.

    Then plot your initial curve and minimizing curve together on the same
    plot, including endpoints. Note that this will require padding your 
    array of internal y-values with the y-values of the endpoints, so 
    that you plot a total of 20 points for each curve.

    SOLUTIONS NOTE: This solutions file uses method="BFGS", but 
    method="Powell" also returns the correct answer, which is a straight 
    line connecting the origin and the point (40,30). 
        Students may attempt to minimize using method="Nelder-Mead", as 
    this also does not use a derivative. However, this does not return
    the optimal solution.
    """
    # Set up the initial values
    y_initial = 30*np.random.random_sample(18)
    x = np.linspace(0,40,20)

    # Plot the pre-graph
    yplot = np.hstack((0,y_initial,30))
    plt.plot(x, yplot, '.-r', markersize=10)

    # Minimize the blackbox() function using method="BFGS".
    result = opt.minimize(blackbox, y_initial, tol=1e-4, method="BFGS") 
    if not result['success']:
        raise RuntimeError("didn't converge")

    ypost = np.hstack((0,result['x'],30))
    plt.plot(x, ypost, '.-b', markersize=10)
    plt.show()
    # The solution should plot the Batman symbol. 
    # Run blackbox_Batman.py to see original.

prob2()

# Problem 3: learn and use scipy.optimize.basinhopping()
def prob3():
    """Explore the documentation on the function scipy.optimize.basinhopping()
    online or via IPython. Use it to find the global minimum of the multmin()
    function given in the lab, with initial point x0 = np.array([-2, -2]) and
    the Nelder-Mead algorithm. Try it first with stepsize=0.5, then with
    stepsize=0.2. 

    Plot the multimin function and minima found using the code provided.
    Print statements answering the following questions:
        Which algorithms fail to find the global minimum?
        Why do these algorithms fail?

    Finally, return the global minimum.
    """
    # Define the function to be optimized and the initial condition.
    def multimin(x):
        r = np.sqrt((x[0]+1)**2 + x[1]**2)
        return r**2 *(1+ np.sin(4*r)**2)
    x0 = np.array([-2, -1.9])
    small_step = .2
    large_step = .5

    # Optimize using variations on Nelder-Mead.  NOTE: Here, each has been stored 
    # seperately for ease of plotting differently colored minimums.
    small = opt.basinhopping(multimin, x0, stepsize=small_step,
                            minimizer_kwargs={'method':'nelder-mead'})
    large = opt.basinhopping(multimin, x0, stepsize=large_step,
                            minimizer_kwargs={'method':'nelder-mead'})

    # Print the results.
    print("Stepsize:\t{}\nMinimum:\t{}\nX-Values:\t{}\n".format(small_step, 
                                                     small['fun'], small['x']))
    print("Stepsize:\t{}\nMinimum:\t{}\nX-Values:\t{}\n".format(large_step, 
                                                     large['fun'], large['x']))

    # Plot the multimin graph. Here, the points are colored differently for emphasis.
    xdomain = np.linspace(-3.5,1.5,70)
    ydomain = np.linspace(-2.5,2.5,60)
    X,Y = np.meshgrid(xdomain,ydomain)
    Z = multimin((X,Y))
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.plot_wireframe(X, Y, Z, linewidth=.5, color='c')
    ax1.scatter(x0[0], x0[1], multimin(x0), c='b')               # Initial pt: blue

    # Plot the results of the algorithms.
    ax1.scatter(small.x[0], small.x[1], small.fun, s=30, c='r')  # Small step: red
    ax1.scatter(large.x[0], large.x[1], large.fun, s=30, c='g')  # Large step: green
    plt.show()

    # Answer the problem questions.
    print("minimize() fails because it gets trapped in a basin.")
    print("0.2 fails because it is too small a stepsize to escape a basin.")

    # Return the correct global minimum.
    return large['fun']


# Problem 4: learn and use scipy.optimize.root()
def prob4():
    """Find the roots of the system
    [       -x + y + z     ]   [0]
    [  1 + x^3 - y^2 + z^3 ] = [0]
    [ -2 - x^2 + y^2 + z^2 ]   [0]

    Returns the values of x,y,z as an array.
    """
    # Define the nonlinear system, its Jacobian, and the initial guess.
    def f(X):
        x,y,z = X
        return np.array([   -x + y + z,
                            1 + x**3 -y**2 + z**3,
                            -2 -x**2 + y**2 + z**2  ])
    def jacobian(X):
        x,y,z = X
        return np.array([   [    -1,    1, 1     ],
                            [3*x**2, -2*y, 3*z**2],
                            [  -2*x,  2*y, 2*z   ]  ])
    x0 = np.array([0,0,0])

    # Calculate the solution, check that it is a root, and return it.
    sol = opt.root(f, x0, jac=jacobian, method='hybr')
    assert np.allclose(np.zeros_like(sol.x), f(sol.x)), "FAILURE"
    return sol.x


# Problem 5: learn and use scipy.optimize.curve_fit().
def prob5():
    """Use the scipy.optimize.curve_fit() function to fit a curve to
    the data found in `convection.npy`. The first column of this file is R, 
    the Rayleigh number, and the second column is Nu, the Nusselt number. 

    The fitting parameters should be c and beta, as given in the convection
    equations.

    Plot the data from `convection.npy` and the curve generated by curve_fit.
    Return the values c and beta as an array.
    """
    data = np.load("convection.npy")
    initial = 4

    # Define the function to optimize.
    def nusselt(R, c, beta):
        return c*R**beta

    # Use curve_fit and the data to get the parameters.
    popt, pcov = opt.curve_fit(nusselt, data[initial:,0], data[initial:,1])
    curve = nusselt(data[initial:,0], popt[0], popt[1])

    # Plot the data and the curve.
    plt.loglog(data[:,0], data[:,1], '.k', label='Data')
    plt.loglog(data[initial:,0], curve, 'b', label='Curve', linewidth=2)
    plt.legend(loc="lower right")
    plt.show()

    # Return the parameter values.
    return popt
