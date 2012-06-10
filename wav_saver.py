import wave
import struct
import itertools
import math
import numpy

from .tracks import SampledData

def _packed_iter(track, maximum, packer):
    for x in track:
        val = max(-maximum, min(maximum, int(maximum * x)))
        yield packer.pack(val)

def save(track, filename, samplerate=44100, blocksize=4096):
    """
    Save a track to a file.
    Forces samplerate of the track to the parameter.
    """
    track.set_samplerate(samplerate)

    save_iterator(iter(track), filename, samplerate, blocksize)

def save_iterator(track, filename, samplerate=44100, blocksize=4096):
    """
    Save an iterator to a file.
    """
    w = wave.open(filename, 'w')
    try:
        w.setparams((1, 2, samplerate, 0, 'NONE', 'not compressed'))

        it = _packed_iter(track, 2**15 - 1, struct.Struct('<h'))

        while True:
            buff = b''.join(itertools.islice(it, blocksize))

            if not len(buff):
                break

            w.writeframes(buff)
    except KeyboardInterrupt:
        print("Keyboard interrupt.")
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
                SampledData(data_float[i::w.getnchannels()], w.getframerate()))

        return ret

    finally:
        w.close()
