# solutions.py
"""Volume II Lab 5: Data Structures II (Trees). Test Driver."""

# Auxiliaries =================================================================

from matplotlib import pyplot as plt
from inspect import getsourcelines
from functools import wraps
import signal

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

from time import time
from sys import stdout
from numpy.random import choice
from solutions import iterative_search, SinglyLinkedList, BST

def test(student_module):
    """Test script. You must import the student's 'solutions.py' as a module.

     5 points for problem 1
    15 points for problem 2
    30 points for problem 3
    10 points for problem 4

    Inputs:
        student_module: the imported module for the student's file.

    Returns:
        score (int): the student's score, out of 60.
        feedback (str): a printout of test results for the student.
    """
    tester = _testDriver()
    tester.test_all(student_module)
    return tester.score, tester.feedback

class _testDriver(object):
    """Class for testing a student's work. See test.__doc__ for more info."""

    # File to pull info from for testing problem 4.
    data_file = "English.txt"

    # Constructor -------------------------------------------------------------
    def __init__(self):
        self.feedback = ""

    # Main routine ------------------------------------------------------------
    def test_all(self, student_module, total=60):
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
        test_one(self.problem2, "Problem 2", 15)   # Problem 2: 15 points.
        test_one(self.problem3, "Problem 3", 30)   # Problem 3: 30 points.
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

    @staticmethod
    def _printCode(f):
        """Print a function's source code."""
        print "".join(getsourcelines(f)[0][len(f.__doc__.splitlines())+1 :])

    def _strTest(self, correct, student, message):
        """Test to see if 'correct' and 'student' have the same string
        representation.
        """
        if str(correct) == str(student):
            return 1
        else:
            self.feedback += "\n\t{}".format(message)
            self.feedback += "\nCorrect response:\n{}".format(correct)
            self.feedback += "\nStudent response:\n{}".format(student)
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
        """Test recursive_search(). 5 points."""

        points = 0

        lls = SinglyLinkedList()
        # Check recursive_search() on empty list (1 point)
        try:
            s.recursive_search(lls, 1)
            self.feedback += "\n\trecursive_search() failed on empty list"
        except ValueError:
            points += 1

        # Check recursive_search() for items in list (3 points)
        lls.append(1)
        lls.append('a')
        lls.append(2)
        points += self._strTest(iterative_search(lls,1),
                               s.recursive_search(lls, 1),
                               "recursive_search(x) failed for x in list")
        points += self._strTest(iterative_search(lls, 'a'),
                               s.recursive_search(lls, 'a'),
                               "recursive_search(x) failed for x in list")
        points += self._strTest(iterative_search(lls, 2),
                               s.recursive_search(lls, 2),
                               "recursive_search(x) failed for x in list")

        # Check recursive_search() for items not in list (1 point)
        try:
            s.recursive_search(lls, 3)
            self.feedback += "\n\trecursive_search(x) failed for x not in list"
        except ValueError:
            points += 1

        # Check that recursion is used somewhere.
        self._printCode(s.recursive_search)
        points *= self._grade(1, "recursive_search() must use recursion!")
        return points

    @_timeout(5)
    def problem2(self, s):
        """Test BST.insert(). 15 Points."""

        points = 0

        # Empty tree (0 pts)
        tree1, tree2 = BST(), s.BST()
        self._strTest(tree1, tree2, "BST() failed initially!")

        # Inserting root (2 pts)
        tree1.insert(4); tree2.insert(4)
        points += 2*self._strTest(tree1, tree2, "BST.insert(4) failed "
                                 "on root insertion.\nPrevious tree:\n[]")

        def test_insert(value, solTree, stuTree):
            oldTree = "\nPrevious tree:\n{}".format(solTree)
            solTree.insert(value); stuTree.insert(value)
            p = self._strTest(tree1, tree2,
                        "BST.insert({}) failed{}".format(value, oldTree))
            return p, solTree, stuTree

        # Inserting nonroot (9 pts)
        for i in [2, 1, 3, 10, 5, 6, 9, 7, 11]:
            p, tree1, tree2 = test_insert(i, tree1, tree2)
            points += p
            if p == 0:
                break

        if points >= 11:
            # Inserting already existing value (4 pts)
            def test_duplicate(value, stuTree):
                try:
                    stuTree.insert(value)
                    self.feedback += "\n\tBST.insert({}) failed ".format(value)
                    self.feedback += "for {} already in tree".format(value)
                    return 0
                except ValueError:
                    return 1

            points +=   test_duplicate(4, tree2)
            points +=   test_duplicate(1, tree2)
            points += 2*test_duplicate(7, tree2)

        else:
            self.feedback += "\nAll BST.remove() tests are likely to fail"
            self.feedback += "\n\tunless all BST.insert() tests pass!"

        return points

    @_timeout(5)
    def problem3(self, s):
        """Test BST.remove(). 30 points."""

        def load_trees(entries):
            solutions_tree, student_tree = BST(), s.BST()
            for i in entries:
                solutions_tree.insert(i)
                student_tree.insert(i)
            if str(solutions_tree) != str(student_tree):
                raise NotImplementedError("BST.remove() cannot be tested "
                                          "until BST.insert() is correct")
            return solutions_tree, student_tree

        def test_remove(value, solTree, stuTree):
            oldTree = "\nPrevious tree:\n{}".format(solTree)
            try:
                solTree.remove(value); stuTree.remove(value)
                p = self._strTest(solTree, stuTree,
                        "BST.remove({}) failed{}".format(value, oldTree))
            except Exception as e:
                self.feedback += "\n\t{} while removing {}".format(
                                                    self._errType(e), value)
                self.feedback += ": {}{}".format(e, oldTree)
                p = 0
            finally:
                return p, solTree, stuTree

        def remove_many(data, targets):
            pts = 0
            tree1, tree2 = load_trees(data)
            for i in targets:
                p, tree1, tree2 = test_remove(i, tree1, tree2)
                if p == 0:
                    break
                pts += p
            return pts

        points = 0
        tree2 = s.BST()
        items = [4, 2, 1, 3, 10, 5, 6, 9, 7, 11, 15, 14, 16, 12]

        # Remove from empty tree (1 points).
        try:
            tree2.remove(5)
            self.feedback += "\n\tBST.remove() failed on empty tree"
        except ValueError:
            points += 1

        # Remove leaf (5 points).
        points += remove_many(items, [1, 7, 12, 16, 14])

        # Remove non-root with 1 child (5 points).
        points += remove_many(items, [9, 6, 5, 11, 14])

        # Remove non-root with 2 children (5 points).
        points += remove_many(items, [2, 15, 10, 11, 12])

        # Remove root with one child (5 points).
        points += remove_many([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5])

        # Remove root with two children (5 points).
        points += remove_many([2, 1, 7, 6, 5, 4, 3], [2, 3, 4, 5, 6])

        # Remove root with no children (2 points).
        points += 2*remove_many([10], [10])

        # Remove nonexistent (2 points)
        tree1, tree2 = load_trees(items)
        try:
            tree2.remove(0)
            self.feedback += "\n\tBST.remove(0) failed for 0 not in tree"
            self.feedback += "\nPrevious tree:\n{}".format(tree1)
        except ValueError:
            points += 1

        try:
            tree2.remove(12.5)
            self.feedback += "\n\tBST.remove(12.5) failed for 12.5 not in tree"
            self.feedback += "\nPrevious tree:\n{}".format(tree1)
        except ValueError:
            points += 1

        return points

    @_autoclose
    def problem4(self, s):
        """Test prob4(). 10 points."""

        print("Running prob4()...")
        stdout.flush()
        s.prob4()
        return self._grade(10)


if __name__ == '__main__':
    import solutions
    test(solutions)
