# testDriver.py
"""Volume II Lab 7: Nearest Neighbor Search. Test Driver.

< IN DEVELOPMENT >

"""

import inspect
import numpy as np
from scipy.spatial import KDTree
from solutions import metric, postal_problem


def test(student_module):
    """Test script. You must import the students file as a module.
    
     5 points for problem 1
     5 points for problem 2
    10 points for problem 3
    10 points for problem 4
    20 points for problem 5
    10 points for problem 6
    
    Inputs:
        student_module: the imported module for the student's file.
    
    Returns:
        score (int): the student's score, out of 80.
        feedback (str): a printout of test results for the student.
    """
    tester = _testDriver()
    tester.test_all(student_module)
    return tester.score, tester.feedback

class _testDriver(object):
    """Class for testing a student's work. See test.__doc__ for more info."""
    def __init__(self):
        self.feedback = ""

    # Main routine -----------------------------------------------------------
    def test_all(self, student_module, total=50):
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
        test_one(self.problem1, "Problem 1", 5)
        test_one(self.problem2, "Problem 2", 5)
        test_one(self.problem5, "Problems 4 and 5", 30)
        test_one(self.problem6, "Problem 6", 10)

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
        if np.allclose(correct, student, atol=1e-04):
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

    def neighbor(self, m, k, func):
        """Do a single nearest neighbor search trial for mxk data,
        solved with the function 'func'.
        """
        data = np.random.random((m, k))
        target = np.random.random(k)
        tree = KDTree(data)
        dist, index = tree.query(target)
        point = tree.data[index]
        spoint, sdist = func(data, target) # func solves the problem
        p1 = self._eqTest(point, spoint,
            "\n\t"+func.__name__+"() failed: incorrect nearest neighbor")
        p2 = self._eqTest(dist, sdist, 
            "\n\t"+func.__name__+"() failed: incorrect minimum distance")
        return p1 + p2

    @staticmethod
    def get_code(func):
        rawcode = inspect.getsource(func).splitlines()[len(
                                            func.__doc__.splitlines())+1:]
        for line in rawcode: print line

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test metric(). 5 Points."""

        # Test with good inputs (4 points)
        x = np.array([1, 2])
        y = np.array([2, 2])
        points = self._eqTest(metric(x,y), s.metric(x,y),
                                            "\n\tmetric() failed.")
        
        x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        y = np.array([2, 6, 4, 8, 0, 2, 4, 7, 5, 11])
        points += self._eqTest(metric(x,y), s.metric(x,y),
                                            "\n\tmetric() failed.")
        
        x = (np.random.random(100)-.5)*200
        y = (np.random.random(100)-.5)*200
        points += self._eqTest(metric(x,y), s.metric(x,y),
                                        "\n\tmetric() failed.")*2
        
        # Test with bad inputs (1 point)
        x = np.array([1, 2])
        y = np.array([1, 2, 3])
        try:
            s.metric(x, y)
            self.feedback += "\n\tmetric() failed to raise a "
            self.feedback += "ValueError for vectors of different lengths"
        except:
            points += 1

        return points

    def problem2(self, s):
        """Test exhaustive_search(). 5 points."""
    
        points  = self.neighbor(100, 10, s.exhaustive_search)
        points += self.neighbor(10, 100, s.exhaustive_search)
        points += 1

        _testDriver.get_code(s.exhaustive_search)
        print "\n(Check that scipy.spatial.KDTree is not used)"
        points *= self._grade(1)

        return points

    def problem3(self, s):
        """Test the KDTNode class. 10 points."""

        points = 0

        # Test KDTNode.__init__ (can only hold np.ndarrays; 2 points)
        try:
            s.KDTNode("This is not a numpy array")
            self.feedback += "\n\tKDTNode(x) failed to raise a TypeError "
            self.feedback += "for x not a numpy array (np.ndarray)"
        except:
            points += 2

        # Test KDTNode.__sub__ (euclidean distance; 2 points)
        x = np.random.random(10); y = np.random.random(10)
        A =   KDTNode(x); B =   KDTNode(y)
        C = s.KDTNode(x); D = s.KDTNode(y)
        points += 2*self._eqTest(A-B, C-D, "\n\tKDTNode.__sub__ failed")

        # Test KDTNode.__eq__ (1 Point)
        D = s.KDTNode(1.5*x)
        if not (C == D):
            points += 1
        else:
            self.feedback += "\n\tKDTNode.__eq__ failed on nonequal"

        # Test KDTNode.__lt__ and KDTNode.__gt__ (5 points)
        x = s.KDTNode(np.array([3,1,0,5], dtype=np.int)); x.axis = 0
        y = s.KDTNode(np.array([1,2,4,3], dtype=np.int)); y.axis = 1
        if x < y: points += 1
        else: self.feedback += "\n\tKDTNode.__lt__ failed"
        if y < x: points += 1
        else: self.feedback += "\n\tKDTNode.__lt__ failed"

        x.axis = 2; y.axis = 3
        if x > y: points += 1
        else: self.feedback += "\n\tKDTNode.__gt__ failed"
        if y > x: points += 2
        else: self.feedback += "\n\tKDTNode.__gt__ failed"

        return points
    
    def problem5(self, s):
        """Test nearest_neighbor(). 30 points."""
        points = 0

        points  = self.neighbor( 10,  10, s.nearest_neighbor)*3
        points += self.neighbor(100,  10, s.nearest_neighbor)*3
        points += self.neighbor( 10, 100, s.nearest_neighbor)*3
        points += self.neighbor(100, 100, s.nearest_neighbor)*3
        points += self.neighbor(100, 100, s.nearest_neighbor)*3

        _testDriver.get_code(s.nearest_neighbor)
        print "\n(Check that scipy.spatial.KDTree is not used)"
        points *= self._grade(1)
        
        return points

    def problem6(self, s):
        """Test postal_problem(). 10 points."""

        print("Correct responses:")
        postal_problem(grading=True)
        print("\nStudent responses:")
        x = s.postal_problem()
        if x is not None:
            print x
        
        return self._grade(10)

if __name__ == '__main__':
    import solutions as sol
    score, feedback = test(sol)

# =============================== END OF FILE =============================== #
