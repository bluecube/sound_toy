from .util import counted_iterator
from .tracks import BaseTrack
from .mixer import Mixer
import string

class DrumMachine(BaseTrack):
    def __init__(self, rhythm, instruments, timings, repeat = 1):
        self._rhythm = rhythm

        max_length = max(len(l) for l in instruments)
        self._instruments = []

        for instrument, timing in zip(instruments, timings):
            

        self._instruments = list(zip(instruments, timings))
        self._repeat = repeat

    def as_iter(self, samplerate):
        mixer = Mixer(samplerate)

        for repeat_count in counted_iterator(self._repeat):
            instruments = [(instrument, iter(timings)) for instrument, timings in self._instruments]
            remaining_timings = len(instruments)

            for trigger in self._rhythm.trigger_iterator(samplerate):
                if trigger:
                    for instrument, timing_it in instruments:
                        try:
                            play_char = next(timing_it)
                        except StopIteration:
                            remaining_timings -= 1
                        else:
                            if not play_char in string.whitespace:
                                mixer.add_track(instrument)

                if not remaining_timings:
                    break
                    print("X")

                yield next(mixer)

        print("XXX")
        while not mixer.is_empty():
            print(len(mixer._playing))
            yield next(mixer)

    #def len(self, samplerate):
    #    beats = max(len(timings) for instrument, timings in self._instruments)
