import itertools
import networkdisk.exception as ndexcept


def unfold(recdict, maxdepth=-1):
    """Enumerate tuplerows from recursive dictionary, as tuples.

        Two yields may have different length.  If `maxdepth` is nonnegative then
        only levels up to depth `maxdepth` are unfold.  Non-unfolded levels are
        kept unchanged (pointer).  The default for `maxdepth` is `-1` meaning
        unbounded.  The enumeration is depth-first.  Calling this on an empty dictionary
    yields the empty tuple.

        Parameters
        ----------
        recdict:
                a recursive dictionary

        maxdepth: int, default=-1
                the max depth to unfold the dictionary.  If -1, then unbounded.

        Examples
        --------
        >>> from networkdisk.tupledict import fold, unfold
        >>> recdict = { 'a': { 'aa': { 'aaa': True, 'aab': False }, 'ab': False }, 'b': False, 'c': {} }
        >>> sorted(unfold(recdict))
        [('a', 'aa', 'aaa', True), ('a', 'aa', 'aab', False), ('a', 'ab', False), ('b', False), ('c',)]
        >>> sorted(unfold(recdict, maxdepth=0))
        [({'a': {'aa': {'aaa': True, 'aab': False}, 'ab': False}, 'b': False, 'c': {}},)]
        >>> sorted(unfold({}, maxdepth=0))
        [({},)]
        >>> sorted(unfold(recdict, maxdepth=1))
        [('a', {'aa': {'aaa': True, 'aab': False}, 'ab': False}), ('b', False), ('c', {})]
    """
    if maxdepth and hasattr(recdict, "keys"):
        empty = True
        for k in recdict.keys():
            empty = False
            v = recdict[k]
            yield from map(lambda t: (k, *t), unfold(v, maxdepth=maxdepth - 1))
        if empty:
            yield ()
    else:
        yield (recdict,)


def fold(tuples, maxdepth=-1, default=None):
    """
    Recursively transforms an iterable of tuples in a recursive
    dictionary. Empty tuples are ignored. If `maxdepth` is given,
    then the tuples are expected to have length at most `maxdepth`
    plus one, and to satisfy the TupleDict condition, namely that
    no two tuples of length `maxdepth` differ only on their last
    coordinate. Furthermore, the `maxdepth`-th is considered as a
    leaf value not to be unfolded. If `tuples` is empty or if it
    contains only empty tuples, then an empty dictionary is
    returned, if `maxdepth` is not equal to `0`, or the value of the
    parameter `default` (default is `None`) otherwise.

    Parameters
    ----------
    tuples:
            an iterable of tuples;
    maxdepth: int, default=-1
            a bound (positive integer) on the tuple length minus one, or
            `-1` (default) meaning “unbounded”.
    default:
            a value for missing leaves (default is `None`).

    Examples
    --------
    >>> recdict = fold([(1, 2, 3), (), (1, 3, 4), (1, 3, 5), (0,), (), (1, 4, 3)])
    >>> type(recdict) is dict
    True
    >>> sorted(recdict.items())
    [(0, {}), (1, {2: {3: {}}, 3: {4: {}, 5: {}}, 4: {3: {}}})]

    """
    tuples = filter(bool, tuples)
    errmsg = "Got a tuple of length greater than"
    if not maxdepth:
        x = default
        for x in tuples:
            if len(x) > 1:
                raise ndexcept.NetworkDiskTupleDictError(
                    f"{errmsg} {maxdepth+1}, {x}", x
                )
            x = x[0]
        return x
    else:
        d = {}
        tuples = itertools.groupby(tuples, key=lambda e: e[0])
        for k, bunch in tuples:
            try:
                res = fold(
                    map(lambda x: x[1:], bunch), maxdepth=maxdepth - 1, default=default
                )
            except ndexcept.NetworkDiskTupleDictError as e:
                if not e.args[0].startswith(errmsg):
                    raise e
                t = (k,) + e.args[1]
                raise ndexcept.NetworkDiskTupleDictError(
                    f"{errmsg} {maxdepth+1}, {t}", t
                )
            if maxdepth == 1:
                d[k] = res
            else:
                d.setdefault(k, {})
                d[k].update(res)
        return d


# tuple mapping
def extend_tuple(t, maxdepth=-1):
    """
    Attempt to complete a tuple `t` by unfolding its last
    coordinate. The result is an iterable of tuples, as unfolding
    yields many tuples.
    """
    yield from map(lambda e: t[:-1] + e, unfold(t[-1], maxdepth=maxdepth - len(t) + 1))


# tuple iterable mapping
def shorten_tuples(tuples, tobound, maxdepth=-1):
    """
    Map an iterable of tuples so that resulting tuples all have
    length at most `tobound`. This is obtained by folding the
    exceeding coordinates of the tuples whose length is greater
    than `tobound` onto their `tobound`-th (`tobound-1`-indexed)
    coordinate, using the `fold` function. In this way, unlike
    mapping with the `truncate_tuples` function, no information is
    lost. This is somehow the inverse of `extend_tuples`.
    tuples.

    Parameters
    ----------
    tuples:
            an iterable of tuples.
    tobound: int
            a positive (not checked) integer.
    maxdepth: int, default=-1
            a bound (positive integer) on the tuple length minus one, or
            `-1` (default) meaning “unbounded”.
    """
    stop = tobound
    maxdepth = maxdepth - tobound if maxdepth > 0 else maxdepth
    for tlen, bunch in itertools.groupby(tuples, key=len):
        if tlen < stop:
            yield from bunch
            continue
        for tpref, bunch in itertools.groupby(bunch, key=lambda t: t[:stop]):
            yield tpref + (fold(map(lambda t: t[stop:], bunch), maxdepth=maxdepth),)
