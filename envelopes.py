import itertools
import math

from . import tracks

def _lin_iterator(a, b, count = None):
    """
    Iterate over linear function a * x + b where x goes from 0 to count.
    If count is None, iterates to infinity.
    """
    if count is None:
        it = itertools.count()
    else:
        it = iter(range(count))

    return (a * x + b for x in it)

def _exp_iterator(n0, l, count):
    """
    Iterate over exponential function n0 * e**(l * x) where x goes from 0 to count.
    If count is None, iterates to infinity.
    """
    if count is None:
        it = itertools.count()
    else:
        it = iter(range(count))

    return (n0 * math.exp(x * l) for x in it)

class ADSR(tracks.BaseTrack):
    def __init__(self, lengths, sustain_volume = 0.5, top_volume = 1,
        noisefloor = 0):
        super(ADSR, self).__init__()

        if len(lengths) != 4:
            raise Exception('lengths must be 4 items long.')

        self._values = [
            (noisefloor, top_volume),
            (top_volume, sustain_volume),
            (sustain_volume, sustain_volume),
            (sustain_volume, noisefloor)
            ]
        self._lengths = lengths

    def _sample_lengths(self, samplerate):
        return (int(l * samplerate) for l in self._lengths)

    def as_iter(self, samplerate):
        lengths_s = self._sample_lengths(samplerate)

        return itertools.chain.from_iterable(
            itertools.starmap(
                _lin_iterator,
                (
                    ((b - a) / l, a, l) for
                    ((a, b), l) in
                    zip(self._values, lengths_s)
                )
            ))

    def len(self, samplerate):
        return sum(self._sample_lengths(samplerate))


class Exponential(tracks.BaseTrack):
    def __init__(self, start_val, stop_val, length):
        super(Exponential, self).__init__()
        self._length = length
        self._start_val = start_val
        self._stop_val = stop_val

    def as_iter(self, samplerate):
        length = self.len(samplerate)

        n0 = self._start_val
        l = math.log(self._stop_val / n0) / length

        return _exp_iterator(n0, l, length)

    def len(self, samplerate):
        return int(self._length * samplerate)


class Linear(tracks.BaseTrack):
    def __init__(self, start_val, stop_val, length):
        super(Linear, self).__init__()
        self._length = length
        self._start_val = start_val
        self._stop_val = stop_val

    def as_iter(self, samplerate):
        length = self.len(samplerate)
        b = float(self._start_val)
        a = (float(self._stop_val) - b) / length

        return _lin_iterator(a, b, length)

    def len(self, samplerate):
        return int(self._length * samplerate)


class Box(tracks.BaseTrack):
    def __init__(self, length, value = 1):
        super(Box, self).__init__()
        self._length = length
        self._value = value

    def as_iter(self, samplerate):
        return itertools.repeat(self._value, self.len(samplerate))

    def len(self, samplerate):
        return int(self._length * samplerate)
