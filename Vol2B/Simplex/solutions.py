# solutions.py
"""Volume II Lab 16: Simplex. Solutions file.

Student Instructions:
Problems 1-6 give instructions on how to build the SimplexSolver class.
The grader will test your class by solving various linear optimization
problems and will only call the constructor and the solve() methods directly.
Write good docstrings for each of your class methods and comment your code.

prob7() will also be tested directly.
"""

import numpy as np

# Problems 1-6
class SimplexSolver(object):
    """Class for solving the standard linear optimization problem

                        maximize        c^Tx
                        subject to      Ax <= b
                                         x >= 0
    via the Simplex algorithm.
    """
    
    def __init__(self, c, A, b):
        """

        Parameters:
            c (1xn ndarray): The coefficients of the linear objective function.
            A (mxn ndarray): The constraint coefficients matrix.
            b (1xm ndarray): The constraint vector.

        Raises:
            ValueError: if the given system is infeasible at the origin.
        """

        # Check for feasibility at the origin.
        if np.min(b) < 0:
            raise ValueError("Infeasible at the origin")

        # Generate the initial Tableau.
        self.tableau = self._generateTableau(c, A, b)

    def _generateTableau(self, c, A, b):
        """Generate the initial tableau.

        [0,0] is the value of the objective function
        Along the top row of the tableau is the objective function
        in the form 0 = -c.

        Down the first column are the system's current constraints.
        The non-negative constraints for all variables is assumed.

        The remaining entries in the matrix are the constraint equations.
        """        
        # Initialize a tableau of zeros.
        m, n = A.shape
        tableau = np.zeros((1+m, 1+m+n))
        
        # Slice in each piece.
        tableau[0,1:] = np.hstack((-c, np.zeros(m)))
        tableau[1:,0] = b
        tableau[1:,1:] = np.hstack((A, np.eye(m)))

        return tableau

    # Problem 4a
    def _pivot_col(self):
        """Return the column index of the next pivot column.
        This is the first negative coefficient of the objective function.
        """
        if np.all(self.tableau[0,1:] >= 0):             # Done pivoting.
            return "Done"
        return np.argmax(self.tableau[0,1:] < 0) + 1    # First negative.

    # Problem 4b
    def _pivot_row(self, index):
        """Determine the row index of the next pivot row using the ratio test
        (Bland's Rule).
        """
        column = self.tableau[1:,index]
        if column.max() <= 0:
            raise ValueError("Problem is unbounded.")
        b = self.tableau[1:,0]
        ratios = []
        for i in xrange(len(column)):
            if column[i] == 0:                      # Avoid dividing by zero.
                ratios.append(np.inf)
            else:                                   # Avoid negative ratios.
                ratio = float(b[i])/column[i]
                if ratio - 1e-06 > 0:
                    ratios.append(ratio)
                else:
                    ratios.append(np.inf)
        return np.argmin(ratios) + 1

    # Problem 5
    def pivot(self):
        """Select the column and row to pivot on. Reduce the column to an
        elementary vector.
        """
        col = self._pivot_col()
        if col == "Done":                                # Done pivoting
            return "DONE"
        row = self._pivot_row(col)

        # Perform the actual pivot.
        self.tableau[row] /= float(self.tableau[row, col])
        for i in xrange(self.tableau.shape[0]):
            if i != row:
                self.tableau[i] -= self.tableau[i,col]*self.tableau[row]

    def solve(self):
        """Solve the linear optimization problem.

        Returns:
            (float) The maximum value of the objective function.
            (dict): The basic variables and their values.
            (dict): The nonbasic variables and their values.
        """
        # Pivot until done.
        progress = self._pivot_col()
        while progress != "DONE":
            progress = self.pivot()
        
        # Read the tableau to construct the final results.
        basic, nonbasic = {}, {}
        for i in xrange(self.tableau.shape[1]-1):
            if self.tableau[0,i+1] == 0:
                index = self.tableau[1:,i+1].argmax()
                basic[i] = self.tableau[index+1, 0]
            else:
                nonbasic[i] = 0

        return self.tableau[0,0], basic, nonbasic

# Problem 7
def prob7(filename='productMix.npz'):
    """Solve the product mix problem for the data in 'productMix.npz'.

    Parameters:
        filename (str): the path to the data file.

    Returns:
        The minimizer of the problem (as an array).
    """
    # Unpack the data.
    data = np.load(filename)
    A, c, m, d = data['A'], data['p'], data['m'], data['d']

    # Put the problem in standard form and use Simplex to solve.
    b = np.hstack((m,d))
    A = np.vstack((A, np.eye(A.shape[1])))
    s = SimplexSolver(c, A, b)
    primal_objective, basic, nonbasic = s.solve()

    # Construct the final results.
    coordinates = []
    for i in xrange(len(c)):
        if i in basic:
            coordinates.append(basic[i])
        else:
            coordinates.append(0)
    return np.array(coordinates)

# END OF SOLUTIONS ============================================================
