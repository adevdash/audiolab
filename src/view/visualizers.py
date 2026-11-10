
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure
from matplotlib import animation

import numpy as np

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

        t = np.linspace(0, 3, 40)
        g = -9.81
        v0 = 12
        z = g * t**2 / 2 + v0 * t

        v02 = 5
        z2 = g * t**2 / 2 + v02 * t

        scat = ax.scatter(t[0], z[0], c="b", s=5, label=f'v0 = {v0} m/s')
        line2 = ax.plot(t[0], z2[0], label=f'v0 = {v02} m/s')[0]
        ax.set(xlim=(0, 3), ylim=(-4, 10), xlabel='Time [s]', ylabel='Z [m]')
        ax.legend()

        def update(frame):
            # for each frame, update the data stored on each artist.
            x = t[:frame]
            y = z[:frame]
            # update the scatter plot:
            data = np.stack([x, y]).T
            scat.set_offsets(data)
            # update the line plot:
            line2.set_xdata(t[:frame])
            line2.set_ydata(z2[:frame])
            return (scat, line2)

        ani = animation.FuncAnimation(fig=self.figure, func=update, frames=40, interval=30)
        ax.plot()
        # refresh canvas
        self.draw()

class SpectrumVisualizer(object):
    def __init__(self):
        pass

class TimeFreqVisualizer(object):
    def __init__(self):
        pass