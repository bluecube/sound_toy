import wave
import struct
import itertools
import math

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
