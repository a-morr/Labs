# testDriver.py
"""Volume II: Interior Point 1. Test Driver."""

# Wrappers ====================================================================

import signal
import numpy as np
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

from real_solutions import randomLP

def test(student_module):
    """Grade a student's entire solutions file.
    
    30 points for problems 1-4
    10 points for problem 5
    
    Inputs:
        student_module: the imported module for the student's file.
    
    Returns:
        score (int): the student's score, out of TOTAL.
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
                self.feedback += "\n\n{} ({} points):".format(
                                                                number, value)
                points = problem(student_module)
                self.score += points
                self.feedback += "\nScore += {}".format(points)
            except BaseException as e:
                self.feedback += "\n{}: {}".format(self._errType(e), e)

        # Grade each problem.
        test_one(self.problem4, "Problems 1-4", 30) # Problems 1-4: 30 points.
        test_one(self.bonus, "Extra Credit", 8)     # Extra Credit: 8 points.
        test_one(self.problem5, "Problem 5", 10)    # Problem 5: 10 points.

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
    def problem4(self, s):
        """Test interiorPoint(). 30 points."""
        points = 0
        for _ in xrange(300):
            m = np.random.randint(3,10)
            A, b, c, x = s.randomLP(m)
            try:
                point, value = s.interiorPoint(A=A, b=b, c=c)
                if np.allclose(x, point):
                    points += 1
            except ValueError as e:
                print e
                print m

        self.feedback += "\nPassed {}/300 tests".format(points)
        return points // 10

    @_timeout(5)
    def bonus(self, s):
        """Test interiorPoint() on non-square systems. 8 points (20 percent)"""
        points = 0
        for _ in xrange(80):
            n = np.random.randint(2,20)
            m = np.random.randint(n,30)
            A, b, c, x = s.randomLP2(m,n)
            point, value = s.interiorPoint(A=A, b=b, c=c)
            if np.allclose(x, point[:n]):
                points += 1
        self.feedback += "\nPassed {}/80 tests".format(points)
        return points // 10

    @_autoclose
    def problem5(self, s):
        """Test leastAbsoluteDeviations(). 10 points."""
        s.leastAbsoluteDeviations()
        return self._grade(10)


# Validation ==================================================================
if __name__ == '__main__':
    """Validate the test driver by testing the solutions file."""
    import solutions
    test(real_solutions)

