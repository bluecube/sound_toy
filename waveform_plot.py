import matplotlib.pyplot as plt

def plot(tracks, samplerate = 100):
    try:
        iter(tracks)
    except TypeError:
        tracks = [tracks]

    for track in tracks:
        fig = plt.figure()
        plot = fig.add_subplot(1, 1, 1)
        plot.set_title(track.name)
        plot.set_xlabel("time [s]")
        plot.plot(track.as_array(samplerate))

    plt.show()
