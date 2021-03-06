import wave
import numpy

from .tracks import NumpyTrack

def save(track, filename, samplerate=44100, blocksize=4096):
    """
    Save a track to a file.
    """

    w = wave.open(filename, 'w')
    w.setparams((1, 2, samplerate, 0, 'NONE', 'not compressed'))

    maximum = 2**15 - 1
    dtype = numpy.dtype('<i2')

    try:
        for values in track.as_arrays_iter(samplerate, blocksize, zfill = False):
            numpy.clip(values, -1, 1, out=values)
            values *= maximum

            values = numpy.array(values, dtype)

            w.writeframes(values.tostring())
    finally:
        w.close()

def open(filename):
    """
    Open a wave file and return a list of tracks corresponding
    to channels in the file.
    """

    w = wave.open(filename, 'r')

    try:
        data = numpy.fromstring(
            w.readframes(w.getnframes()),
            "<i" + str(w.getsampwidth()))

        data_float = numpy.array(data, dtype='float');
        data_float /= 2**(8 * w.getsampwidth() - 1) - 1

        ret = []
        for i in range(w.getnchannels()):
            ret.append(
                NumpyTrack(data_float[i::w.getnchannels()], w.getframerate()))

        return ret

    finally:
        w.close()
