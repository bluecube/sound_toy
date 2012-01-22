import pygame.mixer
import pygame.locals
import pygame.sndarray
import numpy

import struct
import itertools
import math

def _prepare_block(track, maximum, blocksize):
    arr = numpy.zeros(blocksize, dtype=numpy.int16)

    last = None

    for i, val in enumerate(itertools.islice(track, blocksize)):
        arr[i] = max(-maximum, min(maximum, maximum * val))
        last = i
    
    if last is None:
        return None
    elif last != blocksize - 1:
        numpy.resize(arr, last + 1)
    
    return pygame.sndarray.make_sound(arr)

def play(track, samplerate=44100, blocksize=4096):
    track.set_samplerate(samplerate)

    pygame.mixer.init(samplerate, -16, 1, blocksize)
    pygame.display.init()
    maximum = 2**15 - 1

    it = iter(track)

    try:
        channel = pygame.mixer.Channel(0)

        channel.set_endevent(pygame.locals.USEREVENT)

        channel.play(_prepare_block(it, maximum, blocksize))
        sound = _prepare_block(it, maximum, blocksize)
        if sound is not None:
            channel.queue(sound)

        while channel.get_busy():
            event = pygame.event.wait()
            if event.type != pygame.locals.USEREVENT:
                continue

            sound = _prepare_block(it, maximum, blocksize)
            if sound is None:
                break

            channel.queue(sound)

    except KeyboardInterrupt:
        print("Keyboard interrupt.")
    except StopIteration:
        pass
    finally:
        pygame.quit()
