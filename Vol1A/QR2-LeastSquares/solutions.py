# solutions.py
"""Volume 1A: QR 2 (Least Squares and Computing Eigenvalues).Solutions file."""

import numpy as np
from cmath import sqrt
from scipy import linalg as la
from matplotlib import pyplot as plt


# Problem 1
def least_squares(A, b):
    """Calculate the least squares solutions to Ax = b using QR decomposition.

    Inputs:
        A ((m,n) ndarray): A matrix of rank n <= m.
        b ((m, ) ndarray): A vector of length m.

    Returns:
        x ((n, ) ndarray): The solution to the normal equation.
    """
    Q,R = la.qr(A, mode="economic")
    return la.solve_triangular(R, np.dot(Q.T, b))

    # Or do back substitution by hand:
    m,n = A.shape
    Q,R = la.qr(A, mode="economic")
    y = np.dot(Q.T, b)
    x = np.zeros(n)

    for k in reversed(range(n)):
        x[k] = (y[k] - np.dot(R[k,k:], x[k:])) / R[k,k]

    return x


# Problem 2
def line_fit():
    """Load the data from housing.npy. Use least squares to calculate the line
    that best relates height to weight.

    Plot the original data points and the least squares line together.
    """
    year, index = np.load("housing.npy").T
    A = np.column_stack((year, np.ones_like(year)))
    # Or use slicing:
    # A = np.ones((len(height), 2))
    # A[:,0] = height
    slope, intercept = least_squares(A, index)

    plt.plot(year, index, 'k*')
    plt.plot(year, year*slope + intercept, 'b-', lw=2)
    plt.show()


# Problem 3
def polynomial_fit():
    """Load the data from housing.npy. Use least squares to calculate
    the polynomials of degree 3, 6, 9, and 12 that best fit the data.

    Plot the original data points and each least squares polynomial together
    in individual subplots.
    """
    # Load the data and define a more refined domain for plotting.
    year, index = np.load("housing.npy").T
    domain = np.linspace(year.min(), year.max(), 200)

    for i,n in enumerate([3, 6, 9, 12]):
        # Use least squares to compute the coefficients of the polynomial.
        coeffs = la.lstsq(np.vander(year, n+1), index)[0]
        # coeffs = np.polyfit(x, y, deg=n)

        # Plot the polynomial and the data points in an individual subplot.
        plt.subplot(2,2,i+1)
        plt.plot(year, index, 'k*')
        plt.plot(domain, np.polyval(coeffs, domain), 'b-', lw=2)
        plt.title(r"$n = {}$".format(n))
        # plt.axis([x.min(),x.max(),y.min(),y.max()])

    plt.suptitle("Solution to Problem 3")
    plt.show()


def plot_ellipse(a, b, c, d, e):
    """Plot an ellipse of the form ax^2 + bx + cxy + dy + ey^2 = 1."""
    theta = np.linspace(0, 2*np.pi, 200)
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    A = a*(cos_t**2) + c*cos_t*sin_t + e*(sin_t**2)
    B = b*cos_t + d*sin_t
    r = (-B + np.sqrt(B**2 + 4*A))/(2*A)

    plt.plot(r*cos_t, r*sin_t, lw=2)
    plt.gca().set_aspect("equal", "datalim")

# Problem 4
def ellipse_fit():
    """Load the data from ellipse.npy. Use least squares to calculate the
    ellipse that best fits the data.

    Plot the original data points and the least squares ellipse together.
    """
    # Load the data and construct the matrix A and the vector b.
    x, y = np.load("ellipse.npy").T
    A = np.column_stack((x**2, x, x*y, y, y**2))
    b = np.ones_like(x)

    # Use least squares to calculate the ellipse parameters.
    a, b, c, d, e = la.lstsq(A, b)[0]

    # Plot the results.
    plt.plot(x, y, 'k*')
    plot_ellipse(a, b, c, d, e)
    plt.show()


# Problem 5
def power_method(A, N=20, tol=1e-12):
    """Compute the dominant eigenvalue of A and a corresponding eigenvector
    via the power method.

    Inputs:
        A ((n,n) ndarray): A square matrix.
        N (int): The maximum number of iterations.
        tol (float): The stopping tolerance.

    Returns:
        (foat): The dominant eigenvalue of A.
        ((n, ) ndarray): An eigenvector corresponding to the dominant
            eigenvalue of A.
    """
    # Choose a random x_0 with norm 1.
    x = np.random.random(A.shape[0])
    x /= la.norm(x)

    for _ in xrange(N):
        # x_{k+1} = Ax_k / ||Ax_k||
        y = np.dot(A, x)
        x_new = y / la.norm(y)

        # Check for convergence.
        if la.norm(x_new - x) < tol:
            x = x_new
            break

        # Move to the next iteration.
        x = x_new

    return np.dot(x, np.dot(A, x)), x


# Problem 6
def qr_algorithm(A, N=50, tol=1e-12):
    """Compute the eigenvalues of A via the QR algorithm.

    Inputs:
        A ((n,n) ndarray): A square matrix.
        N (int): The number of iterations to run the QR algorithm.
        tol (float): The threshold value for determining if a diagonal block
            is 1x1 or 2x2.

    Returns:
        ((n, ) ndarray): The eigenvalues of A.
    """
    m,n = A.shape
    S = la.hessenberg(A)

    # TODO: introduce shifts.

    for i in xrange(N):
        Q,R = la.qr(S)
        S = np.dot(R,Q)

    eigs = []
    i = 0

    # Get the eigenvalues of each S_i.
    while i < n:
        if i == n-1:                # 1 x 1 block (final diagonal entry).
            eigs.append(S[i,i])
        elif abs(S[i+1,i]) < tol:   # 1 x 1 block.
            eigs.append(S[i,i])
        else:                       # 2 x 2 block.
            a, b, c, d = S[i:i+2,i:i+2].ravel()
            # Use the quadratic formula.
            B = -1*(a+d)
            C = a*d-b*c
            D = sqrt(B**2 - 4*C)
            eigs += [(-B + D)/2., (-B - D)/2.]
            i += 1
        i += 1
    return np.sort(eigs)


# Additional Material?
from matplotlib.animation import FuncAnimation
import warnings

def polynomial_fit_animation():

    warnings.simplefilter("ignore", np.RankWarning)
    x,y = np.load("housing.npy").T
    domain = np.linspace(x.min(), x.max(), 200)
    y_vals = np.array([np.polyval(np.polyfit(x, y, deg=n), domain)
                                                    for n in xrange(len(y))])
    warnings.simplefilter("default", np.RankWarning)

    plt.plot(x, y, 'k*')
    plt.plot(domain, 2*np.sin(domain), 'k--', lw=1)

    fig = plt.figure(1)
    drawing, = plt.plot([],[], lw=2)
    plt.axis([x.min()-1, x.max()+1, y.min()-1, y.max()+1])

    def update(index):
        drawing.set_data(domain, y_vals[index])
        plt.title(r"$n = {}$".format(index))
        return drawing,

    a = FuncAnimation(fig, update, frames=y_vals.shape[0], interval=1000)
    plt.show()
