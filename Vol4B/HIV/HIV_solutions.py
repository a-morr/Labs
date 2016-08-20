
import numpy as np
from matplotlib import pyplot as plt

####### Parameters

# * = value comes from Kirschner and Webb
# ** = value comes from lab
a1, b1 = 0., 0.02 # boundaries for drug1 dosage
a2, b2 = 0., 0.9 # boundaries for drug2 dosage
s1, s2 = 2., 1.5 #source/proliferation constants*
mu = 0.002 #T cell death rate*
k = 0.000025 #infection rate*
g = 30. #input rate of an external virus source*
c = .007 #viral loss rate*
B1, B2 = 14.0, 1.0 #half saturation constants*
A1, A2 = 250000 , 75 # cost weights
T0 = 400 # initial number of T cells**
V0 = 3 #initial concentration of free viruses**
t_f = 50. # number of days
n = 1000 # number of time steps

def initialize_all(y0, t0, t, n):
    """ An initialization routine for the different ODE solving
    methods in the lab. This initializes Y, T, and h. """
    if isinstance(y0, np.ndarray):
        Y = np.empty((n, y0.size)).squeeze()
    else:
        Y = np.empty(n)
    Y[0] = y0
    T = np.linspace(t0, t, n)
    h = float(t - t0) / (n - 1)
    return Y, T, h

def RK4(f, y0, t0, t, n):
    """ Use the RK4 method to compute an approximate solution
    to the ODE y' = f(t, y) at n equispaced parameter values from t0 to t
    with initial conditions y(t0) = y0.
    
    y0 is assumed to be either a constant or a one-dimensional numpy array.
    t and t0 are assumed to be constants.
    f is assumed to accept two arguments.
    The first is a constant giving the value of t.
    The second is a one-dimensional numpy array of the same size as y.
    
    This function returns an array Y of shape (n,) if
    y is a constant or an array of size 1.
    It returns an array of shape (n, y.size) otherwise.
    In either case, Y[i] is the approximate value of y at
    the i'th value of np.linspace(t0, t, n).
    """
    Y,T,h = initialize_all(y0,t0,t,n)
    for i in xrange(n-1):
        K1 = f(T[i],Y[i],i)
        K2 = f(T[i]+h/2.,Y[i]+h/2.*K1,i)
        K3 = f(T[i]+h/2.,Y[i]+h/2.*K2,i)
        K4 = f(T[i+1],Y[i]+h*K3,i)
        Y[i+1] = Y[i] + h/6.*(K1+2*K2 +2*K3+K4)
    return Y

def state_equations(t,y,i):
    '''
    Parameters
    ---------------
    t : float
        the time
    y : ndarray (2,)
        the T cell concentration and the Virus concentration at time t
    i : int
        index for the global variable u.
    Returns
    --------------
    y_dot : ndarray (2,)
        the derivative of the T cell concentration and the virus concentration at time t
    '''
    yprime = np.empty(2)
    yprime[0] = s1 - s2*y[1]/(B1 + y[1]) - mu*y[0] - k*y[1]*y[0] + u[i,0]*y[0] # T prime
    yprime[1] = (g*(1-u[i,1])*y[1]) / (B2 + y[1]) - c*y[1]*y[0] # V prime
    return yprime

def lambda_hat(t,y,i):
    '''
    Parameters
    ---------------
    t : float
        the time
    y : ndarray (2,)
        the lambda_hat values at time t
    i : int
        index for global variables, u and state.
    Returns
    --------------
    y_dot : ndarray (2,)
        the derivative of the lambda_hats at time t.
    '''
    j = n-1-i
    yprime = np.empty(2)
    yprime[0] = -(-1 + y[0]*(mu+k*state[j,1] - u[j,0]) + y[1]*c*state[j,1])
    yprime[1] = -(y[0]*(B1*s2/((B1+state[j,1])**2) + k*state[j,0]) - 
              y[1]*(B2*g*(1-u[j,1])/((B2 + state[j,1])**2) - c*state[j,0]) )
    return yprime

delta = 0.001
test = delta + 1

t=np.linspace(0,t_f,n)

state = np.zeros((n,2))
state0 = np.array([T0, V0])

costate = np.zeros((n,2))
costate0 = np.zeros(2)

u=np.zeros((n,2))
u[:,0] += .02
u[:,1] += .9
while(test > delta): # see if we've converged
    oldu = u.copy();
    
    #solve the state equations with forward iteration
    state = RK4(state_equations,state0,0,t_f,n)
    
    #solve the costate equations with backwards iteration
    costate = RK4(lambda_hat,costate0,0,t_f,n)[::-1]
    
    #update our control
    temp1 = .5/A1*(costate[:,0]*state[:,0])
    temp2 = -.5*costate[:,1]/A2*g*state[:,1]/(B2 + state[:,1])
    u1 = np.minimum(np.maximum(a1*np.ones(temp1.shape),temp1),b1*np.ones(temp1.shape))
    u2 = np.minimum(np.maximum(a2*np.ones(temp2.shape),temp2),b2*np.ones(temp2.shape))
    u[:,0] = 0.5*(u1 + oldu[:,0])
    u[:,1] = 0.5*(u2 + oldu[:,1])
    
    test = abs(oldu - u).sum()

plt.subplot(221)
plt.plot(t,state[:,0])
plt.ylabel('T')
plt.subplot(222)
plt.plot(t,state[:,1])
plt.ylabel('V')
plt.subplot(223)
plt.plot(t,u[:,0])
plt.ylabel('u1')
plt.ylim([0,.022])
plt.xlabel('Days')
plt.subplot(224)
plt.plot(t,u[:,1])
plt.ylabel('u2')
plt.ylim([0,.92])
plt.xlabel('Days')
plt.show()
