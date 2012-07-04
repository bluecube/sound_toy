import alsaaudio
import numpy
import math
import errno

from .tracks import NumpyTrack

def play(track, samplerate=44100, periodsize=32, card='default'):
    """
    Play a track through alsa.
    Forces samplerate of the track.
    """
    pcm = alsaaudio.PCM(
        type=alsaaudio.PCM_PLAYBACK,
        mode=alsaaudio.PCM_NORMAL,
        card=card)

    try:
        samplerate = pcm.setrate(samplerate)
            # There is no other way to query the defaults
        pcm.setchannels(1)
        pcm.setformat(alsaaudio.PCM_FORMAT_FLOAT_LE)
        pcm.setperiodsize(periodsize)

        dtype = numpy.dtype('<f4')

        for values in track.as_arrays_iter(samplerate, periodsize):
            numpy.clip(values, -1, 1, out=values)
            out = numpy.array(values, dtype);

            pcm.write(out.tostring())
    finally:
        pcm.close();

def record(length, card='hw:0', samplerate=None, periodsize=320,
    remove_dc_offset = True):
    """
    Record approximately length seconds of audio.
    Returns numpy track.
    """
    dtype = numpy.dtype('<i2')
    maximum = 2**15 - 1

    pcm = alsaaudio.PCM(
        type=alsaaudio.PCM_CAPTURE,
        mode=alsaaudio.PCM_NORMAL,
        card=card)

    try:
        if samplerate is None:
            samplerate = pcm.setrate(-1)
        else:
            if pcm.setrate(samplerate) != samplerate:
                raise Exception("Couldn't set sample rate")

        channels = pcm.setchannels(-1)
        if pcm.setformat(alsaaudio.PCM_FORMAT_S16_LE) != \
            alsaaudio.PCM_FORMAT_S16_LE:
            raise Exception("Couldn't set sample format rate")
        periodsize = pcm.setperiodsize(periodsize)

        periods = int(math.ceil(length * samplerate / float(periodsize)))
        samples = periods * periodsize

        out_arrays = []
        for i in range(channels):
            out_arrays.append(numpy.empty(samples))

        for i in range(periods):
            count, string = pcm.read()
            if count == -errno.EPIPE:
                raise Exception("Alsa buffer overrun")
            period_array = numpy.fromstring(string, dtype)
            if len(period_array) != periodsize * channels:
                print("count: ", count,
                    "len(period_array): ", len(period_array),
                    "periodsize: ", periodsize,
                    "channels: ", channels)

            period_array = numpy.array(period_array, numpy.float)
            period_array /= maximum

            for j in range(channels):
                out_arrays[j][i * periodsize:i * periodsize + count] = \
                    period_array[j::channels]
    finally:
        pcm.close()

    if remove_dc_offset:
        for array in out_arrays:
            array -= numpy.mean(array)

    ret = []
    for array in out_arrays:
        ret.append(NumpyTrack(array, samplerate))

    return ret
