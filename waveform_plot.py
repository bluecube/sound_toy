import matplotlib.pyplot as plt
import numpy

def plot(tracks, samplerate = 10000):
    try:
        iter(tracks)
    except TypeError:
        tracks = [tracks]

    for track in tracks:
        fig = plt.figure()
        plot = fig.add_subplot(1, 1, 1)
        plot.set_title(track.name)
        plot.set_xlabel("time [s]")

        ys = track.as_array(samplerate)
        xs = numpy.arange(len(ys)) / samplerate
        plot.plot(xs, ys)

    plt.show()
