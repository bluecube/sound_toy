from . import util
from . import oscillators
from . import envelopes

@util.Memoize
def sine(freq, amplitude, length):
    adsr = envelopes.ADSR((0.1, 0.1, length, 0.5), 0.5 * amplitude, amplitude)
    return oscillators.SineOscillator(freq, amplitude = adsr)
