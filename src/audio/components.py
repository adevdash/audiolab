import numpy as np
import sounddevice as sd
import globals
import sys
from PyQt6.QtCore import QRunnable, QThreadPool, QTimer, pyqtSlot
import time

class Playable(object):
    def __init__(self):
        self.isRunning = False

    def genAudio(self, nSamp: int, nCh: int) -> np.ndarray:
        return np.zeros((nSamp, nCh))

    def start(self):
        self.isRunning = True
    def stop(self):
        self.isRunning = False

    def genAudioCallback(self):
        def audioCallback(outdata: np.ndarray, frames: int, time: CData, status: sd.CallbackFlags) -> None:
            if status:
                print(status, file = sys.stderr)

            print(outdata.shape)
            outdata[:] = self.genAudio(frames, outdata.shape[1])

        return audioCallback

class Mixer(Playable):
    def __init__(self, inputs):
        self.inputs = inputs

    def genAudio(self, nSamp: int, nCh: int) -> np.ndarray:
        x = np.zeros((nSamp, nCh))
        for input in self.inputs:
            if input.isRunning:
                x_input = input.genAudio(nSamp, nCh)
                x += x_input
        self.debug += 1
        return x


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
                callback=self.parent.genAudioCallback(),
                samplerate=globals.Fs):
            while self.parent.isRunning:
                time.sleep(self.latency)
        print("Thread complete")

class Speaker(Playable):
    def __init__(self, input, latency = 0.1):
        super().__init__()
        self.threadpool = QThreadPool()
        self.latency = latency
        self.genAudioCallback = input.genAudioCallback

    def start(self):
        self.isRunning = True
        self.threadpool.start(AudioProcess(self, self.latency))