import itertools
from collections.abc import Mapping
from networkdisk.utils import BinRel, Scope, notProvidedArg
from networkdisk.exception import NetworkDiskSQLError


# QUERY OBJECTS
class ScopeValueColumns(Scope):
    def __init__(self, incolumns=(), encoders=()):
        """
        +	incolumns
                iterable of value columns
        +	encoders
                a dict specification, mapping columns from `incolumns`
                to encoder keys.
        """
        super().__init__(incolumns)
        self.encoders = dict(encoders)

    def __hash__(self):
        if not hasattr(self, "_hash"):
            self._hash = hash((self.byindex, tuple(sorted(self.encoders.items()))))
        return self._hash

    def __getstate__(self):
        d = super().__getstate__()
        d.update(encoders=self.encoders)
        return d


class InternalColumns(Scope):
    def __init__(self, *inqueries):
        columns = []  # map an index to a internal column
        origin_query = {}  # map a internal column to its origin query, if any
        origin_columns = {}  # map a internal column to the set of its origin ascendant, including itself
        for q in inqueries:
            if hasattr(q, "default_joinkind"):
                # q is considered as a JoinQuery
                # originate = lambda col: q.internal_columns.origin_query[q.external_columns.sources[col]]
                originate = lambda col: q.internal_columns.origin_query[col]
            else:
                originate = lambda col: q
            for col in q.external_columns:
                columns.append(col)
                oq = originate(col)
                origin_query[col] = oq
                origin_columns[col] = oc = {col}
                ocol = oq.external_columns.sources.get(col, False)
                if hasattr(oq, "internal_columns"):
                    oc.update(oq.internal_columns.origin_columns.get(ocol, ()))
        super().__init__(columns)
        self.origin_query = origin_query
        self.origin_columns = origin_columns

    def __getstate__(self):
        d = super().__getstate__()
        d.update(origin_query=self.origin_query, origin_columns=self.origin_columns)

    def __hash__(self):
        if not hasattr(self, "_hash"):
            horig_q = tuple(sorted(self.origin_query.items(), key=hash))
            horig_c = tuple(
                sorted(
                    map(
                        lambda t: (t[0], tuple(sorted(t[1], key=hash))),
                        self.origin_columns.items(),
                    ),
                    key=hash,
                )
            )
            self._hash = hash((self.byindex, horig_q, horig_c))
        return self._hash


class ExternalColumns(Scope):
    """
    A `Scope` of external columns with possibly a mapping from (external)
    columns to source (internal) columns, and a binary relation
    between `ValueColumn`s (left) and external columns (right).
    """

    def __init__(self, incolumns=(), sources=(), track_values=()):
        """
        +	incolumns:
                iterable of (external) columns;
        +	sources:
                partial mapping from (external) `incolumns` to (internal) columns;
        +	track_values:
                mapping from value columns to `incolumns`.
        """
        # TODO(?): set external columns/sources/track_values from column and context
        # optional arguments: aliases, values (no values, only values, mixed)
        super().__init__(incolumns)
        sources = dict(sources)
        assert all(c in self.byindex for c in sources)
        track_values = BinRel(track_values)  # relation value columns ↔ incolumns
        assert all(c in self.byindex for c in track_values.right)
        for col in self:
            if hasattr(col, "value"):
                track_values.add((col, col))
        self.sources = sources
        self.track_values = track_values

    def __getstate__(self):
        d = super().__getstate__()
        d.update(sources=self.sources, track_values=self.track_values)
        return d

    def __hash__(self):
        hsrc = tuple(sorted(self.sources, key=hash))
        htrack = tuple(sorted(self.track_values, key=hash))
        return hash((self.byindex, hsrc, htrack))

    def __add__(self, other):
        columns = itertools.chain(self, other)
        sources = dict(self.sources)
        sources.update(other.sources)
        track_values = self.track_values.union(other.track_values)
        return self.__class__(columns, sources=sources, track_values=track_values)

    def get_external_column_from_origin(self, ocol, context=None):
        found_one = None
        for fcol in self:
            bcol = self.sources.get(fcol, None)
            if not bcol:
                continue
            if context is None:
                ocols = (bcol,)
            else:
                ocols = context.origin_columns[bcol]
            if ocol in ocols:
                if found_one:
                    raise NetworkDiskSQLError(
                        f"Ambiguity: {fcol} and {found_one} both have {bcol} as origin column"
                    )
                found_one = fcol
        if not found_one:
            raise NetworkDiskSQLError(
                f"No external column with {bcol} as origin column found"
            )
        return found_one

    def get_external_column_from_source(self, bcol, default=notProvidedArg):
        found_one = None
        for fcol in self:
            if self.sources.get(fcol, None) == bcol:
                if found_one is not None:
                    raise ValueError(
                        f"Ambiguity: {fcol} and {found_one} both have source {bcol}"
                    )
                found_one = fcol
        if found_one is None:
            if default is notProvidedArg:
                raise ValueError(f"No external column whose source is {bcol} found")
            found_one = default
        return found_one


class ExposedFreeColumns(Scope):
    def __init__(self, columns):
        super().__init__(columns)


class ScopeQueries(Scope):
    """
    An alias for `Scope`, aimed to store `Query`s and, in
    particular, `SchemaContainer`s.
    """
