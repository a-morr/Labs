# plots.py
"""Volume 1A: SVD and Image Compression. Plotting file."""
import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file("../../matplotlibrc")

import matplotlib.pyplot as plt
from scipy.linalg import svd
import numpy as np

def circles():
	A = np.array([[3,1],[1,3]])
	U, S, V = svd(A,full_matrices=False)
	S = np.diag(S)

	t = np.linspace(0,2*np.pi,100)
	pts = np.array([np.cos(t),np.sin(t)])
	v= V.dot(pts)
	sv = S.dot(v)
	a = U.dot(sv)

	unit_vecs = np.array([[1,0],[0,1]])
	vu = V.dot(unit_vecs)
	svu = S.dot(vu)
	au = U.dot(svu)

	plt.figure()
	plt.plot(pts[0],pts[1],'b')
	plt.plot([0,unit_vecs[0,0]],[0,unit_vecs[1,0]],'g')
	plt.plot([0,unit_vecs[0,1]],[0,unit_vecs[1,1]],'g')
	plt.axis('equal')
	plt.savefig('unit_circle.pdf')

	plt.figure()
	plt.plot(v[0],v[1],'b')
	plt.plot([0,vu[0,0]],[0,vu[1,0]],'g')
	plt.plot([0,vu[0,1]],[0,vu[1,1]],'g')
	plt.axis('equal')
	plt.savefig('vcircle.pdf')

	plt.figure()
	plt.plot(sv[0],sv[1],'b')
	plt.plot([0,svu[0,0]],[0,svu[1,0]],'g')
	plt.plot([0,svu[0,1]],[0,svu[1,1]],'g')
	plt.axis('equal')
	plt.savefig('svcircle.pdf')

	plt.figure()
	plt.plot(a[0],a[1],'b')
	plt.plot([0,au[0,0]],[0,au[1,0]],'g')
	plt.plot([0,au[0,1]],[0,au[1,1]],'g')
	plt.axis('equal')
	plt.savefig('full_transformation.pdf')


def svals(img):
    U, s, Vt = svd(img)
    s = np.sort(s)[::-1]
    plt.semilogy(s)
    plt.xlim([0,670])
    plt.xlabel('Matrix rank')
    plt.ylabel('Singular values')
    plt.savefig('hubble_svals.pdf')
    plt.close()

def lowrank(img, rankvals):
    U, s, Vt = svd(img)

    for n in rankvals:
        u1, s1, vt1 = U[:,0:n], np.diag(s[0:n]), Vt[0:n,:]
        plt.imsave("rank{}.png".format(n), u1.dot(s1).dot(vt1))

    plt.close()


if __name__ == "__main__":
    img = plt.imread('hubble_red.jpg')
    svals(img)
    lowrank(img, [1, 14, 27, 40])
    circles()
    plt.close()
