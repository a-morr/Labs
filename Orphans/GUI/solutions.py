# Solutions.py
from PyQt4 import QtGui
import sys
import numpy as np
import functools


class matrix_calculator(QtGui.QMainWindow):
    def __init__(self):
        super(matrix_calculator, self).__init__()
        self._initUI()
        
    def _initUI(self):
        self.rows = 3
        self.columns = 3
        # For second matrix if multiplication
        self.rows2 = 3
        self.columns2 = 3
        self.color = None

        # Creates menu
        menubar = self.menuBar()                
        
        # Import Matrix
        self.importMatrix = QtGui.QAction('Import Matrix', self)
        self.importMatrix.triggered.connect(functools.partial(self.fileDialog, 1))
        # Note: functools.partial is simply a function that allows you to 
        # pass arguments through this connect function.
        
        self.importMatrix2 = QtGui.QAction('Import Matrix2', self)
        self.importMatrix2.triggered.connect(functools.partial(self.fileDialog, 2))
        
        # Set Background color        
        self.pickColor = QtGui.QAction('Background Color', self)
        self.pickColor.triggered.connect(self.colorDialog)
        
        # Add menus to menubar        
        self.fileMenu = menubar.addMenu('&File')
        self.importMenu = self.fileMenu.addMenu('Import')
        self.importMenu.addAction(self.importMatrix)
        self.customMenu = menubar.addMenu('&Customize')
        self.customMenu.addAction(self.pickColor)
        # We will add importMatrix2 later only if the calculation is set to multiplication
        
        # Creates the table that will be used for the inputted matrix
        self.matrix = QtGui.QTableWidget()
        self.matrix.setRowCount(self.rows)
        self.matrix.setColumnCount(self.columns)
        for i in xrange(self.columns):
            # makes the columns a little skinnier
            self.matrix.setColumnWidth(i, 60)
            
        # Creates a second matrix table for multiplication
        self.matrix2 = QtGui.QTableWidget()
        self.matrix2.setRowCount(self.rows)
        self.matrix2.setColumnCount(self.columns)
        for i in xrange(self.columns):
            # makes the columns a little skinnier
            self.matrix2.setColumnWidth(i, 60)
        # Hide matrix2 until needed
        self.matrix2.setVisible(False)
        
        # Creates a push button to calculate
        self.calculateButton = QtGui.QPushButton("Calculate")

        # Creates a smashing awesome radio button
        self.radio = QtGui.QRadioButton("Fill empty cells with 0")
        
        # Creates the output textbox
        self.output = QtGui.QPlainTextEdit("Output here")
        
        # Creates spinboxes for matrix dimensions
        self.dimRows = QtGui.QSpinBox()
        self.dimCols = QtGui.QSpinBox()
        self.dimRows.setRange(2,10)
        self.dimCols.setRange(2,10)
        self.dimRows.setValue(3)
        self.dimCols.setValue(3)
        labelRows = QtGui.QLabel("Number of Rows")
        labelCols = QtGui.QLabel("Number of Columns")
        
        self.dimRows2 = QtGui.QSpinBox()
        self.dimCols2 = QtGui.QSpinBox()
        self.dimRows2.setRange(2,10)
        self.dimCols2.setRange(2,10)
        self.dimRows2.setValue(3)
        self.dimCols2.setValue(3)
        self.dimRows2.setVisible(False)
        self.dimCols2.setVisible(False)
        
        # Creates drop down menu for calculation options
        self.matrixFunction = QtGui.QComboBox()
        self.matrixFunction.addItem("Determinant")
        self.matrixFunction.addItem("Eigenvalues")
        self.matrixFunction.addItem("Eigenvectors")
        self.matrixFunction.addItem("Inverse")
        self.matrixFunction.addItem("Moore-Penrose")
        self.matrixFunction.addItem("Multiplication")
        self.matrixFunction.addItem("SVD")
        self.matrixFunction.addItem("QR")
        
        
        # Creates grids for side-by-side widgets
        dispgrid = QtGui.QGridLayout()
        dispgrid.addWidget(self.matrix, 0, 0)
        dispgrid.addWidget(self.matrix2, 0, 1)
        
        dispgrid2 = QtGui.QGridLayout()
        dispgrid2.addWidget(self.dimRows, 0, 0)
        dispgrid2.addWidget(labelRows, 0, 1)
        dispgrid2.addWidget(self.dimRows2, 0, 2)
        dispgrid2.addWidget(self.dimCols, 1, 0)
        dispgrid2.addWidget(labelCols, 1, 1)
        dispgrid2.addWidget(self.dimCols2, 1, 2)
        dispgrid2.addWidget(self.radio, 2, 0)
        

        # Creates layout, adding the grids and remaining widgets
        layout = QtGui.QVBoxLayout()
        layout.addLayout(dispgrid)
        layout.addLayout(dispgrid2)
        layout.addWidget(self.matrixFunction)
        layout.addWidget(self.calculateButton)
        layout.addWidget(self.output)
        
        # Sets central layout
        window = QtGui.QWidget()
        window.setLayout(layout)
        self.setCentralWidget(window)
        
        # Sets the location of the window on the screen
        # The first two numbers are the location of the top left corner
        # The last two numbers are the size of the window
        self.setGeometry(50, 50, 500, 600)
        self.setWindowTitle("Deluxe Matrix Calculator")
        self.show()
        
        # Adds the functionality of the buttons
        self.calculateButton.clicked.connect(self.clickCalculate)
        self.radio.clicked.connect(self.clickRadio)
        self.matrixFunction.activated.connect(self.changeDisplay)
        self.dimRows.valueChanged.connect(self.updateRows)
        self.dimCols.valueChanged.connect(self.updateCols)
        self.dimRows2.valueChanged.connect(self.updateRows2)
        self.dimCols2.valueChanged.connect(self.updateCols2)
        

        
    def clickCalculate(self):
        #get matrix out of table
        Matrix = np.zeros((self.rows, self.columns))
        for i in xrange(self.rows):
            for j in xrange(self.columns):
                try:
                    Matrix[i, j] = self.matrix.item(i,j).text()
                except AttributeError:
                    self.output.setPlainText("Attribute Error: please fill in all the boxes.")
                    return
                except ValueError:
                    self.output.setPlainText("Value Error: invalid character detected.")
                    return;
        
        result = "Function not yet implemented."
        calculation = self.matrixFunction.currentText()
        
        #Perform calculation
        if (calculation == "Determinant"):
            try:
                result = str(np.linalg.det(Matrix))
            except:
                self.output.setPlainText("LinAlg Error: Matrix must be square.")
                return
                
        elif (calculation == "Inverse"):
            try:
                result = str(np.linalg.inv(Matrix))
            except:
                self.output.setPlainText("Error: Matrix is not invertible.")
                return
                
        elif (calculation == "Multiplication"):
            # Get second matrix
            Matrix2 = np.zeros((self.rows2, self.columns2))
            for i in xrange(self.rows2):
                for j in xrange(self.columns2):
                    try:
                        Matrix2[i, j] = self.matrix2.item(i,j).text()
                    except AttributeError:
                        self.output.setPlainText("Attribute Error: Please fill in all the boxes.")
                        return
                    except ValueError:
                        self.output.setPlainText("Value Error: Invalid character detected.")
                        return
            try:
                result = str(Matrix.dot(Matrix2))
            except ValueError:
                self.output.setPlainText("Value Error: Dimensions not aligned.")
                return
                
        elif (calculation == "Moore-Penrose"):
            try:
                result = str(np.linalg.pinv(Matrix))
            except:
                self.output.setPlainText("Error: Computation does not converge.")
                return
                
        elif (calculation == "Eigenvalues"):
            try:
                result = str(np.linalg.eig(Matrix)[0])
            except:
                self.output.setPlainText("LinAlg Error: Matrix must be square.")
                return
                
        elif (calculation == "Eigenvectors"):
            try:
                result = str(np.linalg.eig(Matrix)[1])
            except:
                self.output.setPlainText("LinAlg Error: Matrix must be square.")
                return
                
        elif (calculation == "QR"):
            try:                
                q, r = np.linalg.qr(Matrix)                
                result = "Q:\n" + str(q) + "\n\nR:\n" + str(r)
            except:
                self.output.setPlainText("Error: Unknown error.")
                
        elif (calculation == "SVD"):
            try:
                u, s, v = np.linalg.svd(Matrix)
                result = "U:\n" + str(u) + "\n\nSingular Values:\n" + str(s) + "\n\nV.H:\n" + str(v)
            except:
                self.output.setPlainText("Error: Unknown error.")
                return
            

            
        self.output.setPlainText(result)
        
    
    
    def clickRadio(self):
        # There's gotta be a better way to do this
        for i in range(self.rows):
            for j in range(self.columns):
                # To find out if there is something in this slot,
                # attempt to get the item in this slot.
                # If an error is thrown, fill this slot with 0.
                try:
                    a = self.matrix.item(i, j).text()
                except AttributeError:
                    self.matrix.setItem(i, j, QtGui.QTableWidgetItem(str(0)))
                    
        if (self.matrix2.isVisible()):
            for i in range(self.rows2):
                for j in range(self.columns2):
                    try:
                        a = self.matrix2.item(i, j).text()
                    except AttributeError:
                        self.matrix2.setItem(i, j, QtGui.QTableWidgetItem(str(0)))
        
    
    def changeDisplay(self):
        '''Depending on the selected calculation,
        show or hide various Widgets.
        '''
        if (self.matrixFunction.currentText() == "Multiplication"):
            self.matrix2.setVisible(True)
            self.dimRows2.setVisible(True)
            self.dimCols2.setVisible(True)
            
            self.importMenu.addAction(self.importMatrix2)
        else:
            self.matrix2.setVisible(False)
            self.dimRows2.setVisible(False)
            self.dimCols2.setVisible(False)
            self.importMenu.removeAction(self.importMatrix2)
            
            
    def updateRows(self, n):
        '''Changes number of rows'''
        self.rows = n
        self.matrix.setRowCount(self.rows)
        
    def updateCols(self, n):
        '''Changes number of columns'''
        self.columns = n
        self.matrix.setColumnCount(self.columns)
        for i in xrange(self.columns):
            self.matrix.setColumnWidth(i, 60)
            #TODO: make it not resize columns that have been resized by user

    def updateRows2(self, n):
        '''Changes number of rows in matrix2'''
        self.rows2 = n
        self.matrix2.setRowCount(self.rows2)
        
    def updateCols2(self, n):
        '''Changes number of columns in matrix2'''
        self.columns2 = n
        self.matrix2.setColumnCount(self.columns2)
        for i in xrange(self.columns2):
            self.matrix2.setColumnWidth(i, 60)
            #TODO: make it not resize columns that have been resized by user        
            
    def fileDialog(self, which):
        '''Dialog box for importing a matrix.
        Correct format for a matrix file:
        Number of rows, number of columns, all entries;
        separated by whitespace.
        If there are not enough numbers in the file, fill the 
        remainder of the matrix with 0s.  Excess numbers are ignored.
        '''
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        try:
            f = open(filename).read().split()
        except:
            self.output.setPlainText("IO Error: bad file.")
            return
        
        if (which == 1):
            self.rows = int(f[0])
            self.matrix.setRowCount(self.rows)
            self.columns = int(f[1])
            self.matrix.setColumnCount(self.columns)
            
            # Iterate through the list f and set entries of matrix
            for i in xrange(self.rows):
                for j in xrange(self.columns):
                    try:
                        self.matrix.setItem(i, j, QtGui.QTableWidgetItem(str(f[i*self.columns + j + 2])))
                    except IndexError:
                        # If the file did not have enough numbers in it,
                        # fill the remaining entries with 0
                        f = np.zeros((self.rows * self.columns + 2))
                        self.matrix.setItem(i, j, QtGui.QTableWidgetItem(str(f[i*self.columns + j + 2])))
                        
        elif (which == 2):
            self.rows2 = int(f[0])
            self.matrix2.setRowCount(self.rows)
            self.columns2 = int(f[1])
            self.matrix2.setColumnCount(self.columns)
            
            # Iterate through the list f and set entries of matrix2
            for i in xrange(self.rows2):
                for j in xrange(self.columns2):
                    try:
                        self.matrix2.setItem(i, j, QtGui.QTableWidgetItem(str(f[i*self.columns2 + j + 2])))
                    except IndexError:
                        # If the file did not have enough numbers in it,
                        # fill the remaining entries with 0
                        f = np.zeros((self.rows2 * self.columns2 + 2))
                        self.matrix2.setItem(i, j, QtGui.QTableWidgetItem(str(f[i*self.columns2 + j + 2])))
                    
                    
    def colorDialog(self):
        # Sets background color
        color = QtGui.QColorDialog.getColor()
        if color.isValid():
            p = self.palette()
            p.setColor(self.backgroundRole(), color)
            self.setPalette(p)
        
    
if __name__== "__main__":
    app = QtGui.QApplication(sys.argv)
    m = matrix_calculator()
    sys.exit(app.exec_())



