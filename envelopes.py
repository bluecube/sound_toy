import itertools

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

    return (n0 * e**(x * l) for x in it)

class ADSR(tracks.BaseTrack):
    def __init__(self, lengths, sustain_volume = 0.5, top_volume = 1, noisefloor = 0.001):
        super().__init__()

        if len(lengths) != 4:
            raise Exception('lengths must be 4 items long.')

        values = [
            (noisefloor, top_volume),
            (top_volume, sustain_volume),
            (sustain_volume, sustain_volume),
            (sustain_volume, noisefloor)
            ]

        lengths_s = (int(l * samplerate) for l in lengths)

        self._values = [((b - a) / l, a, l)
            for ((a, b), l) in zip(values, lengths_s) if l != 0]

    def __iter__(self):
        return itertools.chain.from_iterable(
            itertools.starmap(_lin_iterator, self._values))


#class Exponential(tracks.BaseTrack):
#    pass

class Linear(tracks.BaseTrack):
    def __init__(self, start_val, stop_val, length):
        super().__init__()
        self._length = length
        self._start_val = start_val
        self._stop_val = stop_val

    def __iter__(self):
        length = int(float(self._length) * self._samplerate)
        print(length)
        b = float(self._start_val)
        a = (float(self._stop_val) - b) / length

        print(self._start_val)
        print(self._stop_val)

        return _lin_iterator(a, b, length)
        

