#!/usr/bin/python3

import sound_toy
import itertools

class SimpleOverdrive(sound_toy.tracks.BaseTrack):
    class HalfOverdrive:
        def __init__(self, limit, hardness):
            self._limit = limit
            self._hardness = hardness

        def __call__(self, x):
            return self._limit * (1 - 1 / (x * self._hardness + 1))

    def __init__(self, track, negative = 1.2, positive = 0.7, hardness_negative = 0.5, hardness_positive = 1):
        self._track = track
        self._negative = self.HalfOverdrive(negative, hardness_negative)
        self._positive = self.HalfOverdrive(positive, hardness_positive)

        super().__init__(track)

    def as_iter(self, samplerate):
        for value in self._track.as_iter(samplerate):
            if value < 0:
                yield -self._negative(-value)
            else:
                yield self._positive(value)

    def len(self, samplerate):
        return self._track.len(samplerate)

rhythm = sound_toy.rhythm.Rhythm(4, 240)
scale = sound_toy.tone.MinorScale("G3")

dm = sound_toy.sequencer.Sequencer(rhythm,
                                   (sound_toy.instruments.sine(scale[i], 0.8, 0.5)
                                    for i in itertools.count()),
                                   """
X X X X X X   X X X X X X X   X 
            X               X
                             X

X               X
   X               X
  X               X
 X               X
""".strip("\n").split("\n"),
                                   repeat=1)

overdriven = dm#SimpleOverdrive(dm)
sound_toy.alsa.play(overdriven)
sound_toy.waveform_plot.plot(sound_toy.instruments.sine(scale[4], 0.8, 0.5))
#sound_toy.wav_file.save(s, "/tmp/sine.wav")

