import operator
import math
import itertools
import numpy

class BaseTrack:
    """
    A track represents any that can be sampled -- sound, frequency, volume, ...
    """
    def __init__(self, *slaves):
        self._slaves = list(slaves)

    def as_iter(self, samplerate):
        """
        Return interator with individual track values.
        """
        raise NotImplemented()

    def as_array(self, samplerate):
        """
        Return numpy array of this track's data
        For infinite tracks this just hangs!
        This is only for reading and for most tracks it's
        generated from the iterator.
        """
        return numpy.fromiter(self.as_iter(samplerate), numpy.float)

    def as_arrays_iter(self, samplerate, size, fill = 0):
        """
        Return iterator that gives numpy arrays of length size containing
        the track's data.
        The last array is filled with fill.
        If fill is None, then the last array may be shorter.
        """
        it = self.as_iter(samplerate)

        while True:
            arr = numpy.fromiter(itertools.islice(it, size), dtype=numpy.float)

            if not len(arr):
                return
            elif len(arr) < size and fill is not None:
                yield numpy.append(
                    arr,
                    numpy.fromiter(
                        itertools.repeat(fill, size - len(arr)),
                        dtype=numpy.float))

                return
            else:
                yield numpy.array(arr)

    def add_slave(self, track):
        """
        Add a track as a slave.
        If track is not a BaseTrack subclass, then this method does nothing.
        """
        if isinstance(track, BaseTrack):
            self._slaves.append(track)

    def len(self, samplerate):
        """
        Return the length of this track in samples or
        or None if the track is infinite.
        """
        raise NotImplemented()


class Mixer(BaseTrack):
    def as_iter(self, saplerate):
        return map(math.fsum,
            itertools.zip_longest(
                *(x.as_iter(samplerate) for x in self._slaves),
                fillvalue=0
            ))

    def len(self, samplerate):
        return max((x.len(samplerate) for x in self._slaves))


class Chain(BaseTrack):
    def as_iter(self, samplerate):
        return itertools.chain.from_iterable(
            (x.as_iter(samplerate) for x in self._slaves)
            )

    def len(self, samplerate):
        return sum((x.len(samplerate) for x in self._slaves))


class NumpyTrack(BaseTrack):
    """
    Track that wraps array of pre-sampled numpy data.
    """

    def __init__(self, data, samplerate):
        super().__init__()
        self._data = data
        self._samplerate = samplerate

    def _check_samplerate(self, samplerate):
        if self._samplerate != samplerate:
            raise Exception("The track has fixed sample rate. Use resampler.")

    def as_iter(self, samplerate):
        self._check_samplerate(saplerate)
        return iter(self._data)

    def as_array(self, samplerate):
        self._check_samplerate(saplerate)
        return self._data

    def as_arrays_iter(self, samplerate, size, fill = 0):
        self._check_samplerate(samplerate)

        for offset in itertools.count(0, size):
            arr = self._data[offset:offset + size]

            if not len(arr):
                return
            elif len(arr) < size and fill is not None:
                yield numpy.append(
                    arr,
                    numpy.fromiter(
                        itertools.repeat(fill, size - len(arr)),
                        dtype=numpy.float))

                return
            else:
                yield numpy.array(arr)

    def len(self, samplerate):
        return len(self._data)
