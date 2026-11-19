from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QColor, QPalette
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, \
    QPushButton, QLabel, QLineEdit, QVBoxLayout, QMenu, QHBoxLayout, QComboBox
import sys, os

from pathlib import Path
sys.path.append(str(Path('./src').resolve()))

from Application import Application
from view.Buttons import Device, VDevicePanel
from audio.source import AudioSource

class MainWindow(Application):
    def __init__(self):
        super().__init__()

        # self.source = AudioSource("SIN")
        # self.device = Device(self.source, self)

        # self.allDevices.append(self.device)
        # self.updateDeviceLists()

        self.devicePanel = VDevicePanel(self)
        self.setCentralWidget(self.devicePanel)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()