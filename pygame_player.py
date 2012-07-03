import pygame.mixer
import pygame.locals
import pygame.sndarray
import numpy

import struct
import itertools
import math

_maximum = 2**15 - 1

def _next_block(it):
    values = next(it)
    numpy.clip(values, -1, 1, out=values)
    values *= _maximum
    values = numpy.array(values, numpy.int16)
    #print(values)

    return pygame.sndarray.make_sound(values)

def play(track, samplerate=44100, blocksize=4096):
    pygame.mixer.init(samplerate, -16, 1, blocksize)
    pygame.display.init() # Needed for events ...

    try:
        channel = pygame.mixer.Channel(0)
        channel.set_endevent(pygame.locals.USEREVENT)

        it = track.as_arrays_iter(samplerate, blocksize, None)

        channel.play(_next_block(it))
        channel.queue(_next_block(it))

        while True:
            event = pygame.event.wait()

            if event.type == pygame.locals.USEREVENT:
                channel.queue(_next_block(it))

    except StopIteration:
        while channel.get_busy():
            pygame.event.wait()
    finally:
        pygame.quit()
