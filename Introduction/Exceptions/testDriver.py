# solution.py
"""Introductory Labs: Exceptions and File I/O. Test Driver."""

import sys
import signal
from os import remove as rm
from solutions import ContentFilter

def test(student_module):
    """Test script. Import the student's solutions file as a module.

    5  points for problem 1: arithmagic()
    5  points for problem 2: random_walk()
    5  points for problem 3: ContentFilter.__init__()
    25 points for problem 4: ContentFilter methods.

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
        data_file (str): the name of the file to use in testing.
    """

    data_file = "contentfilter_test.txt"

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
        test_one(self.problem4, "Problem 4", 25)   # Problem 4: 25 points.

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
    def problem1(self, s):
        """Test arithmagic(). 5 points."""

        def test_arithmagic(entries, err):

            standard_in = sys.stdin
            standard_out = sys.stdout
            try:

                with open("__IN__.txt", 'w') as f:
                    f.writelines([str(i) + '\n' for i in entries])
                sys.stdin = open("__IN__.txt", 'r')     # Redirect std in.
                sys.stdout = open("__OUT__.txt", 'w')   # Redirect std out.
                message = "\narithmagic() failed to raise a ValueError "

                try:
                    s.arithmagic()
                except ValueError as e:
                    sys.stdin = standard_in             # Reset std in.
                    sys.stdout = standard_out           # Reset std out.
                    print("\nCorrect Error message: {}".format(err))
                    print("Student Error message: {}".format(e))
                    return self._grade(1, "Poor error message")
                except Exception as e:
                    self.feedback += message
                    self.feedback +="(got {} instead)".format(self._errType(e))
                    self.feedback += "\n\tError message: {}".format(e)
                else:
                    self.feedback += message
                return 0
            finally:
                sys.stdin = standard_in                 # Reset std in.
                sys.stdout = standard_out               # Reset std out.
                rm("__IN__.txt")
                rm("__OUT__.txt")


        points  = test_arithmagic([1234], "Input must be 3 digits")
        points += test_arithmagic([121],
                            "First and last digit must differ by 2 or more")
        points += test_arithmagic([123, 323], "Incorrect reversal")
        points += test_arithmagic([123, 321, 111], "Incorrect difference")
        points += test_arithmagic([123, 321, 198, 899], "Incorrect reversal")

        return points

    def problem2(self, s):
        """Test random_walk(). 5 points."""

        points = 0
        def _handle(signum, frame):
            raise KeyboardInterrupt("Arificial KeyboardInterrupt")

        # Let random_walk() it run to completion (2 points).
        print("\nCorrect Output:\tProcess Completed\nStudent Output:\t"),
        if s.random_walk(10000) is None:
            self.feedback += "\nrandom_walk() failed to return a value"
        else:
            points += 1
        points += self._grade(1,
                        "random_walk() failed to print 'Process Completed'")

        # Interrupt random_walk() it with a KeyboardInterrupt (3 points).
        print("\nCorrect Output:\tProcess Interrupted at iteration <i>")
        print("Student Output:\t"),
        signal.signal(signal.SIGALRM, _handle)
        signal.alarm(1)
        try:
            s.random_walk(1e12)
        except KeyboardInterrupt:
            self.feedback += "\nrandom_walk() failed to handle the "
            self.feedback += "KeyboardInterrupt"
        else:
            points += 2
        points += self._grade(1,
                        "random_walk() failed to print 'Process Interrupted'")

        return points

    def problem3(self, s):
        """Test ContentFilter.__init__(). 5 points."""
        points = 0

        # Test faulty initialization (2 points).
        try:
            x = s.ContentFilter(123456789)
        except TypeError as e:
            points += 2
        except Exception as e:
            self.feedback += "\nContentFilter.__init__() failed to raise a "
            self.feedback += "TypeError (got {} instead)".format(
                                                            self._errType(e))
        else:
            self.feedback += "\nFailed to raise a TypeError"

        # Test proper initialization (3 points).
        x = s.ContentFilter(self.data_file)
        return points + 3

    def problem4(self, s):
        """Test the ContentFilter class's methods. 25 points."""

        def test_bad(cf, method, *args, **kwargs):
            """Test that eval(statement) raises an ValueError."""
            ags = ["'{}'".format(arg) for arg in args]
            kwgs = ["{}='{}'".format(key, val) for key,val in kwargs.items()]
            message = "\nContentFilter.{}({}, {}) failed to raise a ValueError".format(method, ", ".join(ags), ", ".join(kwgs))
            try:
                eval("cf.{}(*args, **kwargs)".format(method))
            except ValueError:
                return 1
            except Exception as e:
                self.feedback += message
                self.feedback +="\n\t(got {} instead)".format(self._errType(e))
            else:
                self.feedback += message
            return 0

        def test_good(cf, method, value, *args, **kwargs):
            ags = ["'{}'".format(arg) for arg in args]
            kwgs = ["{}='{}'".format(key, val) for key,val in kwargs.items()]
            message = "ContentFilter.{}({}, {})".format(
                                    method, ", ".join(ags), ", ".join(kwgs))
            eval("cf.{}(*args, **kwargs)".format(method))
            print("\n{}:\n".format(message))
            with open(args[0], 'r') as f:
                print(f.read())
            return self._grade(value, message + " failed")

        sCF = s.ContentFilter(self.data_file)

        # Test that each method raises an ValueError for bad 'mode' (3 points).
        points  = test_bad(sCF, "uniform",   "_OUT_", mode='z')
        points += test_bad(sCF, "reverse",   "_OUT_", mode='z')
        points += test_bad(sCF, "transpose", "_OUT_", mode='z')

        # Test that uniform() and reverse() raise ValueErrors (2 points).
        points += test_bad(sCF, "uniform", "_OUT_", case="middle")
        points += test_bad(sCF, "reverse", "_OUT_", unit="chunk")

        print("\nSource file:\n")
        with open(self.data_file) as f:
            print(f.read())

        # Test each method with correct usage (15 points).
        points += test_good(sCF, "uniform", 3, "_OUT_", mode='w', case="upper")
        points += test_good(sCF, "uniform", 3, "_OUT_", mode='w', case="lower")
        points += test_good(sCF, "reverse", 3, "_OUT_", mode="w", unit="word")
        points += test_good(sCF, "reverse", 3, "_OUT_", mode="w", unit="line")
        points += test_good(sCF, "transpose", 3, "_OUT_", mode="w")
        rm("_OUT_")

        # Test ContentFilter.__str__() (5 points).
        print("\nCorrect ContentFilter.__str__() output:\n")
        print(ContentFilter(self.data_file))
        print("\nStudent ContentFilter.__str__() output:\n")
        print(sCF)
        points += self._grade(5,
                    "ContentFilter.__str__() failed:\n\n{}\n".format(sCF))
        return points


# Validation ==================================================================

if __name__ == '__main__':
    import solutions
    test(solutions)
