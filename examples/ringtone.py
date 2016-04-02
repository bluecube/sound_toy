#!/usr/bin/python3

import sound_toy
import itertools

def tone_gen(t, short):
    if short:
        amplitude = sound_toy.envelopes.ADSR((0.1, 0.1, 0.1, 0.5))
    else:
        amplitude = sound_toy.envelopes.ADSR((0.1, 0.1, 0.3, 2))

    phase = sound_toy.oscillators.SineOscillator(freq=10, amplitude=3)

    return sound_toy.oscillators.SineOscillator(freq = sound_toy.tone.Tone(t),
                                                amplitude = amplitude,
                                                phase = phase)

def tones_iter():
    scale = sound_toy.tone.Minofor i in itertools.count():
        yield tone_gen(scale[i], True)

rhythm = sound_toy.rhythm.Rhythm(4, 240)
dm = sound_toy.sequencer.Sequencer(rhythm, tones_iter(), [
    "X  XX",
    "  X  X X X",
    " X   "],
    repeat=None)


#sound_toy.waveform_plot.plot([s], samplerate=100)
sound_toy.alsa.play(dm)
#sound_toy.wav_file.save(s, "/tmp/sine.wav")

