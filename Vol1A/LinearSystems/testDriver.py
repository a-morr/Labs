# testDriver.py
"""Volume 1A: Linear Systems. Test driver."""

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

import numpy as np
from scipy import sparse
from scipy.linalg import lu_factor, solve
from inspect import getsourcelines
from solutions import ref, lu, prob5


np.set_printoptions(precision=3, suppress=True)

def test(student_module):
    """Grade a student's entire solutions file.

     5 points for problem 1
    10 points for problem 2
    10 points for problem 3
     5 points for problem 4
     5 points for problem 5
     5 points for problem 6

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
        test_one(self.problem1, "Problem 1",  5)   # Problem 1:  5 points.
        test_one(self.problem2, "Problem 2", 10)   # Problem 2: 10 points.
        test_one(self.problem3, "Problem 3", 10)   # Problem 3: 10 points.
        test_one(self.problem4, "Problem 4",  5)   # Problem 4:  5 points.
        test_one(self.problem5, "Problem 5",  5)   # Problem 5:  5 points.
        test_one(self.problem6, "Problem 6",  5)   # Problem 6:  5 points.

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
    def _luTestCase(n):
        """Generate an nxn matrix that does not require pivoting with the
        Gaussian elimination or the LU Decomposition.
        """
        A = np.random.randint(0,10,(n,n))
        _, piv = lu_factor(A)
        P = np.eye(n)
        for i,j in enumerate(piv):
            P[i], P[j] = P[j].copy(), P[i].copy()
        return P.dot(A).astype(np.float)

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test ref(). 5 points."""

        @_timeout(2)
        def _test(n, p):
            """Do an nxn test case worth p points."""
            A = self._luTestCase(n)
            return p * self._eqTest(ref(A), s.ref(A), "ref() failed.")

        points = _test(3, 1) + _test(4, 2) + _test(5, 2)
        return int(points * self._checkCode(s.ref, "lu_factor") / 10.)

    def problem2(self, s):
        """Test lu(). 10 points."""

        @_timeout(2)
        def _test(n):
            """Do an nxn test case worth 5 points."""
            A = self._luTestCase(n)
            L1, U1 = lu(A)
            if not np.allclose(L1.dot(U1), A):
                return _test(n)
            stu = s.lu(A.copy())
            try:
                L2, U2 = stu
            except(TypeError, ValueError):
                raise ValueError("lu() failed to return two arrays")

            pts = 5
            if not all(np.allclose(*x) for x in [(np.tril(L2), L2),
                   (np.triu(U2), U2), (L1, L2), (U1, U2), (A, L2.dot(U2))]):
                pts = 2
                self.feedback += "\n\n{}\nA =\n{}".format('- '*20, A)
                if not np.allclose(np.tril(L2), L2):
                    self.feedback += "\nL not lower triangular:\n{}".format(L2)
                    pts -= 1
                if not np.allclose(np.triu(U2), U2):
                    self.feedback += "\nU not upper triangular:\n{}".format(U2)
                    pts -= 1
                pts += self._eqTest(L1, L2, "lu() failed (L incorrect)")
                pts += self._eqTest(U1, U2, "lu() failed (U incorrect)")
                pts += self._eqTest(A, L2.dot(U2), "lu() failed (A != LU)")
            return pts

        points = _test(4) + _test(6)
        return int(points * self._checkCode(s.lu, "lu_factor") / 10.)


    def problem3(self, s):
        """Test solve(). 10 points."""

        @_timeout(2)
        def _test(n, p):
            """Do an nxn test case worth p points."""
            A = self._luTestCase(n)
            b = np.random.randint(0, 10, n).astype(np.float)
            stu = s.solve(A, b)
            if not np.allclose(b, A.dot(stu)):
                self.feedback += "\n\n{}\nA =\n{}\nb =\n{}".format('- '*20,A,b)
                return p * self._eqTest(solve(A,b), stu, "solve() failed")
            else:
                return p

        points = _test(3, 3) + _test(4, 3) + _test(5, 4)
        return int(points * self._checkCode(s.solve, "solve(") / 10.)

    @_autoclose
    def problem4(self, s):
        """Test prob4(). 5 points."""

        print("Running prob4()...(60 second time limit)")
        _timeout(60)(s.prob4)()
        print("""\nSpecifications:
        1. Plots system size n versus execution times.              (1 point)
        2. Four lines, clearly marked:                              (2 points)
            - la.inv()                          (slowest)
            - la.solve()                        (in the middle)
            - la.lu_factor() and la.lu_solve()  (in the middle)
            - la.lu_solve() alone               (fastest)
        3. The difference between each line is apparent.            (2 points)
        (Plot could be loglog or linlin as long as it is clear)
        (Title and axis labels unnecessary)""")
        return self._grade(5, "prob4() does not match specifications")

    @_timeout(3)
    def problem5(self, s):
        """Test prob5(). 5 points."""

        def _test(n, p):
            """Do an nxn test case with p points."""
            stu = prob5(n)
            if not sparse.issparse(stu):
                self.feedback += "\n\tFailed to return a scipy.sparse matrix"
                return 0
            else:
                if type(stu) is not sparse.dia.dia_matrix:
                    self.feedback += "\n\tReturn type should be sparse "
                    self.feedback += "diagonal matrix"
                    stu = sparse.dia_matrix(stu)
                sol = prob5(n)
                if not self._eqTest(stu.offsets,sol.offsets,"prob5({}) failed "
                        "(comparing indices of nonzero diagonals".format(n)):
                    p -= 1
                return p*self._eqTest(stu.data, sol.data, "prob5({}) failed "
                        "(comparing nonzero diagonals)".format(n))

        return _test(100, 2) + _test(100000, 3)

    @_autoclose
    def problem6(self, s):
        """Test prob6(). 5 points."""

        print("\nRunning prob5()...(60 second time limit)")
        _timeout(60)(s.prob6)()
        print("""\nSpecifications:
        1. Plots system size n versus execution times.              (1 point)
        2. Two lines, clearly marked:                               (2 points)
            - scipy.sparse.linalg.spsolve()     (faster)
            - scipy.linalg.solve()              (slower)
        3. The difference between each line is apparent.            (2 points)
        (Plot could be loglog or linlin as long as it is clear)
        (Title and axis labels unnecessary)""")
        return self._grade(5, "prob6() does not match specifications")

# Validation ==================================================================
if __name__ == '__main__':
    """Validate the test driver by testing the solutions file."""
    import solutions
    test(solutions)
