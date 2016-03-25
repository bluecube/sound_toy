#!/usr/bin/python3

import sound_toy

s = sound_toy.oscillators.SineOscillator(
    freq = sound_toy.music.Tone('D'),
    phase = sound_toy.oscillators.SineOscillator(amplitude = 4, freq = 7),
    amplitude = sound_toy.envelopes.Box(10))

#sound_toy.waveform_plot.plot([s], samplerate=100)
sound_toy.alsa.play(s)
