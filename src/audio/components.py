import numpy as np
import sounddevice as sd
import globals
import sys

class Playable(object):
    def __init__(self):
        self.outputs = []
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
                x += input.genAudio(nSamp, nCh)
        return x