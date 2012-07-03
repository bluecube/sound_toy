import alsaaudio
import numpy

def play(track, samplerate=44100, periodsize=512, card='default'):
    """
    Play a track through alsa.
    Forces samplerate of the track.
    """
    track.set_samplerate(samplerate)

    pcm = alsaaudio.PCM(
        type=alsaaudio.PCM_PLAYBACK,
        mode=alsaaudio.PCM_NORMAL,
        card=card)
    pcm.setrate(samplerate)
    pcm.setchannels(1)
    pcm.setformat(alsaaudio.PCM_FORMAT_FLOAT_LE)
    pcm.setperiodsize(periodsize)

    dtype = numpy.dtype('<f4')

    for values in track.as_arrays_iter(periodsize):
        numpy.clip(values, -1, 1, out=values)
        out = numpy.array(values, dtype);

        pcm.write(out.tostring())
