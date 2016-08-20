# solutions.py
"""Volume 1B: Differentiation. Solutions file."""


import numpy as np
from scipy import linalg as la
from matplotlib import pyplot as plt


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
    Df_app = lambda x: .5*(f(x+h)-f(x-h))/h
    return Df_app(pts)


# This problem got pulled out.
def calculate_errors(f,pts,h = 1e-5):
    """Compute the errors using the centered difference quotient approximation.

    Inputs:
        f (function): the function for which the derivative will be approximated
        pts (array): array of values to calculate the derivative

    Returns:
        errors (array): array of the errors for the centered difference quotient
            approximation
    """
    return f(pts)-centered_difference_quotient(f,pts)


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
    J = np.zeros((n,m))
    A = np.eye(m)
    for j in range(m):
        Df_app = lambda x: .5*(f(x+h*A[j,:])-f(x-h*A[j,:]))/h
        J[:,j] = Df_app(pt)
    return J


# Problem 3
def findError():
    """Compute the maximum error of jacobian() for the function
    f(x,y)=[(e^x)*sin(y)+y^3,3y-cos(x)] on the square [-1,1]x[-1,1].

    Returns:
        Maximum error of your jacobian function.
    """
    f = lambda x: np.array([(np.e**x[0])*np.sin(x[1])+x[1]**3, 3.*x[1]-np.cos(x[0])])
    df = lambda x: np.array([[np.e**x[0]*np.sin(x[1]),np.e**x[0]*np.cos(x[1])+3*x[1]**2],[np.sin(x[0]),3]])
    maxerror = np.zeros((2,2))
    for i in np.linspace(-1,1,num=100):
        for j in np.linspace(-1,1,num=100):
            myerror = (df(np.array([i,j]))-jacobian(f,2,2,np.array([i,j])))
            if la.norm(myerror)>la.norm(maxerror):
                maxerror = myerror
    return la.norm(maxerror)


# Problem 4
def Filter(image, F):
    """Applies the filter to the image.

    Inputs:
        image (ndarray): an array of the image
        F (ndarray): an nxn array of the filter to be applied.

    Returns:
        The filtered image.
    """
    m, n = image.shape
    h, k = F.shape
    image_pad = np.zeros((m+h-1, n+k-1))
    image_pad[(h//2):(h//2)+m, (k//2):(k//2)+n] = image
    C = np.zeros((m,n))
    for i in range(m):
        for j in range(n):
            C[i,j] = (F*image_pad[i:h+i, j:k+j]).sum()
    return C

# Problem 5
def sobelFilter(image):
    """Apply the Sobel filter to the image.

    Inputs:
        image (ndarray): an array of the image in grayscale

    Returns:
        The filtered image.
    """
    S = 1./8.*np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    AstarS = Filter(image,S)
    AstarST = Filter(image,S.T)
    gradient = np.sqrt(AstarS**2+AstarST**2)
    threshold = 4*gradient.mean()
    return gradient>threshold


def test_one():
    print "Testing 1"
    f = lambda x: np.exp(x)
    print centered_difference_quotient(f,np.array([1,2,3,4]))

def test_two():
    print "Testing 2"
    f = lambda x: np.exp(x)
    print calculate_errors(f,np.array([1,2,3,4]),h = 1e-5)

def test_three():
    print "Testing 3"
    f = lambda x: np.exp(x)
    print calculate_errors(f,np.array([1,2,3,4]))

def test_four():
    print "Testing 4"
    print findError()

def test_five():
    print "Testing 5"
    image = plt.imread('cameraman.jpg')
    G = 1./159.*np.array([[2,4,5,4,2],[4,9,12,9,4],[5,12,15,12,5],[4,9,12,9,4],[2,4,5,4,2]])
    plt.imshow(image,cmap = 'gray')
    plt.show()
    plt.imshow(Filter(image,G),cmap = 'gray')
    plt.show()

def test_six():
    print "Testing 6"
    image=plt.imread('cameraman.jpg')
    plt.imshow(sobelFilter(image),cmap = 'gray')
    plt.show()


if __name__ == "__main__":
    test_one()
    test_two()
    test_three()
    test_four()
    test_five()
    test_six()

