# testDriver.py
"""Volume 1A: Linear Transformations. Test driver."""

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

from solutions import *

def test(student_module):
    """Grade a student's entire solutions file.

    10 points for problem 1
    10 points for problem 2
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

    data_file = "horse.npy"

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
        test_one(self.problem1, "Problem 1", 10)   # Problem 1: 10 points.
        test_one(self.problem2, "Problem 2", 10)   # Problem 2: 10 points.
        test_one(self.problem3, "Problem 3", 10)   # Problem 3: 10 points.
        test_one(self.problem4, "Problem 4", 10)   # Problem 4: 10 points.

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

    def _eqTest(self, correct, student, message, compare=True):
        """Test to see if 'correct' and 'student' are equal.
        Report the given 'message' if they are not.
        """
        if np.allclose(correct, student):
            return 1
        else:
            self.feedback += "\n{}".format(message)
            if compare:
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
    def problem1(self, s):
        """Test stretch(), shear(), reflect(), and rotate(). 10 points."""
        points = 0
        data = np.load(self.data_file)

        # stretch() (2 points).
        a, b = np.random.randint(1,11,2)
        points += 2 * self._eqTest(stretch(data, a, b), s.stretch(data, a, b),
                                                    "stretch() failed", False)

        # shear() (2 points).
        a, b = np.random.randint(1,11,2)
        points += 2 * self._eqTest(shear(data, a, b), s.shear(data, a, b),
                                                    "shear() failed", False)

        # reflect() (3 points).
        a, b = np.random.randint(1,11,2)
        points += 3 * self._eqTest(reflect(data, a, b), s.reflect(data, a, b),
                                                    "reflect() failed", False)

        # rotate() (3 points).
        theta = np.random.uniform(.1, 2*np.pi-.1)
        points += 3 * self._eqTest(rotate(data, theta), s.rotate(data, theta),
                                                    "rotate() failed", False)

        return points

    @_autoclose
    def problem2(self, s):
        """Test solar_system(). 10 points."""

        s.solar_system(np.pi, 1, 13)
        print("""\nSpecifications:
        1. Blue semicircle from 0 to pi
        2. Green line rotates around blue line 6 times
        (Title and legend unnecessary)
        (Aspect ratio may be stretched)""")
        return self._grade(10, "solar_system() does not match specifications")

    @_autoclose
    def problem3(self, s):
        """Test prob3(). 10 points."""

        print("Running prob3()...(60 second time limit)")
        _timeout(60)(s.prob3)()
        print("""\nSpecifications:
        1. Two plots: matrix-vector times, matrix-matrix times
        2. Both plots are quadratically increasing
        3. Matrix-matrix times are much greater than matrix-vector times
        (Titles and legend unnecessary)""")
        return self._grade(10, "prob3() does not match specifications")

    @_autoclose
    def problem4(self, s):
        """Test prob4(). 10 points."""

        print("Running prob4()...(60 second time limit)")
        _timeout(60)(s.prob4)()
        print("""\nSpecifications:
        1. Two plots: lin-lin scale, log-log scale
        2. All lines are quadratically increasing (at different rates)
        3. NumPy times are significantly lower than list times
        4. A legend with good labels is included
        (Titles unnecessary)
        (NumPy lines may be bumpy in the log-log plot)""")
        return self._grade(10, "prob4() does not match specifications")

# Validation ==================================================================
if __name__ == '__main__':
    """Validate the test driver by testing the solutions file."""
    import solutions
    test(solutions)
