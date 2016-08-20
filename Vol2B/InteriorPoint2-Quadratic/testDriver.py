# solutions.py
"""Volume II: Interior Point II (Quadratic Optimization). Test Driver."""

# Wrappers ====================================================================

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
        raise TimeoutError("Timeout after {0} seconds".format(seconds))

    def decorator(func):
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handler)
            signal.alarm(seconds)               # Set the alarm.
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)                 # Turn the alarm off.
            return result
        return wraps(func)(wrapper)
    return decorator

# Test Script and Class =======================================================

import numpy as np
from real_solutions import portfolio

def test(student_module):
    """Grade a student's entire solutions file.
    
    20 points for problems 1-2
    10 points for problem 3
    10 points for problem 4
    
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

    # Main routine -----------------------------------------------------------
    def test_all(self, student_module, total=40):
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
        test_one(self.problem2, 2, 20)   # Problems 1-2: 20 points.
        test_one(self.problem3, 3, 10)   # Problem 3: 10 points.
        test_one(self.problem4, 4, 10)   # Problem 4: 10 points.

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

    def _eqTest(self, correct, student, message):
        """Test to see if 'correct' and 'student' are equal.
        Report the given 'message' if they are not.
        """
        if not isinstance(student, np.ndarray):
            raise TypeError("Failed to return a NumPy array")
        if np.allclose(correct, student):
            return 1
        else:
            self.feedback += "\n{}".format(message)
            self.feedback += "\n\tCorrect response: {}".format(correct)
            self.feedback += "\n\tStudent response: {}".format(student)
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
    @_timeout(5)
    def problem2(self, s):
        """Test qInteriorPoint(). 20 points."""

        Q = np.array([[1,-1.],[-1,2]])
        c = np.array([-2,-6.])
        A = np.array([[-1, -1], [1, -2.], [-2, -1], [1, 0], [0,1]])
        b = np.array([-2, -2, -3., 0, 0])
        x0 = np.array([.5, .5])
        y0 = np.ones(5)
        m0 = np.ones(5)
        point, value = s.qInteriorPoint(Q=Q, c=c, A=A, b=b, guess=(x0,y0,m0))
        return 20 * self._eqTest(np.array([2/3., 4/3.]), point,
                            "qInteriorPoint() failed for the QP in Problem 2")

    @_autoclose
    def problem3(self, s):
        """Test the circus tent problem. 10 points."""
        s.circus(n=15)
        return self._grade(10, "Incorrect circus tent graph with n=15")

    @_timeout(5)
    def problem4(self, s):
        """Test the portfolio optimization problem. 10 points."""
        
        try:
            s1, s2 = s.portfolio(filename="portfolio.txt")
            s1, s2 = np.ravel(s1), np.ravel(s2)
        except ValueError as e:
            if str(e) == "too many values to unpack":
                raise ValueError("Failed to return two NumPy arrays")
            else: raise
        except TypeError as e:
            if "is not iterable" in str(e):
                raise TypeError("Failed to return two NumPy arrays")
            else: raise
        c1, c2 = portfolio(filename="portfolio.txt")

        points  = 5 * self._eqTest(c1, s1,
                              "Incorrect percentages (with short selling)")
        points += 5 * self._eqTest(c2, s2,
                              "Incorrect percentages (with short selling)")
        return points


# Validation ==================================================================
if __name__ == '__main__':
    """Validate the test driver by testing the solutions file."""
    import solutions
    test(real_solutions)

