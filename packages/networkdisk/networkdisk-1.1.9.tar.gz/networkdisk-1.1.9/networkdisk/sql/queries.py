"""Module containing the SQL-base queries definitions.

TODO: provides details on class hierarchy and organization and scopes stuff.
"""

import abc, functools, itertools, collections, sys
from collections.abc import Mapping
from networkdisk.sql.scope import ScopeValueColumns, InternalColumns, ExternalColumns
from networkdisk.exception import NetworkDiskSQLError
from networkdisk.utils.constants import (
    notProvidedArg,
    IdentityFunction,
    Projection0,
    Projection1,
    BinRel,
)
from collections import OrderedDict
from .dialect import sqldialect as dialect

dialect = dialect.provide_submodule(__name__)

__all__ = [
    "ValuesQuery",
    "NamedQuery",
    "WithQuery",
    "SelectQuery",
    "UnionQuery",
    "ExceptQuery",
    "IntersectQuery",
    "UnionAllQuery",
    "JoinQuery",
    "LeftJoinQuery",
    "InnerJoinQuery",
    "FullJoinQuery",
    "RightJoinQuery",
    "InsertQuery",
    "ReplaceQuery",
    "UpdateQuery",
    "DeleteQuery",
    "CreateTableQuery",
    "CreateViewQuery",
    "CreateIndexQuery",
    "CreateTriggerQuery",
    "DropTableQuery",
    "DropIndexQuery",
    "DropViewQuery",
    "DropTriggerQuery",
]


# decorator
def scopable(f):
    @functools.wraps(f)
    def decored(self, *args, scoped=None):
        if scoped:
            return f"({f(self, *args)})"
        else:
            return f"{f(self, *args)}"

    return decored


def nonscopable(f):
    @functools.wraps(f)
    def decored(self, *args, scoped=None):
        return f(self, *args)

    return decored


# Abstract Query classes
@dialect.register(True)
class AbstractQuery(abc.ABC):
    """Base abstract class for query definition

    All `AbstractQuery`s are immutable by design. They provide
    `qformat`, `get_args`, `subformat`, and `get_subargs` methods
    that will be used for execution. These four methods are
    cached to improve performance. The two '*sub*' methods are
    decorated at subclass definition using the `__init_subclass__`
    hook, while the two other methods are decorated withing this
    abstract class.

    """

    reorder_post_encoding = IdentityFunction

    def __init_subclass__(cls):
        return
        for meth in ["subformat", "get_subargs"]:
            if meth in cls.__dict__:
                # use `cls.__dict__` rather than `dir`, in order to avoid decorating super class methods
                setattr(
                    cls, meth, functools.lru_cache(maxsize=None)(getattr(cls, meth))
                )

    def __init__(self, dialect):
        self.dialect = dialect

    @classmethod
    def build_from(cls, *instances, **kwargs):
        state = {}
        for inst in instances:
            state.update(inst.__getstate__())
        state.update(kwargs)
        self = object.__new__(cls)
        self.__setstate__(state)
        return self

    @abc.abstractmethod
    def subformat(self, scoped=False):
        pass

    def is_dummy(self):
        return False

    @functools.lru_cache(maxsize=None)
    def qformat(self):
        res = self.subformat(scoped=False)
        wqs = [wq.wqformat() for wq in self.get_with_queries().values()]
        if wqs:
            res = f"WITH {', '.join(wqs)} {res}"
        return res

    def get_subargs(self):
        return ScopeValueColumns()

    @functools.lru_cache(maxsize=None)
    def get_args(self):
        return (
            sum(
                (wq.get_wqargs() for wq in self.get_with_queries().values()),
                ScopeValueColumns(),
            )
            + self.get_subargs()
        )

    def get_with_queries(self):
        return {}

    def get_placeholder_args(self):
        return ScopeValueColumns(
            filter(
                lambda c: c.value is self.dialect.constants.Placeholder, self.get_args()
            )
        )

    @functools.lru_cache(maxsize=None)
    def get_args_permutation(self, column_map):
        """Get the correct order of apparition of arguments.

        Parameters
        ----------
        column_map: mapping
                a mapping specification from indices of PLACEHOLDERs,
                with respect to their occurrence order in `self`, to name
                of `columns`
        """
        try:
            column_map = dict(column_map)
        except (TypeError, ValueError):
            column_map = dict(enumerate(column_map))
        qargs = self.get_args()
        pargs = self.get_placeholder_args()
        permut = []
        byvalue = {k: list(v) for k, v in qargs.byvalue.items()}
        for i, parg in enumerate(pargs):
            cdef = column_map.pop(i, i)
            cdef = list(pargs[cdef])
            c = cdef.pop(0)
            target = byvalue[c].pop(0)
            permut.append((i, target, c.encode))
        return permut

    def encode_args(self, permut, args, reorder_post_encoding=None):
        """
        Parameters
        ----------
        self: Query
                the query for which to encode the arguments.

        permut: list
                a list defining a permutation of the values given in args.
                Hence, the list has same length as `args`. Each element of
                the list is a triple `(i, j, encode)` which specifies that
                the `i`-th element of `args` (`args[i]`) becomes the `j`-th
                element of the returned tuple, and is encoded using the
                function `encode`.
        args: tuple of arguments

        reorder_post_encoding: a function to reorder the tuple post encoding.
                a function that permutes tuples. This can be used to reorder
                the resulting tuple coordinates after being encoded (e.g.,
                for putting them in nondecreasing order, see TupleDict rekey
                functions).
        """
        return next(
            self.encode_many_args(
                permut, (args,), reorder_post_encoding=reorder_post_encoding
            )
        )

    def encode_many_args(self, permut, I, append=False, reorder_post_encoding=None):
        encoders = getattr(self, "encoders", {})
        encoders = {k: list(v) for k, v in encoders.items()}
        newt = []
        for c in self.get_args():
            encode = encoders.get(c, [c.encode]).pop(0)
            newt.append(encode(c.value))
        placeholders = [
            j
            for j, v in enumerate(newt)
            if v == self.dialect.constants.Placeholder.sqlize()
        ]

        # 1. encode value expected by PLACEHOLDERS in newt order
        def aux_encode(t):
            for i, _, encode in permut:
                newt[placeholders[i]] = encode(t[i])
            return tuple(newt)

        I = map(aux_encode, I)
        # 2. (optional) apply reorder_post_encoding
        if reorder_post_encoding and reorder_post_encoding is not IdentityFunction:
            I = map(reorder_post_encoding, I)
        # 3.	permut resulting args
        permut2 = [
            (placeholders[i], j, encode)
            for i, j, encode in permut
            if j != placeholders[i]
        ]
        if permut2:

            def aux_permut(t):
                for i, j, _ in permut2:
                    newt[j] = t[i]
                return tuple(newt)

            I = map(aux_permut, I)
        return I

    def get_schema_containers(self):
        if isinstance(self, self.dialect.schema.SchemaContainer.func):
            yield self

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.qformat()}>"

    def __str__(self):
        return self.qformat()

    def __getstate__(self):
        return dict(dialect=self.dialect.name)

    def __setstate__(self, state):
        for k, v in state.items():
            if k == "dialect":
                v = dialect._dialects[v]
            setattr(self, k, v)

    def __hash__(self):
        if not hasattr(self, "_hash"):
            self._hash = hash(
                tuple(sorted(self.__getstate__().items())) + (self.__class__.__name__,)
            )
        return self._hash

    def __eq__(self, other):
        return hash(self) == hash(other)


@dialect.register(True)
class FromQueriesQuery(AbstractQuery):
    def __init__(self, dialect, *subqueries):
        super().__init__(dialect)
        self.subqueries = subqueries

    def add_subquery(self, subquery, *, inplace=False):
        if inplace:
            self.subqueries = *self.subqueries, subquery
        else:
            return self.build_from(self, subqueries=(*self.subqueries, subquery))

    @property
    def internal_columns(self):
        if not hasattr(self, "_internal_columns"):
            self._internal_columns = InternalColumns(*self.subqueries)
        return self._internal_columns

    @functools.lru_cache(maxsize=None)
    def get_subargs(self):
        # if len(self.subqueries) == 1:
        # return self.subqueries[0].get_subargs()
        return sum((sq.get_subargs() for sq in self.subqueries), super().get_subargs())

    @functools.lru_cache(maxsize=None)
    def get_with_queries(self):
        with_queries = {}
        for sq in self.subqueries:
            with_queries.update(sq.get_with_queries())
        return with_queries

    def get_schema_containers(self):
        yield from super().get_schema_containers()
        for sq in self.subqueries:
            yield from sq.get_schema_containers()

    def __getstate__(self):
        state = super().__getstate__()
        state["subqueries"] = self.subqueries
        return state


@dialect.register(True)
class FromQueryQuery(FromQueriesQuery):
    """
    The particular case of `FromQueriesQuery` which have only one
    subquery, that can be accessed through the `subquery`
    property.
    """

    @property
    def subquery(self):
        return self.subqueries[0]


@dialect.register(True)
class Script(collections.abc.Iterable):
    """
    An iterable of queries.
    """


@dialect.register(True)
class ReadQuery(AbstractQuery, Mapping):
    @property
    @abc.abstractmethod
    def external_columns(self):
        pass

    def __iter__(self):
        return iter(self.external_columns)

    def __getitem__(self, k):
        if isinstance(k, slice):
            return self.external_columns[k]
        return self.external_columns.unambiguous_get(k)

    def __len__(self):
        return len(self.external_columns)

    def decode(self, t):
        assert len(self.external_columns) == len(t)
        return tuple(c.decode(v) for c, v in zip(self.external_columns, t))

    def name_query(self, name):
        return self.dialect.queries.NamedQuery(self, name)

    def select_query(self, *args, **kwargs):
        return self.dialect.queries.SelectQuery(self, *args, **kwargs)

    def left_join_query(self, *args, **kwargs):
        return self.dialect.queries.LeftJoinQuery(self, *args, **kwargs)

    def right_join_query(self, *args, **kwargs):
        return self.dialect.queries.RightJoinQuery(self, *args, **kwargs)

    def inner_join_query(self, *args, **kwargs):
        return self.dialect.queries.InnerJoinQuery(self, *args, **kwargs)

    def full_join_query(self, *args, **kwargs):
        return self.dialect.queries.FullJoinQuery(self, *args, **kwargs)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return super().__hash__()


@dialect.register(True)
class FromQueriesReadQuery(ReadQuery, FromQueriesQuery):
    pass


@dialect.register(True)
class WriteQuery(AbstractQuery):
    def __init__(self, dialect, container):
        super().__init__(dialect)
        self.container = container

    def is_dummy(self):
        return False

    @property
    def internal_columns(self):
        if not hasattr(self, "_internal_columns"):
            self._internal_columns = InternalColumns(*self.subqueries)
        return self._internal_columns

    def get_schema_containers(self):
        yield from super().get_schema_containers()
        yield from self.container.get_schema_containers()

    def __getstate__(self):
        state = super().__getstate__()
        state["container"] = self.container
        return state


# Real Query classes
@dialect.register(True)
class DummyQuery(ReadQuery):
    """
    A pseudo table for selecting constants columns, as in Oracle,
    c.f. https://fr.wikipedia.org/wiki/Table_DUAL.
    """

    def __init__(self, dialect):
        super().__init__(dialect)
        self.name = "dummy"
        dummycol = dialect.columns.ValueColumn("X", encoder="TEXT", name="dummy")
        track_values = BinRel()
        track_values.add((dummycol, dummycol))
        self._external_columns = ExternalColumns((dummycol,), track_values=track_values)

    @nonscopable
    def subformat(self):
        return self.name

    def is_dummy(self):
        return True

    @property
    def external_columns(self):
        return self._external_columns


@dialect.register(True)
class ValuesQuery(ReadQuery):
    def __init__(self, dialect, *valuetuples, for_columns=None):
        super().__init__(dialect)
        if not valuetuples:
            raise NetworkDiskSQLError(f"At least one value expected")
        valuetuples = tuple(
            vt if isinstance(vt, tuple) else (vt,) for vt in valuetuples
        )
        sign = len(valuetuples[0])
        if any(len(vt) != sign for vt in valuetuples):
            raise NetworkDiskSQLError(
                f"All VALUES must have the same number of terms -- some have length different to {sign}"
            )
        if for_columns is not None and sign != len(for_columns):
            raise NetworkDiskSQLError(
                f"There should be the same number of “for columns” than the length of value tuples, got {len(for_columns)}!={sign}"
            )
        self.valuetuples = valuetuples
        self.for_columns = tuple(for_columns) if for_columns else ()
        self.set_columns(valuetuples, for_columns=for_columns)

    def set_columns(self, valuetuples, for_columns=None):
        for_columns = for_columns or ()
        fcolumns = []
        f2bcolumns = {}
        tcolumns = []
        track_values = BinRel()
        for j, vt in enumerate(valuetuples):
            tcol = []
            for i, (bcol, vcol) in enumerate(itertools.zip_longest(vt, for_columns)):
                name = f"column{i+1}"
                # if not isinstance(bcol, ValueColumn):
                if not isinstance(bcol, self.dialect.columns.AbstractColumn.func):
                    bcol = self.dialect.columns.ValueColumn(bcol, for_column=vcol)
                tcol.append(bcol)
                if not j:
                    fcol = self.dialect.columns.QueryColumn(
                        name=name,
                        index_in_container=j,
                        encoder=getattr(bcol, "encoder", None),
                        sqltype=bcol.sqltype,
                    )
                    f2bcolumns[fcol] = bcol
                    fcolumns.append(fcol)
                track_values.add((bcol, fcolumns[i]))
            tcol = self.dialect.columns.TupleColumn(*tcol)
            tcolumns.append(tcol)
        self.valuetuples = tuple(tcolumns)
        self._external_columns = ExternalColumns(
            fcolumns, sources=f2bcolumns, track_values=track_values
        )

    @property
    def external_columns(self):
        return self._external_columns

    @functools.lru_cache(maxsize=None)
    @scopable
    def subformat(self, context=None):
        return f"VALUES {', '.join(vt.qformat() for vt in self.valuetuples)}"

    def __getstate__(self):
        state = super().__getstate__()
        state.update(
            _external_columns=self._external_columns,
            valuetuples=self.valuetuples,
            for_columns=self.for_columns,
        )
        return state

    @functools.lru_cache(maxsize=None)
    def get_subargs(self):
        return sum((vt.get_subargs() for vt in self.valuetuples), ScopeValueColumns())

    def union_query(self, other):
        if not isinstance(other, self.__class__) or len(self) != len(other):
            return super().union_query(other)
        ph = self.dialect.constants.Placeholder
        if any(
            any(c is ph for c in v)
            for v in itertools.chain(self.valuetuples, other.valuetuples)
        ):
            return super().intersect_query(other)
        state = self.__getstate__()
        state["valuetuples"] = tuple(set(self.valuetuples).union(other.valuetuples))
        new = object.__new__(self.__class__)
        new.__setstate__(state)
        return new

    def intersect_query(self, other):
        if not isinstance(other, self.__class__) or len(self) != len(other):
            return super().intersect_query(other)
        ph = self.dialect.constants.Placeholder
        if any(
            any(c is ph for c in v)
            for v in itertools.chain(self.valuetuples, other.valuetuples)
        ):
            return super().intersect_query(other)
        state = self.__getstate__()
        state["valuetuples"] = tuple(
            set(self.valuetuples).intersection(other.valuetuples)
        )
        new = object.__new__(self.__class__)
        new.__setstate__(state)
        return new

    def union_all_query(self, other):
        if not isinstance(other, self.__class__) or len(self) != len(other):
            return super().intersect_query(other)
        state = self.__getstate__()
        state["valuetuples"] = self.valuetuples + other.valuetuples
        new = object.__new__(self.__class__)
        new.__setstate__(state)
        return new

    def except_query(self, other):
        if not isinstance(other, self.__class__) or len(self) != len(other):
            return super().intersect_query(other)
        ph = self.dialect.constants.Placeholder
        if any(
            any(c is ph for c in v)
            for v in itertools.chain(self.valuetuples, other.valuetuples)
        ):
            return super().intersect_query(other)
        state = self.__getstate__()
        state["valuetuples"] = tuple(set(self.valuetuples).setminus(other.valuetuples))
        new = object.__new__(self.__class__)
        new.__setstate__(state)
        return new


@dialect.register(True)
def PlaceholdersQuery(dialect, n, for_columns=(), encoders=(), names=()):
    kwargs_d = dict(
        for_column=dict(enumerate(for_columns)),
        encoder=dict(enumerate(encoders)),
        name=dict(enumerate(names)),
    )
    kwargs_i = lambda i: {k: v.get(i, None) for k, v in kwargs_d.items()}
    return dialect.queries.ValuesQuery(
        *(dialect.columns.PlaceholderColumn(**kwargs_i(i)) for i in range(n))
    )


@dialect.register(True)
class NamedQuery(FromQueriesReadQuery):
    def __init__(self, dialect, subquery, name, *subqueries):
        subqueries = (subquery,) + subqueries
        super().__init__(dialect, *subqueries)
        self.name = name
        fcolumns = []
        f2bcolumns = {}
        track_values = BinRel()
        for sq in self.subqueries:
            for j, bcol in enumerate(sq.external_columns):
                if hasattr(bcol, "name"):
                    fcol = self.dialect.columns.QueryColumn(
                        name=bcol.name,
                        index_in_container=j,
                        encoder=bcol.encoder,
                        sqltype=bcol.sqltype,
                        container_name=name,
                    )
                    f2bcolumns[fcol] = bcol
                    vbcol = sq.external_columns.track_values.right.get(bcol, ())
                    track_values.update((v, fcol) for v in vbcol)
                else:
                    fcol = bcol
                fcolumns.append(fcol)
        self._external_columns = ExternalColumns(
            fcolumns, sources=f2bcolumns, track_values=track_values
        )

    @property
    def external_columns(self):
        return self._external_columns

    @functools.lru_cache(maxsize=None)
    @nonscopable
    def subformat(self):
        subqueries = self.subqueries
        while len(subqueries) == 1 and isinstance(subqueries[0], __class__):
            subqueries = subqueries[0].subqueries
        if len(subqueries) > 1:
            return f"({', '.join(sq.subformat(scoped=True) for sq in subqueries)}) AS {self.name}"
        return f"{subqueries[0].subformat(scoped=True)} AS {self.name}"

    def __getstate__(self):
        state = super().__getstate__()
        state["name"] = self.name
        state["_external_columns"] = self._external_columns
        return state

    def recondition(self, condition):
        for new in self:
            old = self.external_columns.sources[new]
            condition = condition.substitute_column(old, new)
        return condition

    def recolumn(self, column):
        return self.external_columns.get_external_column_from_source(column, column)


@dialect.register(True)
class WithQuery(NamedQuery, FromQueryQuery):
    def __init__(self, dialect, subquery, name):
        super().__init__(dialect, subquery, name)

    @functools.lru_cache(maxsize=None)
    def get_with_queries(self):
        with_queries = super().get_with_queries()
        with_queries = dict(with_queries)
        if self.name in with_queries:
            if with_queries[self.name] is not self:
                raise NetworkDiskSQLError(
                    f"Cannot create WithQuery with same name as some owned WithQuery: {self.name}"
                )
        else:
            with_queries[self.name] = self
        return with_queries

    @functools.lru_cache(maxsize=None)
    @nonscopable
    def subformat(self):
        return f"{self.name}"

    @functools.lru_cache(maxsize=None)
    def get_subargs(self):
        return self.dialect.queries.AbstractQuery.func.get_subargs(self)

    @functools.lru_cache(maxsize=None)
    def get_wqargs(self):
        return self.subquery.get_subargs()

    @functools.lru_cache(maxsize=None)
    def wqformat(self):
        return f"{self.name} AS {self.subquery.subformat(scoped=True)}"


@dialect.register(True)
class UnionQuery(FromQueriesReadQuery):
    operator = "UNION"

    def __init__(self, dialect, first, *others):
        subqueries = []
        for sq in (first, *others):
            if len(sq) != len(first):
                raise NetworkDiskSQLError(
                    f"Cannot combine subqueries of different arities in {self.operator}, got {len(first)} and {len(sq)}."
                )
            if type(sq) == type(self):
                # flat union
                subqueries.extend(sq.subqueries)
            else:
                subqueries.append(sq)
        super().__init__(dialect, *subqueries)
        f2bcolumns = {}
        track_values = {}
        fcolumns = []
        for j, bcol in enumerate(first.external_columns):
            if hasattr(bcol, "name"):
                fcol = self.dialect.columns.QueryColumn(
                    name=bcol.name,
                    index_in_container=j,
                    sqltype=bcol.sqltype,
                    encoder=bcol.encoder,
                )
                f2bcolumns[fcol] = bcol
                vbcol = first.external_columns.track_values.right.get(bcol, ())
                track_values.update((v, fcol) for v in vbcol)
            else:
                fcol = bcol
            fcolumns.append(fcol)
        self._external_columns = ExternalColumns(
            fcolumns, sources=f2bcolumns, track_values=track_values.items()
        )

    @property
    def external_columns(self):
        return self._external_columns

    @functools.lru_cache(maxsize=None)
    @scopable
    def subformat(self):
        return f" {self.operator} ".join(
            q.subformat(scoped=False) for q in self.subqueries
        )

    def count(self, alias=None):
        aliases = (alias,) if alias else ()
        return self.dialect.queries.SelectQuery(
            self, columns=(self.dialect.columns.CountColumn(),), aliases=aliases
        )

    def project(self, *columns):
        nq = self.name_query(f"_{self.operator}_query")
        return nq.select_query(columns=columns)

    @functools.wraps(functools.partialmethod(__init__, None, None))
    def union_query(self, other):
        if len(self) != len(other):
            raise NetworkDiskSQLError(
                f"left and right side of query UNION should have same arity, got {len(self)} and {len(other)}"
            )
        return self.dialect.queries.UnionQuery(self, other)

    @functools.wraps(functools.partialmethod(__init__, None, None))
    def except_query(self, other):
        if len(self) != len(other):
            raise NetworkDiskSQLError(
                f"left and right side of query EXCEPT should have same arity, got {len(self)} and {len(other)}"
            )
        return self.dialect.queries.ExceptQuery(self, other)

    @functools.wraps(functools.partialmethod(__init__, None, None))
    def intersect_query(self, other):
        if len(self) != len(other):
            raise NetworkDiskSQLError(
                f"left and right side of query INTERSECTION should have same arity, got {len(self)} and {len(other)}"
            )
        return self.dialect.queries.IntersectQuery(self, other)

    @functools.wraps(functools.partialmethod(__init__, None, None))
    def union_all_query(self, other):
        if len(self) != len(other):
            raise NetworkDiskSQLError(
                f"left and right side of query ALL-UNION should have same arity, got {len(self)} and {len(other)}"
            )
        return self.dialect.queries.UnionAllQuery(self, other)

    @functools.wraps(functools.partialmethod(__init__, None, None))
    def with_query(self, name):
        return self.dialect.queries.WithQuery(self, name)

    def set_columns(self, selcolumns, aliases=()):
        if hasattr(selcolumns, "qformat"):
            selcolumns = (selcolumns,)
        return self.select_query(columns=selcolumns, aliases=aliases)


@dialect.register(True)
class ExceptQuery(UnionQuery):
    operator = "EXCEPT"


@dialect.register(True)
class IntersectQuery(UnionQuery):
    operator = "INTERSECT"


@dialect.register(True)
class UnionAllQuery(UnionQuery):
    operator = "UNION ALL"


@dialect.register(True)
class SelectQuery(FromQueriesReadQuery):
    """
    A `SelectQuery` is a selection of columns of another query,
    which can be of any kind. It has attributes:

    TODO: The following is outdated doc.

    Parameters
    ----------

    subqueries:
            a possibly empty iterable of subqueries from which the
            columns are taken;

    columns: list | None, default=None
            a list of specifications of the selected columns. If None
            the list is automatically computed from the exposed columns
            of the subqueries.

    aliases: dict or tuples of key/values, default=()
            a dictionary defining a partial mapping from column names
            (typically `str`) or indices (`int`) to aliases (`str`).
            The mapping is partial, column with no associated alias
            are just left unaliased. The default value is `()` which
            is interpreted as the empty mapping. When looking for a
            specific column alias, indices have precedence over names.

    condition: a condition or None, default=None
            A condition to apply to the query in the WHERE clause.

    orderby: iterable | None, default=None
            a set of columns that are used for ordering the selected
            tuples, or the value `None`;

    distinct: bool, default=False
            if True, add the FILTER keyword to prevent multiple occurrence
            to be return.

    groupby: tuple of internal columns or None, default=None
                    tuple of internal columns for grouping.

    desc: bool | None, default=None
            a Boolean if `orderby` is not `None`, indicating whether the
            order should be descending or ascending, or the value `None`
            if unspecified;

    limit: int | None, delault=None
            a limit (`int`) on the number of tuples to select or `None`;

    offset: int | None, default=None
            an offset (`int`) when `limit` is not `None`, or `None`.

    """

    all_origins = False

    def __init__(
        self,
        dialect,
        *subqueries,
        columns=None,
        aliases=(),
        condition=None,
        distinct=False,
        groupby=None,
        orderby=None,
        desc=None,
        limit=None,
        offset=None,
    ):
        if subqueries == (None,):
            subqueries = ()
        super().__init__(dialect, *subqueries)
        self.set_columns(columns, aliases, inplace=True)
        self.set_condition(condition, inplace=True)
        self.set_orderby(orderby, desc=desc, inplace=True)
        self.set_distinct(distinct, inplace=True)
        self.set_limit(limit, offset=offset, inplace=True)
        self.set_groupby(groupby, inplace=True)

    @property
    def external_columns(self):
        return self._external_columns

    @functools.lru_cache(maxsize=None)
    def get_subargs(self):
        res = super().get_subargs()
        l = []
        for fcol in self.external_columns:
            fcol = self.external_columns.sources.get(fcol, fcol)
            l.extend(fcol.get_subargs())
        # TODO: prepend list to res (which is a ScopeValueColumns not a list)!!!!!
        l = ScopeValueColumns(l)
        res = l + res
        if self.condition:
            res += self.condition.get_subargs()
        return res

    @functools.lru_cache(maxsize=None)
    def get_with_queries(self):
        with_queries = super().get_with_queries()
        with_queries = dict(with_queries)
        if self.condition:
            for name, wq in self.condition.get_with_queries().items():
                if with_queries.get(name, wq) is not wq:
                    raise NetworkDiskSQLError(f"Ambiguity on with queries {name}")
                with_queries[name] = wq
        return with_queries

    @functools.lru_cache(maxsize=None)
    def get_schema_containers(self):
        yield from super().get_schema_containers()
        yield from self.condition.get_schema_containers()

    @functools.lru_cache(maxsize=None)
    @scopable
    def subformat(self):
        formatted_columns = []
        context = self.internal_columns
        for fcol in self.external_columns:
            bcol = self.external_columns.sources.get(fcol, None)
            if bcol is None:
                formatted_columns.append(fcol.qformat(context=context))
                continue
            alias = fcol.name
            formatted_columns.append(bcol.qformat(context=context, alias=alias))
        formatted_columns = ", ".join(formatted_columns)
        if self.subqueries and any(not sq.is_dummy() for sq in self.subqueries):
            body = f" FROM {', '.join(sq.subformat(scoped=True) for sq in self.subqueries if not sq.is_dummy())}"
        else:
            body = ""
        distinct = "DISTINCT " if self.distinct else ""
        q = f"SELECT {distinct}{formatted_columns}{body}"
        if self.condition:
            q += f" WHERE {self.condition.qformat(context=context)}"
        if self.groupby:
            q += f" GROUP BY {', '.join(c.qformat(context=context) for c in self.groupby)}"
        if self.orderby:
            q += f" ORDER BY {', '.join(c.qformat(context=context) for c in self.orderby)}"
            if self.desc is True:
                q += f" desc"
            elif self.desc is False:
                q += f" asc"
        q = " ".join(
            sq for sq in [q, self.offset_subformat(), self.limit_subformat()] if sq
        )
        return q

    def __getstate__(self):
        state = super().__getstate__()
        state["_external_columns"] = self._external_columns
        state["condition"] = self.condition
        state["orderby"] = self.orderby
        state["desc"] = self.desc
        state["distinct"] = self.distinct
        state["limit"] = self.limit
        state["offset"] = self.offset
        state["groupby"] = self.groupby
        return state

    def offset_subformat(self):
        if self.offset:
            return f"OFFSET {self.offset}"
        return ""

    def limit_subformat(self):
        if self.limit:
            return f"FETCH FIRST {self.limit} ROWS ONLY"
        return ""

    def count(self, alias=None):
        aliases = (alias,) if alias else ()
        countcol = self.dialect.columns.CountColumn()
        return self.dialect.queries.SelectQuery(
            self, columns=(countcol,), aliases=aliases
        )
        Ext = ExternalColumns()
        return self.__class__.build_from(self, _external_columns=Ext)

    @functools.wraps(functools.partialmethod(UnionQuery, None, None))
    def union_query(self, other):
        if len(self) != len(other):
            raise NetworkDiskSQLError(
                f"left and right side of query UNION should have same arity, got {len(self)} and {len(other)}"
            )
        return self.dialect.queries.UnionQuery(self, other)

    @functools.wraps(functools.partialmethod(ExceptQuery, None, None))
    def except_query(self, other):
        if len(self) != len(other):
            raise NetworkDiskSQLError(
                f"left and right side of query EXCEPT should have same arity, got {len(self)} and {len(other)}"
            )
        return self.dialect.queries.ExceptQuery(self, other)

    @functools.wraps(functools.partialmethod(IntersectQuery, None, None))
    def intersect_query(self, other):
        if len(self) != len(other):
            raise NetworkDiskSQLError(
                f"left and right side of query INTERSECTION should have same arity, got {len(self)} and {len(other)}"
            )
        return self.dialect.queries.IntersectQuery(self, other)

    @functools.wraps(functools.partialmethod(UnionAllQuery, None, None))
    def union_all_query(self, other):
        if len(self) != len(other):
            raise NetworkDiskSQLError(
                f"left and right side of query ALL-UNION should have same arity, got {len(self)} and {len(other)}"
            )
        return self.dialect.queries.UnionAllQuery(self, other)

    @functools.wraps(functools.partialmethod(WithQuery, None, None))
    def with_query(self, name):
        return self.dialect.queries.WithQuery(self, name)

    def set_columns(self, selcolumns, aliases=(), *, inplace=False):
        aliases = dict(aliases)
        if selcolumns is None:
            selcolumns = itertools.chain.from_iterable(
                (sq.external_columns for sq in self.subqueries)
            )
        elif hasattr(selcolumns, "qformat") or hasattr(selcolumns, "sqlize"):
            selcolumns = (selcolumns,)
        elif not hasattr(selcolumns, "__iter__"):
            selcolumns = (selcolumns,)
        elif hasattr(selcolumns, "target"):
            selcolumns = selcolumns.target
        if not inplace:
            state = self.__getstate__()
            new = object.__new__(type(self))
            new.__setstate__(state)
            selcolumns = list(selcolumns)
            for i, c in enumerate(selcolumns):
                orig_c = self.external_columns.sources.get(
                    self.external_columns.unambiguous_get(c, c), c
                )
                selcolumns[i] = orig_c
                if c in self and i not in aliases and hasattr(c, "name"):
                    if c in aliases:
                        aliases[orig_c] = aliases.pop(c)
                    else:
                        aliases.setdefault(orig_c, c.name)
            new.set_columns(selcolumns, aliases, inplace=True)
            return new
        fcolumns = []  # list of external columns to build.
        f2bcolumns = {}  # partial mapping from external cols to internal or pseudo-internal cols.
        track_values = (
            BinRel()
        )  # mapping from (deep) ValueColumns to ExternalColumn tuples
        for idx, col in enumerate(selcolumns):
            matchings = self.internal_columns.get(col, None)
            if matchings is None:
                if hasattr(col, "sqlize"):
                    bcol = self.dialect.columns.ConstantColumn(col)
                elif hasattr(col, "qformat"):
                    bcol = col
                else:
                    bcol = self.dialect.columns.ValueColumn(col)
            elif not matchings:
                raise NetworkDiskSQLError(f"AbstractColumn {col} not found")
            elif len(matchings) > 1:
                raise NetworkDiskSQLError(f"Ambiguous column {col}")
            else:
                bcol = matchings[0]
            alias = aliases.get(getattr(bcol, "name", None), None)
            alias = aliases.get(idx, alias)
            alias = aliases.get(bcol, alias)
            if matchings and alias is None:
                if hasattr(bcol, "name"):
                    fcol = self.dialect.columns.QueryColumn(
                        name=bcol.name,
                        index_in_container=idx,
                        encoder=bcol.encoder,
                        sqltype=bcol.sqltype,
                    )
                else:
                    # if matchings evaluates to `True`, this means that `bcol` is a internal column, that we cannot select
                    raise NetworkDiskSQLError(
                        f"Cannot bind unnamed column {col} without alias"
                    )
            elif alias is None:
                fcol = bcol
                bcol = None
            else:
                encoder = bcol.encoder if hasattr(bcol, "encoder") else None
                fcol = self.dialect.columns.QueryColumn(
                    name=alias,
                    index_in_container=idx,
                    encoder=encoder,
                    sqltype=bcol.sqltype,
                )
            fcolumns.append(fcol)
            if bcol:
                f2bcolumns[fcol] = bcol
                if bcol in self.internal_columns.byvalue:
                    qbcol = self.internal_columns.origin_query[bcol]
                    vbcol = qbcol.external_columns.track_values.right.get(bcol, ())
                    track_values.update((v, fcol) for v in vbcol)
                for vcol in bcol.get_subargs():
                    track_values.add((vcol, fcol))
        self._external_columns = ExternalColumns(
            fcolumns, sources=f2bcolumns, track_values=track_values
        )

    def set_limit(self, limit, offset=None, *, inplace=False):
        if not inplace:
            state = self.__getstate__()
            new = object.__new__(type(self))
            new.__setstate__(state)
            new.set_limit(limit, offset=offset, inplace=True)
            return new
        assert offset is None or limit is not None
        self.limit = limit
        self.offset = offset

    def set_condition(self, condition, *, inplace=False):
        if not inplace:
            state = self.__getstate__()
            new = object.__new__(type(self))
            new.__setstate__(state)
            new.set_condition(condition)
            return new
        self.condition = condition or self.dialect.conditions.EmptyCondition()

    def set_orderby(self, orderby, desc=None, *, inplace=False):
        if not inplace:
            state = self.__getstate__()
            new = object.__new__(type(self))
            new.__setstate__(state)
            new.set_orderby(orderby, desc=desc, inplace=True)
            return new
        orderby = desc if orderby is None else orderby
        orderby = columns if orderby is True else orderby
        orderby = list(orderby) if orderby else orderby
        self.orderby = (
            None
            if orderby is None
            else tuple(self.internal_columns.unambiguous_get(c) for c in orderby)
        )
        self.desc = desc

    def set_groupby(self, groupby, *, inplace=False):
        if not inplace:
            state = self.__getstate__()
            new = object.__new__(type(self))
            new.__setstate__(state)
            new.set_groupby(groupby)
            return new
        self.groupby = (
            None
            if groupby is None
            else tuple(self.internal_columns.unambiguous_get(c) for c in groupby)
        )

    def set_distinct(self, distinct, *, inplace=False):
        if not inplace:
            state = self.__getstate__()
            new = object.__new__(type(self))
            new.__setstate__(state)
            new.set_distinct(distinct)
            return new
        self.distinct = distinct


Jspec = collections.namedtuple(
    "Jspec", ("pairs", "pair_condition", "other_condition", "kind")
)


@dialect.register(True)
class JoinQuery(FromQueriesReadQuery):
    """class used to defined JOIN like query.

    Attributes
    ----------
    default_joinkind: str
            The kind of join that will be used.

    Parameters
    ----------

            subqueries: AbsractQuery
                    the ordered tuple of subqueries to build the JOIN with.

            joinpairs: iterable, default=()
                    an iterable defining the partial mapping from subquery
                    indices to list of pairs of columns used for joining the
                    index-corresponding subquery with its preceding one. If
                    not a `dict` then `dict(enumerate(joinpairs, start=1))` is
                    applied first to obtain the mapping. Each mapping image
                    can be a list of specifications of pairs of columns, a
                    single such specification, or the special value `None` or
                    `True`. If it is `None`, then no equality of pairs is used
                    for joining (this is equivalent to the empty list). If it
                    `True`, then the joining is enforced to be natural, whence
                    the `joinconds` parameter should have value `None`. If,
                    otherwise, it is not a `list`, then it is replaced by the
                    singleton list containing the given value, in order to
                    fall back in the first case. A specification of pairs of
                    columns is either a pair of internal column specifications
                    (a column, a column name, or a column index), or a single
                    column name or index. In the latter case, it is repeated
                    twice to get a pair of column specifications whence
                    falling back in the former case. The image associated with
                    `0`, if any, should be `None` since there is no preceding
                    subquery.

            joinconds: iterable, default=()
                    an iterable defining the partial mapping from subquery
                    indices to conditions (not relating on equality of pairs
                    of columns given by the above `joinpairs` mapping-defining
                    argument) associated with each join. These conditions are
                    inserted in the ON clause. If the argument is not a `dict`
                    then `dict(enumerate(joinconds, start=1))` is applied
                    first to obtain the mapping. The mapping images should
                    either be conditions or `None` values, interpreted as the
                    empty condition. The image associated with `0`, if any,
                    should be `None` or the empty condition, since their is no
                    with preceding subquery with which to join.

            joinkinds: iterable, default=()
                    an iterable defining the partial mapping from subquery
                    indices to strings indicating whether LEFT, INNER, RIGHT,
                    or FULL JOIN should be performed for joining the index-
                    corresponding subquery with its preceding one. If not a
                    `dict` then `dict(enumerate(joinkind, start=1))` is
                    applied first in order to obtain the mapping. Subquery
                    indices that do not have a corresponding kind string, are
                    mapped to the `default_joinkind` string. Each string image
                    is case-insensitive, and trimed before being treated. The
                    SQL keywords 'OUTER' and 'JOIN' are optional, e.g., the
                    string "Left Outer Join" will be interpreted as "LEFT". If
                    the prefix "NATURAL" is given, then the mappings resulting
                    from the parameters `joinpairs` and `joinconds` must have
                    undefined image or image equal to `None` (or to `True` for
                    `joinpairs`) associated with the corresponding subquery
                    index. The image associated with `0` is always ignored as
                    there is no preceding subquery.

            default_joinkind: str or None, default=None
                    either `None` or a string defining the default join kind
                    of subqueries (see `joinkinds` documentation). If `None`,
                    the default class attribute `default_joinkind` is used.
    """

    default_joinkind = ""

    def __init__(
        self,
        dialect,
        *subqueries,
        joinpairs=(),
        joinconds=(),
        joinkinds=(),
        default_joinkind=None,
    ):
        # Set joins
        if not isinstance(joinpairs, dict):
            joinpairs = dict(enumerate(joinpairs, start=1))
        if not isinstance(joinconds, dict):
            joinconds = dict(enumerate(joinconds, start=1))
        if not isinstance(joinkinds, dict):
            joinkinds = dict(enumerate(joinkinds, start=1))
        self.default_joinkind = self.format_joinkind(default_joinkind)
        # Flat join
        newsubqueries, newjoinpairs, newjoinconds, newjoinkinds = [], [], [], []
        for i, sq in enumerate(subqueries):
            if hasattr(sq, "default_joinkind"):
                newsubqueries.extend(sq.subqueries)
                newjoinpairs.extend(
                    map(lambda j: list(getattr(j, "pairs", ())) or None, sq.joins)
                )
                newjoinconds.extend(
                    map(lambda j: getattr(j, "other_condition", None), sq.joins)
                )
                newjoinkinds.extend(map(lambda j: getattr(j, "kind", None), sq.joins))
            else:
                dummysq = sq.is_dummy()
                newsubqueries.append(sq)
                newjoinpairs.append(joinpairs.get(i, None))
                newjoinconds.append(joinconds.get(i, None))
                newjoinkinds.append(
                    joinkinds.get(
                        i, self.default_joinkind if i and not dummysq else None
                    )
                )
                if dummysq:
                    assert not newjoinpairs[-1]
                    assert not newjoinconds[-1]
                    assert not newjoinkinds[-1]
        subqueries, joinpairs, joinconds, joinkinds = (
            newsubqueries,
            newjoinpairs,
            newjoinconds,
            newjoinkinds,
        )
        #
        super().__init__(dialect, *subqueries)
        self.set_external_columns()
        joins = []
        left = None
        for i, right in enumerate(self.subqueries):
            jpairs = joinpairs[i]
            jcond = joinconds[i]
            jkind = joinkinds[i]
            jspec = self.get_join_spec(
                self.dialect, left, right, jpairs, jcond=jcond, jkind=jkind
            )
            joins.append(jspec)
            left = right
        self.joins = tuple(joins)

    def set_external_columns(self):
        columns = (c for sq in self.subqueries for c in sq.external_columns)
        sources = {c: c for sq in self.subqueries for c in sq.external_columns}
        self._external_columns = ExternalColumns(columns, sources)

    @property
    def external_columns(self):
        return self._external_columns

    @functools.lru_cache(maxsize=None)
    @nonscopable
    def subformat(self):
        frmt = []
        for i, sq in enumerate(self.subqueries):
            if sq.is_dummy():
                continue
            fsq = sq.subformat(scoped=True)
            join = self.joins[i]
            if not i:
                combi, oncond = "", ""
            else:
                combi = f"{join.kind} "
                oncond = join.pair_condition & join.other_condition
                if oncond:
                    oncond = f" ON {oncond.qformat(context=self.internal_columns)}"
                else:
                    oncond = ""
            frmt.append(f"{combi}{fsq}{oncond}")
        q = " ".join(frmt)
        return q

    def is_dummy(self):
        return all(sq.is_dummy() for sq in self.subqueries)

    def __getstate__(self):
        state = super().__getstate__()
        state["default_joinkind"] = self.default_joinkind
        state["joins"] = self.joins
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        self.set_external_columns()

    @functools.lru_cache(maxsize=None)
    def get_subargs(self):
        subargs = []
        for i, sq in enumerate(self.subqueries):
            subargs.extend(sq.get_subargs())
            if i:
                subargs.extend(self.joins[i].other_condition.get_subargs())
        return tuple(subargs)

    @functools.lru_cache(maxsize=None)
    def get_with_queries(self):
        wqs = dict(super().get_with_queries())
        for jspec in self.joins[1:]:
            for cond in (jspec.pair_condition, jspec.other_condition):
                for n, wq in cond.get_with_queries().items():
                    if n in wqs:
                        if wqs[n] != wq:
                            raise NetworkDiskSQLError(
                                f"Got two distinct with queries {wqs[n]} and {wq} of same name {n}"
                            )
                    else:
                        wqs[n] = wq
        return wqs

    def add_join_conditions(self, joinconds):
        if not isinstance(joinconds, dict):
            joinconds = dict(enumerate(joinconds, start=1))
        joins = list(self.joins)
        for i, jspec in enumerate(joins):
            if i in joinconds:
                if not i:
                    raise NetworkDiskSQLError(
                        f"Cannot condition leftmost subquery, got {joinconds[i]}"
                    )
                jspec = Jspec(
                    jspec.pairs,
                    jspec.pair_condition,
                    jspec.other_condition & joinconds[i],
                    jspec.kind,
                )
                joins[i] = jspec
        return self.build_from(self, joins=tuple(joins))

    @functools.lru_cache(maxsize=None)
    def truncate(self, up_to):
        subqueries = self.subqueries[:up_to]
        joins = self.joins[:up_to]
        return self.build_from(self, subqueries=subqueries, joins=joins)

    @functools.lru_cache(maxsize=None)
    def naturalize(self, ignore=False):
        """
        +	ignore:
                Boolean. If `True` every subquery is joined naturally,
                ignoring existing joinpairs and joinconditions (except for
                the joincondition of the first subquery, which is kept).
                Otherwise, only subqueries with empty joinpairs and empty
                joincondition are made natural, thus keeping the joinpairs
                and joinconditions.
        """
        joins = list(self.joins)
        kw = "NATURAL"
        emptycond = self.dialect.conditions.EmptyCondition()
        for i, jspec in enumerate(joins):
            if not i or jspec.pairs is True:
                continue
            if not jspec.pairs and not jspec.other_condition:
                if ignore is None:
                    raise NetworkDiskSQLError(
                        f"Cannot safely naturalize JOIN query with joinpairs {jspec.pairs} and/or joincondition {jspec.other_condition}"
                    )
                if ignore is False:
                    continue
            jkind = " ".join((kw, jspec.kind))
            joins[i] = Jspec(True, emptycond, emptycond, jkind)
        return self.build_from(self, joins=tuple(joins))

    @functools.lru_cache(maxsize=None)
    def denaturalize(self):
        joins = list(self.joins)
        kw = "NATURAL"
        for i, jspec in enumerate(joins):
            if not i:
                continue
            if jspec.pairs is True:
                jkind = jspec.kind[len(kw) :].strip()
                joins[i] = Jspec(
                    None, jspec.pair_condition, jspec.other_condition, jkind
                )
        return self.build_from(self, joins=tuple(joins))

    @functools.lru_cache(maxsize=None)
    def kindify(self, joinkinds):
        if joinkinds is None:
            joinkinds = {}
        elif not isinstance(joinkinds, dict):
            joinkinds = dict(enumerate(joinkinds, start=1))
        joins = list(self.joins)
        emptycond = self.dialect.conditions.EmptyCondition()
        for i, jspec in enumerate(joins):
            if not i:
                continue
            jkind = joinkinds.get(i, None)
            if jkind is not None:
                jkind = self.format_jkind()
                kw = "NATURAL "
                if jkind.startswith(kw):
                    assert (
                        (jspec.pairs is None or jspec.pairs is True)
                        and not jspec.pair_condition
                        and not jspec.other_condition
                    )
                    jspec = Jspec(
                        True, jspec.pair_condition, jspec.other_condition, jkind
                    )
                else:
                    jspec = Jspec(
                        jspec.pairs, jspec.pair_condition, jspec.other_condition, jkind
                    )
                joins[i] = jspec

    @classmethod
    def format_joinkind(cls, jkind):
        if jkind is None:
            jkind = cls.default_joinkind
        jkind = jkind.strip().upper()
        if jkind == "JOIN":
            jkind = ""
        for kw in [" JOIN", " OUTER"]:
            if jkind.endswith(kw):
                jkind = jkind[: len(kw)].strip()
        jkind = f"{jkind} JOIN".strip()
        return jkind

    @classmethod
    def get_join_spec(
        cls, dialect, left, right, jpairs=None, jcond=None, jkind=None, natural=None
    ):
        """
        Parameters
        ----------
        left: query
                The left query to join or `None`
        right: query
                The right query to join
        jpairs: None | bool | list, default=None
                Either `None`, `True`, a list of specifications of pair of
                columns, or a single specification of pair of columns. The
                last case is initially transformed into the singleton list
                containing the given specification, while the first case
                (`None`) is equivalent to the empty list case. It hence
                remains two cases: `True` and a `list`. If `True`, the
                JOIN is enforced to be NATURAL. In this case both `jcond`
                and `jpaircond` should be `None` or the empty condition.
                Otherwise, the list is considered for getting the list of
                pairs of `left`/`right` columns that should be equal in
                the joining. Each element of the list is expected to be
                either a pair of `left`/`right` column specifications, or
                a column name or index. The latter case is replaced by the
                pair consisting of the given value repeated twice, thus
                falling in the former case. Every pair `(l, r)` of column
                specifications should be such `l` (resp. `r`) can be
                unambiguously resolved within the external columns of the
                subquery `left` (resp. `right`).
        jcond: None | condition, default=None
                Either `None` or a condition, to be additionnally applied
                in the ON clause (conjunction).
        jkind: None | str, default=str
                either `None` or a string which specifies the kind of JOIN
                to performed. It is first trimed and uppercased. The SQL
                keywords "OUTER" and "JOIN" are optional and ignored. If
                it starts with the keywords "NATURAL" then the JOIN is
                ensured to be NATURAL. In this case, `jpairs` should be
                `None` or `True` and `jcond` should be `None` or the empty
                condition.
        natural: bool | None, default=None
                either `None` or a Boolean. If `True` then enforce the
                JOIN to be NATURAL, if `False` enforce the JOIN to be non-
                NATURAL. If `None`, let `jpairs` and/or `jkind` decide.
        """
        emptycond = dialect.conditions.EmptyCondition()
        if not left:
            if jpairs is not None:
                raise NetworkDiskSQLError(
                    f"Illed-formed JoinQuery: unexpected equality column pairs for leftmost subquery: {jpairs}"
                )
            if jcond:
                raise NetworkDiskSQLError(
                    f"Illed-formed JoinQuery: unexpected condition for leftmost subquery: {jcond}"
                )
            if jkind is not None:
                raise NetworkDiskSQLError(
                    f"Illed-formed JoinQuery: unexpected kind for leftmost subquery: {jkind}"
                )
            if natural is not None:
                raise NetworkDiskSQLError(
                    f"Illed-formed JoinQuery: cannot force {'NATURAL' if natural else 'non-NATURAL'} JOIN for leftmost subquery"
                )
            return Jspec((), emptycond, emptycond, None)
        jkind = cls.format_joinkind(jkind)
        if jcond is None:
            jcond = emptycond
        # Check whether JOIN should be NATURAL
        kw = "NATURAL "
        jpaircond = emptycond
        if natural is False:
            if jkind.startswith(kw):
                jkind = jkind[len(kw) :]
            if jpairs is True:
                jpairs = None
        if natural is True:
            if jcond:
                raise NetworkDiskSQLError(
                    f"Illed-formed JoinQuery: unexpected condition in NATURAL JOIN: {jpairs}"
                )
            if not jkind.startswith(kw):
                jkind = f"{kw}{jkind}"
            jpairs = True
        elif jkind.startswith(kw):
            if jpairs is not True and jpairs:
                raise NetworkDiskSQLError(
                    f"Illed-formed JoinQuery: unexpected equality column pairs in NATURAL JOIN: {jpairs}"
                )
            if jcond:
                raise NetworkDiskSQLError(
                    f"Illed-formed JoinQuery: unexpected condition in NATURAL JOIN: {jcond}"
                )
            jpairs = True
            natural = True
        elif jpairs is True:
            jkind = f"{kw}{jkind}"
            natural = True
        elif jpairs is None:
            jpairs = ()
        else:
            if jpairs and not isinstance(jpairs, list):
                jpairs = [jpairs]
            for k, jp in enumerate(jpairs):
                if isinstance(jp, tuple):
                    l, r = jp
                else:
                    l, r = jp, jp
                try:
                    first_succeed = False
                    l1 = left.external_columns.unambiguous_get(l, None)
                    l = l1 or left.external_columns.unambiguous_get(l)
                    first_succeed = True
                    r1 = right.external_columns.unambiguous_get(r, None)
                    r = r1 or right.external_columns.unambiguous_get(r)
                except KeyError:
                    error = r if first_succeed else l
                    raise NetworkDiskSQLError(f"No column {error}")
                jpairs[k] = (l, r)
                jpaircond &= l.eq(r)
            jpairs = tuple(jpairs)
        return Jspec(jpairs, jpaircond, jcond, jkind)

    @classmethod
    def join(cls, dialect, left, right, *on, condition=None, kind=None, natural=None):
        """A wrapper of `JoinQuery` constructor for joining together two queries: `left` and `right`.

        Parameters
        ----------
        left: query
                the left subquery
        right: query
                the right subquery
        *on: specifications of pairs of colunms
                a tuple of specification of pairs of columns
        condition: condition
                a condition to be applied within ON clause
        kind: str | None, default=None
                a string specifying the join kind (default is `"INNER"`)
        natural: bool or None, default=None
                a Boolean (`bool`) indicating whether the join should be
                natural. When `True`, then `on` should be empty and
                `condition` should be `None`.
        """
        if left.is_dummy() or right.is_dummy():
            assert not on and not condition
        subqueries = []
        joins = []
        # LEFT
        if isinstance(left, cls):
            subqueries.extend(left.subqueries)
            joins.extend(left.joins)
        else:
            subqueries.append(left)
            joins.append(None)
        # JOIN
        on = list(on)
        jspec = cls.get_join_spec(
            dialect, left, right, on, condition, kind, natural=natural
        )
        joins.append(jspec)
        # RIGHT
        if isinstance(right, cls):
            subqueries.extend(right.subqueries)
            joins.extend(right.joins[1:])
        elif not right.is_dummy():
            subqueries.append(right)
        # BUILDING
        self = cls.build_from(
            dialect=dialect.name, subqueries=tuple(subqueries), joins=tuple(joins)
        )
        return self


## INSERTION
@dialect.register(True)
class InsertQuery(WriteQuery, FromQueryQuery):
    """A class for Insert Queries

    Parameters
    ----------
    container: SQL container
            Typically a table or a view. See `schema` module.
    query: ReadQueryFromQueries
            Any query from which values to be inserted are taken.
    columns: iterable of columns of `container`
            The columns of `container` in which values should be
            inserted. If `STAR` then all columns are non-explicitly
            taken. If `None` then the columns are automatically
            determined from the external columns of `query`, starting
            by making the correspondence between columns with matching
            names, and then associating the remaining columns with the
            untaken columns of `container`, taken in the order of the
            `container.external_columns` iterable.

    Attributes
    ----------
    _insert: str
            TODO: should it be in the doc?

    """

    _insert = "INSERT"

    # TODO: accept upsert clauses ("ON CONFLICT…")
    def __init__(self, dialect, container, query=None, columns=None):
        columns = tuple(columns)
        args_nb = len(container.external_columns) if not columns else len(columns)
        query = query or dialect.queries.PlaceholdersQuery(args_nb)
        if not isinstance(container, dialect.schema.SchemaContainer.func):
            raise NetworkDiskSQLError(
                f"{container} is expected to be a container with children"
            )
        if len(query.external_columns) > len(container.external_columns):
            raise NetworkDiskSQLError(
                f"Cannot insert more values than table arity, got {len(query.external_columns)}>{len(container.external_columns)}"
            )
        dialect.queries.WriteQuery.func.__init__(self, dialect, container)
        dialect.queries.FromQueryQuery.func.__init__(self, dialect, query)
        self.set_columns(columns)
        self.set_encoders()
        # assert all(hasattr(c, 'name') for c in self.external_columns)
        # assert all(c.name in container for c in self.columns)

    def get_subargs(self):
        return self.subquery.get_subargs()

    @functools.lru_cache(maxsize=None)
    def get_with_queries(self):
        return dict(self.subquery.get_with_queries())

    def get_schema_containers(self):
        yield from self.dialect.queries.WriteQuery.get_schema_containers(self)
        yield from self.dialect.queries.FromQueryQuery.get_schema_containers(self)

    def set_columns(self, incolumns):
        inserted_columns = list(self.subquery.external_columns)
        if not incolumns:
            incolumns = inserted_columns
        assert len(incolumns) == len(inserted_columns)
        contcolnames = OrderedDict(
            ((c.name, c) for c in self.container.external_columns)
        )
        assert len(incolumns) <= len(contcolnames)
        columns = [None] * len(incolumns)
        for i, col in enumerate(incolumns):
            contcol = self.container.get(col, None)
            if contcol:
                assert contcol not in columns
                columns[i] = contcol
            elif hasattr(col, "name") and col.name in contcolnames:
                # TODO: is this too smart, silently?
                col = contcolnames.pop(col.name)
                assert col not in columns
                columns[i] = col
        for i, col in enumerate(incolumns):
            if columns[i] is None:
                columns[i] = contcolnames.popitem(last=False)[1]
        self.columns = tuple(columns)

    def set_encoders(self):
        columns = self.columns
        args = self.get_args().byindex
        fcols = self.subquery.external_columns
        encoders = {}
        for vcol in args:
            s = fcols.track_values.left.get(vcol, ())
            s = tuple(columns[vci] for c in s for vci in fcols.byvalue[c])
            if s:
                assert all(c.encoder == s[0].encoder for c in s)
                encoders.setdefault(vcol, [])
                encoders[vcol].append(s[0].encode)
        self.encoders = {k: tuple(v) for k, v in encoders.items()}

    def get_args_permutation(self, column_map):
        encoders = {k: list(v) for k, v in self.encoders.items()}
        permut = super().get_args_permutation(column_map)
        args = self.get_args()
        newpermut = []
        for i, j, encode in permut:
            vcis = encoders.get(args[j][0])
            res = vcis.pop(0) if vcis else encode
            newpermut.append((i, j, res))
        return newpermut

    @nonscopable
    def subformat(self):
        if self.columns is self.dialect.constants.Star:
            columns = "*"
        else:
            columns = f'({", ".join(c.name for c in self.columns)})'
        query = self.subquery.subformat(scoped=False)
        q = f"{self._insert} INTO {self.container.name}{columns} {query}"
        return q.strip()

    def __getstate__(self):
        state = self.dialect.queries.WriteQuery.func.__getstate__(self)
        state.update(self.dialect.queries.FromQueryQuery.func.__getstate__(self))
        state["columns"] = self.columns
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        self.set_encoders()


@dialect.register(True)
class ReplaceQuery(InsertQuery):
    _insert = "REPLACE"


## UPDATE
@dialect.register(True)
class UpdateQuery(WriteQuery):
    """Class to build Update Query

    Parameters
    ----------
    container: SQLContainer
            see	`SchemaContainer` (view or table) to update in `sql.schema` module

    values: dict | iterable of key,value, default=()
            A dictionary mapping column specification (name, index, or
            the column itself) to associated value to introduce.

    condition: condition | None, default=None
            a condition that rows to update should satisfy.

    **kwargs:
            a keyworded list of parameters to update `values`.

    """

    def __init__(self, dialect, container, values=(), condition=None, **kwargs):
        super().__init__(dialect, container)
        self.condition = condition or self.dialect.conditions.EmptyCondition()
        values = dict(values)
        values.update(kwargs)
        self.value_map = {
            container[k]: self.dialect.columns.ValueColumn(v, for_column=container[k])
            for k, v in values.items()
        }

    @nonscopable
    def subformat(self):
        colval = ", ".join(
            f"{k.qformat()}={v.qformat()}" for k, v in self.value_map.items()
        )
        q = f"UPDATE {self.container.name} SET {colval}"
        if self.condition:
            q = f"{q} WHERE {self.condition.qformat()}"
        return q

    def get_subargs(self):
        subargs = sum(
            (v.get_subargs() for v in self.value_map.values()), ScopeValueColumns()
        )
        if self.condition:
            subargs += self.condition.get_subargs()
        return subargs

    def __getstate__(self):
        state = super().__getstate__()
        state.update(condition=self.condition)
        return state


## DELETE
@dialect.register(True)
class DeleteQuery(WriteQuery):
    def __init__(self, dialect, container, condition=None):
        assert hasattr(container, "name")
        super().__init__(dialect, container)
        self.condition = condition or self.dialect.conditions.EmptyCondition()

    @nonscopable
    def subformat(self):
        q = f"DELETE FROM {self.container.name}"
        if self.condition:
            q = f"{q} WHERE {self.condition.qformat()}"
        return q

    def get_subargs(self):
        if self.condition:
            return self.condition.get_subargs()
        else:
            return super().get_subargs()

    def get_schema_containers(self):
        yield from super().get_schema_containers()
        yield from self.condition.get_schema_containers()

    def __getstate__(self):
        state = super().__getstate__()
        state.update(condition=self.condition)
        return state


## CREATION
@dialect.register(True)
class CreateQuery(WriteQuery):
    @property
    @abc.abstractmethod
    def _kind(self):
        return NotImplemented

    def __init__(self, dialect, container, ifnotexists=False, temporary=False):
        assert hasattr(container, "name")
        super().__init__(dialect, container)
        self.name = container.name
        self.ifnotexists = ifnotexists
        self.temporary = temporary

    def __getstate__(self):
        state = super().__getstate__()
        state.update(ifnotexists=self.ifnotexists, temporary=self.temporary)
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        if "name" not in state:
            self.name = self.container.name

    @nonscopable
    def subformat(self):
        ifnotexists = " IF NOT EXISTS" if self.ifnotexists else ""
        temporary = " TEMPORARY" if self.temporary else ""
        return f"CREATE{temporary} {self._kind}{ifnotexists} {self.name}"

    def set_ifnotexists(self, ifnotexists):
        if ifnotexists == self.ifnotexists:
            return self
        return self.build_from(self, ifnotexists=ifnotexists)

    def get_schema_containers(self):
        yield self.container


@dialect.register(True)
class CreateTableQuery(CreateQuery):
    _kind = "TABLE"

    @nonscopable
    def subformat(self):
        container = self.container
        if container.defquery:
            table_def = f"AS {container.defquery.subformat()}"
        else:
            table_def = [c.defformat() for c in container.external_columns]
            table_def.extend(cons.qformat() for cons in container.constraints)
            table_def = f"({', '.join(table_def)})"
        return f"{super().subformat()} {table_def}"

    def get_subargs(self):
        if self.container.defquery:
            return self.container.defquery.get_subargs()
        return super().get_subargs()

    def get_schema_containers(self):
        yield from super().get_schema_containers()
        if self.container.defquery:
            yield from self.container.defquery.get_schema_containers()


@dialect.register(True)
class CreateViewQuery(CreateQuery):
    _kind = "VIEW"

    def __init__(self, dialect, container, ifnotexists=False, temporary=False):
        assert hasattr(container, "subqueries") and len(container.subqueries) == 1
        super().__init__(
            dialect, container, ifnotexists=ifnotexists, temporary=temporary
        )

    @nonscopable
    def subformat(self):
        container = self.container
        columns = f"({', '.join(c.name for c in container.external_columns)})"
        vquery = container.subqueries[0].subformat(scoped=False)
        return f"{super().subformat()}{columns} AS {vquery}"

    def get_subargs(self):
        return self.container.subqueries[0].get_subargs()

    def get_schema_containers(self):
        yield from super().get_schema_containers()
        yield from self.container.subqueries[0].get_schema_containers()


@dialect.register(True)
class CreateIndexQuery(CreateQuery):
    _kind = "INDEX"

    def __init__(
        self,
        dialect,
        container,
        columns,
        name=None,
        condition=None,
        unique=False,
        ifnotexists=False,
    ):
        super().__init__(dialect, container, ifnotexists=ifnotexists, temporary=False)
        self.set_columns(columns)
        self.name = (
            name or f"_{container.name}_index_{'_'.join(c.name for c in self.columns)}"
        )
        self.unique = unique
        self.condition = condition or self.dialect.conditions.EmptyCondition()

    def set_columns(self, columns):
        columns = self.container.external_columns if columns is None else columns
        self.columns = tuple(map(self.container.__getitem__, columns))

    @nonscopable
    def subformat(self):
        unique = " UNIQUE" if self.unique else ""
        ifnotexists = " IF NOT EXISTS" if self.ifnotexists else ""
        columns = ", ".join(c.name for c in self.columns)
        condition = f" WHERE {self.condition.qformat()}" if self.condition else ""
        q = f"CREATE{unique} INDEX{ifnotexists} {self.name} ON {self.container.name}({columns}){condition}"
        return q

    def __getstate__(self):
        state = super().__getstate__()
        state.update(
            name=self.name,
            unique=self.unique,
            condition=self.condition,
            columns=self.columns,
        )
        state.pop("temporary", None)
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        self.temporary = False


@dialect.register(True)
class CreateTriggerQuery(CreateQuery, FromQueriesQuery):
    """
    A trigger is a collection of write queries to be executed when
    some event occurs. The events are of the kind:
    - "INSTEAD OF <action> ON <container>"
    - "AFTER <action> ON <container>"
    - "BEFORE <action> ON <container>"

    where '<action>' is one of "INSERT", "DELETE", "UPDATE", or
    "UPDATE OF <coma separated column list>", and <container> is
    a container object such as VIEWs or TABLEs.

    Parameters
    ----------
    when: str
            either `"INSTEAD OF"`, `"BEFORE"`, or `"AFTER"`;
    action: str | tuple of (str, columns)
            either `"INSERT"`, `"DELETE"`, `"UPDATE"`, or a pair of the
            form `("UPDATE", cols)` where `cols` is a list of container
            columns;
    container:
            a container (`SchemaView` or `SchemaTable`);
    subqueries:
            a tuple of queries to be executed when the event happen.

    """

    _kind = "TRIGGER"

    def __init__(
        self,
        dialect,
        container,
        when,
        action,
        *queries,
        name=None,
        ifnotexists=False,
        temporary=False,
    ):
        if not queries:
            raise NetworkDiskSQLError(
                f"{self.__class__.__name__} expects at least one query"
            )
        dialect.queries.CreateQuery.func.__init__(
            self, dialect, container, ifnotexists=ifnotexists, temporary=temporary
        )
        self.dialect.queries.FromQueriesQuery.func.__init__(self, dialect, *queries)
        self.when = when
        if isinstance(action, tuple):
            action = action[0].upper(), *action[1:]
        self.action = action
        self.name = (
            name
            or f"{when.lower().replace(' ', '_')}_{action.lower().replace(' ', '_')}_{container.name}"
        )

    def get_schema_containers(self):
        yield from self.dialect.queries.CreateQuery.get_schema_containers(self)
        yield from self.dialect.queries.FromQueryQuery.get_schema_containers(self)

    def __getstate__(self):
        state = self.dialect.queries.CreateQuery.func.__getstate__(self)
        state.update(self.dialect.queries.FromQueriesQuery.func.__getstate__(self))
        state["when"] = self.when.upper()
        state["action"] = self.action
        state["name"] = self.name
        return state

    @nonscopable
    def subformat(self):
        body = ";\n\t".join(sq.subformat() for sq in self.subqueries)
        when = self.when
        action = self.action
        if isinstance(action, tuple):
            action = f"{action[0]} OF {', '.join(c.qformat(context=self.internal_columns) for c in action[1])}"
        supersubformat = self.dialect.queries.CreateQuery.func.subformat(self)
        return f"{supersubformat} {when} {action} ON {self.container.name}\nBEGIN\n\t{body};\nEND"


# DROP
@dialect.register(True)
class DropTableQuery(AbstractQuery):
    _to_drop = "TABLE"

    def __init__(self, dialect, name, ifexists=False):
        super().__init__(dialect)
        self.name = name
        self.ifexists = ifexists

    @nonscopable
    def subformat(self):
        ifexists = "" if not self.ifexists else " IF EXISTS"
        return f"DROP {self._to_drop}{ifexists} {self.name}"

    def __getstate__(self):
        state = super().__getstate__()
        state.update(name=self.name, ifexists=self.ifexists)
        return state


@dialect.register(True)
class DropIndexQuery(DropTableQuery):
    _to_drop = "INDEX"


@dialect.register(True)
class DropViewQuery(DropTableQuery):
    _to_drop = "VIEW"


@dialect.register(True)
class DropTriggerQuery(DropTableQuery):
    _to_drop = "TRIGGER"


# TRANSACTION
@dialect.register(True)
class BeginTransactionQuery(AbstractQuery):
    def __init__(self, dialect, mode=None):
        super().__init__(dialect)
        self.mode = mode

    def __getstate__(self):
        state = super().__getstate__()
        state.update(mode=self.mode)
        return state

    @nonscopable
    def subformat(self):
        mode = f" {self.mode}" if self.mode else ""
        return f"BEGIN{mode} TRANSACTION"


@dialect.register(True)
class CommitTransactionQuery(AbstractQuery):
    @nonscopable
    def subformat(self):
        return "COMMIT TRANSACTION"


@dialect.register(True)
class RollbackTransactionQuery(AbstractQuery):
    def __init__(self, dialect, to_savepoint=None):
        super().__init__(dialect)
        self.to_savepoint = to_savepoint

    def __getstate__(self):
        state = super().__getstate__()
        state.update(to_savepoint=self.to_savepoint)
        return state

    @nonscopable
    def subformat(self):
        to_savepoint = f" TO SAVEPOINT {self.to_savepoint}" if self.to_savepoint else ""
        return f"ROLLBACK TRANSACTION{to_savepoint}"


@dialect.register(True)
class SavepointQuery(AbstractQuery):
    def __init__(self, dialect, name):
        super().__init__(dialect)
        self.name = name

    def __getstate__(self):
        state = super().__getstate__()
        state.update(name=self.name)
        return state

    @nonscopable
    def subformat(self):
        return f"SAVEPOINT {self.name}"


@dialect.register(True)
class ReleaseSavepointQuery(SavepointQuery):
    @nonscopable
    def subformat(self):
        return f"RELEASE SAVEPOINT {self.name}"


# SHORTHAND'S
LeftJoinQuery = functools.partial(JoinQuery.join, kind="LEFT")
RightJoinQuery = functools.partial(JoinQuery.join, kind="RIGHT")
InnerJoinQuery = functools.partial(JoinQuery.join, kind="INNER")
FullJoinQuery = functools.partial(JoinQuery.join, kind="FULL")
dialect.register(
    True,
    LeftJoinQuery=LeftJoinQuery,
    RightJoinQuery=RightJoinQuery,
    InnerJoinQuery=InnerJoinQuery,
    FullJoinQuery=FullJoinQuery,
)
