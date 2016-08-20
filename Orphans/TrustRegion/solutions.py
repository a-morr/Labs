# solutions.py
from scipy import linalg as la
import numpy as np
from scipy import optimize as op

# problem 1
def trustRegion(f,grad,hess,subprob,x0,r0,rmax=2.,eta=1./16,gtol=1e-5):
    """Implement the trust regions method.  
    
    Parameters:
        f : callable function object
            The objective function to minimize.
        g : callable function object
            The gradient (or approximate gradient) of the objective function
        hess : callable function object
            The hessian (or approximate hessian) of the objective function
        subprob: callable function object
            Returns the step p_k
        x0 : numpy array of shape (n,)
            The initial point
        r0 : float
            The initial trust-region radius
        rmax : float
            The max value for trust-region radii
        eta : float in [0,0.25)
            Acceptance threshold
        gtol : float
            Convergence threshold
        
    
    Returns:
        x : the minimizer of f
    Notes
    -----
    The functions f, g, and hess should all take a single parameter.
    The function subprob takes as parameters a gradient vector, hessian
         matrix, and radius.
    """
    
    x = x0
    r = r0
    while la.norm(grad(x)) > gtol:
        p = subprob(grad(x),hess(x),r)
        rho = (f(x)-f(x+p))/(-np.dot(p,grad(x))-.5*p.T.dot(hess(x).dot(p)))
        if rho < .25:
            r = .25*r
        else:
            if rho >.75 and np.allclose(la.norm(p),r):
                r = min(2*r,rmax)
        if rho > eta:
            x = x + p
    return x

# problem 2   
def dogleg(gk,Hk,rk):
    """Calculate the dogleg minimizer of the quadratic model function.
    
    Parameters:
        gk : ndarray of shape (n,)
            The current gradient of the objective function
        Hk : ndarray of shape (n,n)
            The current (or approximate) hessian
        rk : float
            The current trust region radius
    Returns:
        pk : ndarray of shape (n,)
            The dogleg minimizer of the model function.
    """
    pB = la.solve(-Hk,gk)
    pU = -(gk.T.dot(gk))/(gk.T.dot(Hk.dot(gk)))*gk
    
    if la.norm(pB) <= rk:
        return pB
    
    if la.norm(pU) >= rk:
        return rk*pU/la.norm(pU)
    
    a = pB.T.dot(pB) - 2.*pB.T.dot(pU) + pU.T.dot(pU)
    b = 2*pB.T.dot(pU) -2.*pU.T.dot(pU)
    c = pU.T.dot(pU) - rk**2
    t = 1. + (-b + np.sqrt(b**2-4.*a*c))/(2.*a)
    return pU + (t-1.)*(pB-pU)

# problem 3
def problem3():
    """Test your trustRegion() method on the Rosenbrock function.
    Define x0 = np.array([10.,10.]) and r = .25
    Return the minimizer.
    """
    x = np.array([10.,10.])
    r = .25
    return trustRegion(op.rosen,op.rosen_der,op.rosen_hess,dogleg,x,r)

    
# problem 4
def problem4():
    """Solve the described non-linear system of equations.
    Return the minimizer.
    """
    def r(x):
        return np.array([np.sin(x[0])*np.cos(x[1])-4*np.cos(x[0])*np.sin(x[1]),np.sin(x[1])*np.cos(x[0])-4*np.cos(x[1])*np.sin(x[0])])
    
    
    def f(x):
        return .5*(r(x)**2).sum()
    def J(x):
        return np.array([[np.cos(x[0])*np.cos(x[1])+4*np.sin(x[0])*np.sin(x[1]),-np.sin(x[0])*np.sin(x[1])-4*np.cos(x[0])*np.cos(x[1])],[-np.sin(x[1])*np.sin(x[0])-4*np.cos(x[0])*np.cos(x[1]),np.cos(x[0])*np.cos(x[1])+4*np.sin(x[0])*np.sin(x[1])]])
    def g(x):
        return J(x).dot(r(x))
    def B(x):
        return J(x).T.dot(J(x))
    
    rr = .25
    x = np.array([3.5,-2.5])
    xstar = trustRegion(f,g,B,dogleg,x,rr)
    return xstar

if __name__ == "__main__":
    print problem3()
    print problem4()