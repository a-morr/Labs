# solutions.py
"""Introductory Labs: Getting Started. Test Driver."""

# Decorators ==================================================================

import signal
from functools import wraps

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

# Test Driver =================================================================

from numpy.random import randint
from solutions import *

def test(student_module):
    """Test script. Import the student's solutions file as a module.

     5 points for problem 2
    10 points for problem 3
     5 points for problem 4
     5 points for problem 5
    10 points for problem 6
     5 points for problem 7

    Parameters:
        student_module: the imported module for the student's file.

    Returns:
        score (int): the student's score, out of 40.
        feedback (str): a printout of results for the student.
    """
    tester = _testDriver()
    tester.test_all(student_module)
    return tester.score, tester.feedback

class _testDriver(object):
    """Class for testing a student's work. See test.__doc__ for more info.

    This and all other test drivers can be used to grade the entire lab
    assignment at once via test_all(), or to grade one problem at a time
    via the different problemX() functions.

    The point distribution is only a suggestion; the instructor may alter
    the weight of each problem as they see fit.
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

        def test_one(problem, label, value):
            """Test a single problem, checking for errors."""
            try:
                self.feedback += "\n\n{} ({} points):".format(label, value)
                points = problem(student_module)
                self.score += points
                self.feedback += "\nScore += {}".format(points)
            except BaseException as e:
                self.feedback += "\n{}: {}".format(self._errType(e),e)

        # Grade each problem.
        test_one(self.problem2, "Problem 2",  5)    # Problem 2:  5 points.
        test_one(self.problem3, "Problem 3", 10)    # Problem 3: 10 points.
        test_one(self.problem4, "Problem 4",  5)    # Problem 4:  5 points.
        test_one(self.problem5, "Problem 5",  5)    # Problem 5:  5 points.
        test_one(self.problem6, "Problem 6", 10)    # Problem 6: 10 points.
        test_one(self.problem7, "Problem 7",  5)    # Problem 7:  5 points.

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
    @_timeout(5)
    def problem2(self, s):
        """Test sphere_volume(). 5 Points."""
        if s.sphere_volume(1) is None:
            raise NotImplementedError("sphere_volume() returned nothing")

        points  = 2*self._eqTest(sphere_volume(5), s.sphere_volume(5),
                                            "sphere_volume(5) failed")
        points += 3*self._eqTest(sphere_volume(3.14), s.sphere_volume(3.14),
                                            "sphere_volume(3.14) failed")
        return points

    @_timeout(5)
    def problem3(self, s):
        """Test first_half() and backward(). 10 points."""
        if s.first_half("abcde") is None:
            raise NotImplementedError("first_half() returned nothing")
        if s.backward("abcde") is None:
            raise NotImplementedError("backward() returned nothing")

        points  = 2*self._eqTest(first_half("abcde"), s.first_half("abcde"),
                                            "first_half('abcde') failed")
        points += 3*self._eqTest(first_half("TK421"), s.first_half("TK421"),
                                            "first_half('TK421') failed")
        points += 2*self._eqTest(backward("abcde"), s.backward("abcde"),
                                            "backward('abcde') failed")
        points += 3*self._eqTest(backward("TK421"), s.backward("TK421"),
                                            "backward('TK421') failed")
        return points

    @_timeout(5)
    def problem4(self, s):
        """Test list_ops(). 5 points."""
        if s.list_ops() is None:
            raise NotImplementedError("list_ops() returned nothing")

        return 5*self._eqTest(list_ops(), s.list_ops(), "list_ops() failed")

    @_timeout(5)
    def problem5(self, s):
        """Test pig_latin(). 5 points."""
        if s.pig_latin("piglatin") is None:
            raise NotImplementedError("pig_latin() returned nothing")

        points = 2*self._eqTest(  pig_latin("college"),
                                s.pig_latin("college"),
                                            "pig_latin('college') failed")
        points += 3*self._eqTest(  pig_latin("university"),
                                 s.pig_latin("university"),
                                        "pig_latin('university') failed")
        return points

    @_timeout(10)
    def problem6(self, s):
        """Test palindrome(). 5 points."""
        if s.palindrome() is None:
            raise NotImplementedError("palindrome() returned nothing")

        correct, student = palindrome(), s.palindrome()
        if correct > student:
            self.feedback += "\npalindrome() failed: {} is too low".format(
                                                                    student)
        elif correct < student:
            self.feedback += "\npalindrome() failed: {} is too high".format(
                                                                    student)
        return 10 if correct == student else 0

    @_timeout(5)
    def problem7(self, s):
        """Test alt_harmonic(). 10 points."""
        if s.alt_harmonic(10) is None:
            raise NotImplementedError("alt_harmonic() returned nothing")

        points = 2*self._eqTest(alt_harmonic(100), s.alt_harmonic(100),
                                            "alt_harmonic(100) failed")
        points += 3*self._eqTest(alt_harmonic(5000), s.alt_harmonic(5000),
                                            "alt_harmonic(5000) failed")
        return points


if __name__ == '__main__':
    import solutions
    test(solutions)
