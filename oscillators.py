from tracks import BaseTrack
import itertools
import math

class _Negate:
    def __init__(self, track):
        self.track = track


class Oscillator(BaseTrack):
    def __init__(self, freq, amplitude = 1, amplitudeLow = None, amplitudeHigh = None, phase = 0):
        super().__init__()

        self._freq = freq
        if isinstance(freq, BaseTrack):
            self.add_slave(freq)

        self._phase = phase
        if isinstance(phase, BaseTrack):
            self.add_slave(phase)

        if amplitudeLow is None and amplitudeHigh is None:
            self._amplitudeHigh = amplitude
            self._amplitudeLow = _Negate(amplitude)
            if isinstance(amplitude, BaseTrack):
                self.add_slave(amplitude)
        elif amplitudeLow is not None and amplitudeHigh is not None:
            self._amplitudeHigh = amplitudeHigh
            self._amplitudeLow = amplitudeLow
            if isinstance(amplitudeLow, BaseTrack):
                self.add_slave(amplitudeLow)
            if isinstance(amplitudeHigh, BaseTrack):
                self.add_slave(amplitudeHigh)
        else:
           raise Exception("Both amplitudeLow and amplitudeHigh must be either None or not None")

    def _func(self, x):
        raise NotImplemented()
    
    @staticmethod
    def _make_iter(x):
        if isinstance(x, _Negate):
            x = x.track
            if isinstance(x, BaseTrack):
                return (-value for value in x)
            else:
                return itertools.repeat(-float(x))
        if isinstance(x, BaseTrack):
            return iter(x)
        else:
            return itertools.repeat(float(x))

    @staticmethod
    def _cumsum(it):
        accumulator = 0
        for x in it:
            yield accumulator
            accumulator += x

    def __iter__(self):
        # TODO: some performance hides in here
        zipped = zip(
            self._cumsum(self._make_iter(self._freq)),
            self._make_iter(self._phase),
            self._make_iter(self._amplitudeLow),
            self._make_iter(self._amplitudeHigh)
            )
        
        return (amplitudeLow + (amplitudeHigh - amplitudeLow) * (0.5 + 0.5 * 
            self._func(2 * math.pi * freq_integral / self._samplerate + phase)) for
            (freq_integral, phase, amplitudeLow, amplitudeHigh) in zipped)


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
