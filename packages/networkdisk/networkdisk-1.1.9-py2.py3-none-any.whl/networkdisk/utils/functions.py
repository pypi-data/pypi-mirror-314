import collections

Hashable = collections.abc.Hashable


def hashable_checker(c):
    hash(c)
    return True
