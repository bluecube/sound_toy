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
