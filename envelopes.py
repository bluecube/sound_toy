import itertools
import math
import operator

from . import tracks

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

class Interpolate(tracks.BaseTrack):
    """ An envelope that go through the given points using
    a interpolation function."""

    def __init__(self, points, length = None):
        """ Points is an iterable of (time, value) tuples.
        Unless the points define it otherwise, the envelope starts in (0, 0)
        and ends by repeating the last value.
        If length is None, then it defaults to the time position of the last point."""
        super(Interpolate, self).__init__()

        points = [(float(x), float(y)) for (x, y) in points]

        points.sort(key=operator.itemgetter(0))

        if length is None:
            if not len(points):
                raise Exception("Length is not specified and ther are no points. This is bad.")

            length = points[-1][0]

        if not len(points) or points[0][0] > 0:
            points = [(0, 0)] + points

        if points[-1][0] < length:
            points = points + [(length, points[-1][1])]

        i0 = None
        i1 = None
        for i, (x, y) in enumerate(points):
            if x >= 0 and i0 is None:
                if i == 0:
                    assert x == 0
                    i0 = 0
                else:
                    i0 = i - 1
            if x > length:
                if i == len(poins) - 1:
                    assert x == length
                    i1 = len(points)
                else:
                    i1 = i + 1
                break

        self._points = points[i0:i1]
        self._length = length

    def as_iter(self, samplerate):
        points = [
            (round(t * samplerate), v)
            for (t, v) in self._points]

        return itertools.chain.from_iterable(
            self._interp_iterator(
                range(points[i][0], points[i + 1][0]),
                points, i)
            for i in range(len(points) - 1))

    def len(self, samplerate):
        return int(self._length * samplerate)

    @staticmethod
    def _interp_iterator(x_iter, points, i):
        """ Yield values for every x in x_iter.

        x_iter -- iterator of x values.
        points -- sorted list of (x, y) tuples.
        i -- specifies the pair of points to interpolate between (from i to (i + 1))."""
        raise NotImplementedError()


class PiecewiseLinear(Interpolate):
    """ Interpolate the points using line segments """
    @staticmethod
    def _interp_iterator(x_iter, points, i):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]

        count = x1 - x0

        if count == 0:
            return []

        a = (y1 - y0) / count
        b = y0 - a * x0

        return (a * x + b for x in x_iter)


class ADSR(PiecewiseLinear):
    def __init__(self, lengths, sustain_volume = 0.5, top_volume = 1, noisefloor = 0):
        if len(lengths) != 4:
            raise Exception('lengths must be 4 items long.')

        values = [noisefloor, top_volume, sustain_volume, sustain_volume, noisefloor]
        times = [0]
        for length in lengths:
            times.append(times[-1] + length)

        super(ADSR, self).__init__(points = zip(times, values))


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


class Box(PiecewiseLinear):
    """Box envelope. Triggers fast paths in oscillators."""

    def __init__(self, length, value = 1):
        self._length = length
        self._value = value

        super(Box, self).__init__(points = [(0, value)], length = length)

    def as_iter(self, samplerate):
        return itertools.repeat(self._value, self.len(samplerate))
