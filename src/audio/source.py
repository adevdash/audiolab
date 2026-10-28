import globals
import numpy as np
import sounddevice as sd
import sys
from audio.components import Playable
class AudioSource(Playable):
    def __init__(self, source_type, f = 440.0):
        self.source_type = source_type
        self.active = False
        self.f = f  # Default frequency in Hz
        self.A = 1.0    # Default amplitude (0.0 to 1.0)
        self.samples_sent = 0

    def genAudio(self, nSamp):
        if self.source_type == 'SIN':
            x = np.sin(2*np.pi * self.f * (np.arange(nSamp) + self.samples_sent) / globals.Fs)
        elif self.source_type == 'SAW':
            pass
        elif self.source_type == 'PWM':
            pass
        elif self.source_type == 'TRI':
            pass
        self.samples_sent += nSamp
        return self.A * np.expand_dims(x, axis=1)

    def reset(self):
        self.samples_sent = 0