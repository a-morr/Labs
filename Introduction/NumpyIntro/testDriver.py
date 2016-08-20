# solutions.py
"""Introductory Labs: Intro to NumPy. Solutions file."""

# Decorators ==================================================================

import signal
from functools import wraps
from inspect import getsourcelines

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
    """Test script. Import the student's solutions file as a module.

     5 points for problem 1
     5 points for problem 2
     5 points for problem 3
     5 points for problem 4
     5 points for problem 5
     5 points for problem 6
    10 points for problem 7

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
    """Class for testing a student's work. See test.__doc__ for more info."""

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
        test_one(self.problem5, "Problem 5",  5)   # Problem 5:  5 points.
        test_one(self.problem6, "Problem 6",  5)   # Problem 6:  5 points.
        test_one(self.problem7, "Problem 7", 10)   # Problem 7: 10 points.

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
        """Check a function's source code for a key word."""
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
        """Test prob1(). 5 points."""
        points  = 5*self._eqTest(prob1(), s.prob1(), "prob1() failed")
        points *= self._checkCode(s.prob1, "58,")/10.
        return int(points)

    def problem2(self, s):
        """Test prob2(). 5 points."""
        points  = 5*self._eqTest(prob2(), s.prob2(), "prob2() failed")
        points *= self._checkCode(s.prob2, "0,")/10.
        return int(points)

    def problem3(self, s):
        """Test prob3(). 5 points."""

        points = 0
        sol, stu = prob3(), s.prob3()

        # Make sure the data type is np.int64 (2 points)
        if stu.dtype == np.int64:
            points += 1
        else:
            self.feedback += "\nprob3() failed to change array data type"

        # Check for correct matrix multiplication (4 points).
        points += 4*self._eqTest(stu, sol, "prob3() failed")

        # Check code quality.
        points *= self._checkCode(s.prob3, "48,")/10.
        return int(points)

    def problem4(self, s):
        """Test prob4(). 5 points."""

        def test_single(A):
            pts = 0
            out = "prob4(array({})) ".format(A)
            B = A.copy()
            sol, stu = prob4(A.copy()), s.prob4(B)

            # Make sure a copy was made (1 point).
            if stu is not B:
                pts += 1
            else:
                self.feedback += "\n{}failed to copy the array".format(out)

            # Make sure the answer was correct (1 point).
            pts += self._eqTest(sol,stu,"{}failed".format(out))
            return pts

        points  = test_single(np.array([-3,-1,3]))
        points += test_single(np.random.randint(-50,50,10))
        A = np.random.randint(-50,50,10)
        points += self._eqTest(prob4(A),s.prob4(A),
                               "prob4(array({})) failed".format(A))

        return points

    def problem5(self, s):
        """Test prob5(). 5 points."""
        return 5*self._eqTest(prob5(), s.prob5(), "prob5() failed")

    def problem6(self, s):
        """Test prob5(). 5 points."""

        points = 0
        out = "prob6() failed"

        A = np.array([[1,1,0],[0,1,0],[1,1,1]])
        points += self._eqTest(prob6(A.copy()), s.prob6(A.copy()), out)

        A = np.random.random((5,3))
        points += 2*self._eqTest(prob6(A.copy()), s.prob6(A.copy()), out)

        A = np.random.randint(1,9,(2,4))
        points += 2*self._eqTest(prob6(A.copy()), s.prob6(A.copy()), out)

        return points

    def problem7(self, s):
        """Test prob7(). 10 points."""
        points  = 10*self._eqTest(prob7(), s.prob7(), "prob7() failed")
        points *= self._checkCode(s.prob7, "70600674")/10.
        return int(points)


# Validation ==================================================================

if __name__ == '__main__':
    import solutions
    test(solutions)
