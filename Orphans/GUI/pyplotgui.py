import sys
from PyQt4 import QtGui, QtCore
import numpy as np

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # Creates Figure object to draw on
        self.fig = plt.figure()
        # Canvas widget displays figure
        self.canvas = FigureCanvas(self.fig)
        # Nav takes canvas object and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.calculateButton = QtGui.QPushButton("Plot")
        
        # Puts plot stuff into a box
        plotbox = QtGui.QVBoxLayout()
        plotbox.addWidget(self.toolbar)
        plotbox.addWidget(self.canvas)
        plotbox.addWidget(self.calculateButton)
        
        #make a slider to vary a parameter        
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider.setVisible(False)
        self.slider.setTickInterval(2)
        self.slider.setRange(1,100)
        
        plotbox.addWidget(self.slider)

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.calculateButton)
        
        # Connect button and slider to function
        self.calculateButton.clicked.connect(self.plot)
        self.slider.sliderMoved.connect(self.plot)
        
        # Set Window size and name
        self.setGeometry(50, 50, 500, 400)
        self.setWindowTitle("Plotting GUI")
        
        # Set central widget
        window = QtGui.QWidget()
        window.setLayout(plotbox)
        self.setCentralWidget(window)

    def plot(self):
        self.slider.setVisible(True)
        n = self.slider.value()
        
        g = lambda x: np.sin(x)
        y = np.linspace(0, n, 500)
        
        # create an axis
        ax = self.fig.add_subplot(111)
                
        # discards the old graph
        ax.hold(False)

        #ax.plot(x, f(x))
        ax.plot(y, g(y))

        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
    
    