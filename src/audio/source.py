import globals
import numpy as np

class AudioSource(object):
    def __init__(self, source_type, block_size=4096):
        self.source_type = source_type
        self.block_size = block_size
        self.active = False
        self.f = 440.0  # Default frequency in Hz
        self.A = 1.0    # Default amplitude (0.0 to 1.0)
        self.samples_sent = 0

    def genAudio(self):
        if self.source_type == 'SIN':
            x = np.sin(2*np.pi * self.f * (np.arange(self.block_size) + self.samples_sent) / globals.Fs)
        elif self.source_type == 'SAW':
            pass
        elif self.source_type == 'PWM':
            pass
        elif self.source_type == 'TRI':
            pass
        self.samples_sent += self.block_size
        return self.A * x