import operator
import math
import itertools
import numpy

class BaseTrack:
    """
    A track represents any that can be sampled -- sound, frequency, volume, ...
    """
    def __init__(self, *slaves):
        self._samplerate = None
        self._slaves = list(slaves)

    def as_array(self):
        """
        Return numpy array of this track's data
        For infinite tracks this just hangs!
        This is only for reading and for most tracks it's
        generated from the iterator.
        """
        return numpy.fromiter(iter(self), numpy.float)

    def as_arrays_iter(self, size, fill = 0):
        """
        Return iterator that gives numpy arrays of length size containing
        the track's data.
        The last array is filled with fill.
        If fill is None, then the last array is shorter.
        """
        it = iter(self)

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
            else:
                yield numpy.array(arr)

    def add_slave(self, track):
        """
        Add a track as a slave.
        Slave hierarchy is used to distribute the information about samplerate.
        If track is not a BaseTrack subclass, then this method does nothing.
        """
        if isinstance(track, BaseTrack):
            self._slaves.append(track)
    
    def set_samplerate(self, samplerate):
        if self._samplerate is not None:
            if self._samplerate != samplerate:
                raise Exception("Sample rate already set to different value!")
            else:
                return

        self._samplerate = samplerate
        for track in self._slaves:
            track.set_samplerate(samplerate)
    
    def get_samplerate(self):
        return self._samplerate

    def check_samplerate(self):
        """
        Check that samperate was set for this track and all its slaves.
        To be called in __iter__ methods of subclasses.
        """

        if self._samplerate is None:
            raise Exception("Sample rate not set!")

        for track in self._slaves:
            track.set_samplerate(self._samplerate)

    def __len__(self):
        """
        Return the length of this track in samples or
        or None if the track is infinite.
        """
        raise NotImplemented()

    def __iter__(self):
        raise NotImplemented()


class Mixer(BaseTrack):
    def add_track(self, track):
        add_slave(track)

    def __iter__(self):
        self.check_samplerate()
        return map(math.fsum,
            itertools.zip_longest(
                *self._slaves,
                fillvalue=0
            ))

class Chain(BaseTrack):
    def add_track(self, track):
        add_slave(track)

    def __iter__(self):
        self.check_samplerate()
        return itertools.chain.from_iterable(self._slaves)







class SampledData(BaseTrack):
    """
    Track that wraps array of pre-sampled numpy data.
    """

    def __init__(self, data, samplerate):
        super().__init__()
        self._data = data
        self.set_samplerate(samplerate)

    def as_array(self):
        return self._data

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)
