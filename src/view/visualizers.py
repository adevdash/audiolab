
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure

import random

class WaveformVisualizer(FigureCanvas):
    def __init__(self, source = None):
        self.figure = Figure()
        super().__init__(self.figure)
        self.source = source

    def plot(self):
        ''' plot some random stuff '''
        data = [random.random() for i in range(10)]
        # create an axis
        ax = self.figure.add_subplot(111)
        # discards the old graph
        ax.clear()

        ax.plot(data, '*-')
        # refresh canvas
        self.draw()

class SpectrumVisualizer(object):
    def __init__(self):
        pass

class TimeFreqVisualizer(object):
    def __init__(self):
        pass