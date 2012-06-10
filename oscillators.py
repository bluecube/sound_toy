from .tracks import BaseTrack
import itertools
import math

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
            self._amplitude = amplitude
            self._amplitudeHigh = None
            self._amplitudeLow = None
            if isinstance(amplitude, BaseTrack):
                self.add_slave(amplitude)
        elif amplitudeLow is not None and amplitudeHigh is not None:
            self._amplitude = None
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
        if Oscillator._is_constant(x):
            return itertools.repeat(x)
        else:
            return iter(x)

    @staticmethod
    def _convert(x):
        if x is None:
            return None
        elif isinstance(x, BaseTrack):
            return iter(x)
        else:
            return float(x)

    @staticmethod
    def _cumsum(it, add = 0, multiplier = 1):
        accumulator = add
        for x in it:
            yield accumulator
            accumulator += x * multiplier

    def _is_constant(x):
        return not hasattr(x, '__next__')

    def __iter__(self):
        freq = self._convert(self._freq)
        phase = self._convert(self._phase)
        amplitude = self._convert(self._amplitude)
        amplitudeHigh = self._convert(self._amplitudeHigh)
        amplitudeLow = self._convert(self._amplitudeLow)

        freq_multiplier = 2 * math.pi / self._samplerate

        if Oscillator._is_constant(freq):
            if Oscillator._is_constant(phase):
                x_iterator = itertools.count(phase, freq * freq_multiplier)
            else:
                x_iterator = itertools.count(0, freq * freq_multiplier)
        else:
            if Oscillator._is_constant(phase):
                x_iterator = self._cumsum(freq, phase, freq_multiplier)
            else:
                x_iterator = self._cumsum(freq, 0, freq_multiplier)


        if Oscillator._is_constant(phase):
            if amplitude is not None:
                if Oscillator._is_constant(amplitude):
                    return (amplitude * self._func(x) for x in x_iterator)
                else:
                    return (a * self._func(x) for x, a in zip(x_iterator, amplitude))
        else:
            if amplitude is not None:
                if Oscillator._is_constant(amplitude):
                    return (amplitude * self._func(x + p) for x, p in zip(x_iterator, phase))
                else:
                    return (a * self._func(x + p) for x, a, p in zip(x_iterator, amplitude, phase))


        assert amplitude is None

        zipped = zip(
            self._cumsum(self._make_iter(freq), 0, freq_multiplier),
            self._make_iter(amplitudeHigh),
            self._make_iter(amplitudeLow),
            self._make_iter(phase))

        return (((ah + al) + (ah - al) *
            self._func(x + p)) * 0.5 for
            x, ah, al, p in zipped)


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
