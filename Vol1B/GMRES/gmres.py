"""
Vol I Lab __: GMRES
Name:
Date:
"""

#Problem 1: Implement the following function
def gmres(A, b, x0, k=100, tol=1e-8):
    '''Calculate approximate solution of Ax=b using GMRES algorithm.
    
    INPUTS:
    A    - Callable function that calculates Ax for any input vector x.
    b    - A NumPy array of length m.
    x0   - An arbitrary initial guess.
    k    - Maximum number of iterations of the GMRES algorithm. Defaults to 100.
    tol  - Stop iterating if the residual is less than 'tol'. Defaults to 1e-8.
    
    RETURN:
    Return (y, res) where 'y' is an approximate solution to Ax=b and 'res' 
    is the residual.
    '''
    raise NotImplementedError("Problem 1 incomplete.")
    
    
#Problem 2: Implement the following two functions
def plot_gmres(A, b, x0, tol=1e-8):
    '''Use the GMRES algorithm to approximate the solution to Ax=b.  Plot the
    eigenvalues of A and the convergence of the algorithm.
    
    INPUTS:
    A   - A 2-D NumPy array of shape mxm.
    b   - A 1-D NumPy array of length m.
    x0  - An arbitrary initial guess.
    tol - Stop iterating and create the desired plots when the residual is
          less than 'tol'. Defaults to 1e-8.
    
    OUTPUT:
    Follow the GMRES algorithm until the residual is less than tol, for a 
    maximum of m iterations. Then create the two following plots (subplots
    of a single figure):
     
    1. Plot the eigenvalues of A in the complex plane.
    
    2. Plot the convergence of the GMRES algorithm by plotting the
    iteration number on the x-axis and the residual on the y-axis.
    Use a log scale on the y-axis.
    '''
    raise NotImplementedError("Problem 2 incomplete.")

    
def make_plots(m=200):
    '''Create the matrix An defined in problem 2 in the manual 
    for n = -4, -2, -0, 2, 4.  Call plot_gmres on each, with b 
    a vector of ones, and an initial guess x0 a vector of zeros.
    Print a statement explaining how the convergence relates to 
    the eigenvalues.
    '''
    raise NotImplementedError("make_plots not yet implemented.")
    
    
#Problem 3: Implement the following two functions
def gmres_k(Amul, b, x0, k=5, tol=1E-8, restarts=50):
    '''Use the GMRES(k) algorithm to approximate the solution to Ax=b.
    
    INPUTS:
    A   - A Callable function that calculates Ax for any vector x.
    b   - A NumPy array.
    x0  - An arbitrary initial guess.
    k   - Maximum number of iterations of the GMRES algorithm before
        restarting. Defaults to 100.
    tol - Stop iterating if the residual is less than 'tol'. Defaults
        to 1E-8.
    restarts - Maximum number of restarts. Defaults to 50.
    
    OUTPUT:
    Return (y, res) where 'y' is an approximate solution to Ax=b and 'res'
    is the residual.
    '''
    raise NotImplementedError("Problem 3 incomplete.")
    
    
def time_gmres(m=200):
    '''Time the gmres and gmres_k functions on each of the matrices
    from problem 2.  Let x0 be a vector of zeros or anything you like.
    The results might be more dramatic with an x0 of larger magnitude.
    Print your results.  What do you observe?
    '''
    raise NotImplementedError("time_gmres not yet implemented.")
    