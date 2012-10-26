#!/usr/bin/python3

import sound_toy

r = sound_toy.rhythm.Rhythm(2, 100)

ping1 = sound_toy.oscillators.SineOscillator(
    freq = 500,
    amplitude = sound_toy.envelopes.Box(r(0.1)))

ping2 = sound_toy.oscillators.SquareOscillator(
    freq = 250,
    amplitude = sound_toy.envelopes.ADSR((0.05, 0.05, r(0.25), r(0.75))))

repeated1 = sound_toy.rhythm.Repeat(ping1, r, {0, 0.75, 1})
repeated2 = sound_toy.rhythm.Repeat(ping2, r, {0})

sound_toy.alsa.play(sound_toy.tracks.Mixer(repeated1, repeated2))
