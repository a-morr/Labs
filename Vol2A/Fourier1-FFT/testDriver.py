# testDriver.py
"""Volume 2A: Fouier I (Discrete Fourier Transform). Test driver.
This lab should be turned in as a Jupyter Notebook, so this file
shouldn't be necessary.
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

from os import system
from sys import stdout
from scipy.io import wavfile

# Test script
def test(student_module):
    """Test script. Import the student's solutions file as a module.

    20 points for Signal class
    10 points for generate_chord()

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
    def test_all(self, student_module, total=30):
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
        test_one(self.problem5, "Signal Class", 15)   # Class: 15 points.
        test_one(self.problem6, "Problem 6", 15)   # Problem 6: 15 points.

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
    @_autoclose
    def problem5(self, s):
        """Test the Signal Class. 15 points."""
        if not hasattr(s, "Signal"):
            raise NotImplementedError("Signal class not found")

        rate, sig = wavfile.read("tada.wav")
        signal = s.Signal(rate, sig)
        signal.plot()
        return self._grade(15)

    @_autoclose
    def problem6(self, s):
        """Test generate_chord(). 15 points."""
        if not hasattr(s, "generate_chord"):
            raise NotImplementedError("Problem 6 Incomplete")

        s.generate_chord()

        print("chord1.wav\t"),; stdout.flush()
        system("afplay chord1.wav")
        points  = self._grade(5, "chord1.wav failed")
        system("rm chord1.wav")

        print("chord2.wav\t"),; stdout.flush()
        system("afplay chord2.wav")
        points += self._grade(10, "chord2.wav failed")
        system("rm chord2.wav")

        return points

if __name__ == '__main__':
    import solutions
    test(solutions)
