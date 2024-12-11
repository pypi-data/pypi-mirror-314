import itertools, functools, abc, collections
from networkdisk import tupledict as ndtd
import networkdisk.utils as ndutls

__all__ = [
    "ReadOnlyTupleDictView",
    "ReadWriteTupleDictView",
    "BaseAbstractRowStore",
    "ReadWriteAbstractRowStore",
    "tupleDictFactory",
]


# Dict-like Views on addressses
class ReadOnlyTupleDictView(collections.abc.Mapping):
    def __new__(cls, rowstore, address, cache_level=0, **kwargs):
        self = super().__new__(cls)
        self.__setstate__(
            dict(rowstore=rowstore, address=address, cache_level=cache_level, **kwargs)
        )
        assert self.height > 0
        return self

    def __getstate__(self):
        return dict(
            rowstore=self.rowstore, address=self.address, cache_level=self.cache_level
        )

    def __setstate__(self, state):
        for k, v in state.items():
            setattr(self, k, v)
        if self.cache_level:
            self._cache = dict(
                len=None,  # length if known or None otherwise
                exists=None
                if self.lazy
                else True,  # whether the tupleDict view exists or not (or has not been checked)
                items={},  # if lazy, some items are not real tupleDict items
                keys=set(),  # known keys
                all_keys=False,  # whether all the keys are in keys
            )

    @classmethod
    def build_from(cls, *instances, **kwargs):
        state = {}
        for inst in instances:
            state.update(inst.__getstate__())
        state.update(kwargs)
        return cls.__new__(cls, **state)

    @property
    def depth(self):
        return len(self.address)

    @property
    def height(self):
        return self.rowstore.height - self.depth

    @property
    def Null(self):
        return self.rowstore.Null

    @property
    def lazy(self):
        return self.rowstore.lazy

    @lazy.setter
    def lazy(self, v):
        self.rowstore.lazy = v

    @property
    def coordinate_checker(self):
        return self.rowstore.key_coordinate_checkers[self.depth]

    def to_readonly(self):
        rowstore = self.rowstore.to_readonly()
        return ReadOnlyTupleDictView.build_from(self, rowstore=rowstore)

    def check_existence(self):
        if not self.lazy or not self.address:
            return True
        elif self.cache_level and self._cache["exists"] is not None:
            return self._cache["exists"]
        else:
            res = self.rowstore.is_keyprefix(self.address)
            if self.cache_level:
                self._cache["exists"] = res
            return res

    # Mapping methods
    def __getitem__(self, k):
        assert not self.coordinate_checker or self.coordinate_checker(k)
        if self.cache_level and k in self._cache["items"]:
            return self._cache["items"][k]
        key_prefix = self.address + (k,)
        preflen = len(key_prefix)
        if self.height == 1:
            key_prefix = self.address + (k,)
            res = self.rowstore.select(key_prefix=key_prefix, start=preflen)
            preflen = len(key_prefix)
            try:
                res = next(iter(res))[0]
            except StopIteration:
                raise KeyError(key_prefix)
            if self.cache_level:
                self._cache["keys"].add(k)
                self._cache["exists"] = True
        else:
            if not self.lazy:
                if not self.rowstore.is_keyprefix(key_prefix):
                    raise KeyError(key_prefix)
                elif self.cache_level:
                    self._cache["keys"].add(k)
                    self._cache["exists"] = True
            res = self.build_from(
                self, address=key_prefix, cache_level=max(0, self.cache_level - 1)
            )
        if self.cache_level:
            self._cache["items"][k] = res
        return res

    def __len__(self):
        if self.cache_level and self._cache["len"] is not None:
            return self._cache["len"]
        key_prefix = self.address
        preflen = len(key_prefix)
        res = self.rowstore.select(
            key_prefix=key_prefix,
            start=preflen,
            stop=preflen + 1,
            distinct=True,
            notnull=True,
            count=True,
        )
        if self.cache_level:
            self._cache["len"] = res
            if res:
                self._cache["exists"] = True
        return res

    def __iter__(self):
        if self.cache_level and self._cache["all_keys"]:
            return iter(self._cache["keys"])
        key_prefix = self.address
        preflen = len(key_prefix)
        if self.lazy and self.address and not self.check_existence():
            # TODO: cache membership
            addr = self.address[:-1]
            while addr:
                if self.rowstore.is_keyprefix(addr):
                    break
                addr = addr[:-1]
            raise KeyError(self.address[len(addr)])
        res = self.rowstore.select(
            key_prefix=key_prefix,
            start=preflen,
            stop=preflen + 1,
            distinct=True,
            notnull=True,
        )
        res = map(lambda t: t[0], res)
        if self.cache_level:
            self._cache["keys"] = res = set(res)
            self._cache["len"] = len(res)
            self._cache["all_keys"] = True
            if res:
                self._cache["exists"] = True
        return iter(res)

    def __contains__(self, k):
        assert not self.coordinate_checker or self.coordinate_checker(k)
        if self.cache_level:
            if k in self._cache["keys"]:
                return True
            elif self._cache["all_keys"]:
                return False
        res = self.rowstore.is_keyprefix(self.address + (k,))
        if res and self.cache_level:
            self._cache["keys"].add(k)
            self._cache["exists"] = True
            if self._cache["len"] == len(self._cache["keys"]):
                self._cache["all_keys"] = True
        return res

    def items(self):
        if self.cache_level:
            if self._cache["all_keys"]:
                if all(k in self._cache["items"] for k in self._cache["keys"]):
                    if self.lazy:
                        return {
                            k: self._cache["items"][k] for k in self._cache["keys"]
                        }.items()
                    else:
                        return self._cache["items"].items()
                elif self.lazy and self.height > 1:
                    return {k: self[k] for k in self._cache["keys"]}.items()
        key_prefix = self.address
        preflen = len(key_prefix)
        if self.lazy and self.address and not self.check_existence():
            addr = self.address[:-1]
            while addr:
                if self.rowstore.is_keyprefix(addr):
                    break
                addr = addr[:-1]
            if self.cache_level:
                self._cache["exists"] = False
            raise KeyError(self.address[len(addr)])
        if self.height == 1:
            res = self.rowstore.select(
                key_prefix=key_prefix,
                start=preflen,
                stop=preflen + 2,
                distinct=True,
                notnull=preflen,
                orderby=(preflen,),
            )
        else:
            res = super().items()
        if self.cache_level:
            res = list(res)
            self._cache["items"].update(res)
            self._cache["keys"] = {k for k, _ in res}
            self._cache["len"] = len(res)
            self._cache["all_keys"] = True
            self._cache["exists"] = True
        return res

    # Export
    def __repr__(self):
        """
        Repr can be costly but clever alternative are hard to design.
        We perform at most 3^depth query.
        """
        limit = 3
        if self.cache_level and len(self._cache["keys"]) > limit:
            somekeys = sorted(
                self._cache["keys"], key=lambda e: e not in self._cache["items"]
            )[:limit]
        else:
            somekeys = self.rowstore.select(
                key_prefix=self.address,
                start=self.depth,
                stop=self.depth + 1,
                notnull=True,
                limit=limit + 1,
                ordered=True,
                distinct=True,
            )
        r = []
        for i, a in enumerate(somekeys):
            a = a[0]
            if a is None:
                continue
            if i == limit:
                r.append("…")
                break
            r.append(f"{a}: {repr(self[a])}")
        return f"{{{', '.join(r)}}}"

    def unfold(self, stop=None, trim=True):
        res = self.rowstore.select(
            key_prefix=self.address,
            start=self.depth,
            stop=stop,
            notnull=len(self.address),
        )
        if trim:
            res = map(lambda t: ndtd.trim(t, null=self.Null), res)
        return res

    def fold(self, stop=None):
        res = ndtd.fold(self.unfold(stop=stop, trim=True), maxdepth=self.height)
        return res

    copy = fold

    def filter(self, condition):
        return ReadOnlyTupleDictView(
            self.rowstore.filter_from_column(self.depth, condition), self.address
        )

    def __eq__(self, other):
        return other == self.fold()


class ReadWriteTupleDictView(ReadOnlyTupleDictView, collections.abc.MutableMapping):
    def __setitem__(self, k, value):
        """
        Arguments:
        +	k:
                a key (tuplekey coordinate) under which to insert value.
        +	value:
                a possible unfoldable value to insert under `k`.

        Semantics:
        1.	The _setitem_ action if overwriting, namely, existing
                items in the recursive dictionary view `self[k]` if any,
                are replaced by those from `values`.
                (This is step #2, below.)
        2.	The TupleDict semantic in `self.rowstore` is preserved,
                namely, at the end of computation, no tuplekey consisting
                of a prefix of `self.address` followed by only `self.Null`
                exist in `self.rowstore`.
                (This is ensured by step #1, below.)
        """

        with self.rowstore._contextmanager:
            assert not self.coordinate_checker or self.coordinate_checker(k)
            key_prefix = self.address + (k,)
            preflen = len(key_prefix)
            # 1.	Remove the tuplerow consisting of a strict prefix of `key_prefix` followed by `self.Null`s
            for i in range(preflen - 1, 0, -1):
                prow = key_prefix[:i] + (self.rowstore.Null,)
                if self.rowstore.is_keyprefix(prow):
                    self.rowstore.delete(key_prefix[:i])
                    shift = i - 1
                    break
            # 2.	Remove tuplekeys which have kpref as prefix;
            else:
                self.rowstore.delete(key_prefix)
                shift = 0
            # 3.	Complete the row by unfolding the structure of val, and/or appending None's;
            rows = ndtd.unfold(value, maxdepth=self.rowstore.height - preflen)
            rows = map(lambda t: key_prefix + t, rows)
            # rows = map(lambda t: ndtd.padd(t, self.rowstore.height+1, null=self.rowstore.Null), rows)
            # 4.	Insert the resulting rows
            # TODO: in non-lazy case, shift could be len(key_prefix)-1 assuming self.address is valid
            self.rowstore.bulk_insert(rows, shift=shift)

    def __delitem__(self, k):
        """
        Arguments:
        +	k:
                a key (tuplekey coordinate).

        Assumed:
        +	`self.address+(k,)` is an address in `self.rowstore`.

        Semantics:
        1.	All recursive directories under `k` are removed.
        2.	The TupleDict semantics is preserved, namely,
                `self.address` remains an address in `self.rowstore`.

        TODO: In some cases, checking key_prefix is not necessary.
        """
        with self.rowstore._contextmanager:
            assert not self.coordinate_checker or self.coordinate_checker(k)
            key_prefix = self.address + (k,)
            if not self.rowstore.is_keyprefix(key_prefix):
                raise KeyError(k)
            self.rowstore.delete(key_prefix)
            key_prefix = key_prefix[:-1]
            if key_prefix and not self.rowstore.is_keyprefix(key_prefix):
                self.rowstore.insert(key_prefix, shift=len(key_prefix) - 1)

    def clear(self):
        with self.rowstore._contextmanager:
            self.rowstore.delete(())


# Base
class BaseAbstractRowStore(abc.ABC):
    """Abstract class for tupleDict back-end storing rows

    An abstract class whose implementations are the TupleDict
    base class. It assume to implement selection of partial _rows_
    in a data store.

    Notes
    -----

    Abstract methods:
    +	select
            the class core method, which allows a fine control on row
            selection, e.g., selection under condition, projections, and
            aggregation.

    Abstract properties:
    +	height:
            the height of the tupleDict tree. It is therefore the length
            of the rows minus one (the last coordinate being the
            _tuplevalue_).
    +	lazy:
            a Boolean specifying whether partial _tuplekey_ membership
            should be checked on reading or not. When `False`, some
            TupleDictViews might have invalid addresses.

    Terminology:
    +	the _height_ is the depth of the represented recursive dict
    +	a _row_ is a `tuple` of fixed length height plus one
    +	a _tuplekey_ is a row prefix of length height
    +	a _tuplevalue_ is a row last coordinate
    +	_Null_ is a special value, indicating void coordinates
    +	a _trimmed row_, is a row prefix obtained by dropping off
            Null values from the right

    Semantic restrictions:
    1.	All rows have length `height+1`
    2.	No two rows are equal
    3.	No two rows differ on their last coordinate only
    4.	In each row, the Null coordinates form a suffix of the row
    5.	No trimmed row is a prefix of another trimmed row
    6.	No row can have Null value on its last coordinate only

    Class attributes:
    +	_View:
            the class to use for providing a tupledict (recursive dict of
            bounded depth) interface. The view class is initialized with
            a pointer to the rowstore instance, as well as a tuple of
            length less than `height`, called `address` and representing
            a row prefix. See the method `view` below.
    +	Null:
            a value (default is `None`) to use for padding incomplete
            rows.
    """

    _updateondelvalue = False
    _View = ReadOnlyTupleDictView
    Null = None
    lazy = False

    @property
    def _RO(self):
        return type(self)

    @property
    def key_coordinate_checkers(self):
        return (ndutls.TrueChecker,) * self.height

    @property
    @abc.abstractmethod
    def height(self):
        pass

    @abc.abstractmethod
    def select(
        self,
        key_prefix=(),
        start=None,
        stop=None,
        count=None,
        agg=None,
        notnull=False,
        distinct=False,
        limit=None,
        offset=None,
        ordered=False,
        groupby=None,
        condition=ndtd.TrueCondition(),
    ):
        """
        Arguments:

        +	key_prefix:
                consider only rows for which `key_prefix` is a prefix;
                this is equivalent to passing the conjunction condition
                of `ndtd.CompareCondition(i, key_prefix(i))` for `i`
                ranging over the index of `key_prefix`. Default is the
                empty tuple.
        +	condition:
                consider only rows satisfying condition (default is
                `ndtd.TrueCondition`);
        +	start, stop:
                a slice specification for columns to return.
        +	notnull:
                consider only rows whose last selected column is not
                `self.Null`
        +	distinct:
                do not yield repeated tuples.
        +	count:
                counts selected row parts rather than enumerating them.
        +	limit:
                consider the `limit` first selected rows only.
        +	offset:
                ignore the `offset` first rows.
        +	ordered:
                enumerate rows in order

        Return:
        +	an iterable of rows, or an aggregate (`int` if `count` is `True`).
        """
        res = iter(self)
        if key_prefix:
            res = filter(lambda t: t[: len(key_prefix)] == key_prefix, res)
        if condition:
            res = filter(condition, res)
        if notnull is True:
            notnull = -1
        if notnull:
            res = filter(lambda t: t[notnull] is not self.Null, res)
        if columns is not None:
            res = map(lambda t: [t[i] for i in columns], res)
        if start or stop is not None:
            res = map(lambda t: t[start:stop], res)
        if ordered or groupby:
            res = sorted(res)
        if distinct:
            if ordered:
                res = filter(
                    lambda e: not e[0] or res[e[0] - 1] != e[1], enumerate(res)
                )
            else:
                res = list(res)
                res = filter(lambda e: e[0] == res.index(e[1]), enumerate(res))
        if groupby:
            res = itertools.groupby(res, key=lambda t: tuple(t[i] for i in groupby))
            if agg is None:
                agg = lambda e: next(iter(e))
            res = map(lambda e: agg(e[1]), res)
            agg = None
        if limit or offset:
            res = itertools.islice(offset, limit)
        if agg:
            assert not count
            res = agg(res)
        if count:
            return sum(1 for _ in res)
        return res

    def __getstate__(self):
        if hasattr(super(), "__getstate__"):
            return super().__getstate__()
        return {}

    def __setstate__(self, state):
        for k, v in state.items():
            setattr(self, k, v)

    @classmethod
    def build_from(cls, *instances, **kwargs):
        state = {}
        for i in instances:
            state.update(i.__getstate__())
        state.update(kwargs)
        self = object.__new__(cls)
        self.__setstate__(state)
        return self

    @abc.abstractmethod
    def filter(self, col, condition):
        # use self._RO
        pass

    def view(self, key_prefix=()):
        return self._View(
            self, key_prefix, cache_level=max(0, self.cache_level - len(key_prefix))
        )

    def is_keyprefix(self, key_prefix):
        res = self.select(key_prefix=key_prefix, count=True, limit=1)
        return bool(res)

    def partial_fold(self, depth, maxfolddepth=None, **kwargs):
        kwargs.setdefault("ordered", True)
        res = self.select(**kwargs)

        def func(iterquer):
            iterquer = map(lambda t: ndtd.trim(t, null=self.Null), iterquer)
            iterquer = itertools.groupby(iterquer, key=lambda t: t[:depth])
            iterquer = map(
                lambda t: (
                    t[0],
                    ndtd.fold(map(lambda u: u[depth:], t[1]), maxdepth=maxfolddepth),
                ),
                iterquer,
            )
            return iterquer

        res = res.apply(func)
        return res

    def is_valid(self):
        """
        Returns `True` or `False` according to whether `self`
        respects the tupleDict semantics.

        1.	`None` values form suffixes of rows, of length unequal to 1;
        2.	not-`None` maximal prefixes of rows are unique.
        """
        prevpref, prevsuff = (), ()
        for r in self.select(ordered=True):
            if None in r:
                i = r.index(None)
                prefix = r[:i]
                suffix = r[i:]
                if not prefix:
                    return False
                if len(suffix) == 1:
                    return False
                if not all(c is None for c in suffix):
                    return False
                m = min(len(prefix), len(prevpref))
                if m and prevpref[:m] == prefix[:m]:
                    return False
            else:
                prefix = r
                suffix = ()
                if not prevsuff and r[:-1] == prevpref[:-1]:
                    return False
            prevpref = prefix
            prevsuff = suffix
        return True

    def to_readonly(self):
        return self


class ReadWriteAbstractRowStore(BaseAbstractRowStore):
    """
    A read/write version of `BaseAbstractRowStore`. In
    addition to the `select` method of the parent class, it
    should provide two methods for inserting or deleting data.

    Abstract methods:
    +	select
            (see `BaseAbstractRowStore`)
    +	insert
            for inserting a partial row
    +	delete
            for deleting all rows starting with a row_prefix

    Abstract properties:
    +	height, lazy
            (see `ReadOnlyAbstractRowStore`)

    Methods:
    +	bulk_insert
    +	bulk_insert_onepass
    +	bulk_insert_reiterable
    """

    _View = ReadWriteTupleDictView
    _RO = BaseAbstractRowStore
    _contextmanager = ndutls.nullcontext
    _ReadOnlyRowStore = BaseAbstractRowStore

    def to_readonly(self):
        state = self.__getstate__()
        new = object.__new__(self._ReadOnlyRowStore)
        new.__setstate__(state)
        return new

    @abc.abstractmethod
    def insert(self, row, shift=0):
        """
        Parameters
        ----------
        row: tuple
                a tuple of coordinate of length `self.height+1` or less.
                In the latter case, the tuple is padded using the value
                `self.Null` so that its length becomes `self.height+1`.
        shift: int
                an integer (default 0) specifying that the first `shift`
                coordinates of `row` are supposed to form a valid tuplekey
                prefix. In other word, `row[:shift]` is a tuple such that
                `self.is_keyprefix(row[:shift])` returns `True` (this is
                assumed and not checked).

        Raises
        ------
        NetworkdiskTupleDictError
                if the length of `row` is greater than `self.height+1`.
        """
        pass

    @abc.abstractmethod
    def delete(self, row_prefix, no_reinsert=0):
        """
        Parameters
        ----------
        row_prefix: tuple
                a tuple of coordinates, indicating a row prefix.

        no_reinsert: bool or int or iterable
                defines a set of tuplekey lengths for which no reinsertion is
                required.  If an iterable, then its integers members are in the set.
                If a Boolean, then none (`False`) or all (`True`) lengths are in the
                set.  If an integer, all length up to that integer (included) are in
                the set (e.g., `no_reinsert=3` is equivalent to `range(4)`).
                Furthermore, the rowstore height is always added in the set.

        Raises:
        -------
        NetworkdiskTupleDictError
                if `row` has length greater than `self.height`.

        KeyError
                if `row` is not in the store.
        """
        if isinstance(no_reinsert, int):
            no_reinsert = set(range(no_reinsert + 1))
        elif no_reinsert is True:
            no_reinsert = set(range(self.depth))
        elif no_reinsert is False:
            no_reinsert = set()
        no_reinsert.add(self.height)
        pass  # should do the job here

    # BULK INSERT
    def bulk_insert(self, rows, shift=0):
        if iter(rows) is rows:
            return self.bulk_insert_onepass(rows, shift=shift)
        else:
            return self.bulk_insert_reiterable(rows, shift=shift)

    def bulk_insert_onepass(self, rows, shift=0):
        for row in rows:
            if len(row) <= shift:
                continue
            return self.insert(row)

    def bulk_insert_reiterable(self, rows, shift=0):
        return self.bulk_insert_onepass(rows, shift=shift)

    # BULK DELETE
    def bulk_delete(self, row_prefixes, no_reinsert=(0,)):
        row_prefixes = set(row_prefixes)
        for row_prefix in row_prefixes:
            self.delete(row_prefix)
        if no_reinsert is True:
            return
        elif no_reinsert is not False:
            row_prefixes = {
                r[:-1]
                for r in row_prefixes
                if len(r[:-1]) not in no_reinsert and r[:-1] not in row_prefixes
            }
        for row_prefix in row_prefixes:
            self.insert(row_prefix)


# Auxiliary class for TupleDict creation
class tupleDictFactory:
    """
    Callable class used to construct TupleDict from RowStore.
    Returns a TupleDictWrapper that creates a RowStore with given
    arguments, and then returns a View on it (with empty address).
    """

    def __init__(self, RowStore):
        self.RowStore = RowStore

    def __call__(self, *args, **kwargs):
        rs = self.RowStore(*args, **kwargs)
        return rs.view()
