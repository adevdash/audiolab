import globals
import numpy as np
import sounddevice as sd
import sys
class AudioSource(object):
    def __init__(self, source_type, block_size=4096, f = 440.0):
        self.source_type = source_type
        self.block_size = block_size
        self.active = False
        self.f = f  # Default frequency in Hz
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

    def genAudioCallback(self):
        freq = self.f
        def audioCallback(outdata: np.ndarray, frames: int,
            time: any, status: sd.CallbackFlags) -> None:
            if status:
                print(status, file=sys.stderr)
            print("Calling callback")
            
            outdata[:, 0] = np.sin(2*np.pi * freq * (np.arange(frames) + self.samples_sent) / globals.Fs)
            self.samples_sent += frames
        return audioCallback

    def reset(self):
        self.samples_sent = 0