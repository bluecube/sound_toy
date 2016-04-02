from .util import counted_iterator
from .tracks import BaseTrack
from .mixer import Mixer
import string
import itertools

class Sequencer(BaseTrack):
    def __init__(self, rhythm, samples, timings, repeat = 1):
        self._rhythm = rhythm
        self._samples = list(itertools.zip_longest(*[[(sample, mark) for mark in timings]
                                                     for sample, timings in
                                                     zip(samples, timings)],
                                                   fillvalue=(None, None)))
        # Brutal :-)

        self._repeat = repeat

    def as_iter(self, samplerate):
        mixer = Mixer(samplerate)

        trigger_iterator = self._rhythm.trigger_iterator(samplerate)
        for i in counted_iterator(self._repeat):
            for marks in self._samples:
                while not next(trigger_iterator): # This one is infinite
                    yield next(mixer)

                for sample, mark in marks:
                    if sample is None:
                        continue
                    if mark not in string.whitespace:
                        mixer.add_track(sample)

                yield next(mixer)

        while not mixer.is_empty():
            yield next(mixer)

    #def len(self, samplerate):
    #    beats = max(len(timings) for sample, timings in self._samples)
