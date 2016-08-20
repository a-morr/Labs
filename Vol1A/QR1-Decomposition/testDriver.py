# testDriver.py
"""Volume 1A: QR 1 (Decomposition). Test driver."""

# Decorator ===================================================================

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

    10 points for problem 1
     5 points for problem 2
     5 points for problem 3
    10 points for problem 4
    10 points for problem 5

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
        test_one(self.problem1, "Problem 1", 10)   # Problem 1: 10 points.
        test_one(self.problem2, "Problem 2",  5)   # Problem 2:  5 points.
        test_one(self.problem3, "Problem 3",  5)   # Problem 3:  5 points.
        test_one(self.problem4, "Problem 4", 10)   # Problem 4: 10 points.
        test_one(self.problem5, "Problem 5", 10)   # Problem 5: 10 points.

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

    @staticmethod
    def _qrTestCase(m, n):
        """Generate an nonsingular mxn matrix."""
        A = np.random.randint(1,10,(m,n)).astype(np.float)
        if np.linalg.matrix_rank(A) != n:
            return _testDriver._qrTestCase(m,n)
        return A[:,la.qr(A, pivoting=True)[-1]]

    @_timeout(2)
    def _qrTest(self, m, n, func):
        """Do an mxn test of a QR factorization via func() worth 5 points."""
        A = self._qrTestCase(m,n)
        stu = func(A.copy())
        try:
            Q,R = stu
        except(TypeError, ValueError):
            raise ValueError("{} failed to return two arrays".format(
                                                                func.__name__))
        pts = 5
        if not all(np.allclose(*x) for x in [(A, Q.dot(R)), (np.triu(R), R),
                                        (np.eye(Q.shape[1]), np.dot(Q.T, Q))]):
            pts = 3
            self.feedback += "\n\n{}\nA =\n{}".format('- '*20, A)
            if not np.allclose(np.triu(R), R):
                self.feedback += "\nR not upper triangular:\n{}".format(R)
                pts -= 1
            if not np.allclose(np.eye(Q.shape[1]), np.dot(Q.T, Q)):
                self.feedback += "\nQ not orthonormal:\n{}".format(Q)
                pts -= 2
            pts += 2*self._eqTest(A, Q.dot(R), "A != QR")
        return pts

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test qr_gram_schmidt(). 10 points."""
        points = sum([self._qrTest(4, 4, s.qr_gram_schmidt),
                      self._qrTest(8, 6, s.qr_gram_schmidt)])
        return int(points * self._checkCode(s.qr_gram_schmidt, "qr(") / 10.)

    def problem2(self, s):
        """Test abs_det(). 5 points."""

        @_timeout(2)
        def _test(n,p):
            """Do an nxn test case worth p points."""
            A = self._qrTestCase(n,n)
            return p * self._eqTest(abs(la.det(A)), s.abs_det(A),
                            "abs_det(A) failed for A =\n{}".format(A))

        points = _test(2, 1) + _test(5, 2) + _test(10, 2)
        return int(points * self._checkCode(s.abs_det, "det(") / 10.)

    def problem3(self, s):
        """Test solve(). 5 points."""

        @_timeout(2)
        def _test(n,p):
            """Do an nxn test case worth p points."""
            A = self._qrTestCase(n,n)
            b = np.random.randint(1,10,n)
            return p * self._eqTest(la.solve(A, b), s.solve(A, b),
                        "solve(A, b) failed for A =\n{}\nb=\n{}".format(A,b))

        points = _test(2, 1) + _test(5, 2) + _test(10, 2)
        return int(points * self._checkCode(s.abs_det, "solve(") / 10.)

    def problem4(self, s):
        """Test qr_householder(). 10 points."""
        points =  sum([self._qrTest( 5, 5, s.qr_householder),
                       self._qrTest(10, 6, s.qr_householder)])
        return int(points * self._checkCode(s.qr_householder, "qr(") / 10.)

    def problem5(self, s):
        """Test hessenberg(). 10 points."""

        @_timeout(2)
        def _test(n):
            """Do an nxn test worth 5 points."""
            A = self._qrTestCase(n,n)
            stu = s.hessenberg(A.copy())
            try:
                H,Q = stu
            except(TypeError, ValueError):
                raise ValueError("hessenberg() failed to return two arrays")

            pts = 5
            if not all(np.allclose(*x) for x in [(np.triu(H, -1), H),
                                        (np.eye(Q.shape[1]), np.dot(Q.T, Q)),
                                                (A, np.dot(Q, H.dot(Q.T)))]):
                pts = 3
                self.feedback += "\n\n{}\nA =\n{}".format('- '*20, A)
                if not np.allclose(np.triu(H, -1), H):
                    self.feedback += "\nH not upper Hessenberg:\n{}".format(H)
                    pts -= 1
                if not np.allclose(np.eye(Q.shape[1]), np.dot(Q.T, Q)):
                    self.feedback += "\nQ not orthonormal:\n{}".format(Q)
                    pts -= 2
                pts += 2*self._eqTest(A, np.dot(Q, H.dot(Q.T)), "A != QHQ^T")
            return pts

        points = _test(4) + _test(10)
        return int(points * self._checkCode(s.hessenberg, "hessenberg(") / 10.)

# Validation ==================================================================
if __name__ == '__main__':
    """Validate the test driver by testing the solutions file."""
    import solutions
    test(solutions)
