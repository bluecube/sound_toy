import operator
import math
import itertools
import numpy

class BaseTrack(object):
    """
    A track represents any that can be sampled -- sound, frequency, volume, ...
    """
    def __init__(self, *slaves):
        self._slaves = list(slaves)

        self.name = self.__class__.__name__

    def as_iter(self, samplerate):
        """
        Return interator with individual track values.

        Parameters:
            samplerate: Samplerate for whitch to generate the values.
        """
        raise NotImplemented()

    def as_array(self, samplerate):
        """
        Return numpy array of this track's data
        For infinite tracks this just hangs!
        This is only for reading and for most tracks it's
        generated from the iterator.

        Parameters:
            samplerate: Samplerate for whitch to generate the values.
        """
        return numpy.fromiter(self.as_iter(samplerate), numpy.float)

    def as_arrays_iter(self, samplerate, size, zfill = True):
        """
        Return iterator that gives numpy arrays of limited size containing
        the track's data.

        Parameters:
            samplerate: Samplerate for whitch to generate the values.
            size: Size of the arrays returned
            zfill: If True, the last array is zero padded,
                otherwise it may be shorter.
        """
        it = self.as_iter(samplerate)

        while True:
            arr = numpy.fromiter(itertools.islice(it, size), dtype=numpy.float)

            if not len(arr):
                return
            elif len(arr) < size and zfill:
                yield numpy.append(arr, numpy.zeros(size - len(arr)))
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
        or infinity if the track is infinite.
        May sometime return a too high value (for mixers).
        """
        raise NotImplemented()


class Chain(BaseTrack):
    def as_iter(self, samplerate):
        for slave in self._slaves:
            for x in slave.as_iter(samplerate, i):
                yield x
                i += 1

    def len(self, samplerate):
        return sum((x.len(samplerate) for x in self._slaves))


class NumpyTrack(BaseTrack):
    """
    Track that wraps array of pre-sampled numpy data.
    """

    def __init__(self, data, samplerate):
        super(NumpyTrack, self).__init__()
        self._data = data
        self._samplerate = samplerate

    def _check_samplerate(self, samplerate):
        if self._samplerate != samplerate:
            raise Exception(
                ("The track has samplerate fixed to {} Hz, requested {} Hz. " +
                "Use resampler.").format(self._samplerate, samplerate))

    def as_iter(self, samplerate):
        self._check_samplerate(saplerate)
        return iter(self._data)

    def as_array(self, samplerate):
        self._check_samplerate(saplerate)
        return self._data

    def as_arrays_iter(self, samplerate, size, zfill = True):
        self._check_samplerate(samplerate)

        for offset in itertools.count(0, size):
            arr = self._data[offset:offset + size]

            if not len(arr):
                return
            elif len(arr) < size and zfill:
                yield numpy.append(arr, numpy.zeros(size - len(arr)))
                return
            else:
                yield numpy.array(arr)

    def len(self, samplerate):
        self._check_samplerate(saplerate)
        return len(self._data)
