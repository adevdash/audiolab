from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QColor, QPalette
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, \
    QPushButton, QLabel, QLineEdit, QVBoxLayout, QMenu, QHBoxLayout, QComboBox
import sys
import random
import numpy as np

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure

import globals
from view.Buttons import PlayPause, PowerButton
from audio.source import AudioSource
from audio.components import Mixer, Speaker

class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)



# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMouseTracking(True)
        self.setWindowTitle("My App")
        self.label = QLabel("Click on this window")
        self.label.setMouseTracking(True)


        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()

        self.audioSource1 = AudioSource("SIN", 440)
        self.audioSource2 = AudioSource("SIN", 480)
        self.mixer = Mixer([self.audioSource1, self.audioSource2])
        self.speaker = Speaker(self.mixer)

        self.figure = Figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        # layout = QtGui.QVBoxLayout()
        # layout.addWidget(self.toolbar)
        # layout.addWidget(self.canvas)
        # layout.addWidget(self.button)
        # self.setLayout(layout)

        layout2.addWidget(QLabel("440 Hz"))
        layout2.addWidget(PowerButton(self.audioSource1))
        layout2.addWidget(QLabel("480 Hz"))
        layout2.addWidget(PowerButton(self.audioSource2))
        layout2.addWidget(QLabel("Mixer"))
        layout2.addWidget(PowerButton(self.mixer))
        layout2.addWidget(QLabel("Speaker"))
        layout2.addWidget(PowerButton(self.speaker))
        layout2.addWidget(Color("purple"))

        layout1.addLayout(layout2)

        layout1.addWidget(Color("green"))

        layout3.addWidget(PowerButton(self.audioSource1))
        layout3.addWidget(self.button)
        layout3.addWidget(self.canvas)

        layout1.addLayout(layout3)

        container = QWidget()
        container.setLayout(layout1)
        self.setCentralWidget(container)
        self.setMinimumSize(QSize(400, 300))

    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec(e.globalPos())

    def plot(self):
        ''' plot some random stuff '''
        data = [random.random() for i in range(10)]
        # create an axis
        ax = self.figure.add_subplot(111)
        # discards the old graph
        ax.clear()

        ax.plot(data, '*-')
        # refresh canvas
        self.canvas.draw()

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.