import numpy as np
cimport numpy as np
# from libc.math cimport fabs, exp, fmin, fmax, sqrt
from scipy.misc import imread, imsave
# cimport cython

np.set_printoptions(precision=15)
norm = np.linalg.norm
# 
def gradient_descent_heat(str imagename,int time_steps=120):
	print 2*"\n"+"Diffusion Based Denoising"+2*"\n"
	# Read the image file imagename.
	# Multiply by 1. / 255 to change the values so that they are floating point
	# numbers ranging from 0 to 1.
	# cdef np.ndarray[dtype=double, ndim=2] IM
	IM = (imread(imagename, flatten=True) * (1. / 255))
	print IM.dtype
	cdef int IM_x, IM_y 
	IM_x, IM_y = IM.shape

	cdef double delta_t = 1e-3 # 5e-8
	# delta_x, delta_y = 1./IM_x, 1./IM_y
	# lmbda = 1.
	cdef np.ndarray[dtype=double, ndim=3] u = np.empty((2,IM_x,IM_y))
	u[1] = IM

	# cdef heat_v1(np.ndarray[dtype=double, ndim=2] z,np.ndarray[dtype=float, ndim=2] IM, double delta_t, ):
	# 	cdef double lmbda = 50.
	# 	# Approximate first and second derivatives to second order accuracy.
	# 	# cdef np.ndarray[dtype=double, ndim=2] z_xx, z_yy
	# 	# Find approximation for the next time step, using a first order Euler step
	# 	# z_xx = (np.roll(z,-1,axis=0) - 2.*z + np.roll(z,1,axis=0))
	# 	# z_yy = (np.roll(z,-1,axis=1) - 2.*z + np.roll(z,1,axis=1))
	# 	# z[1:-1,1:-1] -= delta_t*(   (z[1:-1,1:-1]-IM[1:-1,1:-1])
	# 	# 							-lmbda*(z_xx[1:-1,1:-1] + z_yy[1:-1,1:-1]))
	# 	# z_xx = (z[2:,1:-1] - 2.*z[1:-1,1:-1] + z[1:-1,:-2])
	# 	# z_yy = (z[1:-1,2:] - 2.*z[1:-1,1:-1] + z[:-2,1:-1])
	# 	# z[1:-1,1:-1] -= delta_t*(   (z[1:-1,1:-1]-IM[1:-1,1:-1])
	# 	# 							-lmbda*(z_xx + z_yy))
	#
	# 	z[1:-1,1:-1] -= delta_t*(   (z[1:-1,1:-1]-IM[1:-1,1:-1])
	# 								-lmbda*(z[2:,1:-1] + z[1:-1,:-2] +
	# 								z[1:-1,2:] + z[:-2,1:-1] -
	# 								4.*z[1:-1,1:-1] )
	# 							)
	# 	return

	# Time step until successive iterations are close
	cdef int iteration = 0
	while iteration < time_steps:
		heat_v1(u[1],IM,delta_t)
		if norm(np.abs((u[0] - u[1]))) < 1e-6: break
		# print iteration, norm(np.abs((u[0] - u[1])))
		u[0] = u[1]
		iteration+=1

	imsave(name=("de"+imagename),arr=IM)
	return


cdef heat_v1(np.ndarray[dtype=double, ndim=2] z,np.ndarray[dtype=float, ndim=2] IM, double delta_t, ):
	cdef double lmbda = 50.
	# Approximate first and second derivatives to second order accuracy.
	# cdef np.ndarray[dtype=double, ndim=2] z_xx, z_yy
	# Find approximation for the next time step, using a first order Euler step
	# z_xx = (np.roll(z,-1,axis=0) - 2.*z + np.roll(z,1,axis=0))
	# z_yy = (np.roll(z,-1,axis=1) - 2.*z + np.roll(z,1,axis=1))
	# z[1:-1,1:-1] -= delta_t*(   (z[1:-1,1:-1]-IM[1:-1,1:-1])
	# 							-lmbda*(z_xx[1:-1,1:-1] + z_yy[1:-1,1:-1]))
	# z_xx = (z[2:,1:-1] - 2.*z[1:-1,1:-1] + z[1:-1,:-2])
	# z_yy = (z[1:-1,2:] - 2.*z[1:-1,1:-1] + z[:-2,1:-1])
	# z[1:-1,1:-1] -= delta_t*(   (z[1:-1,1:-1]-IM[1:-1,1:-1])
	# 							-lmbda*(z_xx + z_yy))
	
	z[1:-1,1:-1] -= delta_t*(   (z[1:-1,1:-1]-IM[1:-1,1:-1])
								-lmbda*(z[2:,1:-1] + z[1:-1,:-2] + 
								z[1:-1,2:] + z[:-2,1:-1] -
								4.*z[1:-1,1:-1] )
							)
	return
#
# def gradient_descent_totalvariation(imagename,time_steps=120):
# 	print 2*"\n"+"Total Variation Denoising"+2*"\n"
# 	# Read the image file imagename.
# 	# Multiply by 1. / 255 to change the values so that they are floating point
# 	# numbers ranging from 0 to 1.
# 	IM = imread(imagename, flatten=True) * (1. / 255)
# 	IM_x, IM_y = IM.shape
#
# 	delta_t = 1e-3
# 	# delta_t = 5e-8
# 	delta_x, delta_y = 1./IM_x, 1./IM_y
# 	u = np.empty((2,IM_x,IM_y))
# 	u[1] = IM
#
# 	def total_variation(z):
# 		lmbda = 1.
# 		epsilon = 2e-7
# 		# Approximate first and second derivatives to second order accuracy.
# 		z_x = (np.roll(z,-1,axis=0) - np.roll(z,1,axis=0))/2. # (2.*delta_x)
# 		z_y  = (np.roll(z,-1,axis=1) - np.roll(z,1,axis=1))/2. # (2.*delta_y)
#
# 		z_xy = (np.roll(z_x,-1,axis=1) - np.roll(z_x,1,axis=1))/2. # (2.*delta_y)
# 		z_yx = (np.roll(z_y,-1,axis=0) - np.roll(z_y,1,axis=0))/2. # (2.*delta_x)
#
# 		z_xx = (np.roll(z,-1,axis=0) - 2.*z + np.roll(z,1,axis=0))
# 		z_yy = (np.roll(z,-1,axis=1) - 2.*z + np.roll(z,1,axis=1))
# 		# Find approximation for the next time step, using a first order Euler step
# 		z[1:-1,1:-1] -= delta_t*(   lmbda*(z[1:-1,1:-1]-IM[1:-1,1:-1])
# 									  -(z_xx[1:-1,1:-1]*z_y[1:-1,1:-1]**2. +
# 										z_yy[1:-1,1:-1]*z_x[1:-1,1:-1]**2. -
# 										z_x[1:-1,1:-1]*z_y[1:-1,1:-1]*(z_xy[1:-1,1:-1] + z_yx[1:-1,1:-1])
# 										)/(
# 										(epsilon + z_x[1:-1,1:-1]**2. + z_y[1:-1,1:-1]**2.)**(3./2) )
# 										)
#
#
# 	def total_variation_fd1(z):
# 		lmbda = 1.
# 		epsilon = 2e-7
# 		# Approximate first and second derivatives to first order accuracy.
# 		z_x = (np.roll(z,-1,axis=0) - np.roll(z,0,axis=0))
# 		z_y  = (np.roll(z,-1,axis=1) - np.roll(z,0,axis=1))
#
# 		z_xy = (np.roll(z_x,-1,axis=1) - np.roll(z_x,0,axis=1))
# 		z_yx = (np.roll(z_y,-1,axis=0) - np.roll(z_y,0,axis=0))
#
# 		z_xx = (np.roll(z,-1,axis=0) - 2.*z + np.roll(z,1,axis=0))
# 		z_yy = (np.roll(z,-1,axis=1) - 2.*z + np.roll(z,1,axis=1))
# 		# Find approximation for the next time step, using a first order Euler step
# 		z[1:-1,1:-1] -= delta_t*(   lmbda*(z[1:-1,1:-1]-IM[1:-1,1:-1])
# 									  -(z_xx[1:-1,1:-1]*z_y[1:-1,1:-1]**2. +
# 										z_yy[1:-1,1:-1]*z_x[1:-1,1:-1]**2. -
# 										z_x[1:-1,1:-1]*z_y[1:-1,1:-1]*(z_xy[1:-1,1:-1] + z_yx[1:-1,1:-1])
# 										)/(
# 										(epsilon + z_x[1:-1,1:-1]**2. + z_y[1:-1,1:-1]**2.)**(3./2) )
# 										)
#
# 	# Time step until successive iterations are close
# 	iteration = 0
# 	while iteration < time_steps:
# 		total_variation(u[1])
# 		# total_variation_fd1(u[1])
# 		if norm(np.abs((u[0] - u[1]))) < 1e-6:
# 			break
# 		print iteration, norm(np.abs((u[0] - u[1])))
# 		u[0] = u[1]
# 		iteration+=1
#
# 	imsave(name=("de"+imagename),arr=u[1])
# 	return
#
#
#
