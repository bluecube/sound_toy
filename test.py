#!/usr/bin/python3

from music import *
from oscillators import *
from envelopes import *
#from sounds import *
#from tracks import *

import wav_saver
import pygame_player

test = SawtoothOscillator(
    Tone('C')
    #freq = SawtoothOscillator(0.3, amplitudeLow = Tone('C4'), amplitudeHigh = Tone('C5')),
    #amplitudeHigh = SineOscillator(1, amplitudeLow = 0.5, amplitudeHigh = 1),
    #amplitudeLow = SineOscillator(0.7, amplitudeLow = -0.25, amplitudeHigh = -1)
    )

pygame_player.play(test)
#wav_saver.save(test, '/tmp/test.wav')

print('done')

