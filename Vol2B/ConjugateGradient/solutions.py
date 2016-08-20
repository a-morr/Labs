import numpy as np
from scipy import linalg as la
from scipy import optimize as opt
from matplotlib import pyplot as plt

# Problem 1
def conjugateGradient(b,x0,Q,tol = .0001):
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
    xk = x0
    rk = Q.dot(x0)-b
    dk = -rk
    k = 0
    while la.norm(rk) > tol:
        alphak = rk.T.dot(rk)/dk.T.dot(Q.dot(dk))
        xk1 = xk + alphak*dk
        rk1 = rk + alphak*Q.dot(dk)
        betak1 = rk1.T.dot(rk1)/rk.T.dot(rk)
        dk1 = -rk1 + betak1*dk
        k = k+1
        xk = xk1
        rk = rk1
        dk = dk1
    return xk1

# Problem 2
def prob2(filename = 'linregression.txt'):
    """Use conjugateGradient() to solve the linear regression problem with
    the data from linregression.txt.
    Return the solution x*.
    """
    data = np.loadtxt(filename)
    m,n = data.shape
    b = data[:,0]
    A = np.column_stack((np.ones(m),data[:,1:]))
    x0 = np.random.random(n)
    return conjugateGradient(A.T.dot(b),x0,A.T.dot(A))

    '''Correct Answer:
    [   -3482258.6159527,   15.06187214,    -0.03581918,    -2.0202298
        -1.03322686,        -0.05110411,    1829.15145504               ]

    or

    [ -3.48225866e+06   1.50618728e+01  -3.58191800e-02  -2.02022981e+00
      -1.03322687e+00  -5.11041030e-02   1.82915148e+03 ]
    '''

# Problem 3
def prob3(filename = 'logregression.txt'):
    """Use scipy.optimize.fmin_cg() to find the maximum likelihood estimate
    for the data in logregression.txt.
    """
    def objective(b):
        return (np.log(1+np.exp(x.dot(b))) - y*(x.dot(b))).sum()
    
    data = np.loadtxt(filename)
    m,n = data.shape
    y = data[:,0]
    x = np.empty_like(data)
    x[:,0] = np.ones_like(data[:,0])
    x[:,1:] = data[:,1:]
    y = data[:,0]

    guess = np.ones(4)
    b = opt.fmin_cg(objective, guess)
    
    return b

    '''Correct Answer:
    [-0.41307717, 0.92181585, 0.21007539, -0.55791808]
    '''
    
if __name__ == '__main__':
    n = 10
    A = np.random.random((n,n))
    Q = A.T.dot(A)
    b = np.random.random(n)
    x0 = np.random.random(n)
    x = conjugateGradient(b, x0, Q)
    # np.set_printoptions(suppress=True)
    if not np.allclose(x, la.solve(Q,b)):
        raise ValueError("Problem 1 Failed")
    print prob2()
    print prob3()
    np.set_printoptions()
    # test()