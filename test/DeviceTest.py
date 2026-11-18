from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QColor, QPalette
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, \
    QPushButton, QLabel, QLineEdit, QVBoxLayout, QMenu, QHBoxLayout, QComboBox
import sys, os

from pathlib import Path
sys.path.append(str(Path('./src').resolve()))

from view.Buttons import Device
from audio.source import AudioSource

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.allDevices = []

        self.source = AudioSource("SIN")
        self.device = Device(self.source, self)

        self.allDevices.append(self.device)
        self.updateDeviceLists()

        self.setCentralWidget(self.device)

    def removeDevice(self):
        print("removeDevice stub")

    def updateDeviceLists(self):
        for device in self.allDevices:
            device.updateDeviceList()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()