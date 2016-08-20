#gaussquad16.py
'''
Shane McQuarrie		Math 347	22 January 2015
Lab 16: Gaussian Quadrature
'''

import numpy as np
from matplotlib import pyplot as plt
from math import sqrt, exp
from scipy.linalg import eig
from scipy.integrate import quad
from scipy.stats import norm

# ============================== PROBLEM 1 ============================== #

# Testing the integral (numerically) of the function x**2 and its shift.
def shift_test():
	def g(x):
		return (9.0/4.0)*x**2 + (15.0/2.0)*x + (25.0/4.0)
	def G(x):
		return (9.0/8.0)*x**3 + (45.0/8.0)*x**2 + (75.0/8.0)*x
	a = G(1)-G(-1)
	b = (4**3)/3.0 - 1/3.0
	if np.allclose(a,b):
		print "Success! G(1)-G(-1) = integral of x^2 from 1 to 4 = ",a
		return True
	else:
		print "FAILURE! a = ",a,", b = ",b
		return False

# function shifting problem
def shift_function(f, a, b):
	'''
	'f' is a callable function, 'a' and 'b' are
	the limits of the interval.
	Return the shifted function g.
	'''
	g = lambda x: f(((b-a)/2.)*x + (b+a)/2.)
	return g

# plotting for the example in the function shifting problem
def funcplot(f, a, b, n=401):
	'''
	Constructs and plots the example given in the
	problem on shifting the domain of a function to [-1, 1].
	'n' is the number of points to use to generate the plot.

	This def should plot f on [a,b] and the shifted function
	(b-a)/2*g on [-1,1]
	'''
	g = shift_function(f,a,b)
	X = np.linspace(a,b,n)
	plt.subplot(121)
	plt.plot(X,f(X),label='f(x)')
	plt.title('f(x)')
	plt.subplot(122)
	Y = np.linspace(-1,1,n)
	plt.plot(Y,g(Y)*(b-a)/2.0)
	plt.title('(b-a)g(x)/2')
	plt.suptitle('Function Shifting')
	plt.show()

# ============================== PROBLEM 2 ============================== #

# integral estimation problem
def estimate_integral(f, a, b, points, weights):
	'''
	Estimate the value of an integral given
	the function 'f', the interval bounds 'a' and 'b',
	the nodes to use for sampling, and their
	corresponding weights.

	Return:
	The value of the integral
	'''
	g = shift_function(f,a,b)
	return ((b-a)/2.) * np.inner(weights, g(points))

# ============================== PROBLEM 3 ============================== #

# Jacobi construction problem
def construct_jacobi(gamma, alpha, beta):
	'''
	Construct the Jacobi matrix given the
	sequences 'alpha', 'beta', and 'gamma' from the 
	three term recurrence relation.

	Return:
	The Jacobi matrix
	'''

	''' First attempt
	n = len(alpha)
	jac = np.zeros((n,n))
	b = np.sqrt(gamma[1]/(alpha[0]*alpha[1])) #initial b
	for i in xrange(n):
		jac[i,i] = -beta[0]/alpha[0] # diagonal
		if i > 0: jac[i,i-1] = b #subdiagonal
		if i < n-1:
			jac[i,i+1] = b #superdiagonal
			b = sqrt(gamma[i+1]/(alpha[i]*alpha[i+1]))
	return jac
	''' # Faster attempt
	n = len(alpha)
	jac = np.zeros((n,n))
	a = - beta / alpha
	b = np.sqrt(gamma[1:]/(alpha[:-1]*alpha[1:]))
	np.fill_diagonal(jac,a)
	np.fill_diagonal(jac[:,1:], b)
	np.fill_diagonal(jac[1:,:], b)
	return jac

# ============================== PROBLEM 4 ============================== #

# points and weights problem
def points_and_weights(n,p=False):
	'''
	Find the set of 'n' nodes and their
	corresponding weights for the interval [-1, 1].

	Return:
	The points and weights used to calculate the integral of the Legendre polynomials.
	Using scipy.linalg.eig(A) can help find eigenvalues and eigenvectors of A.
	'''
	alpha = np.zeros(n)
	beta = np.zeros(n)
	gamma = np.zeros(n)
	for i in np.arange(1,n+1,dtype='float'):#xrange(len(X)):
		alpha[i-1] = (2.*i - 1)/i
		beta[i-1] = 0
		gamma[i-1] = (i - 1)/i
	jac = construct_jacobi(gamma, alpha, beta)
	if p: print X,alpha,beta,gamma,jac
	evals, evecs = eig(jac)
	print evecs
	weights = [(evecs[i,0]**2)*2 for i in xrange(evecs.shape[0])]
	return evals, weights

# ============================== PROBLEM 5 ============================== #

# normal distribution cdf problem
def normal_cdf(x,p=False):
	'''
	Compute the CDF of the standard normal
	distribution at the point 'x'.
	'''
	f = lambda z: (1./np.sqrt(2.*np.pi))*np.e**((-z**2)/2.)
	answer = quad(f,-5,x)[0]
	if p and np.allclose(answer,norm.cdf(x)): print "Success!"
	return answer

# ============================== END OF FILE ============================== #

from numpy.random import randn

# Test script
def test(student_module):
    """Test script. Import the student's solutions file as a module.
    
     5 points for problem 2
    30 points for problem 6
     5 points for problem 7
    
    Inputs:
        student_module: the imported module for the student's file.
    
    Returns:
        score (int): the student's score, out of TOTAL.
        feedback (str): a printout of test results for the student.
    """
    tester = _testDriver()
    tester.test_all(student_module)
    return tester.score, tester.feedback

def _autoclose(func):
    """function decorator for closing figures automatically."""
    def wrapper(*args, **kwargs):
        try:
            plt.ion()
            return func(*args, **kwargs)
        finally:
            plt.close('all')
            plt.ioff()
    return wrapper

class _testDriver(object):
    """Class for testing a student's work. See test.__doc__ for more info."""

    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize the feedback attribute."""
        self.feedback = ""

    # Main routine -----------------------------------------------------------
    def test_all(self, student_module, total=40):
        """Grade the provided module on each problem and compile feedback."""
        # Reset feedback and score.
        self.feedback = ""
        self.score = 0

        def test_one(problem, number, value):
            """Test a single problem, checking for errors."""
            try:
                self.feedback += "\n\nProblem %d (%d points):"%(number, value)
                points = problem(student_module)
                self.score += points
                self.feedback += "\nScore += %d"%points
            except BaseException as e:
                self.feedback += "\n%s: %s"%(self._errType(e),e)

        # Grade each problem.
        test_one(self.problem2, 2, 5)   # Problem 1:  5 points.
        test_one(self.problem6, 6, 30)  # Problem 2: 30 points.
        test_one(self.problem7, 7, 5)   # Problem 2:  5 points.

        # Report final score.
        percentage = (100. * self.score) / total
        self.feedback += "\n\nTotal score: %d/%d = %s%%"%(
                                    self.score, total, percentage)
        if   percentage >=  98: self.feedback += "\n\nExcellent!"
        elif percentage >=  90: self.feedback += "\n\nGreat job!"

        # Add comments (optionally).
        print(self.feedback)
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += '\n\n\nComments:\n\t%s'%comments

    # Helper Functions --------------------------------------------------------
    @staticmethod
    def _errType(error):
        """Get just the name of the exception 'error' in string format."""
        if isinstance(error, BaseException):
            return str(type(error)).lstrip("<type 'exceptions.").rstrip("'>")
        else:
            return str(error)

    def _eqTest(self, correct, student, message):
        """Test to see if 'correct' and 'student' are equal.
        Report the given 'message' if they are not.
        """
        if abs(correct - student) < 1e-6:
            return 1
        else:
            self.feedback += "\n%s"%message
            self.feedback += "\n\tCorrect response: %s"%correct
            self.feedback += "\n\tStudent response: %s"%student
            return 0

    def _grade(self, points, message=None):
        """Manually grade a problem worth 'points'. Return the score."""
        credit = -1
        while credit > points or credit < 0:
            try:
                credit = int(input("\nScore out of %d: "%points))
            except:
                credit = -1
        if credit != points:
            # Add comments (optionally),
            comments = raw_input("Comments: ")
            if len(comments) > 0:
                self.feedback += "\n%s"%comments
            # Or add a predetermined error message.
            elif message is not None:
                self.feedback += "\n%s"%message
        return credit

    # Problems ----------------------------------------------------------------
    @_autoclose
    def problem2(self, s):
        """Test shift_example(). 5 points."""
        s.shift_example()
        return self._grade(5, "shift_example() failed")

    def problem6(self, s):
        """Test gaussian_quadrature(). 30 points."""
        f = lambda x: x**2
        points =  10*self._eqTest(21, s.gaussian_quadrature(f, 1, 4, 5),
                            "gaussian_quadrature() failed for f(x) = "
                            "x^2 over [1, 4]")
        
        g = lambda x: 4*x**3 - 3*x**2 + 2*x - 5
        points += 10*self._eqTest(46, s.gaussian_quadrature(g, 2, 3, 6),
                            "gaussian_quadrature() failed for f(x) = "
                            "4x^3 - 3x^2 + 2x - 5 over [2, 3]")

        h = lambda x: (x-5)**3
        points += 10*self._eqTest(0, s.gaussian_quadrature(h, 3, 7, 5),
                            "gaussian_quadrature() failed for f(x) = "
                            "x^2 - 2x + 1 over [3, 7]")
        return points

    def problem7(self, s):
        """Test normal_cdf(). 5 points."""
        points  = 2*self._eqTest(norm.cdf(1), s.normal_cdf(1),
                                        "normal_cdf(1) failed")
        x = randn()
        points += 3*self._eqTest(norm.cdf(x), s.normal_cdf(x),
                                        "normal_cdf(%f) failed"%x)
        return points
