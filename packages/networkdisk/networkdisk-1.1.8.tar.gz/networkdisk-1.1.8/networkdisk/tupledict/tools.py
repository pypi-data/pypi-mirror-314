import functools


@functools.cmp_to_key
def none_smaller_than_any(u, v):
    if u == v:
        return 0
    if u is None:
        return -1
    elif v is None:
        return 1
    return int(u > v) * 2 - 1


def tuple_sorted(itr):
    return sorted(itr, key=lambda t: tuple(map(none_smaller_than_any, t)))


def trim(t, null=None):
    try:
        return t[: t.index(null)]
    except ValueError:
        return t


def padd(t, length, null=None):
    if len(t) >= length:
        return t
    else:
        return t + (null,) * (length - len(t))
