# testDriver.py
"""Volume 1A: QR 2 (Least Squares and Computing Eigenvalues). Test driver."""

# Decorators ==================================================================

import signal
from functools import wraps
from matplotlib import pyplot as plt

def _autoclose(func):
    """Decorator for closing figures automatically."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            plt.ion()
            return func(*args, **kwargs)
        finally:
            plt.close('all')
            plt.ioff()
    return wrapper

def _timeout(seconds):
    """Decorator for preventing a function from running for too long.

    Inputs:
        seconds (int): The number of seconds allowed.

    Notes:
        This decorator uses signal.SIGALRM, which is only available on Unix.
    """
    assert isinstance(seconds, int), "@timeout(sec) requires an int"

    class TimeoutError(Exception):
        pass

    def _handler(signum, frame):
        """Handle the alarm by raising a custom exception."""
        message = "Timeout after {} seconds".format(seconds)
        print(message)
        raise TimeoutError(message)


    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handler)
            signal.alarm(seconds)               # Set the alarm.
            try:
               return func(*args, **kwargs)
            finally:
                signal.alarm(0)                 # Turn the alarm off.
        return wrapper
    return decorator

# Test Driver =================================================================

import numpy as np
from scipy import linalg as la
from inspect import getsourcelines

np.set_printoptions(precision=3, suppress=True)

def test(student_module):
    """Grade a student's entire solutions file.

     5 points for problem 1
     5 points for problem 2
     5 points for problem 3
     5 points for problem 4
    10 points for problem 5
    10 points for problem 6

    Inputs:
        student_module: the imported module for the student's file.

    Returns:
        score (int): the student's score, out of 40.
        feedback (str): a printout of test results for the student.
    """
    tester = _testDriver()
    tester.test_all(student_module)
    return tester.score, tester.feedback


class _testDriver(object):
    """Class for testing a student's work.

    Attributes:
        Score (int)
        Feedback (str)
    """

    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize the feedback attribute."""
        self.feedback = ""

    # Main routine ------------------------------------------------------------
    def test_all(self, student_module, total=40):
        """Grade the provided module on each problem and compile feedback."""
        # Reset feedback and score.
        self.feedback = ""
        self.score = 0

        def test_one(problem, label, value):
            """Test a single problem, checking for errors."""
            try:
                self.feedback += "\n\n{} ({} points):".format(label, value)
                points = problem(student_module)
                self.score += points
                self.feedback += "\nScore += {}".format(points)
            except BaseException as e:
                self.feedback += "\n{}: {}".format(self._errType(e), e)

        # Grade each problem.
        test_one(self.problem1, "Problem 1",  5)   # Problem 1:  5 points.
        test_one(self.problem2, "Problem 2",  5)   # Problem 2:  5 points.
        test_one(self.problem3, "Problem 3",  5)   # Problem 3:  5 points.
        test_one(self.problem4, "Problem 4",  5)   # Problem 4:  5 points.
        test_one(self.problem5, "Problem 5", 10)   # Problem 5: 10 points.
        test_one(self.problem6, "Problem 6", 10)   # Problem 6: 10 points.

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
        return str(type(error).__name__)

    def _checkCode(self, func, keyword):
        """Check a function's source code for a key word. If the word is found,
        print the code to the screen and prompt the grader to check the code.
        Use this function to detect cheating. Returns a score out of 10.
        """
        code = getsourcelines(func)[0][len(func.__doc__.splitlines())+1 :]
        if any([keyword in line for line in code]):
            print("\nStudent {}() code:\n{}\nCheating? [OK=10, Bad=0]".format(
                                                func.__name__, "".join(code)))
            return self._grade(10)
        return 10

    def _eqTest(self, correct, student, message):
        """Test to see if 'correct' and 'student' are equal.
        Report the given 'message' if they are not.
        """
        if np.allclose(correct, student):
            return 1
        else:
            self.feedback += "\n{}".format(message)
            self.feedback += "\n\tCorrect response:\n{}".format(correct)
            self.feedback += "\n\tStudent response:\n{}".format(student)
            return 0

    def _grade(self, points, message=None):
        """Manually grade a problem worth 'points'. Return the score.
        If full points are not earned, get feedback on the problem.
        """
        credit = -1
        while credit > points or credit < 0:
            try:
                credit = int(input("\nScore out of {}: ".format(points)))
            except:
                credit = -1
        if credit != points:
            # Add comments (optionally),
            comments = raw_input("Comments: ")
            if len(comments) > 0:
                self.feedback += "\n{}".format(comments)
            # Or add a predetermined error message.
            elif message is not None:
                self.feedback += "\n{}".format(message)
        return credit

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test least_squares(). 5 points."""

        @_timeout(2)
        def _test(m,n,p):
            """Do an mxn test case worth p points."""
            A = np.random.random((m,n))
            b = np.random.random(m)
            return p * self._eqTest(la.lstsq(A,b)[0], s.least_squares(A,b),
                        "least_squares(A, b) failed for A.shape = {}, "
                        "b.shape = {}".format(A.shape, b.shape))

        points = _test(5, 2, 1) + _test(10, 8, 2) + _test(100, 50, 2)
        return int(points * self._checkCode(s.least_squares, "lstsq(") / 10.)

    @_autoclose
    def problem2(self, s):
        """Test line_fit(). 5 points."""

        s.line_fit()
        print("""\nSpecifications:
        1. Scatter plot of year versus price index      (2 points)
        2. Positive-slope regression line               (3 points)
        (Title and legend unnecessary)""")
        points = self._grade(5, "line_fit() plot incorrect")
        return int(points * self._checkCode(s.line_fit, "lstsq(") / 10.)

    @_autoclose
    def problem3(self, s):
        """Test polynomial_fit(). 5 points."""

        s.polynomial_fit()
        print("""\nSpecifications:
        1. 4 subplots, clearly labeled                  (1 point)
        2. Scatter plot of data on each subplot         (1 point)
        3. 1st polynomial isn't a great fit             (1 point)
        4. 2nd, 3rd, and 4th polynomials are good fits  (2 points)
        (Title and legend unnecessary)""")
        points = self._grade(5, "polynomial_fit() plot incorrect")
        return int(points * self._checkCode(s.polynomial_fit, "polyfit(") /10.)

    @_autoclose
    def problem4(self, s):
        """Test ellipse_fit(). 5 points."""

        s.ellipse_fit()
        print("""\nSpecifications:
        1. Scatter plot of data points                  (2 points)
        2. Best-fit ellipse                             (3 points)
        (Title and legend unnecessary)""")
        return self._grade(5, "ellipse_fit() plot incorrect")

    def problem5(self, s):
        """Test power_method(). 10 points."""

        @_timeout(2)
        def _test(n):
            """Do an nxn test worth 5 points."""
            A = np.random.random((n,n))
            eigs, vecs = la.eig(A)
            loc = np.argmax(eigs)
            eig, vec = eigs[loc], vecs[:,loc]
            try:
                stueig, stuvec = s.power_method(A, 20, 1e-12)
            except(TypeError, ValueError):
                raise ValueError("power_method() failed to return two objects")
            pts = 2 * self._eqTest(eig, stueig,
                            "power_method() failed (dominant eigenvalue)")
            pts += 3 * self._eqTest(np.round(A.dot(stuvec), 12),
                                    np.round(stueig * stuvec, 12),
                                    "power_method() failed (Ax != eig * x")
            return pts

        points = _test(4) + _test(10)
        return int(points * self._checkCode(s.power_method, "eig(") / 10.)

    def problem6(self, s):
        """Test qr_algorithm(). 10 points."""

        @_timeout(2)
        def _test(n):
            """Do an nxn test worth 5 points."""
            A = np.random.randint(1,5,(n,n))
            A += A.T                            # Test symmetric matrices only.
            eigs = np.sort(la.eig(A)[0])
            stueigs = np.sort(s.qr_algorithm(A, 200, 1e-16))
            return 5 * self._eqTest(eigs, stueigs,
                                "qr_algorithm(A) failed for A =\n{}".format(A))

        points = _test(4) + _test(5)
        return int(points * self._checkCode(s.qr_algorithm, "eig(") / 10.)

# Validation ==================================================================
if __name__ == '__main__':
    """Validate the test driver by testing the solutions file."""
    import solutions
    test(solutions)
