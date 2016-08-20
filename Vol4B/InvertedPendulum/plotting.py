import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from scipy.linalg import inv
from scipy.optimize import root
from scipy.integrate import ode
from scipy import linalg as la
from scipy.misc import imread, imsave
plt.switch_backend('tkagg')


def linearized_init(M,m,l,q1,q2,q3,q4,r):
	g = 9.8
	A = np.array([[0.,1.,0.,0.],[0.,0.,1.*m*g/M,0.],[0.,0.,0.,1.],[0.,0.,1.*g/l*(1+1.*m/M),0.]])
	B = np.array([[0.],[1./M],[0.],[1./(M*l)]])
	Q = np.array([[q1,0.,0.,0.],[0.,q2,0.,0.],[0.,0.,q3,0.],[0.,0.,0.,q4]])
	R = np.array([[r]])
	return A,B,Q,R

def find_P(A,B,Q,R):
	R_inv = inv(R)
	def riccati(P):
		P = P.reshape((4,4))
		sol = P.dot(A)+A.T.dot(P)+Q-P.dot(B).dot(R_inv).dot(B.T).dot(P)
		return sol.reshape(16)
	P0 = np.ones(16)
	P1 = root(riccati,P0)
	print P1.success
	P = P1.x.reshape((4,4))
	return P

def rickshaw(tf,X0,A,B,Q,R_inv,P,plot_=True):
	t = np.linspace(0,tf,tf+1)
	dt = t[1]-t[0]
	def Xdot_f(t,X):
		return (A-B.dot(R_inv).dot(B.T).dot(P)).dot(X)
	evolve = ode(Xdot_f).set_integrator('dopri5')
	evolve.set_initial_value(X0,0)
	
	X = np.empty((tf+1,4))
	X[0] = X0
	u_coeff = -R_inv.dot(B.T).dot(P)
	U = np.empty(tf)
	iters = 1
	while evolve.successful() and evolve.t < tf:
		X[iters] = evolve.integrate(evolve.t+dt)
		U[iters-1] = u_coeff.dot(X[iters])
		iters += 1
	
	if plot_:
		plt.plot(t,X[:,0],'g',label='x')
		plt.plot(t,X[:,1],'r',label='dx')
		plt.plot(t,X[:,2],'k',label='theta')
		plt.plot(t,X[:,3],'b',label='dtheta')
		plt.plot(t[1:],U,'y',label='u')
		plt.axis([0,30,-40,40])
		plt.legend(loc='best')
		plt.savefig('sol.pdf')
		plt.show()
	
	return X,U


def my_rickshaw(t,X0,A,B,Q,R_inv,P,plot_=True):
	# t = np.linspace(0,tf,n)
	dt = t[1]-t[0]
	def Xdot_f(t,X):
		return (A-B.dot(R_inv).dot(B.T).dot(P)).dot(X)
	evolve = ode(Xdot_f).set_integrator('dopri5')
	# evolve.set_initial_value(X0,0)
	
	X = np.zeros((len(t),4))
	X[0] = X0
	u_coeff = -R_inv.dot(B.T).dot(P)
	# print "P = \n", P
	# print "u_coeff = ", u_coeff
	U = np.empty(t.shape)
	U[0] = 0
	iters = 1
	time = 0
	total_iters = len(t)
	while evolve.successful() and iters < total_iters:
		evolve.set_initial_value(X0,0)
		X[iters] = evolve.integrate(t[iters])
		U[iters] = u_coeff.dot(X[iters])
		time +=dt
		iters += 1
	
	if plot_:
		plt.rc("font", size=16)
		plt.plot(t,X[:,0],'g',linewidth=1.8,label='$x$')
		plt.plot(t,X[:,1],'r',linewidth=1.8,label='$\dot{x}$')
		plt.plot(t,X[:,2],'k',linewidth=1.8,label=r'$\theta$')
		plt.plot(t,X[:,3],'b',linewidth=1.8,label=r'$\dot{\theta}$')
		plt.plot(t[1:],U[1:],'y',linewidth=1.8,label='$u$')
		plt.xticks(size=12)
		plt.yticks(size=12)
		# plt.axis([0,t[-1],-15,5])
		plt.legend(loc='best')
		plt.savefig('mysol.pdf')
		plt.show()
		# print U[:5]
		# print X[:5,:]
	
	return X,U
	



def my_stochastic_rickshaw(t,X0,A,B,Q,R_inv,P,plot_=True):
	# t = np.linspace(0,tf,tf+1)
	dt = t[1]-t[0]
	def Xdot_f(t,X):
		return (A-B.dot(R_inv).dot(B.T).dot(P)).dot(X)
	evolve = ode(Xdot_f).set_integrator('dopri5')
	# evolve.set_initial_value(X0,0)
	
	X = np.zeros((len(t),4))
	X[0] = X0
	u_coeff = -R_inv.dot(B.T).dot(P)
	U = np.empty(t.shape)
	U[0] = 0
	iters = 1
	time = 0
	total_iters = len(t)
	while evolve.successful() and iters < total_iters:
		evolve.set_initial_value(X0,0)
		X[iters] = evolve.integrate(t[iters])
		U[iters] = u_coeff.dot(X[iters])
		time +=dt
		iters += 1
	
	if plot_:
		plt.plot(t,X[:,0],'g',label='$x$')
		plt.plot(t,X[:,1],'r',label='$dx$')
		plt.plot(t,X[:,2],'k',label='$\theta$')
		plt.plot(t,X[:,3],'b',label='dtheta')
		plt.plot(t[1:],U[1:],'y',label='u')
		plt.axis([0,t[-1],-15,5])
		plt.legend(loc='best')
		plt.savefig('mysol.pdf')
		plt.show()
	
	return X,U
	


def animate_rickshaw(l,X):
	scaling_xfactor = 40
	scaling_yfactor = 10
	
	import os; print os.getcwd()
	rick = plt.imread("rickshaw.png")
	# print "rick.shape = ", rick.shape
	rick = rick.mean(axis=2)
	rick[np.where(rick<=.9)] = 0
	rick[np.where(rick>.9)] = 1
	rick2 = np.argwhere(rick==0)
	ricky = -rick2[:,0]
	rickx = rick2[:,1]
	ricky -= ricky.min()
	rickx -= rickx.mean()
	rickx += 30
	
	present = plt.imread("present.png")
	print "present.shape = ", present.shape
	present[np.where(present<=.5)] = 0
	present[np.where(present>.5)] = 1
	present2 = np.argwhere(present==0)
	presenty = -present2[:,0]
	presentx = present2[:,1]
	presentx -= presentx.mean()
	presenty -= presenty.mean()
	
	assumedl = scaling_yfactor*l
	
	position = X[:,0]
	angle = X[:,2]
	rickshaw_height = 75
	tf = len(position)
	xpos = (position-np.sin(angle))
	ypos = (rickshaw_height+l+1-np.cos(angle))

	fig = plt.figure()
	ax = plt.axes(xlim=(scaling_xfactor*position.min()-150, scaling_xfactor*position.max()+150), ylim=(0, 250+assumedl))
	line, = ax.plot([], [],lw=0.00001)
	line.set_marker('o')
	line.set_markersize(.5)
	presenty += ypos[0]-50
	
	def init():
		line.set_data([], [])
		return line,
		
	def animate(i):				   
		x = np.linspace(scaling_xfactor*xpos[i],scaling_xfactor*xpos[i]-scaling_xfactor*np.sin(angle[i]),200)
		y = np.linspace(rickshaw_height,rickshaw_height+scaling_yfactor*ypos[i]-70*scaling_yfactor,200)
		
		xr = np.concatenate((rickx+x[0], presentx+x[-1],x))
		yr = np.concatenate((ricky,presenty+y[-1],y))
		
		line.set_data(xr, yr)
		return line,

	anim = animation.FuncAnimation(fig, animate, init_func=init,
							   frames=tf, interval=350, blit=True)
	plt.show()

def prob1():
	# Write the function linearized_init()
	pass

# def prob2():
# 	# Write the function find_P
# 	M = 10.
# 	m = 5.
# 	l = 7.
# 	q1,q2,q3,q4 = 1.,1.7,.1,0.
# 	r = 5.
# 	tf = 5#30
# 	X0 = np.array([5.,-.1,1.,-.4])
#
# 	A,B,Q,R = linearized_init(M,m,l,q1,q2,q3,q4,r)
# 	R_inv = inv(R)
# 	P = find_P(A,B,Q,R)
# 	RHS = A-B.dot(R_inv).dot(B.T).dot(P)
# 	print "The eigenvalues of $A - BR^{-1}B^TP are \n", la.eigvals(RHS)

def prob2():
	# Write the function find_P
	M, m = 23., 5.
	l = 4.
	q1, q2, q3, q4 = 1., 1., 1., 1.
	r = 5.
	# tf = 5#30
	# X0 = np.array([5.,-.1,1.,-.4])

	A,B,Q,R = linearized_init(M,m,l,q1,q2,q3,q4,r)
	R_inv = inv(R)
	P = find_P(A,B,Q,R)
	RHS = A-B.dot(R_inv).dot(B.T).dot(P)
	print "The eigenvalues of $A - BR^{-1}B^TP are \n", la.eigvals(RHS)

def prob3():
	# Write the function rickshaw()
	pass

# def prob3():
# 	M, m = 23., 5.
# 	l = 5.
# 	q1, q2, q3, q4 = .05,20,.5,.05
# 	r = 20
# 	tf = 100.
# 	X0 = np.array([1,.5,-.1,-.05])
#
# 	A,B,Q,R = linearized_init(M,m,l,q1,q2,q3,q4,r)
# 	P = la.solve_continuous_are(A,B,Q,R)
# 	R_inv = inv(R)
# 	X,U = my_rickshaw(np.linspace(0,tf,400),X0,A,B,Q,inv(R),P)

def prob4():
	# Write the function find_P
	M, m = 23., 5.
	l = 4.
	q1, q2, q3, q4 = 1., 1., 1., 1.
	r = 10.
	tf = 60
	X0 = np.array([-1, -1, .1, -.2])

	A,B,Q,R = linearized_init(M,m,l,q1,q2,q3,q4,r)
	R_inv = inv(R)
	# P = find_P(A,B,Q,R)
	# X,U = my_rickshaw(np.linspace(0,tf,400),X0,A,B,Q,inv(R),P)
	P = la.solve_continuous_are(A,B,Q,R)
	X,U = my_rickshaw(np.linspace(0,tf,400),X0,A,B,Q,inv(R),P)

def prob5():
	# Write the function find_P
	M, m = 23., 5.
	l = 4.
	q1, q2, q3, q4 = 1., 1., 1., 1.
	r = 10.
	tf = 60
	X0 = np.array([-1, -1, .1, -.2])

	A,B,Q,R = linearized_init(M,m,l,q1,q2,q3,q4,r)
	R_inv = inv(R)
	P = la.solve_continuous_are(A,B,Q,R)
	X,U = my_rickshaw(np.linspace(0,tf,400),X0,A,B,Q,inv(R),P)

	

if __name__ == "__main__":
	# prob2()
	# prob3()
	prob4()
	# prob5()

# M = 10.
# m = 5.
# l = 7.
# q1,q2,q3,q4 = 1.,1.7,.1,0.
# r = 5.
# tf = 5#30
# X0 = np.array([5.,-.1,1.,-.4])
#
# A,B,Q,R = linearized_init(M,m,l,q1,q2,q3,q4,r)
# P = find_P(A,B,Q,R)
# P = la.solve_continuous_are(A,B,Q,R)
# R_inv = inv(R)
# X,U = rickshaw(tf,X0,A,B,Q,R_inv,P)

# X,U = my_rickshaw(np.linspace(0,tf,400),X0,A,B,Q,inv(R),P)

# X,U = my_stochastic_rickshaw(t,X0,A,B,Q,R_inv,P,plot_=True)
# animate_rickshaw(l,X)
# prob5sol = [6.,1.7,.1,0.,5.]




