from .tracks import BaseTrack
from .mixer import Mixer
import string

class DrumMachine(BaseTrack):
    def __init__(self, rhythm, instruments, timings):
        self._rhythm = rhythm
        self._instruments = list(zip(instruments, timings))

    def as_iter(self, samplerate):
        mixer = Mixer(samplerate)
        instruments = [(instrument, iter(timings)) for instrument, timings in self._instruments]
        i = 0
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

            yield next(mixer)
            i += 1

        while not mixer.is_empty():
            yield next(mixer)

    #def len(self, samplerate):
    #    beats = max(len(timings) for instrument, timings in self._instruments)
