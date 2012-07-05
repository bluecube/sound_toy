from .tracks import BaseTrack
from .envelopes import Box
import itertools
import math
import collections

class Oscillator(BaseTrack):
    """
    Oscillators are based on simple periodic functions and
    generate signals with selectable (and possibly variable)
    frequency, amplitude and phase.
    The oscillator implementation attempts to minimize the amount
    of work necessary for generating the signal and contains several
    fast paths to do this.

    Specifically, if any parameter is a instance of envelopes.Box,
    it is treated as a constant and the track is shortened elsewhere.
    """

    def __init__(self, freq, amplitude = 1, amplitudeLow = None,
        amplitudeHigh = None, phase = 0):

        super(Oscillator, self).__init__()

        self._freq = freq
        self.add_slave(freq)

        self._phase = phase
        self.add_slave(phase)

        if amplitudeLow is None and amplitudeHigh is None:
            self._amplitude = amplitude
            self._amplitudeHigh = None
            self._amplitudeLow = None
            self.add_slave(amplitude)
        elif amplitudeLow is not None and amplitudeHigh is not None:
            self._amplitude = None
            self._amplitudeHigh = amplitudeHigh
            self._amplitudeLow = amplitudeLow
            self.add_slave(amplitudeLow)
            self.add_slave(amplitudeHigh)
        else:
           raise Exception("Both amplitudeLow and amplitudeHigh" +
            "must be either None or not None")

    def _func(self, x):
        """
        The actual function that generates the sound.
        Should be periodic from 0 to 2 Pi, return values from -1 to 1.
        Must be overriden in subclasses.
        """
        raise NotImplemented()

    def _convert(self, x, samplerate):
        if x is None:
            return None
        elif isinstance(x, Box):
            if self._limit is None:
                self._limit = x.len(samplerate)
            else:
                self._limit = min(self._limit, x.len(samplerate))
            return float(x._value)
        elif isinstance(x, BaseTrack):
            return x.as_iter(samplerate)
        else:
            return float(x)

    @staticmethod
    def _cumsum(it, add, multiplier):
        """
        Calculate cumulative sum of it, modifying each result
        using linear function.
        """
        accumulator = add
        for x in it:
            yield multiplier * accumulator
            accumulator += x

    @staticmethod
    def _cumsum2(it, add_it, multiplier):
        """
        Calculate cumulative sum of it, modifying each result
        using linear function.
        Add is an iterator.
        """
        accumulator = 0
        for x, add in zip(it, add_iter):
            yield multiplier * accumulator + add
            accumulator += x

    def _count_and_add(add, step):
        """
        Iterate over i * step + add
        where i goes 1, 2, 3 ...
        and add is an iterator.
        """
        accumulator = 0
        for x in zip(add):
            yield accumulator + x
            accumulator += step

    @staticmethod
    def _is_constant(x):
        return not isinstance(x, collections.Iterator)

    def as_iter(self, samplerate):
        self._limit = None

        freq = self._convert(self._freq, samplerate)
        phase = self._convert(self._phase, samplerate)
        amplitude = self._convert(self._amplitude, samplerate)
        amplitudeHigh = self._convert(self._amplitudeHigh, samplerate)
        amplitudeLow = self._convert(self._amplitudeLow, samplerate)

        freq_multiplier = 2 * math.pi / samplerate

        # TODO: Measure and optimize this part
        if self._is_constant(freq):
            if self._is_constant(phase):
                x_iterator = itertools.count(phase, freq * freq_multiplier)
            else:
                x_iterator = self._count_and_add(phase, step)
        else:
            if self._is_constant(phase):
                x_iterator = self._cumsum(freq, phase, freq_multiplier)
            else:
                x_iterator = self._cumsum2(freq, phase, freq_multiplier)

        if amplitude == 1:
            ret = (self._func(x) for x in x_iterator)
        elif amplitude is not None:
            if self._is_constant(amplitude):
                ret = (amplitude * self._func(x) for x in x_iterator)
            else:
                ret = (a * self._func(x) for x, a in zip(x_iterator, amplitude))
        else:
            assert amplitude is None

            # this option is a little too complicated, so I'll just collapse it
            # to the most general case.
            if self._is_constant(amplitudeHigh):
                amplitudeHigh = itertools.repeat(amplitudeHigh)
            if self._is_constant(amplitudeLow):
                amplitudeLow = itertools.repeat(amplitudeLow)

            ret = (((ah + al) + (ah - al) *
                self._func(x)) * 0.5 for
                x, ah, al in zip(x_iter, amplitudeHigh, amplitudeLow))

        if self._limit is None:
            return ret
        else:
            return itertools.islice(ret, self._limit)

    def len(self, samplerate):
        if not len(self._slaves):
            return None
        else:
            return min((len(slave) for slave in self._slaves))


class SineOscillator(Oscillator):
    _func = math.sin


class SawtoothOscillator(Oscillator):
    @staticmethod
    def _func(x):
        return math.fmod(x / math.pi + 1, 2) - 1


class SquareOscillator(Oscillator):
    @staticmethod
    def _func(x):
        return 1 - math.fmod(x // math.pi, 2) * 2


class TriangleOscillator(Oscillator):
    @staticmethod
    def _func(x):
        return 1 - math.fabs(math.fmod(x * 2 / math.pi + 1, 4) - 2)
