#!/usr/bin/python3

import sound_toy

waveforms = []
waveforms.append(sound_toy.oscillators.SineOscillator(
    1,
    amplitude = sound_toy.envelopes.Box(1)))
waveforms[-1].name = "Sine"

waveforms.append(sound_toy.oscillators.SawtoothOscillator(
    1,
    amplitude = sound_toy.envelopes.Box(1)))
waveforms[-1].name = "Sawtooth"

waveforms.append(sound_toy.oscillators.SquareOscillator(
    1,
    amplitude = sound_toy.envelopes.Box(1)))
waveforms[-1].name = "Square"

waveforms.append(sound_toy.oscillators.TriangleOscillator(
    1,
    amplitude = sound_toy.envelopes.Box(1)))
waveforms[-1].name = "Triangle"


sound_toy.waveform_plot.plot(waveforms)

