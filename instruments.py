from . import util
from . import oscillators
from . import envelopes

@util.Memoize
def sine(freq, length):
    return oscillators.SineOscillator(freq,
                                      amplitude = envelopes.ADSR((0.1, 0.1, length, 0.5)))
