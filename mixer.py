from . import tracks
import collections


class Mixer:
    """
    This is a component for tracks.
    Keeps a list of playing tracks and mixes them all together.
    Tracks can be added during playing (but not removed), each
    runs until it returns.
    Behaves as an infinite iterator.
    """

    def __init__(self, samplerate):
        self._samplerate = samplerate
        self._playing = []

    def add_track(self, track):
        self._playing.append(track.as_iter(self._samplerate))

    def is_empty(self):
        return not len(self._playing)

    def __iter__(self):
        return self

    def __next__(self):
        new_playing = []
        value = 0

        for playing in self._playing:
            try:
                value += next(playing)
            except StopIteration:
                continue
            else:
                new_playing.append(playing)

        self._playing = new_playing
        return value
