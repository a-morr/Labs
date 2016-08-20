import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../matplotlibrc')
from matplotlib import pyplot as plt

import numpy as np
from cvxopt import matrix, solvers
from pyfftw.interfaces import scipy_fftpack as fftpack
import math
import scipy.misc
from scipy import linalg as la
import scipy.io as io
from solutions import l1Min

def l2Min(A,b):
    """
    Solve min ||x||_2 s.t. Ax = b using CVXOPT.
    Inputs:
        A -- numpy array of shape m x n
        b -- numpy array of shape m
    Returns:
        x -- numpy array of shape n
    """
    m, n = A.shape
    P = np.eye(n)
    q = np.zeros(n)

    P = matrix(P)
    q = matrix(q)
    A = matrix(A)
    b = matrix(b)
    sol = solvers.qp(P,q, A=A, b=b)
    return np.array(sol['x']).flatten()

def sparse():
    # build sparse and nonsparse arrays, plot
    m = 5
    s = np.zeros(100)
    s[np.random.permutation(100)[:m]] = np.random.random(m)
    z = np.random.random_integers(0, high=1, size=(100,100)).dot(s)
    plt.subplot(211)
    plt.plot(s)
    plt.subplot(212)
    plt.plot(z)
    plt.savefig('sparse.pdf')
    plt.clf()

def incoherent():
    # example of sparse image in time domain, diffuse in Fourier domain
    s = np.random.random((50,50))
    mask = s < .98
    s[mask] = 0
    fs = fftpack.fft2(s)
    fs = np.abs(fs)
    plt.subplot(121)
    plt.imshow(1-s, cmap=plt.cm.Greys_r, interpolation='nearest')
    plt.xticks([])
    plt.yticks([])
    plt.subplot(122)
    plt.imshow(fs, cmap=plt.cm.Greys_r, interpolation='nearest')
    plt.xticks([])
    plt.yticks([])
    plt.savefig('incoherent.pdf')
    plt.clf()

def reconstruct():
    # reconstruct a simple image

    R = np.zeros((30,30))
    for i in xrange(13):
        R[27-2*i, 2+i] = 1.
        R[27-2*i, -2-i] = 1.
    R[16,9:22] = 1.
    ncols, nrows = R.shape
    n = ncols * nrows
    m = n / 4
    # generate DCT measurement matrix
    D1 = math.sqrt(1./8) * fftpack.dct(np.eye(n), axis=0)[np.random.permutation(n)[:m]]

    # create measurements
    b = D1.dot(R.flatten())

    rec_sig = l1Min(D1, b).reshape((nrows, ncols))
    rec_sig2 = l2Min(D1, b).reshape((nrows, ncols))
    plt.subplot(1,3,1)
    plt.imshow(R, cmap=plt.cm.Greys_r, interpolation='nearest')
    plt.xticks([])
    plt.yticks([])
    plt.subplot(1,3,2)
    plt.imshow(rec_sig, cmap=plt.cm.Greys_r, interpolation='nearest')
    plt.xticks([])
    plt.yticks([])

    plt.subplot(1,3,3)
    plt.imshow(rec_sig2, cmap=plt.cm.Greys_r, interpolation='nearest')
    plt.xticks([])
    plt.yticks([])

    plt.savefig('reconstruct.pdf')
    plt.clf()


def prob2_err(filename='ACME.png'):
    """Reconstruct the image in the indicated file using 100, 200, 250,
    and 275 measurements. Seed NumPy's random number generator with
    np.random.seed(1337) before each measurement to obtain consistent
    results.

    Plot the Euclidean distance between each reconstruction and the
    original image. (This isn't currently in the lab, but could be
    an instructive thing to do).

    This function takes several minutes to run to completion.
    """
    plt.clf()
    image = 1 - plt.imread(filename)[:,:,0]
    measurements, err = range(100,280,5), []
    
    for m in measurements:
        print "m =", m
        # Get 'm' random measurements.
        np.random.seed(1337)
        A = np.random.randint(0,2,(m,image.shape[0]*image.shape[1]))
        b = A.dot(image.flatten())

        # Reconstruct the image and calculate the 2-norm error.
        reconstruction = l1min(A,b).reshape(image.shape)
        err.append(np.linalg.norm(image - reconstruction))
    
    plt.plot(measurements, err, '.-', linewidth=2)
    plt.xlabel("Measurements"); plt.ylabel("$\|\ \|_{l_2}$ Error")
    plt.title("Error on Reconstructions of {}".format(filename))
    plt.savefig("prob2_error.pdf")
    plt.clf()

    
if __name__ == "__main__":
    sparse()
    incoherent()
    reconstruct()
