from . import tracks
import math
import collections
import itertools

class Echo(tracks.BaseTrack):
    def __init__(self, input, time, attenuation, noisefloor = 0.01):
        super().__init__(input)
        self._time = time
        self._persistence = 1 - attenuation
        self._noisefloor = noisefloor

    def _buffer_length(self, samplerate):
        # Buffer size is selected like this:
        # buffer_length = repeat * time * samplerate
        # attenuation ** repeat <= noisefloor
        repeat = math.ceil(math.log(self._noisefloor, self._persistence))
        buffer_length = repeat * self._time * samplerate
        return repeat, buffer_length

    def as_iter(self, samplerate):
        repeat, buffer_length = self._buffer_length(samplerate)

        buffer = collections.deque([0] * buffer_length, buffer_length)

        for value in self._slaves[0].as_iter(samplerate):
            out = 0
            for index in range(0, buffer_length, self._time * samplerate):
                out += buffer[index]
                out = out * self._persistence
            out += value

            buffer.append(out)
            yield out

        for i in range(buffer_length):
            out = 0
            for index in range(0, buffer_length, self._time * samplerate):
                out += buffer[index]
                out = out * self._persistence

            buffer.append(out)
            yield out

    def len(self, samplerate):
        repeat, buffer_length = self._buffer_length(samplerate)
        return self._slaves[0].len(samplerate) + buffer_length
