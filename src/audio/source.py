import globals
import numpy as np
import sounddevice as sd
import sys
from audio.components import Playable
class AudioSource(Playable):
    def __init__(self, source_type, f = 440.0):
        super().__init__()
        self.source_type = source_type
        self.active = False
        self.f = f
        self.A = 1.0
        self.samples_sent = 0
        self.phase = 0

    @property
    def f(self):
        return self._f
    @f.setter
    def f(self, f):
        self._f = f
        self._smp_per_period = globals.Fs/f

    def genAudio(self, nSamp, nCh):
        if self.source_type == 'SIN':
            x = np.sin(2*np.pi * self.f * (np.arange(nSamp) + self.samples_sent) / globals.Fs)
        elif self.source_type == 'SAW':
            x = (np.arange(nSamp) + self.samples_sent) / self._smp_per_period
            x = 2 * np.modf(x)[0] - 1
        elif self.source_type == 'SQR':
            pass
        elif self.source_type == 'TRI':
            pass
        self.samples_sent += nSamp
        self.phase += np.modf(nSamp/self._smp_per_period)[0]
        return self.A * np.tile(x, (nCh, 1)).T

    def reset(self):
        self.samples_sent = 0