import tracks
import wave
import struct
import numpy

class Sampler(tracks.BaseTrack):
    def __init__(self, samplerate, filename):
        w = wave.open(filename, 'r')

        nchannels = w.getnchannels()
        samplewidth = w.getsamwidth()
        
        ratio = w.getframerate() / samplerate
        
