# testDriver.py
"""Introductory Labs: The Standard Library. Test Driver."""

from subprocess import call
from numpy.random import randint
from solutions import prob1, prob2, prob3

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


# Test script
def test(student_module):
    """Test script. Import the student's solutions file as a module.

    5  points for problem 1
    10  points for problem 2
    10  points for problem 3
    15 points for problem 4

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
        test_one(self.problem2, "Problem 2", 10)   # Problem 2: 10 points.
        test_one(self.problem3, "Problem 3", 10)   # Problem 3: 10 points.
        test_one(self.problem4, "Problem 4", 15)   # Problem 4: 15 points.

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
        # if np.allclose(correct, student):
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
    def problem1(self, s):
        """Test prob1() (built-in functions). 5 points."""

        l = list(randint(-50,50,10))
        correct, student = prob1(l), s.prob1(l)
        if student is None:
            raise NotImplementedError("Problem 1 Incomplete")

        points  = 1*self._eqTest(correct[0], student[0], "Incorrect maximum")
        points += 2*self._eqTest(correct[1], student[1], "Incorrect minimum")
        points += 2*self._eqTest(correct[2], student[2], "Incorrect average")

        return points

    def problem2(self, s):
        """Test prob2() (mutable vs. immutable objects). 10 points."""

        print("\nCorrect output:");   prob2()
        print("\nStudent output:"); s.prob2()
        return self._grade(10, "Incorrect response(s)"
                     "\n(Hint: 3 are immutable and 2 are mutable)")

    @_timeout(5)
    def problem3(self, s):
        """Test prob3() (make and use the calculator module). 10 points."""

        points  = 5*self._eqTest(prob3(5,12), s.prob3(5,12),
                                "Incorrect hypotenuse length")
        a, b = randint(1,50,2)
        points += 5*self._eqTest(prob3(a,b), s.prob3(a,b),
                                "Incorrect hypotenuse length")
        return points

    def problem4(self, s):
        """Test prob4() (using another module). 15 points."""

        print("\n------- Testing Problem 4: Play 'Shut the Box' twice -------")
        call(["python", s.__file__, "TA"])
        call(["python", s.__file__])
        return self._grade(15, "'Shut the box' does not match specifications")


# Validation ==================================================================
if __name__ == '__main__':
    """Validate the test driver by testing the solutions file."""
    import solutions
    test(solutions)
