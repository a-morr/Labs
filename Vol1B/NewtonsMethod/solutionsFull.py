# solutions.py
import numpy as np
from matplotlib import pyplot as plt

# Problem 1: Implement this function.
def Newtons_method(f, x0, Df, iters=15, tol=.002):
    '''
    Use Newton's method to approximate a zero of a function.
    Inputs:
        f (function): A function handle. Should represent a function 
            from R to R.
        x0 (float): Initial guess.
        Df (function): A function handle. Should represent the derivative
             of f.
        iters (int): Maximum number of iterations before the function
            returns. Defaults to 15.
        tol (float): The function returns when the difference between
            successive approximations is less than tol.
    Returns:
        A tuple (x, converged, numiters) with
        x (float): the approximation for a zero of f
        converged (bool): a Boolean telling whether Newton's method converged
        numiters (int): the number of iterations the method computed
    '''
    xold = x0
    for numiters in range(1,iters+1):
        xnew = xold-f(xold)*1./Df(xold)
        if abs(xnew-xold)<tol:
            return xnew,True,numiters
        else:
            xold = xnew
    return xnew,False,numiters
        

# Problem 2.1: Implement this function.
def problemTwoOne():
    '''
    Return a tuple of the number of iterations to get five digits of accuracy
    for f = cos(x) with x_0 = 1 and x_0 = 2.
    '''
    f = lambda x : np.cos(x)
    df = lambda x: -1*np.sin(x)
    iter1 = Newtons_method(f,1,df,tol=.00001)
    iter2 = Newtons_method(f,2,df,tol=.00001)
    return iter1[2],iter2[2]

# Problem 2.2: Implement this function.
def problemTwoTwo():
    '''
    Plot f(x) = sin(x)/x - x on [-4,4].  Return the zero of this function to
    7 digits of accuracy.
    '''
    f = lambda x : (1.*np.sin(x))/x - x
    df = lambda x : -1*(x**2+np.sin(x)-x*np.cos(x))/(x**2)
    x = np.linspace(-4,4,num=100)
    plt.plot(x,f(x))
    plt.show()
    xnew,converged,numiters = Newtons_method(f,1,df,tol = .0000001)
    return xnew

# Problem 2.3: Implement this function.
def problemTwoThree():
    '''
    Return a tuple of
    1. The number of iterations to get five digits of accuracy for f(x) = x^9
        with x_0 = 1.
    2. A string with the reason to why you think the convergence is slow for 
        this function.
    '''
    f = lambda x : x**9
    df = lambda x : 9*x**8
    xnew,converged,numiters = Newtons_method(f,1,df,iters=3000,tol=1e-5)
    return numiters,"The derivative is very close to zero so it will converge slowly"
    

# Problem 2.4: Implement this function.
def problemTwoFour():
    '''
    Return a string as to what happens and why for the function f(x) = x^(1/3) where
    x_0 = .01.
    '''
    f = lambda x: np.sign(x)*np.power(np.abs(x), 1./3)
    df = lambda x :1./3./np.power(np.abs(x), 2./3)
    xnew,converged,numiters = Newtons_method(f,.01,df)
    return "The values are getting further and further away from the correct value so it never converges.  Because the derivative at the root is infinity."

# Problem 3 (Optional): Modify the function Newtons_method() to calculate the numerical
# derivative of f using centered coefficients.

def Newtons_method_II(f, x0, Df=None, iters=15, tol=.002):
    
    if Df == None:
        h = 1e-5
        Df = lambda x: .5 * (f(x+h) - f(x-h))/h
        
    xold = x0
    for numiters in range(1,iters+1):
        xnew = xold-f(xold)*1./Df(xold)
        if abs(xnew-xold)<tol:
            return xnew,True,numiters
        else:
            xold = xnew
    return xnew,False,numiters


# Problem 4: Implement this function.
def plot_basins(f, Df, roots, xmin, xmax, ymin, ymax, numpoints=1000,iters=15, colormap='brg'):
    '''
    Plot the basins of attraction of f.
    INPUTS:
        f (function): Should represent a function from C to C.
        Df (function): Should be the derivative of f.
        roots (array): An array of the zeros of f.
        xmin, xmax, ymin, ymax (float,float,float,float): Scalars that define the domain
            for the plot.
        numpoints (int): A scalar that determines the resolution of the plot. Defaults to 100.
        iters (int): Number of times to iterate Newton's method. Defaults to 15.
        colormap (str): A colormap to use in the plot. Defaults to 'brg'.
    '''
    xreal = np.linspace(xmin,xmax,numpoints)
    ximag = np.linspace(ymin,ymax,numpoints)
    Xreal,Ximag = np.meshgrid(xreal,ximag)
    Xold = Xreal + 1j*Ximag
    for numiters in xrange(iters):
        x = Xold - 1.* f(Xold)/Df(Xold)
        Xold = x

    convergedarray = np.zeros(Xold.shape)
    for i in range(Xold.shape[0]):
        for j in range(Xold.shape[1]):
            convergedarray[i,j] = np.abs(roots-x[i,j]).argmin()
    plt.pcolormesh(Xreal,Ximag,convergedarray,cmap=colormap)
    plt.show()
    

# Problem 5: Implement this function.
def problemFive():
    '''
    Run plot_basins() on the function x^3-1 on the domain [-1.5,1.5]x[-1.5,1.5].
    '''
    f = lambda x : x**3 - 1
    Df = lambda x : 3*x**2
    roots = np.array([1,-1j**(1./3),1j**(2./3)])
    xmin = -1.5
    xmax = 1.5
    ymin = -1.5
    ymax = 1.5
    plot_basins(f,Df,roots,xmin,xmax,ymin,ymax)

def testing():
    f = lambda x : x**3-x
    Df = lambda x : 3*x**2 - 1
    roots = np.array([0,1,-1])
    xmin = -1.5
    xmax = 1.5
    ymin = -1.5
    ymax = 1.5
    plot_basins(f,Df,roots, xmin,xmax,ymin,ymax)

if __name__ == '__main__':
    print problemTwoOne()
    print problemTwoTwo()
    print problemTwoThree()
    print problemTwoFour()
    print problemFive()
    print testing()