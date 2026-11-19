from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QPushButton, QWidget, QHBoxLayout,
    QVBoxLayout, QLabel,
    QComboBox)
from PyQt6.QtGui import QAction, QColor, QPalette

import sounddevice as sd
import globals
import time

from PyQt6.QtCore import QRunnable, QThreadPool, QTimer, pyqtSlot
# ...

class AudioProcess(QRunnable):
    """Worker thread."""

    def __init__(self, parent, latency):
        super().__init__()
        self.parent = parent
        self.latency = latency

    @pyqtSlot()
    def run(self):
        """Your long-running job goes in this method."""
        print("Thread start")
        with sd.OutputStream(
                #device=args.device,
                channels=1,
                callback=self.parent.audioSource.genAudioCallback(),
                samplerate=globals.Fs):
            while self.parent.isChecked():
                time.sleep(self.latency)
        print("Thread complete")

class PowerButton(QPushButton):
    # Simple Button to start or stop a device
    def __init__(self, device):
        super().__init__()
        self.setText("OFF")
        self.setCheckable(True)
        self.setChecked(False)
        self.clicked.connect(self.onClick)
        self.device = device

    def onClick(self):
        if self.isChecked():
            self.device.start()
            self.setText("ON")
        else:
            self.device.stop()
            self.setText("OFF")

class PlayPause(QPushButton):
    def __init__(self, audioSource):
        super().__init__()
        self.setText("Play")
        self.setCheckable(True)
        self.clicked.connect(self.onClick)
        self.setMinimumSize(QSize(100, 50))
        self.audioSource = audioSource
        self.threadpool = QThreadPool()
        thread_count = self.threadpool.maxThreadCount()
        print(f"Multithreading with maximum {thread_count} threads")

    def onClick(self):
        if self.isChecked():
            self.setText("Pause")
            self.threadpool.start(AudioProcess(self, .1))
        else:
            self.setText("Play")
class Device(QWidget):
    def __init__(self, device, app):
        super().__init__()

        self.layout = QVBoxLayout()
        self.app = app

        self.device = device

        row1 = QHBoxLayout()
        row1.addWidget(QLabel(device.name))
        closeButton = QPushButton("X")
        closeButton.clicked.connect(self.removeDevice)
        row1.addWidget(closeButton)
        self.layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(PowerButton(device))
        self.deviceList = QComboBox()
        row2.addWidget(self.deviceList)

        self.layout.addLayout(row2)
        
        self.setLayout(self.layout)

    def updateDeviceList(self):
        self.deviceList.clear()
        self.deviceList.addItems([None] + [d.name for d in self.app.allDevices if d and d != self])

    def removeDevice(self):
        self.setParent(None)
        self.app.removeDevice(self)

    @property
    def name(self):
        return self.device.name
class VDevicePanel(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.allDevices = app.allDevices
        self.devices = []

        self.layout = QVBoxLayout()

        self.addDeviceButton = QPushButton("+")
        self.addDeviceButton.clicked.connect(self.addDevice)

        self.layout.addWidget(self.addDeviceButton)
        self.setLayout(self.layout)

    def addDevice(self):
        newDevice = self.app.createDevice()
        self.layout.addWidget(newDevice)
        self.devices.append(newDevice)