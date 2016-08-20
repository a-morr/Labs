import numpy as np

def initialize_all(y0, t0, t1, n):
    """ An initialization routine for the different ODE solving
    methods in the lab. This initializes Y, T, and h. """
    if isinstance(y0, np.ndarray):
        Y = np.empty((n, y.size)).squeeze()
    else:
        Y = np.empty(n)
    Y[0] = y0
    T = np.linspace(t0, t1, n)
    h = float(t1 - t0) / (n - 1)
    return Y, T, h

def euler(f, y0, t0, t1, n):
    """ Use the Euler method to compute an approximate solution
    to the ODE y' = f(t, y) at n equispaced parameter values from t0 to t
    with initial conditions y(t0) = y0.
    
    y0 is assumed to be either a constant or a one-dimensional numpy array.
    t and t0 are assumed to be constants.
    f is assumed to accept two arguments.
    The first is a constant giving the value of t.
    The second is a one-dimensional numpy array of the same size as y.
    
    This function returns an array Y of shape (n,) if
    y is a constant or an array of size 1.
    It returns an array of shape (n, y.size) otherwise.
    In either case, Y[i] is the approximate value of y at
    the i'th value of np.linspace(t0, t, n).
    """
    Y, T, h = initialize_all(y0, t0, t1, n)
    for i in xrange(1, n):
        Y[i] = Y[i-1] + f(T[i-1], Y[i-1]) * h
    return Y

def euler_accuracy(y0, t0, t1, N=(11, 21, 41)):
    """ Test the accuracy of the Euler method using the
    initial value problem y' + y = 2 - 2x, with y(0) = y0
    Plot your solutions over the given domain with n as 11, 21, and 41.
    Also plot the exact solution.
    Show the plot. """
    f = lambda x, y: 2 - y - 2 * x
    for n in N:
        T = np.linspace(t0, t1, n)
        plt.plot(T, euler(f, y0, t0, t1, n))
    plt.plot(T, 4 - 2 * T - 4 * np.exp(-T))
    plt.show()

# The inversion here could also be done using scipy.optimize's Newton's method.
# Currently in the lab, this function isn't required.
def backwards_euler(f, fsolve, y0, t0, t1, n):
    """ Use the backward Euler method to compute an approximate solution
    to the ODE y' = f(t, y) at n equispaced parameter values from t0 to t
    with initial conditions y(t0) = y0.
    
    y0 is assumed to be either a constant or a one-dimensional numpy array.
    t and t0 are assumed to be constants.
    f is assumed to accept two arguments.
    The first is a constant giving the value of t.
    The second is a one-dimensional numpy array of the same size as y.
    fsolve is a function that solves the equation
    y(x_{i+1}) = y(x_i) + h f(x_{i+1}, y(x_{i+1}))
    for the appropriate value for y(x_{i+1}).
    It should accept three arguments.
    The first should be the value of y(x_i).
    The second should be the distance between values of t.
    The third should be the value of x_{i+1}.
    
    This function returns an array Y of shape (n,) if
    y is a constant or an array of size 1.
    It returns an array of shape (n, y.size) otherwise.
    In either case, Y[i] is the approximate value of y at
    the i'th value of np.linspace(t0, t, n).
    """
    Y, T, h = initialize_all(y0, t0, t1, n)
    for i in xrange(1, n):
        Y[i] = fsolve(Y[i-1], h, T[i])
    return Y

def midpoint(f, y0, t0, t1, n):
    """ Use the midpoint method to compute an approximate solution
    to the ODE y' = f(t, y) at n equispaced parameter values from t0 to t1
    with initial conditions y(t0) = y0.
    
    y0 is assumed to be either a constant or a one-dimensional numpy array.
    t0 and t1 are assumed to be constants.
    f is assumed to accept two arguments.
    The first is a constant giving the value of t.
    The second is a one-dimensional numpy array of the same size as y.
    
    This function returns an array Y of shape (n,) if
    y is a constant or an array of size 1.
    It returns an array of shape (n, y.size) otherwise.
    In either case, Y[i] is the approximate value of y at
    the i'th value of np.linspace(t0, t, n).
    """
    Y, T, h = initialize_all(y0, t0, t1, n)
    for i in xrange(1, n):
        Y[i] = Y[i-1] + h * f(T[i-1] + h / 2., Y[i-1] + (h / 2.) * f(T[i-1], Y[i-1]))
    return Y

# This one isn't currently required in the lab.
def modified_euler(f, y0, t0, t1, n):
    """ Use the modified Euler method to compute an approximate solution
    to the ODE y' = f(t, y) at n equispaced parameter values from t0 to t1
    with initial conditions y(t0) = y0.
    
    y0 is assumed to be either a constant or a one-dimensional numpy array.
    t and t0 are assumed to be constants.
    f is assumed to accept two arguments.
    The first is a constant giving the value of t.
    The second is a one-dimensional numpy array of the same size as y.
    
    This function returns an array Y of shape (n,) if
    y is a constant or an array of size 1.
    It returns an array of shape (n, y.size) otherwise.
    In either case, Y[i] is the approximate value of y at
    the i'th value of np.linspace(t0, t, n).
    """
    Y, T, h = initialize_all(y0, t0, t1, n)
    for i in xrange(1, n):
        Y[i] = Y[i-1] + (h / 2.) * (f(T[i-1], Y[i-1]) + f(T[i-1], Y[i-1] + h * f(T[i-1], Y[i-1])))
    return Y



def RK4(f, y0, t0, t1, n):
    """ Use the RK4 method to compute an approximate solution
    to the ODE y' = f(t, y) at n equispaced parameter values from t0 to t
    with initial conditions y(t0) = y0.
    
    'y0' is assumed to be either a constant or a one-dimensional numpy array.
    't0' and 't1' are assumed to be constants.
    'f' is assumed to accept two arguments.
    The first is a constant giving the current value of t.
    The second is a one-dimensional numpy array of the same size as y.
    
    This function returns an array Y of shape (n,) if
    y is a constant or an array of size 1.
    It returns an array of shape (n, y.size) otherwise.
    In either case, Y[i] is the approximate value of y at
    the i'th value of np.linspace(t0, t, n).
    """
    Y, T, h = initialize_all(y0, t0, t1, n)
    for i in xrange(1, n):
        K1 = f(T[i-1], Y[i-1])
        tplus = (T[i] + T[i-1]) * .5
        K2 = f(tplus, Y[i-1] + .5 * h * K1)
        K3 = f(tplus, Y[i-1] + .5 * h * K2)
        K4 = f(T[i], Y[i-1] + h * K3)
        Y[i] = Y[i-1] + (h / 6.) * (K1 + 2 * K2 + 2 * K3 + K4)
    return Y