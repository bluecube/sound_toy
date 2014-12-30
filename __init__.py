import sys

from sound_toy import (
    tracks,
    oscillators,
    envelopes,
    wav_file,
    rhythm,
    tone)

try:
    from sound_toy import alsa
except ImportError:
    print("No alsa support, sorry.", file=sys.stderr)

try:
    from sound_toy import pygame_player
except ImportError:
    print("no pygame support, sorry.", file=sys.stderr)

try:
    from sound_toy import waveform_plot
except ImportError:
    print("no matplotilb support, sorry.", file=sys.stderr)
