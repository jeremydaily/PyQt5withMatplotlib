
# Simple Qt5 application embedding matplotlib canvases
#
# Based on material from 
# Copyright (C) 2005 Florent Rougon
#               2006 Darren Dale
#
#
# Modified by Jeremy Daily on 21 May 2017
#
# This file is a modified example program for matplotlib. It may be used and
# modified with no restriction; raw copies as well as modified versions
# may be distributed without limitation.

import sys
import os
import random
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from numpy import arange, sin, pi

from matplotlib.backends import qt_compat
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

class DataConnection():
    def __init__(self):
        pass

    def provide_data(self,n = 10):
        return [random.randint(0, 10) for i in range(n)]

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class MyStaticMplCanvas(MyMplCanvas):
    """Simple static canvas from matplotlib with a sine plot."""
    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself frequently with a new plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_figure)
        self.timer.start(100)

    def compute_initial_figure(self):
        pass
    
    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class ApplicationWindow(QWidget):
    def __init__(self, parent=None):
        super(ApplicationWindow, self).__init__(parent)
        self.setWindowTitle("Matplotlib in QT Demo")

        self.main_widget = QWidget(self)

        self.data_generator = DataConnection()
        
        print(self.data_generator.provide_data())
        
        layout = QVBoxLayout(self.main_widget)
        self.static_canvas = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        layout.addWidget(self.static_canvas)

        button = QPushButton('Generate Data', self)
        button.setToolTip('This is a tool tip')
        button.clicked.connect(self.on_click)
        layout.addWidget(button)

       
        #self.dynamic_canvas = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        #layout.addWidget(self.dynamic_canvas)

        self.setLayout(layout)
    def on_click(self):
        print(self.data_generator.provide_data(20))
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = ApplicationWindow()
    screen.show()
    app.exec_()
    screen.dynamic_canvas.timer.stop() #Stops the repeating plotter
    sys.exit()


