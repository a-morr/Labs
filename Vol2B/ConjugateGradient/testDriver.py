# solutions.py
"""Volume II Lab 18: Conjugate Gradient. Test Driver."""


import numpy as np
from real_solutions import prob2, prob3


def test(student_module):
    """Grade a student's entire solutions file.
    
    20 points for problem 2.
    20 points for problem 3.
    
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
                self.feedback += "\n\nProblem {} ({} points):".format(
                                                                number, value)
                points = problem(student_module)
                self.score += points
                self.feedback += "\nScore += {}".format(points)
            except BaseException as e:
                self.feedback += "\n{}: {}".format(self._errType(e), e)

        # Grade each problem.
        test_one(self.problem2, 2, 20)   # Problem 1: 20 points.
        test_one(self.problem3, 3, 20)   # Problem 2: 20 points.

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
        if np.allclose(correct, student, atol=1e-4, rtol=1e-4):
            return 1
        else:
            self.feedback += "\n{}".format(message)
            self.feedback += "\n\tCorrect response: {}".format(correct)
            self.feedback += "\n\tStudent response: {}".format(student)
            return 0

    # Problems ----------------------------------------------------------------
    def problem2(self, s):
        """Test prob2() (linregression problem). 20 points."""

        correct, student = prob2(), s.prob2()
        if type(student) != np.ndarray:
            raise TypeError("Failed to return a NumPy array.")

        return 20 * self._eqTest(correct, student, "Incorrect Answer.")

    def problem3(self, s):
        """Test prob3() (logregression problem). 20 points."""
        
        correct, student = prob3(), s.prob3()
        if type(student) != np.ndarray:
            raise TypeError("Failed to return a NumPy array.")

        return 20 * self._eqTest(correct, student, "Incorrect Answer.")


# Validation ==================================================================
if __name__ == '__main__':
    """Validate the test driver by testing the solutions file."""
    import solutions
    test(solutions)

