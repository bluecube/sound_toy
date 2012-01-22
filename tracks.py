import operator
import math
import itertools

import pdb

class BaseTrack:
    """
    A track corresponds to any data that repeats every sample --
    sound, frequency, volume, ...
    """
    def __init__(self, *slaves):
        self._samplerate = None
        self._slaves = list(slaves)
        self._mixer = None

    def add_slave(self, track):
        self._slaves.append(track)
    
    def set_samplerate(self, samplerate):
        if self._samplerate is not None:
            if self._samplerate != samplerate:
                raise Exception("Sample rate already set to wrong value!")
            else:
                return

        self._samplerate = samplerate
        for track in self._slaves:
            track.set_samplerate(samplerate)

    def set_mixer(mixer):
        if self._mixer is not None:
            return

        self._mixer = samplerate
        for track in self._slaves:
            track.set_mixer(samplerate)

    def check_samplerate():
        if self._samplerate is None:
            raise Exception("Sample rate not set!")

    def __iter__(self):
        raise NotImplemented()


class Mixer(BaseTrack):
    def add_track(self, track):
        add_slave(track)

    def __iter__(self):
        return map(math.fsum,
            itertools.zip_longest(
                *self._slaves,
                fillvalue=0
            ))

class Chain(BaseTrack):
    def add_track(self, track):
        add_slave(track)

    def __iter__(self):
        return itertools.chain.from_iterable(self._slaves)


class Repeat(BaseTrack):
    def __init__(self, start, stop, repeat, sound):
        """
        Start, stop and repeat are in seconds and are simillar in meaning to range() arguments.
        """
        super().__init__()

        self._start = int(start * samplerate)
        
        if stop is None:
            self._count = None
        else:
            self._count = int((stop - start) / repeat)
        self._repeat = int(repeat * samplerate)
        self._sound = sound

    @classmethod
    def from_rhythm(cls, samplerate, sound, rhythm, beat, repeat, first_measure, last_measure):
        """
        High level consturctor.
        Repeats sound every "repeat" measures, on "beat".
        """
        return cls(samplerate,
            rhythm.time(beat, first_measure), rhythm.time(beat, last_measure),
            rhythm.measure_len() * repeat, sound)
        
    def __iter__(self):
        for i in range(self._start):
            yield 0

        playing = []

        if self._count is None:
            periods = itertools.count()
        else:
            periods = range(self._count - 1)

        for i in periods:
            playing.append(iter(self._sound))

            for j in range(self._repeat):
                if not len(playing):
                    # For short sounds this should save some power,
                    # for long ones it shouldn't do any harm.
                    for k in range(j, self._repeat):
                        yield 0

                    break

                ret = 0

                newplaying = []
                for x in playing:
                    try:
                        ret += next(x)
                    except StopIteration:
                        pass
                    else:
                        newplaying.append(x)
                playing = newplaying

                yield ret

        playing.append(iter(self._sound))

        while len(playing):
            ret = 0

            newplaying = []
            for x in playing:
                try:
                    ret += next(x)
                except StopIteration:
                    pass
                else:
                    newplaying.append(x)
            playing = newplaying

            yield ret
