# testDriver.py
"""Outline for Foundations of Applied Mathematics lab test drivers.

Test driver files should be named testDriver.py and should be placed in the
same folder as the lab that it corresponds to. The testDriver.py file should
have dependencies on the corresponding solutions.py file so that student
submissions are tested directly against the solutions when possible.

test() function and _testDriver class -----------------------------------------

The _testDriver class is designed to be flexible. The test_all() routine will
grade each problem and collect feedback, but each problem can be graded
individually via the different problemX() methods. This allows the instructor
to grade from IPython, or to automate grading using Git, Google Drive, or
another file system manager.

The test() function creates an instance of the _testDriver class, grades every
problem, and returns the score feedback. Use this function to automate the
grading process.

Customize the docstrings of the test() function and the _testDriver class to
give specific instructions about how the lab is to be graded.

Tags --------------------------------------------------------------------------

The @_autoclose tag makes it easy to grade a problem that produces a plot.
It should only be on a problem-grading function that uses _testDriver._grade()
or some other pausing command (like raw_input()) so that the plot is not closed
immediately after it is created.

The @_timeout tag prevents a function from running for longer than a
specificied number of seconds. Be careful not to use this wrapper in
conjunction with _testDriver._grade() or another pausing command that waits
for the grader's response. NOTE: this decorator will only work on Unix.

Testing -----------------------------------------------------------------------

To test the test driver, make sure that the solutions file passes with full
points. The if __name__ == '__main__' clause imports the solutions file and
grades it.
"""

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

from inspect import getsourcelines
# from solutions import [functions / classes that are needed for testing]

def test(student_module):
    """Grade a student's entire solutions file.

    X points for problem 1
    X points for problem 2
    ...

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
        test_one(self.problem1, "Problem 1", 0)   # Problem 1: X points.
        test_one(self.problem2, "Problem 2", 0)   # Problem 2: X points.

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

    @staticmethod
    def _printCode(f):
        """Print a function's source code."""
        print "".join(getsourcelines(f)[0][len(f.__doc__.splitlines())+1 :])

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
        # if np.allclose(correct, student):
        # if str(correct) == str(student):
        # if correct is student:            # etc.
        if correct == student:
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
    def problem1(self, s):
        """Test Problem 1. X points."""
        points = 0
        # Test problem 1 here.
        return points

    def problem2(self, s):
        """Test Problem 2. X points."""
        points = 0
        # Test problem 2 here.
        return points


# Validation ==================================================================
if __name__ == '__main__':
    """Validate the test driver by testing the solutions file."""
    import solutions
    # If you really like using IPython for validation, include these lines:
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    # reload(solutions)
    test(solutions)
