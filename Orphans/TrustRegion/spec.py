# Name this file 'solutions.py'
"""Volume II Lab 19: Trust Region Methods
<Name>
<Class>
<Date>
"""

# Problem 1
def trustRegion(f,grad,hess,subprob,x0,r0,rmax=2.,eta=1./16,gtol=1e-5):
    """Implement the trust regions method.
    
    Parameters:
        f (function): The objective function to minimize.
        g (function): The gradient (or approximate gradient) of the objective
            function 'f'.
        hess (function): The hessian (or approximate hessian) of the objective
            function 'f'.
        subprob (function): Returns the step p_k.
        x0 (ndarray of shape (n,)): The initial point.
        r0 (float): The initial trust-region radius.
        rmax (float): The max value for trust-region radii.
        eta (float in [0,0.25)): Acceptance threshold.
        gtol (float): Convergence threshold.
        
    
    Returns:
        x (ndarray): the minimizer of f.
    
    Notes:
        The functions 'f', 'g', and 'hess' should all take a single parameter.
        The function 'subprob' takes as parameters a gradient vector, hessian
            matrix, and radius.
    """
    raise NotImplementedError("Problem 1 Incomplete")

# Problem 2   
def dogleg(gk,Hk,rk):
    """Calculate the dogleg minimizer of the quadratic model function.
    
    Parameters:
        gk (ndarray of shape (n,)): The current gradient of the objective
            function.
        Hk (ndarray of shape (n,n)): The current (or approximate) hessian.
        rk (float): The current trust region radius
    
    Returns:
        pk (ndarray of shape (n,)): The dogleg minimizer of the model function.
    """
    raise NotImplementedError("Problem 2 Incomplete")

# Problem 3
def problem3():
    """Test your trustRegion() method on the Rosenbrock function.
    Define x0 = np.array([10.,10.]) and r = .25
    Return the minimizer.
    """
    raise NotImplementedError("Problem 3 Incomplete")

# Problem 4
def problem4():
    """Solve the described non-linear system of equations.
    Return the minimizer.
    """
    raise NotImplementedError("Problem 4 Incomplete")