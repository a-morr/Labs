# solutions.py
"""Volume 2 Lab 14: Optimization Packages II (CVXOPT)"""

from cvxopt import matrix, solvers
import numpy as np
from scipy import linalg as la


def prob1():
    """Solve the following convex optimization problem:

    minimize        2x + y + 3z
    subject to      x + 2y          >= 3
                    2x + 10y + 3z   >= 10
                    x               >= 0
                    y               >= 0
                    z               >= 0

    Returns (in order):
        The optimizer x (ndarray)
        The optimal value (sol['primal objective'])
    """

    # Note that 'matrix' initializes by column, not row.
    c = matrix([2., 1., 3.])
    G = matrix(np.array([[-1.,-2.,0.],
                         [-2.,-10.,-3.],
                         [-1.,0.,0.],
                         [0.,-1.,0.],
                         [0.,0.,-1.]]))

    h = matrix([ -3., -10., 0., 0., 0.])
    sol = solvers.lp(c,G,h)
    return np.ravel(sol['x']), sol['primal objective']

    # Answers:
    # np.array([ -1.14760916e-09,   1.50000000e+00,   6.95278285e-11])
    # 1.4999999996249482

# Problem 2
def l1Min(A, b):
    """Calculate the solution to the optimization problem

        minimize    ||x||_1
        subject to  Ax = b

    Parameters:
        A ((m,n) ndarray)
        b ((m, ) ndarray)

    Returns:
        The optimizer x (ndarray), without any slack variables u
        The optimal value (sol['primal objective'])
    """

    assert A.shape[0] == b.shape[0], "mismatched dimensions"

    n = A.shape[1]
    I = np.eye(n, dtype=np.float)

    '''The optimization problem to solve is:

    minimize                [u]
                      [1 0] [x]

    subject to      [-I  I] [u]     [0]
                    [-I -I] [x]  <= [0]

                            [u]
                    [0   A] [x]  ==  b
    '''

    # Build the matrices for cvxopt (make sure dtype=np.floats)
    c = matrix(np.hstack((np.ones(n), np.zeros(n))).astype(np.float))
    G = matrix(np.vstack((np.hstack((-I, I)),np.hstack((-I, -I)))))
    h = matrix(np.zeros(2*n))
    new_A = matrix(np.hstack((np.zeros_like(A), A)).astype(np.float))
    new_b = matrix(b.astype(np.float))

    # Perform the optimization.
    sol = solvers.lp(c, G, h, new_A, new_b)

    # Flatten out the array and remove the u values.
    return np.ravel(sol['x'])[n:], sol['primal objective']


def prob3():
    """Solve the transportation problem by converting the last equality constraint
    into inequality constraints.

    Returns (in order):
        The optimizer x (ndarray)
        The optimal value (sol['primal objective'])
    """
    c = matrix([4., 7., 6., 8., 8., 9.])
    G = matrix(np.array([[-1.,0.,0.,0.,0.,0.],
                         [0.,-1.,0.,0.,0.,0.],
                         [0.,0.,-1.,0.,0.,0.],
                         [0.,0.,0.,-1.,0.,0.],
                         [0.,0.,0.,0.,-1.,0.],
                         [0.,0.,0.,0.,0.,-1.],
                         [0.,1.,0.,1.,0.,1.],
                         [0.,-1.,0.,-1.,0.,-1.]]))
    h = matrix([0.,0.,0.,0.,0.,0., 8., -8.])
    A = matrix(np.array([[1.,1.,0.,0.,0.,0.],
                         [0.,0.,1.,1.,0.,0.],
                         [0.,0.,0.,0.,1.,1.],
                         [1.,0.,1.,0.,1.,0.]]))
    b = matrix([7.,2.,4.,5.])
    sol = solvers.lp(c,G,h,A,b)  
    return np.ravel(sol['x']), sol['primal objective']

    # Answers:
    # np.array([[ 5.00e+00],[ 2.00e+00],[ -7.03e-09],
    #           [ 2.00e+00],[ -5.45e-09],[ 4.00e+00]])
    # 86


def prob4():
    """Find the minimizer and minimum of

    g(x,y,z) = (3/2)x^2 + 2xy + xz + 2y^2 + 2yz + (3/2)z^2 + 3x + z

    Returns (in order):
        The optimizer x (ndarray)
        The optimal value (sol['primal objective'])
    """
    P = matrix(np.array([[3.,2.,1.],
                         [2.,4.,2.],
                         [1.,2.,3.]]))

    q = matrix([3., 0., 1.])
    sol = solvers.qp(P, q)
    return np.ravel(sol['x']), sol['primal objective']

    # Answers:
    # np.array([[-1.50],[ 1.00],[-.5]])
    # -2.5


# Problem 5
def l2Min(A, b):
    """Calculate the solution to the optimization problem

        minimize    ||x||_2
        subject to  Ax = b

    Parameters:
        A ((m,n) ndarray)
        b ((m, ) ndarray)

    Returns:
        The optimizer x (ndarray)
        The optimal value (sol['primal objective'])
    """

    assert A.shape[0] == b.shape[0], "mismatched dimensions"

    n = A.shape[1]
    I = np.eye(n, dtype=np.float)

    '''The optimization problem to solve is:

        minimize              x*x
        subject to          A  =  b
    '''

    # Build the matrices for cvxopt (make sure dtype=np.floats)
    P = matrix(2*I)
    q = matrix(np.zeros(n))
    new_A = matrix(A.astype(np.float))
    new_b = matrix(b.astype(np.float))

    # Perform the optimization.
    sol = solvers.qp(P, q, A=new_A, b=new_b)

    # Flatten out the array and only get the x value.
    return np.ravel(sol['x']), sol['primal objective']


def prob6():
    """Solve the allocation model problem in 'ForestData.npy'.
    Note that the first three rows of the data correspond to the first
    analysis area, the second group of three rows correspond to the second
    analysis area, and so on.

    Returns (in order):
        The optimizer x (ndarray)
        The optimal value (sol['primal objective']*-1000)
    """
    data = np.load('ForestData.npy')

    c = matrix(data[:,3]*-1)

    A = la.block_diag(*[[1.,1.,1.] for _ in xrange(7)])
    b = data[::3,1].copy()

    G = np.vstack((-data[:,4], -data[:,5], -data[:,6], -np.eye(21))) # flip the inequality signs
    h = np.hstack(([-40000., -5., -70.*788.], np.zeros(21)))         # flip the inequality signs

    c = matrix(c)
    A = matrix(A)
    b = matrix(b)
    G = matrix(G)
    h = matrix(h)

    sol = solvers.lp(c,G,h,A,b)
    return np.ravel(sol['x']), sol['primal objective']*-1000.

    # Answers:
    # np.array([[ 1.41e-08],[ 6.76e-08],[ 7.50e+01],[ 9.00e+01],[ 1.28e-07],
    #           [ 2.52e-07],[ 1.40e+02],[ 4.18e-07],[ 5.52e-06],[ 1.04e-08],
    #           [ 8.94e-09],[ 6.00e+01],[ 1.23e-07],[ 1.54e+02],[ 5.80e+01],
    #           [ 3.16e-08],[ 3.58e-08],[ 9.80e+01],[ 1.63e-08],[ 9.12e-09],
    #           [ 1.13e+02]])
    # 322514998.983

''' # Generate the forest data.
forest=np.array([[1,75.,1,503.,310.,0.01,40],
[0,0,2,140,50,0.04,80],
[0,0,3,203,0,0,95],
[2,90.,1,675,198,0.03,55],
[0,0,2,100,46,0.06,60],
[0,0,3,45,0,0,65],
[3,140.,1,630,210,0.04,45],
[0,0,2,105,57,0.07,55],
[0,0,3,40,0,0,60],
[4,60.,1,330,112,0.01,30],
[0,0,2,40,30,0.02,35],
[0,0,3,295,0,0,90],
[5,212.,1,105,40,0.05,60],
[0,0,2,460,32,0.08,60],
[0,0,3,120,0,0,70],
[6,98.,1,490,105,0.02,35],
[0,0,2,55,25,0.03,50],
[0,0,3,180,0,0,75],
[7,113.,1,705,213,0.02,40],
[0,0,2,60,40,0.04,45],
[0,0,3,400,0,0,95]])
np.save('ForestData',forest)
'''

# END OF SOLUTIONS ============================================================

def test(student_module):
    """Test script. Import the student's solutions file as a module.
    
    10 points for problem 1
    10 points for problem 2
    10 points for problem 3
    10 points for problem 4
    10 points for problem 5
    20 points for problem 6
    
    Inputs:
        student_module: the imported module for the student's file.
    
    Returns:
        score (int): the student's score, out of 70.
        feedback (str): a printout of test results for the student.
    """
    tester = _testDriver()
    tester.test_all(student_module)
    return tester.score, tester.feedback


class _testDriver(object):
    """Class for testing a student's work. See test.__doc__ for more info."""

    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize the feedback attribute."""
        self.feedback = ""

    # Main routine -----------------------------------------------------------
    def test_all(self, student_module, total=70):
        """Grade the provided module on each problem and compile feedback."""
        # Reset feedback and score.
        self.feedback = ""
        self.score = 0

        def test_one(problem, number, value):
            """Test a single problem, checking for errors."""
            try:
                self.feedback += "\n\nProblem {} ({} points):".format(
                                                                number, value)
                points = problem(student_module)
                self.score += points
                self.feedback += "\nScore += {}".format(points)
            except BaseException as e:
                self.feedback += "\n{}: {}".format(self._errType(e), e)

        # Grade each problem.
        test_one(self.problem1, 1, 10)  # Problem 1: 10 points.
        test_one(self.problem2, 2, 10)  # Problem 2: 10 points.
        test_one(self.problem3, 3, 10)  # Problem 3: 10 points.
        test_one(self.problem3, 4, 10)  # Problem 4: 10 points.
        test_one(self.problem3, 5, 10)  # Problem 5: 10 points.
        test_one(self.problem4, 6, 20)  # Problem 6: 20 points.

        # Report final score.
        percentage = (100. * self.score) / total
        self.feedback += "\n\nTotal score: {}/{} = {}%".format(
                                    self.score, total, round(percentage, 2))
        if   percentage >=  98: self.feedback += "\n\nExcellent!"
        elif percentage >=  90: self.feedback += "\n\nGreat job!"

        # Add comments (optionally).
        print(self.feedback)
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += '\n\n\nComments:\n\t{}'.format(comments)

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
        if student is None:
            self.feedback += "\nFailed to return a value."
            return 0
        if np.allclose(correct, student, atol=1e-1, rtol=1e-1):
            return 1
        else:
            self.feedback += "\n{}".format(message)
            self.feedback += "\n\tCorrect response:\n{}".format(correct)
            self.feedback += "\n\tStudent response:\n{}".format(student)
            return 0

    # Problems ----------------------------------------------------------------
    def _test_problem(self, s, ans_1, ans_2, stu, index):
        """Test a problem with solutions 'ans' and submission 'stu'."""
        
        # Attempt to unpack the student's solutions values.
        try:
            stu_1, stu_2 = stu
        except (TypeError, ValueError):
            self.feedback += "\nprob{}() must return 2 values.".format(index)
            raise

        # Test the student's values against the true solution.
        points = 0
        points += 5*self._eqTest(ans_1, stu_1, "Incorrect optimizer")
        points += 5*self._eqTest(ans_2, stu_2, "Incorrect optimial value")
        print("PROBLEM {}: {}".format(index, points))
        return points

    def problem1(self, s):
        """Test prob1(). 10 points."""
        return self._test_problem(s,
                        np.array([[1.54643957],[ 1.20887997],[ 1.89941363]]),
                        10, s.prob1(), 1)

    # np.array([ -1.14760916e-09,   1.50000000e+00,   6.95278285e-11])
    # 1.4999999996249482

    def problem3(self, s):
        """Test prob3(). 10 points."""
        return self._test_problem(s,
                        np.array([[ 5.00e+00],[ 2.00e+00],[ -7.03e-08],
                                  [ 2.00e+00],[ -5.44e-09],[ 4.00e+00]]),
                        86, s.prob3(), 3)

    def problem4(self, s):
        """Test prob4(). 10 points."""
        return self._test_problem(s, np.array([[-1.50],[ 1.00],[-.5]]),
                        -2.5, s.prob4(), 4)

    def problem6(self, s):
        """Test prob6(). 20 points."""
        return 2*self._test_problem(s,
                        np.array([[ 1.41e-08],[ 6.76e-08],[ 7.50e+01],
                                  [ 9.00e+01],[ 1.28e-07],[ 2.52e-07],
                                  [ 1.40e+02],[ 4.18e-07],[ 5.52e-06],
                                  [ 1.04e-08],[ 8.94e-09],[ 6.00e+01],
                                  [ 1.23e-07],[ 1.54e+02],[ 5.80e+01],
                                  [ 3.16e-08],[ 3.58e-08],[ 9.80e+01],
                                  [ 1.63e-08],[ 9.12e-09],[ 1.13e+02]]),
                        322514998.983, s.prob6(), 6)

# END OF FILE =================================================================
