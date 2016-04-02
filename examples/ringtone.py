#!/usr/bin/python3

import sound_toy
import itertools

rhythm = sound_toy.rhythm.Rhythm(4, 240)
scale = sound_toy.tone.MinorScale("G4")

dm = sound_toy.sequencer.Sequencer(rhythm,
                                   (sound_toy.instruments.sine(scale[i], 0.3)
                                    for i in itertools.count()),
                                   ["X",
                                    " X",
                                    "  X",
                                    "   X",
                                    "    X",
                                    "     X"
                                    ],
                                   repeat=None)


sound_toy.alsa.play(dm)
#sound_toy.waveform_plot.plot(dm)
#sound_toy.wav_file.save(s, "/tmp/sine.wav")

