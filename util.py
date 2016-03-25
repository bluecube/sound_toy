import itertools

def counted_iterator(count):
    """ Returns iterator that counts from 0 to count,
    or to infinity if count is None """

    if count is None:
        return itertools.count()
    else:
        return iter(range(count))
