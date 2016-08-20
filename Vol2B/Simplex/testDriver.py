# testDriver.py
"""Volume 2 Lab 16: Simplex. Test Driver."""

import signal
import numpy as np
from functools import wraps
from solutions import SimplexSolver, prob7

# Wrapper =====================================================================
class TimeoutError(Exception):
    pass

def _timeout(seconds):
    """Decorator for preventing a function from running for too long.

    Inputs:
        seconds (int): The number of seconds allowed.

    Notes:
        This decorator uses signal.SIGALRM, which is only available on Unix.
    """
    assert isinstance(seconds, int), "@timeout(sec) requires an int"

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

def test(student_module):
    """Test script. Import the student's solutions file as a module.
    
    30 points for the Simplex Solver (example problem)
    10 points for problem 7: Product Mix.
    
    Inputs:
        student_module: the imported module for the student's file.
    
    Returns:
        score (int): the student's score, out of 40.
        feedback (str): a printout of test results for the student.
    """
    driver = _testDriver()
    driver.test_all(student_module)
    return driver.score, driver.feedback


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
                self.feedback += "\n\nProblem {} ({} points):".format(
                                                                number, value)
                points = problem(student_module)
                self.score += points
                self.feedback += "\nScore += {}".format(points)
            except BaseException as e:
                self.feedback += "\n{}: {}".format(self._errType(e), e)

        # Grade each problem.
        test_one(self.problem6, '1-6', 30)   # Problems 1-6: 30 points.
        test_one(self.problem7, '7',   10)   # Problem 7:    10 points.

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
        if isinstance(error, TimeoutError):
            return "TimeoutError"
        if isinstance(error, BaseException):
            return str(type(error)).lstrip("<type 'exceptions.").rstrip("'>")
        else:
            return str(error)

    def _eqTest(self, correct, student, message):
        """Test to see if 'correct' and 'student' are equal.
        Report the given 'message' if they are not.
        """
        if np.allclose(correct, student):
            return 1
        else:
            self.feedback += "\n{}".format(message)
            self.feedback += "\n\tCorrect response: {}".format(correct)
            self.feedback += "\n\tStudent response: {}".format(student)
            return 0

    def _dicTest(self, correct, student):
        """Test to see if the dictionaries 'correct' and 'student' have the
        same string representation. Report the given 'message' if they are not.
        """
        assert isinstance(correct, dict), "Expected a dictionary"
        if not isinstance(student, dict):
            self.feedback += "\nExpected a dictionary"
            return 0

        points = 0
        success = True
        for key in correct:
            if key in student:
                points += 1
                if correct[key] == student[key]:
                    points += 1
                else:
                    success = False
            else:
                success = False
        if not success:
            self.feedback += "\n{}".format("Incorrect Dictionary")
            self.feedback += "\n\tCorrect response: {}".format(correct)
            self.feedback += "\n\tStudent response: {}".format(student)
        return points

    # Problems ----------------------------------------------------------------
    def test_simplex(self, s, c, b, A, simple=False):
        """Test the student's SimplexSolver class on the linear program
                maximize    c^t x
                subject to  Ax <= b
        If simple=True, the amount of points earned is 15. If simple=False,
        the amount of points earned is
            15 + number of basic variables + number of nonbasic variables
        """
        points = 0
        key = SimplexSolver(c, A, b)
        student = s.SimplexSolver(c, A, b)
        sol1, sol2 = key.solve(), student.solve()

        # Test the primal objective.
        points += 15 * self._eqTest(sol1[0], sol2[0],
                                            "Incorrect primal objective")
        if simple is False:
            # Test the basic and nonbasic variable dictionaries.
            points += self._dicTest(sol1[1], sol2[1])
            points += self._dicTest(sol1[2], sol2[2])

        return points

    @_timeout(3)
    def problem6(self, s):
        """Test the SimplexSolver class. 30 points."""
        points = 0

        # Test SimplexSolver on a system that is infeasible at the origin.
        c = np.array([3., 2.])
        b = np.array([2., 5., -7.])
        A = np.array([[1., -1.],
                      [3.,  1.],
                      [4.,  3.]])
        try:
            self.test_simplex(s, c, b, A, simple=True)
        except ValueError as e:
            points += 5
        else:
            self.feedback += "\nExpected ValueError for infeasible system"

        # Test SimplexSolver on a valid, closed system.
        b = np.array([2., 5., 7.])
        points += self.test_simplex(s, c, b, A, simple=False)
        
        return points

    @_timeout(3)
    def problem7(self, s):
        """Test prob7(). 10 points."""

        sol1, sol2 = prob7(), s.prob7()
        c = np.load('productMix.npz')['p']
        sol1, sol2 = c.dot(sol1), c.dot(sol2)

        # primal = 7453.59649123
        # assert np.allclose(sol1, primal)

        return 10 * self._eqTest(sol1, sol2, "Incorrect maximizer")


# END OF FILE =================================================================
