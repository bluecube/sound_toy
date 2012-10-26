#!/usr/bin/python3

import sound_toy
from sound_toy.music import Tone

r = sound_toy.rhythm.Rhythm(8, 180)

envelope = sound_toy.envelopes.PiecewiseLinear([
        (0, Tone('G2')),
        (r(4), Tone('G4')),
        (r(8), Tone('G4')),

        (r(8), Tone('G2')),
        (r(10), Tone('G4')),

        (r(10), Tone('G2')),
        (r(12), Tone('G4')),
        ])

sawtooth = sound_toy.oscillators.SawtoothOscillator(freq = envelope)

sound_toy.alsa.play(sawtooth)
sound_toy.wav_file.save(envelope, '/tmp/x.wav')
