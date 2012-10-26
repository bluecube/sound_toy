import sound_toy
import nose.tools

def interpolate_test():
    pass


def box_test():
    b = sound_toy.envelopes.Box(10, 0.5)

    # This tested, because oscillators depend on this.
    nose.tools.assert_equals(b._length, 10)
    nose.tools.assert_equals(b._value, 0.5)

    it = b.as_iter(100)

    expected_count = 10 * 100
    for i in range(expected_count):
        nose.tools.assert_equals(next(it), 0.5)

    with nose.tools.assert_raises(StopIteration):
        next(it)
