from __future__ import division, print_function
from time import time

import numpy as np
np.set_printoptions(precision=15)
from numpy.linalg import norm
from numpy.random import random_integers, uniform, randn
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.optimize import root
from scipy.misc import imread, imsave
import numexpr as ne

from solution import cheb, cheb_vectorized


def nonlinear_minimal_area_surface_of_revolution():
	l_bc, r_bc = 1., 7.
	N = 80
	D, x = cheb_vectorized(N)
	M = np.dot(D, D)
	guess = 1. + (x--1.)*((r_bc - l_bc)/2.)
	
	def pseudospectral_ode(y):
		out = np.zeros(y.shape)
		yp, ypp = D.dot(y), M.dot(y)
		out = y*ypp - 1. - yp**2.
		out[0], out[-1] = y[0] - r_bc, y[-1] - l_bc
		return out
	
	u = root(pseudospectral_ode,guess,method='lm',tol=1e-9)
	return x, u.x


def example_text():
	a, b = -1, 1.
	alpha, beta = 1., 7.
	x_steps, final_T, time_steps = 50, 10., 80000
	# Define variables x_steps, final_T, time_steps
	delta_t, delta_x = final_T/time_steps, (b-a)/x_steps
	x0 = np.linspace(a,b,x_steps+1)
	
	# Check a stability condition for this numerical method
	if delta_t/delta_x**2. > .5:
		print("stability condition fails")
		return 
	
	u = np.empty((2,x_steps+1))
	u[0]  = (beta - alpha)/(b-a)*(x0-a)	 + alpha
	u[1] = (beta - alpha)/(b-a)*(x0-a)	+ alpha
	
	def rhs(y):
		# Approximate first and second derivatives to second order accuracy.
		yp = (np.roll(y,-1) - np.roll(y,1))/(2.*delta_x)
		ypp = (np.roll(y,-1) - 2.*y + np.roll(y,1))/delta_x**2.
		# Find approximation for the next time step, using a first order Euler step
		y[1:-1] -= delta_t*(1. + yp[1:-1]**2. - 1.*y[1:-1]*ypp[1:-1])
		
	
	# Time step until successive iterations are close
	iteration = 0
	while iteration < time_steps:
		rhs(u[1])
		if norm(np.abs((u[0] - u[1]))) < 1e-5: 
			break
		u[0] = u[1]
		iteration+=1
	
	print("Difference in iterations is ", norm(np.abs((u[0] - u[1]))) )
	print("Final time = ", iteration*delta_t)

	plt.plot(x0,(beta - alpha)/(b-a)*(x0-a)	 + alpha,'-k',linewidth=2.,label="Initial guess")
	plt.plot(x0,u[1],'-b',linewidth=2.,label="Minimizing curve")
	temp1, temp2 = nonlinear_minimal_area_surface_of_revolution()
	plt.plot(temp1, temp2,'*r',linewidth=2.,label="Pseudospectral result")
	plt.axis([a-.2,b+.2,0,8])
	plt.legend(loc='best')
	plt.xlabel('$x$',fontsize=18)
	plt.ylabel('$y$',fontsize=18)
	# plt.savefig('min_surface_area.pdf')
	plt.show()
	return


def add_noise(imagename,changed_pixels=10000):
	# Read the image file imagename.
	# Multiply by 1. / 255 to change the values so that they are floating point
	# numbers ranging from 0 to 1.
	IM = imread(imagename, flatten=True) * (1. / 255)
	IM_x, IM_y = IM.shape
	
	for lost in xrange(changed_pixels):
		x_,y_ = random_integers(1,IM_x-2), random_integers(1,IM_y-2)
		val =  .25*randn() + .5
		IM[x_,y_] = max( min(val+ IM[x_,y_],1.), 0.)
	# imsave(name=("noised_"+imagename),arr=IM)


def plot_image(imagename):
	IM = imread(imagename, flatten=True) * (1. / 255)
	plt.imshow(IM, cmap=cm.gray)
	plt.show()


def gradient_descent_heat(imagename,time_steps=120):
	print(2*"\n"+"Diffusion Based Denoising"+2*"\n")
	IM = imread(imagename, flatten=True) * (1. / 255)
	IM_x, IM_y = IM.shape
	
	delta_t = 1e-3 # 5e-8
	delta_x, delta_y = 1./IM_x, 1./IM_y
	lmbda = 40 
	u = np.empty((2,IM_x,IM_y))
	u[1] = IM
	
	def laplace(z):
		# Approximate first and second derivatives to second order accuracy.
		z_xx = (np.roll(z,-1,axis=0) - 2.*z + np.roll(z,1,axis=0))#/delta_x**2.
		z_yy = (np.roll(z,-1,axis=1) - 2.*z + np.roll(z,1,axis=1))#/delta_y**2.
		# Find approximation for the next time step, using a first order Euler step
		z[1:-1,1:-1] -= delta_t*(	(z[1:-1,1:-1]-IM[1:-1,1:-1])
									-lmbda*(z_xx[1:-1,1:-1] + z_yy[1:-1,1:-1]))
	
	# Time step until successive iterations are close
	iteration = 0
	while iteration < time_steps:
		laplace(u[1])
		if norm(np.abs((u[0] - u[1]))) < 1e-6: break
		# print iteration, norm(np.abs((u[0] - u[1])))
		u[0] = u[1]
		iteration+=1
	
	# imsave(name=("de"+imagename),arr=u[1])
	plt.imshow(u[1], cmap=cm.gray)
	plt.show()
	return



def gradient_descent_totalvariation(imagename,time_steps=120):
	print(2*"\n"+"Total Variation Denoising"+2*"\n")
	IM = imread(imagename, flatten=True) * (1. / 255)
	IM_x, IM_y = IM.shape
	
	delta_t = 1e-3
	# delta_t = 5e-8
	delta_x, delta_y = 1./IM_x, 1./IM_y
	u = np.empty((2,IM_x,IM_y))
	u[1] = IM
	
	def total_variation(z):
		lmbda = 1.
		epsilon = 2e-7
		# Approximate first and second derivatives to second order accuracy.
		z_x = (np.roll(z,-1,axis=0) - np.roll(z,1,axis=0))/2. # (2.*delta_x)
		z_y	 = (np.roll(z,-1,axis=1) - np.roll(z,1,axis=1))/2. # (2.*delta_y)
		
		z_xy = (np.roll(z_x,-1,axis=1) - np.roll(z_x,1,axis=1))/2. # (2.*delta_y)
		z_yx = (np.roll(z_y,-1,axis=0) - np.roll(z_y,1,axis=0))/2. # (2.*delta_x)
		
		z_xx = (np.roll(z,-1,axis=0) - 2.*z + np.roll(z,1,axis=0))
		z_yy = (np.roll(z,-1,axis=1) - 2.*z + np.roll(z,1,axis=1))
		# Find approximation for the next time step, using a first order Euler step
		z[1:-1,1:-1] -= delta_t*(	lmbda*(z[1:-1,1:-1]-IM[1:-1,1:-1])
									  -(z_xx[1:-1,1:-1]*z_y[1:-1,1:-1]**2. + 
										z_yy[1:-1,1:-1]*z_x[1:-1,1:-1]**2. - 
										z_x[1:-1,1:-1]*z_y[1:-1,1:-1]*(z_xy[1:-1,1:-1] + z_yx[1:-1,1:-1])
										)/(
										(epsilon + z_x[1:-1,1:-1]**2. + z_y[1:-1,1:-1]**2.)**(3./2) )
										)
	
	
	
	def total_variation_properly_regularized(z): # Not yet working. 
		lmbda = .02
		epsilon = 3e-7
		# Approximate first and second derivatives to second order accuracy.
		z_x = (np.roll(z,-1,axis=0) - np.roll(z,1,axis=0))/2. # (2.*delta_x)
		z_y	 = (np.roll(z,-1,axis=1) - np.roll(z,1,axis=1))/2. # (2.*delta_y)
		
		z_xy = (np.roll(z_x,-1,axis=1) - np.roll(z_x,1,axis=1))/2. # (2.*delta_y)
		z_yx = (np.roll(z_y,-1,axis=0) - np.roll(z_y,1,axis=0))/2. # (2.*delta_x)
		
		z_xx = (np.roll(z,-1,axis=0) - 2.*z + np.roll(z,1,axis=0))
		z_yy = (np.roll(z,-1,axis=1) - 2.*z + np.roll(z,1,axis=1))
		# Find approximation for the next time step, using a first order Euler step
		z[1:-1,1:-1] -= delta_t*(	lmbda*(z[1:-1,1:-1]-IM[1:-1,1:-1])#*( (epsilon + z_x[1:-1,1:-1]**2. + z_y[1:-1,1:-1]**2.)**(3./2) )
									  -(z_xx[1:-1,1:-1]*((z_y[1:-1,1:-1]+epsilon)**2.) + 
										z_yy[1:-1,1:-1]*((z_x[1:-1,1:-1]+epsilon)**2.) - 
										(z_x[1:-1,1:-1]+epsilon)*(z_y[1:-1,1:-1]+epsilon)*(z_xy[1:-1,1:-1] + z_yx[1:-1,1:-1])
										)/ (
										((z_x[1:-1,1:-1] + epsilon)**2. + (z_y[1:-1,1:-1] + epsilon)**2.)**(2./2) )
								  )
		
		
	def total_variation_numexpr(z):
		lmbda = .02
		epsilon = 1e-8
		dt = delta_t
		
		# temporary arrays
		new_IM = IM.copy()
		znew = np.zeros(z.shape)
		z_x = np.zeros(z.shape)
		z_y = np.zeros(z.shape)
		
		# Approximate first and second derivatives to second order accuracy.
		z_N = np.roll(z,-1,axis=0)
		z_S = np.roll(z,1,axis=0)
		z_E = np.roll(z,-1,axis=1)
		z_W = np.roll(z,1,axis=1)
		
		ne.evaluate('.5*(z_N-z_S)', out=z_x)
		ne.evaluate('.5*(z_E-z_W)', out=z_y)
		
		numerator = np.zeros(z.shape)
		denominator = np.zeros(z.shape)
		# ne.evaluate('(z_N - 2*z + z_S)*(z_y*z_y) + (z_E - 2*z + z_W)*(z_x*z_x) - .5*z_x*z_y*(z_N + z_E - z_S - z_W)',out=numerator)
		# ne.evaluate('(epsilon + z_x**2. + z_y**2.)',out=denominator)
		# ne.evaluate('denominator**(3/2.)',out=denominator)
		ne.evaluate('(z_N - 2*z + z_S)*(z_y+epsilon)*(z_y+epsilon) + (z_E - 2*z + z_W)*(z_x+epsilon)*(z_x+epsilon) - .5*(z_x+epsilon)*(z_y+epsilon)*(z_N + z_E - z_S - z_W)',out=numerator)
		ne.evaluate('( (z_x+epsilon)**2. + (z_y+epsilon)**2.)',out=denominator)
		ne.evaluate('denominator**(2/2.)',out=denominator)
		
		ne.evaluate('z-dt*( lmbda*(z-new_IM) - numerator/denominator )',out=znew)
		z[1:-1,1:-1] = znew[1:-1,1:-1]
		
								
		
		
		
	def total_variation_fd1(z):
		lmbda = .05
		epsilon = 1e-7
		# Approximate first and second derivatives to first order accuracy.
		z_x = (np.roll(z,-1,axis=0) - np.roll(z,0,axis=0))
		z_y	 = (np.roll(z,-1,axis=1) - np.roll(z,0,axis=1))
		
		z_xy = (np.roll(z_x,-1,axis=1) - np.roll(z_x,0,axis=1))
		z_yx = (np.roll(z_y,-1,axis=0) - np.roll(z_y,0,axis=0))
		
		z_xx = (np.roll(z,-1,axis=0) - 2.*z + np.roll(z,1,axis=0))
		z_yy = (np.roll(z,-1,axis=1) - 2.*z + np.roll(z,1,axis=1))
		# Find approximation for the next time step, using a first order Euler step
		z[1:-1,1:-1] -= delta_t*(	lmbda*(z[1:-1,1:-1]-IM[1:-1,1:-1])
									  -(z_xx[1:-1,1:-1]*z_y[1:-1,1:-1]**2. + 
										z_yy[1:-1,1:-1]*z_x[1:-1,1:-1]**2. - 
										z_x[1:-1,1:-1]*z_y[1:-1,1:-1]*(z_xy[1:-1,1:-1] + z_yx[1:-1,1:-1])
										)/(
										(epsilon + z_x[1:-1,1:-1]**2. + z_y[1:-1,1:-1]**2.)**(3./2) )
										)
	
	# Time step until successive iterations are close
	iteration = 0
	while iteration < time_steps:
		total_variation(u[1])
		# total_variation_properly_regularized(u[1])
		# total_variation_numexpr(u[1])
		# total_variation_fd1(u[1])
		if norm(np.abs((u[0] - u[1]))) < 1e-4:#1e-6:
			break
		print(iteration, norm(np.abs((u[0] - u[1]))) )
		u[0] = u[1]
		iteration+=1
	
	imsave(name=("de"+imagename),arr=u[1])
	plt.imshow(u[1], cmap=cm.gray)
	plt.show()
	return



if __name__=="__main__":
	# example_text()
	# add_noise(imagename='baloons_resized_bw.jpg',changed_pixels=40000)
	# gradient_descent_heat('noised_baloons_resized_bw.jpg',time_steps=550)
	start = time()
	plot_image('lab_noised_baloons_resized_bw.jpg')
	gradient_descent_totalvariation('lab_noised_baloons_resized_bw.jpg',time_steps=220)
	print (time()- start), " seconds"