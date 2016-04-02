import itertools
import functools

def counted_iterator(count):
    """ Returns iterator that counts from 0 to count,
    or to infinity if count is None """

    if count is None:
        return itertools.count()
    else:
        return iter(range(count))


class Memoize:
    def __init__(self, f):
        self._f = f
        self._cache = {}

    def __call__(self, *args, **kwargs):
        key = (tuple(args), tuple(sorted(kwargs.items())))
        if key not in self._cache:
            self._cache[key] = self._f(*args, **kwargs)
        return self._cache[key]

    def __repr__(self):
       return self._f.__doc__
