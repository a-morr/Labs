# plots.py. IVP Lab
from __future__ import print_function, division
import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../matplotlibrc')

import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from scipy.integrate import ode
from solutions import euler, midpoint, RK4
import solutions
from solutions import *

def problem_euler():
# Figure #2 in the Lab: The solution of y'=y-2x+4, y(0)=0, is
# y(x) = -2 + 2x + (ya + 2)e^x. This code plots the solution for 0<x<2,
# and then plots the approximation given by Euler's method
# Text Example
	a, b, ya = 0.0, 2.0, 0.0
	def f(x,ya=0.):
		return -2. + 2.*x + (ya + 2.)*np.exp(x)

	def ode_f(x,y):
		return np.array([1.*y -2.*x + 4.])


	plt.plot(np.linspace(a,b,11), euler(ode_f,ya,a,b,11) , 'b-',label="h = 0.2")
	plt.plot(np.linspace(a,b,21), euler(ode_f,ya,a,b,21) , 'g-',label="h = 0.1")
	plt.plot(np.linspace(a,b,41), euler(ode_f,ya,a,b,41) , 'r-',label="h = 0.05")

	x = np.linspace(0,2,200); k =int(200/40)
	plt.plot(x[::k], f(x[::k]), 'k*-',label="Solution") # The solution
	plt.plot(x[k-1::k], f(x[k-1::k]), 'k-') # The solution

	plt.legend(loc='best')
	plt.xlabel('x'); plt.ylabel('y')
	# plt.savefig('prob1.pdf')
	plt.show()
	plt.clf()
	return

def lab_example():
# Figure 1 in the lab.
# Integral curves for y' = sin y using dopri5
	a, b, n = 0.0, 5.0, 50
	k, x= n//10, np.linspace(a,b,n+1)
	def ode_f3(x,y):
		return np.array([np.sin(y)])

	def dopri5_integralcurves(ya):
			test1 = ode(ode_f3).set_integrator('dopri5',atol=1e-7,rtol=1e-8,nsteps=500)
			y0 = ya; x0 = a; test1.set_initial_value(y0,x0)
			Y = np.zeros(x.shape); Y[0] = y0
			for j in range(1,len(x)):
					test1.integrate(x[j])
					Y[j]= test1.y
			return Y

	plt.plot(x[::k], dopri5_integralcurves(5.0*np.pi/2.0)[::k], 'k-')
	plt.plot(x[::k], dopri5_integralcurves(3.0*np.pi/2.0)[::k], 'k-')
	plt.plot(x[::k], dopri5_integralcurves(7.0*np.pi/4.0)[::k], 'k-')
	plt.plot(x[::k], dopri5_integralcurves(0.0*np.pi/2.0)[::k], 'k*-')
	plt.plot(x[::k], dopri5_integralcurves(-np.pi)[::k], 'k*-',label='Equilibrium solutions')
	plt.plot(x[::k], dopri5_integralcurves(np.pi)[::k], 'k*-')
	plt.plot(x[::k], dopri5_integralcurves(2*np.pi)[::k], 'k*-')
	plt.plot(x[::k], dopri5_integralcurves(3*np.pi)[::k], 'k*-')
	plt.plot(x[::k], dopri5_integralcurves(np.pi/4.0)[::k], 'k-')
	plt.plot(x[::k], dopri5_integralcurves(np.pi/2.0)[::k], 'k-')
	plt.plot(x[::k], dopri5_integralcurves(-np.pi/2.0)[::k], 'k-')
	plt.legend(loc='best')
	plt.xlabel('x')
	plt.ylabel('y')
	# plt.savefig('example.pdf')
	plt.show()
	plt.clf()


def example_relative_error():
	# Figure 3 in the lab.
	a, b, ya = 0., 2., 0.

	def ode_f(x,y):
		return np.array([1.*y -2.*x + 4.])

	best_grid = 320					#  number of subintervals in most refined grid
	best_val = euler(ode_f,ya,a,b,best_grid)[-1]
	smaller_grids = [10,20,40,80]  # number of subintervals in smaller grids
	h = [2./N for N in smaller_grids]
	Euler_sol = [euler(ode_f,ya,a,b,N)[-1] for N in smaller_grids]
	Euler_error = [abs(( val - best_val)/best_val ) for val in Euler_sol]

	plt.loglog(h, Euler_error, '-b', label="Euler method"	  , linewidth=2.)
	# plt.xlabel("$h$", fontsize=16)
	# plt.ylabel("Relative Error", fontsize = 16)
	# plt.legend(loc='best')
	plt.show()
	plt.clf()


def problem_relative_error():
	# Figure 3 in the lab.
	a, b, ya = 0., 2., 0.
	def f(x,ya):
		return -2. + 2.*x + 2.*np.exp(x)

	def ode_f(x,y):
		return np.array([1.*y -2.*x + 4.])

	N = np.array([10,20,40,80,160])	 # Number of subintervals
	Euler_sol, Mid_sol, RK4_sol = np.zeros(len(N)), np.zeros(len(N)), np.zeros(len(N))
	for j in range(len(N)):
			Euler_sol[j] = euler(ode_f,ya,a,b,N[j])[-1]
			Mid_sol[j] = midpoint(ode_f,ya,a,b,N[j])[-1]
			RK4_sol[j] = RK4(ode_f,ya,a,b,N[j])[-1]

	h = 2./N
	plt.loglog(h, abs(( Euler_sol - f(2.,0.))/f(2.,0.) ), '-b', label="Euler method"   , linewidth=2.)
	plt.loglog(h, abs(( Mid_sol - f(2.,0.))/f(2.,0.) ),	  '-g', label="Midpoint method", linewidth=2. )
	plt.loglog(h, abs(( RK4_sol - f(2.,0.))/f(2.,0.) ),	  '-k', label="Runge Kutta 4"  , linewidth=2. )
	plt.xlabel("$h$", fontsize=16)
	plt.ylabel("Relative Error", fontsize = 16)
	# plt.title("loglog plot of relative error in approximation of $y(2)$.")
	plt.legend(loc='best')
	# plt.savefig('relative_error.pdf')
	plt.show()
	plt.clf()



def problem_quadrature():
	str = """	When y' = f(t,y) = f(t), these IVP methods are well known quadrature methods.
	Euler's method corresponds to the left hand sum.
	Backward Euler's method corresponds to the right hand sum.
	Modified Euler's method corresponds to the trapezoidal rule.
	The midpoint method corresponds to the midpoint rule.
	RK4 corresponds to Simpson's rule."""
	print(str)
	return


def harmonic_oscillator_ode(t,y,m,gamma,k,F):
	return np.array([ y[1], -gamma*y[1]/m -k*y[0]/m+F(t)/m ])




def problem_simple_oscillator():
# Parameters
	a, b, ya = 0.0, 20.0, np.array([2., -1.])

	m , gamma, k, F = 3., 0., 1.,lambda x: 0.

	func1 = lambda x,y: harmonic_oscillator_ode(x,y,m,gamma,k,F)
	Y1 = RK4(func1,ya,a,b,801) # 2 dimensional system
	plt.plot(np.linspace(a,b,801), Y1[:,0], '-k',label="$m=3$",linewidth=2.)

	m , gamma, k, F = 1, 0, 1,lambda x: 0
	func2 = lambda x,y: harmonic_oscillator_ode(x,y,m,gamma,k,F)
	Y2 = RK4(func2,ya,a,b,801)
	plt.plot(np.linspace(a,b,801), Y2[:,0], '-b',label="$m=1$",linewidth=2.)

	###################################################
	#	# Computing relative error of approximation	  #
	# m , gamma, k, F = 3., 0., 1.,lambda x: 0.
	# Need about 70 subintervals to get Relative error< 5*10^{-5}
	# Y_coarse = RK4(func1,ya,a,b,70)

	# Relative_Error = np.abs(Y_coarse[-1,0] - Y1[-1,0])/np.abs(Y1[-1,0])
	# print("Relative Error = ", Relative_Error)
	###################################################
	plt.axhline(color='k',linestyle='-')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.legend(loc='best')
	# plt.savefig('simple_oscillator.pdf')
	plt.show()
	plt.clf()


def problem_damped_free_oscillator():
	a, b, ya = 0.0, 20.0, np.array([1., -1.])		# Parameters
	# Needs about 180 subintervals to achieve Rel Error < 5*10**(-5)

# Damped Oscillators
	def plot_function(param,color):
			func = lambda x,y: harmonic_oscillator_ode(x,y,m=1.,gamma=param,k=1.,F=lambda x: 0.)
			Y = RK4(func,ya,a,b,801)
			plt.plot(np.linspace(a,b,801), Y[:,0], color,linestyle='-',linewidth=2.0)
			Relative_Error = np.abs( Y[-1,0] - RK4(func,ya,a,b,180)[-1,0] )/np.abs(Y[-1,0])
			print("Relative Error = ", Relative_Error)
			return


	plot_function(.5,'k')
	plot_function(1.,'b')

	plt.axhline(color='k',linestyle='-')
	plt.xlabel('x')
	plt.ylabel('y')
	# plt.savefig('Exercise5.pdf')
	plt.show()
	plt.clf()


def problem_damped_forced_oscillator():
# Parameters: Interval = [a,b], n = number of subintervals, ya = y(a)
	a, b, n, ya = 0.0, 40.0, 600, np.array([2., -1.])
	m, k = 2., 2.

# A Forced Oscillator with Damping: m*y'' + gamma*y' + k*y = F(x)
# Requires about 300 subintervals for Rel Error < 5*10**(-5)
	def print_func(gamma, omega):
			func = lambda x,y: harmonic_oscillator_ode(x,y,m,gamma,k,lambda x: 2.*np.cos(omega*x))
			Y = RK4(func,ya,a,b,n)
			Relative_Error = np.abs(Y[-1,0] - RK4(func,ya,a,b,n//2)[-1,0])/np.abs(Y[-1,0])
			print("Relative Error = ", Relative_Error)
			return np.linspace(a,b,n), Y[:,0]




	x1,y1 = print_func(.5,1.5)
	x2,y2 = print_func(.1,1.1)
	x3,y3 = print_func(0.,1.)

	plt.plot(x1,y1, '-k',linewidth=2.0,label='$\gamma=.5,\, \omega=1.5$')
	plt.plot(x2,y2, '-b',linewidth=2.0,label='$\gamma=.1,\, \omega=1.1$')
	plt.plot(x3,y3, '-g',linewidth=2.0,label='$\gamma=0,\, \omega=1$')



	plt.legend(loc='best')
	plt.axhline(color='k',linestyle='-')
	plt.xlabel('x')
	plt.ylabel('y')
	# plt.savefig('damped_forced_oscillator.pdf')
	plt.show()
	plt.clf()





def example_comparisons():
	a, b = 0., 8.
	ya = 1.
	ans = np.exp(np.sin(8))
	# a, b = 0., 1.
	# ya = np.array([1,1.])

	from math import cos
	A = np.array([[-80.6,119.4],[79.6,-120.4]])

	def f(x,y):
		return A.dot(y)

	def ode_f(x,y):
		return np.array([y*cos(x)])

	def return_error(method,func,iter):
		# Array containing number of subintervals to use in each approximation
		N = np.array([10*2**j for j in range(iter)])
		solutions = [0]*(iter-1)
		error = [0]*(iter-1)

		for i,n in enumerate(N[:-1]):
			# Return solution at last time value for each discretization.
			solutions[i] = method(func,ya,a,b,n)[-1]

		# Use the most refined grid to obtain a value of y(1) that is closest to the true
		# solution. This value will be used to approximate the relative error of the
		# approximation on less refined grids.
		# best_solution = method(func,ya,a,b,N[-1])[-1]

		for j in range(len(error)):
			error[j] = norm((solutions[j]-ans))/norm(ans)
		# print solutions
		return N[:-1], error


	N_rk4, error_rk4 = return_error(RK4,ode_f,16)
	# N_euler, error_euler = return_error(euler,ode_f,2)
	# N_midpoint, error_midpoint = return_error(midpoint,ode_f,2)

	# N_rk4, error_rk4 = return_error(RK4,f,14)
	# N_euler, error_euler = return_error(euler,f,21)
	# N_midpoint, error_midpoint = return_error(midpoint,f,19)
	#
	# print(error_rk4)
	# print(error_euler)
	# print(error_midpoint)
	#
	N_euler = np.array([10*2**j for j in range(37)])
	euler_data = np.loadtxt('euler.txt')
	error_euler = abs((euler_data-ans)/ans)
	print(np.shape(error_euler))

	N_midpoint = np.array([10*2**j for j in range(28)])
	midpoint_data = np.loadtxt('midpoint.txt')
	error_midpoint = abs((midpoint_data-ans)/ans)
	print(midpoint_data)

	# Plot number of function evaluations versus relative error
	# Function Evaluations = # of subintervals * 4
	plt.loglog(4*N_rk4,error_rk4,'-k',label="RK4")
	plt.loglog(N_euler,error_euler,'-g',label='Euler')
	plt.loglog(2*N_midpoint,error_midpoint,'-b',label="Midpoint")
	plt.ylabel("Relative Error", fontsize=16)
	plt.xlabel("Functional Evaluations", fontsize = 16)
	plt.legend(loc='best')
	plt.savefig('Efficiency.pdf')
	plt.show()
	plt.clf()


if __name__ == "__main__":
	# lab_example()				# Produces Figure 1 in the lab
	# problem_euler()			# Produces Figure 2 in the lab
	# problem_relative_error()	# Produces Figure 3 in the lab
	example_relative_error()
	# problem_quadrature()
	# problem_simple_oscillator()
	# problem_damped_free_oscillator()
	# problem_damped_forced_oscillator()

	# example_comparisons()
