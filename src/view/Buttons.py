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
            
            