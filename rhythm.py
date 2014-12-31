import math
import itertools

from .tracks import BaseTrack

class Rhythm:
    """
    Rhythm is a class converting beats and measures to time.
    """
    def __init__(self, measure_len, bpm = 100):
        """
        Initialize the rhythm.

        Parameters:
            measure_len: Number of beats per measure.
            bpm: Beats per minute.
        """
        self.measure_len = measure_len
        self.bpm = bpm
        self._spb = 60 / bpm

    def time(self, beat, measure = 0):
        """
        Returns the absolute time of the given beat in given measure,
        or equivalently note length. 

        r.time(2, 4) returns time of a third beat in fifth measure (0 based),
        r.time(0.5) returns time of halfth beat in first measure or length
            of 0.5 beat note (cf. eighth note in ?/4 rhythm)
        """
        return (measure * self.measure_len + beat) * self._spb

    def trigger_iterator(self, samplerate):
        """ Returns infinite iterator of bools, one per sample, True if beat falls into this sample. """
        beat = self._spb * samplerate
        i = beat # First sample is beat
        while True:
            if i >= beat:
                i -= beat
                yield True
            else:
                yield False
            i += 1

    __call__ = time

    def __str__(self):
        return "Rhythm @ {} bpm, {} beats per measure".format(self.bpm, self.measure_len)

class Repeat(BaseTrack):
    def __init__(self, track, rhythm, beat_set, repeat_period = None):
        super(Repeat, self).__init__()
        self._track = track
        self._rhythm = rhythm
        self._beat_set = beat_set

        if repeat_period is None:
            self._modulus = (max(beat_set) // rhythm.measure_len + 1) * rhythm.measure_len
        else:
            self._modulus = repeat_period

        self.add_slave(track)

    def as_iter(self, samplerate, offset = 0):
        beat_set = {int(self._rhythm.time(x) * samplerate) for x in self._beat_set}
        modulus = int(self._rhythm.time(self._modulus) * samplerate)

        started = []

        for i in itertools.count(offset):
            if (i % modulus) in beat_set:
                started.append(self._track.as_iter(samplerate, i))

            new_started = []
            out = 0
            for it in started:
                try:
                    out += next(it)
                except StopIteration:
                    pass
                else:
                    new_started.append(it)

            started = new_started
            yield out
