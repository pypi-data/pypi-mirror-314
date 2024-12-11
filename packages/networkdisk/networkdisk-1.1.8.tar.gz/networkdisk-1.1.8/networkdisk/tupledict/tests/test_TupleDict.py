import pytest, itertools, functools, more_itertools
from networkdisk.tupledict import (
    BaseAbstractRowStore,
    ReadOnlyTupleDictView,
    extend_tuple,
    padd,
    trim,
)


class RORS(BaseAbstractRowStore):
    def __init__(self, height, iterable):
        super().__init__(height)
        iterable = map(tuple, iterable)
        iterable = map(lambda t: extend_tuple(t, maxdepth=height), iterable)
        iterable = itertools.chain.from_iterable(iterable)
        iterable = map(lambda t: padd(t, height + 1, null=self.Null), iterable)
        self.storage = list(iterable)
        assert all(len(t) == height + 1 for t in self.storage)

    def select(
        self,
        key_prefix=(),
        start=None,
        stop=None,
        count=False,
        notnull=False,
        distinct=False,
        limit=None,
        offset=None,
        ordered=None,
        condition=None,
    ):
        res = iter(self.storage)
        if key_prefix:
            res = filter(lambda t: t[: len(key_prefix)] == key_prefix, res)
        if condition:
            res = filter(condition, res)
        if start or stop:
            res = map(lambda t: t[start:stop], res)
        if notnull:
            res = filter(lambda t: t[-1] != self.Null, res)
        if ordered:
            res = sorted(res)
        if distinct:
            if ordered:
                res = more_itertools.unique_justseen(res)
            else:
                res = more_itertools.unique_everseen(res)
        if limit or offset:
            res = itertools.islice(res, offset, limit)
        if count:
            res = sum(1 for _ in res)
        return res


# TODO: should we do those tests:
class ReadOnlyTupleDictBase:
    def setup_method(self):
        rs = RORS(
            3,
            (
                (i, j, k)
                for i in range(4)
                for j in range(i + 1)
                for k in range(i + j + 1)
            ),
        )
        self.td = rs.view()

    def test_partial(self):
        td = self.td
        for x in td:
            assert x in td
            assert (x,) in self.td.rowstore
            for y in td[x]:
                assert y in td[x]
                assert (x, y) in self.td.rowstore
                for z in td[x][y]:
                    assert z in td[x][y]
                    assert (x, y, z) in self.td.rowstore
        with pytest.raises(TypeError):
            sorted(td[0][0][0])
        assert sorted(td[2][2]) == [0, 1, 2, 3, 4]
        assert sorted(td[3]) == [0, 1, 2, 3]
        assert sorted(td[3][3]) == [0, 1, 2, 3, 4, 5, 6]
        with pytest.raises(KeyError):
            next(td[4])
