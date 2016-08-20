# testDriver.py
"""Volume II: Breadth-First Search (Kevin Bacon) Test Driver."""

from solutions import *
import inspect

'''
def getCode():
    rawcode = inspect.getsource(Graph.shortest_path).splitlines()[21:]
    code = ""
    for line in rawcode: code += line
    if len(code.partition('shortest_path(')[1]) > 0:
        for line in rawcode:
            print line
'''
# Old Test script
def old_test(student_module):
    """Old test script. UNDER CONSTRUCTION."""

    try:    # Problem 6: 10 points
        feedback += "\n\nProblem 6 (10 points):"
        points = 0
        sBacon = s.BaconSolver()
        
        try: # Test invalid input
            sBacon.path_to_bacon("Bad Name")
            feedback += "\n\tBaconSolver.path_to_bacon(x) failed"
            feedback += " to raise an exception for invalid x"
        except ValueError: points += 2
        
        try: # Test no connection to Kevin Bacon
            sBacon.path_to_bacon("Arandi, Jose")
            feedback += "\n\tBaconSolver.path_to_bacon('Arandi, Jose') failed"
            feedback += " to raise an exception for no connection to target"
        except nx.NetworkXNoPath: points += 2
        
        # Test BaconSolver.path_to_bacon() for valid cases
        print("Student path from 'Thurman, Uma' to 'Bacon, Kevin':")
        print(sBacon.path_to_bacon('Thurman, Uma'))
        p,f = grade(2,
            "\n\tBaconSolver.path_to_bacon('Thurman, Uma') failed")
        points += p; feedback += f
        print("Student path from 'Bartseh, Peter' to 'Bacon, Kevin':")
        print(sBacon.path_to_bacon('Bartseh, Peter'))
        p,f = grade(2,
            "\n\tBaconSolver.path_to_bacon('Bartseh, Peter') failed")
        points += p; feedback += f
        print("Student path from 'Clooney, George' to 'Damon, Matt':")
        print(sBacon.path_to_bacon('Clooney, George', 'Damon, Matt'))
        p,f = grade(2,"\n\tBaconSolver.path_to_bacon("
                        + "'Clooney, George', 'Damon, Matt') failed")
        points += p; feedback += f

        score += points; feedback += "\nScore += " + str(points)
    except Exception as e: feedback += "\nError: " + e.message

    try:    # Problem 7: 10 points
        feedback += "\n\nProblem 7 (10 points):"
        points = 0
        sBacon = s.BaconSolver()
        
        try: # Test invalid input
            sBacon.bacon_number("Bad Name")
            feedback += "\n\tBaconSolver.bacon_number(x) failed"
            feedback += " to raise an exception for invalid x"
        except ValueError: points += 1
        
        try: # Test no connection to Kevin Bacon
            sBacon.bacon_number("Arandi, Jose")
            feedback += "\n\tBaconSolver.bacon_number('Arandi, Jose') failed"
            feedback += " to raise an exception for no connection to target"
        except nx.NetworkXNoPath: points += 1

        # Test BaconSolver.bacon_number() for valid cases
        if 5 == sBacon.bacon_number('Bartseh, Peter'): points += 1
        else:
            feedback += "\n\tBaconSolver.bacon_number('Bartseh, Peter') failed"
        if 2 == sBacon.bacon_number('Clooney, George', 'Damon, Matt'):
            points += 1
        else:
            feedback += "\n\tBaconSolver.bacon_number("
            feedback += "'Clooney, George', 'Damon, Matt') failed"
        
        # Test BaconSolver.average_bacon()
        average, isolated = sBacon.average_bacon()
        if 847 == isolated: points += 2
        else:
            feedback += "\n\tBaconSolver.average_bacon() failed"
            feedback += " for actors not connected to Kevin Bacon"
        if abs(average - 2.66) < .01: points += 4
        else:
            feedback += "\n\tBaconSolver.average_bacon() failed"
            feedback += " for average Bacon number"
        
        score += points; feedback += "\nScore += " + str(points)
    except Exception as e: feedback += "\nError: " + e.message

    if hasattr(sBacon, 'plot_bacon'):
        try:    # Problem 8: 3 points
            feedback += "\n\nProblem 8 (3 points):"
            points = 0
            sBacon.plot_bacon()
            p,f = grade(3, "\n\tBaconSolver.plot_bacon() failed")
            points += p; feedback += f
            
            score += points; feedback += "\nScore += " + str(points)
        except Exception as e: feedback += "\nError: " + e.message

def test(student_module):
    """Test script. Import the student's solutions file as a module.

     5 points for problem 1
    10 points for problem 2
    15 points for problem 3
     3 points for problem 4 (Extra Credit)
    10 points for problem 5
    10 points for problem 6
    10 points for problem 7
     3 points for problem 8 (Extra Credit)
    
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

    # Constructor and Main routine --------------------------------------------
    def __init__(self):
        self.feedback = ""

    def test_all(self, student_module):
        """Grade each problem...TODO"""
        self.feedback = ""
        score = 0

        try:    # Problem 1: 5 points
            self.feedback += "\n\nProblem 1 (5 points):"
            points = self.problem1(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message
        
        try:    # Problem 2: 10 points
            self.feedback += "\n\nProblem 2 (10 points):"
            points = self.problem2(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message

        try:    # Problem 4: 15 points
            self.feedback += "\n\nProblem 4 (15 points):"
            points = self.problem4(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message

        try:    # BaconSolver: 20 points
            self.feedback += "\n\nBaconSolver (20 points):"
            points = self.baconator(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message


        # Report final score.
        total = 50
        percentage = (100.0 * score) / total
        self.feedback += "\n\nTotal score: " + str(score) + "/"
        self.feedback += str(total) + " = " + str(percentage) + "%"
        if   percentage >=  98.0: self.feedback += "\n\nExcellent!"
        elif percentage >=  90.0: self.feedback += "\n\nGreat job!"

        # Add comments (optionally).
        print self.feedback
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += '\n\n\nComments:\n\t' + comments
        self.score = score

    # Helper Functions --------------------------------------------------------
    def strTest(self, correct, student, message):
        """Test to see if correct and student have the same
        string representation.
        """
        if str(correct) == str(student):
            return 1
        else:
            self.feedback += message
            self.feedback += "\nCorrect response:\n" + str(correct)
            self.feedback += "\nStudent response:\n" + str(student)
            return 0

    def grade(self, points):
        """Manually grade a problem out of 'points' with error message 'm'.
        The points earned are returned.
        """
        credit = -1
        while credit > points or credit < 0:
            try:
                credit = int(input("\nScore out of " + str(points) + ": "))
            except:
                credit = -1
        if credit != points:
            self.feedback += '\t\n' + str(raw_input("Feedback: "))
        return credit

    # Test cases --------------------------------------------------------------
    graph1 = {'A':['B'], 'B':['A', 'C',], 'C':['B']}
    graph2 = {'A':['D', 'B'], 'D':['A', 'C'],
              'C':['B', 'D'], 'B':['C', 'A']}
    graph3 = {'A':['B', 'F'], 'B':['A', 'C'], 'C':['B', 'D'],
              'D':['C', 'E'], 'E':['D', 'F'], 'F':['A', 'E', 'G'],
              'G':['A', 'F']}
    graph4 = {'A':['B'], 'B':['C', 'D'], 'C':['B', 'D'], 'D':['B', 'E'],
              'E':['F', 'G'], 'F':['E', 'H'], 'H':['F'],
              'G':['E', 'I', 'J'], 'I':['G', 'J'], 'J':['G', 'J', 'K'],
              'K':['J', 'L'], 'L':['K']}

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test Graph.__str__. 5 points.""" # TODO: Modify later
        print("Example graph printout:")
        print(Graph(_testDriver.graph4))
        print("Student graph printouts:")
        print(s.Graph(_testDriver.graph1))
        points = self.grade(2)
        print(s.Graph(_testDriver.graph2))
        return points + self.grade(3)

    def problem2(self, s):
        """Test Graph.traverse(). 10 Points."""
        print("Correct:")
        print(Graph(_testDriver.graph3).traverse('A'))
        print("Student response:")
        print(s.Graph(_testDriver.graph3).traverse('A'))
        points = self.grade(5)
        print("Correct:")
        print(Graph(_testDriver.graph4).traverse('A'))
        print("Student response:")
        print(s.Graph(_testDriver.graph4).traverse('A'))
        points += self.grade(5)
        return points

        '''
        def test_traverse(graph):
            solution = Graph(graph).traverse('A')
            student = list(s.Graph(graph).traverse('A'))
            return self.strTest(solution, student,
                                "\n\tGraph.traverse() failed.")

        points  = test_traverse(_testDriver.graph1)*2
        points += test_traverse(_testDriver.graph2)*2
        points += test_traverse(_testDriver.graph3)*3
        points += test_traverse(_testDriver.graph4)*3
        '''
        
        return points

    def problem4(self, s):
        """Test Graph.shortest_path(). 15 Points."""

        print("Correct:")
        print(Graph(_testDriver.graph2).traverse('A'))
        print("Student response:")
        print(s.Graph(_testDriver.graph2).traverse('A'))
        points = self.grade(5)
        print("Correct:")
        print(Graph(_testDriver.graph3).traverse('A'))
        print("Student response:")
        print(s.Graph(_testDriver.graph3).traverse('A'))
        points += self.grade(5)
        print("Correct:")
        print(Graph(_testDriver.graph4).traverse('A'))
        print("Student response:")
        print(s.Graph(_testDriver.graph4).traverse('A'))
        points += self.grade(5)
        return points
        '''
        def test_shortest_path(graph, target):
            solution = Graph(graph).shortest_path('A', target)
            student = list(s.Graph(graph).shortest_path('A', target))
            return self.strTest(solution, student,
                                "\n\tGraph.shortest_path() failed.")

        points  = test_shortest_path(_testDriver.graph1, 'C')*3
        points += test_shortest_path(_testDriver.graph2, 'C')*3
        points += test_shortest_path(_testDriver.graph3, 'G')*4
        points += test_shortest_path(_testDriver.graph4, 'K')*5

        rawcode = inspect.getsource(s.Graph.shortest_path).splitlines()[21:]
        code = ""
        for line in rawcode: code += line
        if len(code.partition('shortest_path(')[1]) > 0:
            for line in rawcode: print line
            print("\nCheck that the above code is NetworkX-free")
            points *= self.grade(1)
            points *= p; feedback += f

        return points
        '''
    def problem5(self, s):
        """Test convert_to_networkx. 10 points. (NOT USED HERE)"""

        def test_convert(graph):
            solution = convert_to_networkx(graph)
            student = s.convert_to_networkx(graph)
            count = self.strTest(solution.nodes(), student.nodes(),
                        "\n\tconvert_to_networkx() failed (nodes)")
            count += self.strTest(solution.edges(), student.edges(),
                        "\n\tconvert_to_networkx() failed (edges)")
            return count

        points  = test_convert(_testDriver.graph1)
        points += test_convert(_testDriver.graph2)
        points += test_convert(_testDriver.graph3)
        points += test_convert(_testDriver.graph4)*2

        return 0 #points

    def baconator(self, s):
        bacon = s.BaconSolver('movieData.txt')
        print("Path from Neeson, Liam to Bacon, Kevin:")
        print(bacon.path_to_bacon("Neeson, Liam"))
        print("Bacon number of Mortensen, Viggo: "),
        print(bacon.bacon_number("Mortensen, Viggo"))
        print("Average Bacon number: "),
        print(bacon.average_bacon("Bacon, Kevin"))
        print("Correct: %f"%2.6646202338108345)
        return self.grade(20)


if __name__ == '__main__':
    import solutions
    test(solutions)
