#!/usr/bin/python3

import sound_toy

s = sound_toy.oscillators.SineOscillator(
    freq = 1000,
    #phase = sound_toy.envelopes.Box(20),
    amplitude = sound_toy.oscillators.SquareOscillator(0.2, amplitudeLow=0, amplitudeHigh=1))

#sound_toy.waveform_plot.plot([s], samplerate=100)
sound_toy.alsa.play(s)
