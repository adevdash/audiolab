import numpy as np
import sounddevice as sd
import globals
import sys

class Playable(object):
    def __init__(self):
        self.outputs = []

    def genAudio(self, nSamp: int) -> np.ndarray:
        return np.zeros((nSamp, 1))

    def genAudioCallback(self):
        def audioCallback(outdata: np.ndarray, frames: int, time: CData, status: sd.CallbackFlags) -> None:
            if status:
                print(status, file = sys.stderr)

            print(outdata.shape)
            outdata[:] = self.genAudio(frames)

        return audioCallback


class Mixer(Playable):
    def __init__(self, inputs):
        self.inputs = inputs
        self.outputBuffer = np.empty(0)

    def writeOutSamples(self):
        def audioCallback(outdata: np.ndarray, frames: int,
            time: any, status: sd.CallbackFlags) -> None:
            if status:
                print(status, file=sys.stderr)
            outdata[:, 0] = self.genAudio(frames)
        return audioCallback

