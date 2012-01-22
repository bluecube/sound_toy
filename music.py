class Tone:
    """
    A tone.
    Internally represented in chromatic scale.
    """

    NAMES = {0:'C', 2:'D', 4:'E', 5:'F', 7:'G', 8:'A', 10:'B'}
    OCTAVE = 12
    FREQ_A = 440
    CHROMATIC_POS_A = OCTAVE * 4 + 8

    def __init__(self, n, octave=4):
        if isinstance(n, str):
            self.n, new_octave = self._parsename(n)
            if new_octave is not None:
                octave = new_octave
        else:
            self.n = n

        self.n += octave * self.OCTAVE

    @classmethod
    def _parsename(cls, name): 
        name = name.strip()

        n = None

        for index, tone_name in cls.NAMES.items():
            if name[0] == tone_name:
                n = index
                break

        if n is None:
            raise Exception('"{}" is not a valid tone name'.format(name))

        if len(name) == 1:
            return n, None

        if name[1] == '#':
            n += 1
            octave = name[2:]
        elif name[1] == 'b':
            n -= 1
            octave = name[2:]
        else:   
            octave = name[1:]

        if not octave:
            return n, None

        octave = int(octave)
        
        return n, octave

    @property
    def name(self):
        n = self.n % self.OCTAVE
        octave = self.n // self.OCTAVE

        if n in self.NAMES:
            return "{}{}".format(self.NAMES[n], octave)
        else:
            return "{}#{}".format(self.NAMES[n - 1], octave)

    @property
    def freq(self):
        return self.FREQ_A * 2**((self.n - self.CHROMATIC_POS_A) / self.OCTAVE)
        
    def __str__(self):
        return "{} ({} Hz)".format(self.name, self.freq)

    def __repr__(self):
        return self.name

    def __float__(self):
        return self.freq

# ********************************** Scales ************************************


class Scale:
    def __init__(self, root=Tone('C4')):
        self.root = root

    def __getitem__(self, index):
        if isinstance(index, slice):
            start = index.start
            stop = index.stop
            step = index.step

            if step is None:
                step = 1

            return (self.tone(i) for i in range(start, stop, step))
        else:
            return self.tone(index)

    def __len__(self):
        return len(self.HALFTONES)

    def tone(self, i):
        a, b = divmod(i, len(self.HALFTONES))
        return Tone(self.root.n + a * Tone.OCTAVE + self.HALFTONES[b])


class ChromaticScale(Scale):
    def tone(self, i):
        return Tone(self.root.n + index)

    def __len__(self):
        return Tone.OCTAVE


class MajorScale(Scale):
    HALFTONES = [0, 2, 4, 5, 7, 9, 11]


class MinorScale(Scale):
    HALFTONES = [0, 2, 3, 5, 7, 8, 11]


class MajorPentatonicScale(Scale):
    HALFTONES = [0, 2, 4, 7, 9]


class MinorPentatonicScale(Scale):
    HALFTONES = [0, 3, 5, 9, 10]


# ********************************** Rhythm ************************************


class Rhythm:
    def __init__(self, time_sig, bpm = 100):
        """
        Time sig is tuple (beat_count_per_measure, beat_note_value)
        """
        self._sig = time_sig
        self._bpm = bpm

    def timing(self, beat, measure, note_value):
        """
        Returns tuple with absolute time and length of a note.
        """
        return (self.time(beat, measure), self.note_len(note_value))

    def note_len(self, note_value):
        """
        Return length of note in seconds.
        note_value is 4, 16 ... 
        """
        return 60 * self._sig[1] / (note_value * self._bpm)

    def time(self, beat, measure):
        """
        Returns the absolute time of the given beat in given measure.
        """
        return (measure * self._sig[0] + beat) * 60 / self._bpm

    def measure_len(self):
        return self.time(0, 1)

    def __str__(self):
        return "{}/{} rhythm @ {} bpm".format(self._sig[0], self._sig[1], self._bpm)
