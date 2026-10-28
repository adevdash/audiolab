from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QPushButton

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
