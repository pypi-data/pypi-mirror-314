import itertools, functools
from networkdisk.utils import notProvidedArg, Attributes, DataClass
import networkdisk.tupledict as ndtd
import networkdisk.utils as ndutls
from networkdisk.sql.scope import (
    ExternalColumns,
    InternalColumns,
    ScopeQueries,
    ExposedFreeColumns,
)
from networkdisk.exception import NetworkDiskSQLError
from .dialect import sqldialect as dialect

TDColumn = ndutls.namedtuple(
    "TDColumn",
    ("column", "subquery_index", "conditions", "alias"),
    defaults=((), None),
    module=__name__,
)
TDSubquery = ndutls.namedtuple(
    "TDSubquery", ("subquery", "start", "stop", "write_subquery"), module=__name__
)

subdialect = dialect.provide_submodule(__name__)


@subdialect.register(True)
class ReadOnlyTupleDictSchema(dialect.queries.JoinQuery.func):
    """
    Class attributes:
    +	sql, default_joinkind
            c.f. JoinQuery

    Instance attributes:
    +	subqueries, joins, internal_columns, external_columns
            c.f. JoinQuery
    +	_columns
            a total map (tuple) from column index to column properties
            gathered in a named tuple. The properties are:
            0.	the column
            1.	the column name if any, `None` otherwise
            2.	the column subquery index
    +	_subqueries
            a total map (tuple) from subquery index to subquery
            properties gathered in a name tuple. The properties are:
            0.	the subquery
            1.	the subquery name if any, `None` otherwise
            2.	the start column index for the subquery
            3.	the stop column index for the subquery

    The sub-mapping associating column indices with their subquery
    index (dropping columns not originating from a subquery)
    should be weakly increasing.
    """

    def __init__(
        self,
        dialect,
        *subqueries,
        columns=None,
        joinpairs=(),
        joinconds=(),
        joinkinds=(),
        rekey=ndtd.rekey_functions.Identity(),
        from_column_conditions=(),
        column_conditions=(),
        aliases=(),
    ):
        """
        +	subqueries:
                a tuple of subqueries
        +	columns:
                an iterable of internal column specifications
        +	joinon:
                a dict-spec mapping subquery indices to its join
                condition specification, for joining with the preceding
                subquery
        +	joinconds:
                #TODO
        +	from_column_conditions:
                specification of map from column index to tuple of condition
        +	column_conditions:
                specification of map from column index to condition
        +	aliases:
                a dict-spec mapping column-specification to alias.
        """
        super().__init__(
            dialect,
            *subqueries,
            joinpairs=joinpairs,
            joinconds=joinconds,
            joinkinds=joinkinds,
        )
        from_column_conditions = dict(from_column_conditions)
        column_conditions = dict(column_conditions)
        aliases = dict(aliases)
        subqueries = self.subqueries
        Error = NetworkDiskSQLError
        emptycond = dialect.conditions.EmptyCondition()
        if columns is None:
            columns = self.external_columns
        cols = []  # map from external column indices to TDColumn named tuple
        subqs = []  # map from subquery indices to TDSubquery named tuple
        seensqs = {}  # map from subqueries to subquery indices
        isq, start, stop = 0, 0, 0
        prev = None
        sq = subqueries[isq]

        def aux_add_subquery():
            if sq in seensqs:
                raise Error(
                    f"Ill-formed tupleDict: repeated subquery {sq} (at index {isq} and {seensqs[sq]})"
                )
            seensqs[sq] = isq
            target = (
                sq.subqueries[0]
                if isinstance(sq, dialect.queries.NamedQuery.func)
                and len(sq.subqueries) == 1
                else sq
            )
            subqs.append(TDSubquery(sq, start, stop, target))

        for icol, c in enumerate(columns):
            while isq < len(subqueries):
                sq = subqueries[isq]
                col = sq.external_columns.get(c)
                if not col:
                    aux_add_subquery()
                    isq, start, stop = isq + 1, icol, icol
                    continue
                elif len(col) > 1:
                    raise Error(f"Ambiguous column specification {c} in subquery {sq}")
                elif isq < len(subqueries) - 1:
                    nsq = subqueries[isq + 1]
                    if nsq.external_columns.get(c):
                        if any(sqc is c for sqc in sq.external_columns):
                            if any(nsqc is c for nsqc in nsq.external_columns):
                                raise Error(
                                    f"Ambiguous column specification {c} found in successive subqueries {sq} and {nsq}"
                                )
                        elif any(nsqc is c for nsqc in nsq.external_columns):
                            aux_add_subquery()
                            isq, start, stop = isq + 1, icol, icol
                            sq = subqueries[isq]
                            col = sq.external_columns.get(c)
                        else:
                            raise Error(
                                f"Ambiguous column specification {c} found in successive subqueries {sq} and {nsq}"
                            )
                col = col[0]
                break
            else:
                # column not found: verbosely raise in any case
                if prev:
                    for psq in subqueries:
                        if psq.external_columns.get(c):
                            raise Error(
                                f"Wrong column order: {prev[0]} from subquery {prev[1]} occurred before {c} from previous subquery {psq}"
                            )
                        if psq is sq:
                            break
                raise Error(f"Wrong column specification: {c} column not found")
            stop += 1
            prevconditions = cols[-1].conditions if cols else ()
            newconditions = from_column_conditions.get(icol, ())
            if icol in column_conditions:
                if len(newconditions) > isq:
                    newconditions = (
                        newconditions[:isq]
                        + (newconditions[isq] & column_conditions[icol],)
                        + newconditions[ids + 1 :]
                    )
                else:
                    newconditions = (
                        newconditions
                        + (emptycond,) * (isq - len(newconditions) - 1)
                        + (column_conditions[icol],)
                    )
            if len(prevconditions) == 1 and len(newconditions) > 1:
                prevconditions = (emptycond, *prevconditions)
            conditions = tuple(
                emptycond & pc & nc
                for (pc, nc) in itertools.zip_longest(prevconditions, newconditions)
            )
            cols.append(TDColumn(col, isq, conditions, aliases.get(icol)))
            prev = c, sq
            prevconditions = conditions
        else:
            aux_add_subquery()
        self.rekey = rekey
        self._columns = tuple(cols)
        self._subqueries = tuple(subqs)
        self._subquery_indices = seensqs

    @property
    def exposed_external_columns(self):
        if not hasattr(self, "_exposed_external_columns"):
            self._exposed_external_columns = ExternalColumns(
                map(lambda ic: ic[0], self._columns)
            )
        return self._exposed_external_columns

    def __iter__(self):
        return iter(self.exposed_external_columns)

    def __getitem__(self, k):
        if isinstance(k, slice):
            return self.exposed_external_columns[k]
        return self.exposed_external_columns.unambiguous_get(k)

    def __len__(self):
        return len(self.exposed_external_columns)

    @property
    def height(self):
        return len(self) - 1

    def is_readonly(self):
        return True

    def to_readonly(self):
        return self

    # Mapping methods
    def __repr__(self):
        return f"{self.__class__.__name__}<{', '.join(c.qformat(context=self.internal_columns, force=True) for c in self)}>"

    # Set/Get State
    def __getstate__(self):
        state = super().__getstate__()
        state.update(
            _columns=self._columns, _subqueries=self._subqueries, rekey=self.rekey
        )
        return state

    def __setstate__(self, state):
        for k, v in state.items():
            if k == "dialect":
                v = dialect._dialects[v]
            setattr(self, k, v)
        self.set_external_columns()
        self._subquery_indices = {
            sq.subquery: isq for isq, sq in enumerate(self._subqueries)
        }

    @classmethod
    def build_from(cls, *instances, **kwargs):
        if "_subqueries" in kwargs and "subqueries" not in kwargs:
            kwargs["subqueries"] = tuple(sq.subquery for sq in kwargs["_subqueries"])
        return super().build_from(*instances, **kwargs)

    @functools.lru_cache(maxsize=None)
    def row_prefix_condition(self, row_prefix, start=0, stop=None):
        conds = tuple(
            self.dialect.conditions.CompareCondition(self[i], x)
            for i, x in enumerate(row_prefix[start:stop], start=start)
        )
        if conds:
            return self.dialect.conditions.ConjunctionCondition(*conds)
        return self.dialect.conditions.EmptyCondition()

    @functools.lru_cache(maxsize=None)
    def get_index_of_condition(self, condition):
        rightmostcondsbq = -1
        rightmostcondcol = -1
        if condition is None:
            return rightmostcondsbq, rightmostcondcol
        for col in condition.columns:
            allcols = getattr(col, "get_columns", lambda: (col,))()
            for c in allcols:
                c = self.internal_columns.unambiguous_get(c, None)
                if not c:
                    continue
                if c in self:
                    rightmostcondcol = max(
                        rightmostcondcol, self.exposed_external_columns.index(c)
                    )
                sbq = self.internal_columns.origin_query[c]
                sbq_idx = self._subquery_indices[sbq]
                rightmostcondsbq = max(rightmostcondsbq, sbq_idx)
        return (rightmostcondsbq, rightmostcondcol)

    @functools.lru_cache(maxsize=None)
    def select_row_query(
        self,
        cols=None,
        condition=None,
        notnull=False,
        count=False,
        agg=None,
        distinct=False,
        ordered=False,
        **kwargs,
    ):
        """
        +	cols:
                an iterable of column specifications which are resolved.
                They are instances of (a subclass of) `AbstractColumn`, or
                a tupleDict column index (`int`). Notice that some
                `AbstractColumn` objects that do not belong to the
                tupleDict (e.g., `ValueColumns`, `TransformColumn`) might
                be passed. If empty, then the constant `1` is selected. If
                `None` (default), then all exposed external columns are
                selected.
        +	condition:
                a `Condition` or `None` (default).
        +	notnull:
                either Boolean which indicates that only non NULL values
                should be returned if `True`, or not if `False` (default),
                or an integer that specifies a rightmost column index
                that could not be NULL. If not `False`, two consequences
                hold: (1) a `NotNullCondition` on the specified column
                (or the rightmost (i.e., highest-indexed) selected column
                if `True`) of the tupleDict is "added" (conjunction) to
                `condition` and (2) the SQL "INNER JOIN" is preferred to
                the default "LEFT JOIN" when joining the various tables
                forming the tupleDict.
        +	kwargs:
                any keyworded parameters to be passed to the `SelectQuery`
                built by the method (e.g., `limit=3`).
        """
        # Parse columns ⇒ create one list `selcols` of `AbstractColumns`; find the rightmost selected column of the tupleDict
        emptycond = self.dialect.conditions.EmptyCondition()
        condition = emptycond & condition
        selcols = []
        rightmostselsbq = -1
        rightmostselcol = -1
        if cols is None:
            cols = () if count else self
        elif not hasattr(cols, "__iter__"):
            cols = (cols,)
        for col in cols:
            allcols = getattr(col, "get_subcolumns", lambda: (col,))()
            for c in allcols:
                fcol = self.exposed_external_columns.unambiguous_get(
                    c, None
                )  # returns None if not found, raises if ambiguous
                if fcol:  # c is a external column specification
                    col_idx = self.exposed_external_columns.index(fcol)
                    rightmostselcol = max(rightmostselcol, col_idx)
                    sbq_idx = self._columns[col_idx].subquery_index
                    rightmostselsbq = max(rightmostselsbq, sbq_idx)
                else:  # c is not a external column specification
                    fcol = self.external_columns.unambiguous_get(c, None)
                    if fcol:
                        bcol = self.external_columns.sources.get(fcol, None)
                    else:
                        bcol = self.internal_columns.unambiguous_get(c, None)
                    if not bcol:
                        continue
                    # c is a internal column specification
                    sbq = self.internal_columns.origin_query[
                        bcol
                    ]  # all internal columns have an origin query
                    sbq_idx = self._subquery_indices[sbq]
                    rightmostselsbq = max(rightmostselsbq, sbq_idx)
            col = self.exposed_external_columns.unambiguous_get(col, col)
            # returns col if not found, raises if ambiguous
            selcols.append(
                col
            )  # col is either a external column, or an external column specification to be resolved later by SelectQuery
        if not selcols:
            selcols = (self.dialect.columns.ValueColumn(1),)
        if count:
            selcols = (self.dialect.columns.CountColumn(*selcols, distinct=distinct),)
            distinct = False
        elif agg:
            selcols = self.dialect.columns.TransformColumn(
                agg, *selcols, distinct=distinct
            )
            distinct = False
        # Find tupleDict subqueries not involved in selection but involved in condition
        rightmostcondsbq, rightmostcondcol = self.get_index_of_condition(condition)
        rightmostcol = max(rightmostselcol, rightmostcondcol)
        colconds = self._columns[rightmostcol].conditions
        colcondsbq = len(colconds) - 1
        # Handle ordered parameter
        if ordered:
            kwargs.setdefault("orderby", selcols)
            if ordered == "desc":
                kwargs.setdefault("desc", True)
            elif ordered == "asc":
                kwargs.setdefault("desc", False)
        # Join involved subqueries
        # We might want some helper in JoinQuery for setting kinds, conds, pairs, and subqueries…
        up_to = max(rightmostselsbq, rightmostcondsbq, colcondsbq) + 1
        # Handle notnull parameter
        if isinstance(notnull, bool):
            if notnull and rightmostselcol > 0:
                condition = self[rightmostselcol].isnotnull() & condition
                notnull = rightmostselsbq
            else:
                notnull = 0
            notnull = max(colcondsbq, notnull)
            possiblynull = rightmostselsbq - notnull
            finalinner = up_to - rightmostselsbq
        else:
            up_to = max(up_to, notnull)
            condition = self[notnull].isnotnull() & condition
            notnull = self._columns[notnull].subquery_index
            possiblynull = up_to - notnull
            finalinner = 0
        subqueries = self.subqueries[:up_to]

        joinpairs = list(map(lambda j: list(j.pairs), self.joins[1:up_to]))
        joinconds = list(map(lambda j: j.other_condition, self.joins[1:up_to]))
        if up_to > 1:
            joinconds = list(
                emptycond & cj & cc
                for cj, cc in itertools.zip_longest(joinconds, colconds[1:up_to])
            )
        if colconds:
            condition &= colconds[0]
        joinkinds = (
            ("INNER",) * notnull + ("LEFT",) * possiblynull + ("INNER",) * finalinner
        )
        if up_to > 1:
            subqueries = (
                self.dialect.queries.JoinQuery(
                    *subqueries,
                    joinpairs=joinpairs,
                    joinconds=joinconds,
                    joinkinds=joinkinds,
                ),
            )
        # Selection
        query = self.dialect.queries.SelectQuery(
            *subqueries,
            columns=selcols,
            condition=condition,
            distinct=distinct,
            **kwargs,
        )
        return query

    # @functools.lru_cache(maxsize=None)
    def drop_columns(self, *columns):
        """
        Build a tupleDict obtained from `self` by forgetting the
        exposed external columns specified in `columns`. The result
        might be a invalid tupleDict. In order for the result to be
        valid, it is sufficient that no two rows differs only on a
        dropped column, and that the rightmost column is kept.
        However, it is possible in certain cases to drop the
        rightmost column, e.g., when no two rows differ only on
        the two rightmost columns.

        Use case: the `left_projection_tupledict` method uses the
        present method, dropping one single column, after having
        filtered the rows in such a way that they all have a fixed
        value or none on the corresponding column.

        +	columns
                tuple of external column specifications to drop.
        """
        # resolve columns
        columns = list(map(self.exposed_external_columns.index, columns))

        # initialize state structures
        _columns = self._columns
        _subqueries = list(self._subqueries)

        # drop columns
        for i in reversed(sorted(columns)):
            sqidx = _columns[i].subquery_index
            _columns = _columns[:i] + _columns[i + 1 :]
            for j, sq in enumerate(_subqueries[sqidx:]):
                _subqueries[sqidx + j] = TDSubquery(
                    sq.subquery, sq.start - int(bool(j)), sq.stop - 1, sq.write_subquery
                )

        return self.build_from(self, _columns=_columns, _subqueries=tuple(_subqueries))

    def strip(self):
        """
        Pop off subqueries not contributing to exposed columns, but
        the first one.  These subqueries correspond to a maximal
        suffix of enriched subqueries of `self._subqueries` tuple,
        for which the `stop` and `start` attributes are both equal
        to `len(self)`.
        """
        _subqueries = self._subqueries
        for i, sq in enumerate(reversed(_subqueries)):
            if sq.start < len(self):
                break
        if i:
            return self.build_from(self, _subqueries=_subqueries[:-i])
        return self

    @functools.lru_cache(maxsize=None)
    def left_projection_tupledict(self, *args, keep_column=False, **kwargs):
        """
        Splits the tupleDict on column `c`, and realizes a LEFT JOIN
        with left and right resulting parts, with condition that the
        column `c` has value `v` in the ON clause. The resulting
        tupleDict has one external column less and possibly one more
        or one less subquery. The column `c` cannot be the first nor
        the last tupleDict column. Both `c` and `v` are specified by
        the arguments, as follows.

        +	args:
                if provided, should consist in two positional arguments,
                respectively `c` and `v`, and `kwargs` should be empty.
        +	kwargs:
                if provided, should consist in a single key/value (`c`/`v`)
                association and `args` should be empty.

        In such a configuration:
        +	c
                a tupleDict column specification, but the first and the
                last.
        +	v
                a value or column, as expected by the `eq` methods of
                columns, which returns an equality condition.

        The optional Boolean parameter `keep_column` allows to
        control whether the projected column should be kept in the
        resulting tupleDict (as a constant column) or not.  Default
        is to drop it (`False`).
        """
        if args:
            kwargs.update((args,))
        if len(kwargs) != 1:
            raise ValueError(f"One argument expected, got {len(kwargs)}")
        column, value = kwargs.popitem()
        column = self.exposed_external_columns.unambiguous_get(column)
        icol = self.exposed_external_columns.index(column)
        if icol == len(self) - 1 or icol == 0:
            raise ValueError(
                "Left projection is not possible on the first nor the last tupleDict column"
            )
        col = self._columns[icol]
        isq = col.subquery_index
        sq = self._subqueries[isq]
        if icol == sq.start:
            oncond = column.eq(value)
            tds = self.add_join_conditions({isq: oncond})
            if not keep_column:
                tds = tds.drop_columns(icol)
            return tds
        # SPLIT subqueries INTO *subqueries[:isq], sq.LEFT, sq.RIGHT, *subqueries[isq+1:] where LEFT, RIGHT is a split of sq
        # BEFORE					LEFT		RIGHT						AFTER
        # possibly, RIGHT is dropped (when it contributes with no external columns, c.f., `noright` below)
        # join specs are altered in LEFT, RIGHT, and subqueries[isq+1] (if any)

        sqname = getattr(sq.subquery, "name", "")
        noright = (
            not keep_column and icol > sq.stop
        )  # True if RIGHT should be dropped #TODO: is it possible that icol>sq.stop?

        # BEFORE
        _subqueries = self._subqueries[:isq]
        _columns = self._columns[: sq.start]
        subqueries = self.subqueries[:isq]
        joins = self.joins[:isq]

        # LEFT
        left = sq.subquery
        left_target = left
        ljspec = self.joins[isq]
        lcols = self._columns[sq.start : icol]
        if not noright:
            left = self.dialect.queries.NamedQuery(left, f"{sqname}_left")
            if isq:
                ljpairs = [(l, left.recolumn(r)) for l, r in ljspec.pairs]
                ljcond = left.recondition(ljspec.other_condition)
                ljspec = self.get_join_spec(
                    self.dialect,
                    self.subqueries[isq - 1],
                    left,
                    jpairs=ljpairs,
                    jcond=ljcond,
                )
            lcols = tuple(
                TDColumn(
                    left.recolumn(c.column),
                    isq,
                    tuple(map(left.recondition, c.conditions)),
                    c.alias,
                )
                for c in lcols
            )
        _subqueries += (TDSubquery(left, sq.start, icol, left_target),)
        _columns += lcols
        subqueries += (left,)
        joins += (ljspec,)

        # RIGHT (if needed)
        right_target = right
        if not noright:
            right = self.dialect.queries.NamedQuery(sq.subquery, f"{sqname}_right")
            rjpairs = [i for i in range(icol - sq.start)]
            rcol = right.recolumn(col.column)
            rjcond = rcol.eq(value)
            rjspec = self.get_join_spec(
                self.dialect, left, right, jpairs=rjpairs, jcond=rjcond
            )
            if keep_column:
                _subqueries += (TDSubquery(right, icol, sq.stop, right_target),)
                _columns += (
                    TDColumn(
                        rcol,
                        isq + 1,
                        tuple(map(right.recondition, col.conditions)),
                        col.alias,
                    ),
                )
            else:
                _subqueries += (TDSubquery(right, icol, sq.stop - 1, right_target),)
            _columns += tuple(
                TDColumn(
                    right.recolumn(c.column),
                    isq + 1,
                    tuple(map(right.recondition, c.conditions)),
                    c.alias,
                )
                for c in self._columns[icol + col_shift : sq.stop]
            )
            subqueries += (right,)
            joins += (rjspec,)
            left = right

        # AFTER
        if isq + 1 < len(self.subqueries):
            right = self.subqueries[isq + 1]
            jspec = self.joins[isq + 1]
            jcond = left.recondition(jspec.other_condition)
            jpairs = jspec.pairs
            if noright:
                jcond &= col.column.eq(value)
            else:
                jpairs = [(left.recolumn(l), r) for l, r in jpairs]
            jspec = self.get_join_spec(
                self.dialect, left, right, jpairs=jpairs, jcond=jcond
            )
            joins += (jspec,)

            _subqueries += tuple(
                TDSubquery(
                    rsq.subquery, rsq.start - 1, rsq.stop - 1, rsq.write_subquery
                )
                for rsq in self._subqueries[isq + 1 :]
            )
            if noright:
                _columns += self._columns[sq.stop :]
            else:
                _columns += tuple(
                    TDColumn(c.column, c.subquery_index + 1, c.conditions, c.alias)
                    for c in self._columns[sq.stop :]
                )
            subqueries += self.subqueries[isq + 1 :]
            joins += self.joins[isq + 2 :]

        return self.build_from(
            self,
            subqueries=subqueries,
            joins=joins,
            _subqueries=_subqueries,
            _columns=_columns,
        )

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def overlap(dialect, left, right, up_to=1):
        """
        Combine two tupleDicts `left` and `right` to create a new
        one, by joining the `up_to` leftmost columns of `left` with
        the columns of `right` but the `up_to` leftmost ones.  The
        join is made on equality of the tupleDict row prefixes up to
        `up_to`.
        +	left
                a tupleDict of height at least `up_to`
        +	right
                a tupleDict of height at least `up_to`
        +	up_to
                a coordinate index, being at least 1, and at most <TODO: right.height-1??>.
        """

        if left.is_readonly() or right.is_readonly():
            left = left.to_readonly()
            right = right.to_readonly()
        cls = type(left)
        emptycond = dialect.conditions.EmptyCondition()

        # outline (intuition)
        # columns = left[:up_to] + right[up_to:]
        # subqueries = left.subqueries[lisq:] + right.subqueries

        # Build tupleDict subqueries and columns
        subqueries = []
        columns = []

        # about left
        lisq = left._columns[up_to - 1].subquery_index
        lsq = left._subqueries[lisq]

        # FROM LEFT
        _subqueries = left._subqueries[:lisq]
        _subqueries += (
            TDSubquery(
                lsq.subquery, lsq.start, min(up_to, lsq.stop), lsq.write_subquery
            ),
        )
        _columns = left._columns[:up_to]
        joins = left.joins[: lisq + 1]

        lcolconds = _columns[-1].conditions
        lcolconds_padded = lcolconds + (emptycond,) * (
            len(_subqueries) - len(lcolconds)
        )

        # FROM RIGHT
        sqnames = [sq.subquery.name for sq in _subqueries]
        renamed_sqs = []

        for i, sq in enumerate(right._subqueries):
            sqsq = sq.subquery
            sqsq_target = sqsq
            if not hasattr(sqsq, "name") or sqsq.name in sqnames:
                sqsq = sqsq.name_query(f"{getattr(sqsq, 'name', '')}_repeated4overlap")
                renamed_sqs.append(sqsq)

            overlap_jpairs = []
            overlap_jcond = dialect.conditions.EmptyCondition()
            for j in range(sq.start, sq.stop):
                rcol = right._columns[j]
                rcolcol = rcol.column
                rcolconds = rcol.conditions
                rcolalias = rcol.alias
                if renamed_sqs and renamed_sqs[-1] is sqsq:
                    rcolconds = tuple(map(sqsq.recondition, rcolconds))
                    rcolcol = sqsq.recolumn(rcolcol)
                if j >= up_to:
                    if rcolconds:
                        rcolconds = lcolconds_padded + rcolconds
                    else:
                        rcolconds = lcolconds
                    _columns += (
                        TDColumn(rcolcol, len(_subqueries), rcolconds, rcolalias),
                    )
                else:
                    lcol = left._columns[j]
                    lsq = left.subqueries[lcol.subquery_index]
                    lcol = lcol.column
                    if not i and lsq is _subqueries[-1].subquery:
                        overlap_jpairs.append((lcol, rcolcol))
                    else:
                        overlap_jcond &= lcol.eq(rcolcol)

            jspec = right.joins[i]
            jspec_changed = False
            jpairs = jspec.pairs
            jcond = jspec.other_condition
            for rnsq in renamed_sqs:
                njpairs = [(rnsq.recolumn(l), rnsq.recolumn(r)) for (l, r) in jpairs]
                njcond = rnsq.recondition(jcond)
                if njpairs != jpairs or njcond != jcond:
                    jspec_changed = True
                    jpairs, jcond = njpairs, njcond
            if overlap_jpairs or overlap_jcond:
                jspec_changed = True
                jpairs = list(jpairs) + overlap_jpairs
                jcond &= overlap_jcond
            if jspec_changed:
                jspec = cls.get_join_spec(
                    dialect, _subqueries[-1].subquery, sqsq, jpairs=jpairs, jcond=jcond
                )

            start = max(sq.start, up_to)
            stop = max(sq.stop, up_to)

            _subqueries += (TDSubquery(sqsq, start, stop, sqsq_target),)
            joins += (jspec,)

        kwargs = {}
        if not left.is_readonly():
            try:
                kwargs["_write_permutation"] = ndtd.Permutation(
                    tuple(left.write_permutation)[:up_to]
                    + tuple(right.write_permutation)[up_to:]
                )
            except ValueError:
                raise NotImplementedError(
                    f"Cannot overlap tupleDict {left} and {right} with write_permutation {left.write_permutation or right.write_permutation}. Consider to turn the tupleDict read-only first."
                )
            if left._write_target or right._write_target:
                kwargs["_write_target"] = cls.overlap(
                    dialect, left.write_target, right.write_target, up_to=up_to
                )

        return cls.build_from(
            left, _subqueries=_subqueries, _columns=_columns, joins=joins, **kwargs
        )

    def left_overlap(self, left, up_to=1):
        return self.overlap(self.dialect, left, self, up_to=up_to)

    def right_overlap(self, right, up_to=1):
        return self.overlap(self.dialect, self, right, up_to=up_to)

    @functools.lru_cache(maxsize=None)
    def swap(self, i, j):
        """
        Returns a tupleDict object obtained by swapping the exposed
        external columns `i` and `j`.  The two indices should be
        at most the tupleDict height `self.height`.  The following
        semantics holds: (x₀,…,xᵢ₋₁,xⱼ,xᵢ₊₁,…,xⱼ₋₁,xᵢ,xⱼ₊₁,…,xₕ) is
        a row in the resulting tupleDict, if and only if (x₀,…,xₕ)
        was a row in `self`, where h is `self.height`.  Moreover, in
        order to produce a valid tupleDict, it is necessary that
        over all the rows of `self`, `xᵢ is None` if and only if
        `xⱼ is None`.  This last condition is not checked.
        +	i
                an exposed external column index
        +	j
                an exposed external column index
        """
        i, j = sorted((i, j))

        lidx = self._columns[i].subquery_index
        lsq = self._subqueries[lidx]
        ridx = self._columns[j].subquery_index
        rsq = self._subqueries[ridx]
        # intuition:
        # subqueries:		self.subqueries[:lidx] +  self.subqueries[lidx:ridx+1]   + self.subqueries[ridx+1:]
        # columns:					self[:i]	   + self[j] + self[i+1:j] + self[i] +		self[j+1:]
        # outline:				  LEFT		 +			 MIDDLE			  +		  RIGHT

        # LEFT
        _subqueries = self._subqueries[:lidx]
        _columns = self._columns[: lsq.start]

        # MIDDLE
        _columns += self._columns[lsq.start : i] + (self._columns[j],)
        if lidx == ridx:
            _subqueries += (self._subqueries[lidx],)
            _columns += self._columns[i + 1 : j] + (self._columns[i],)
        else:
            _subqueries += (TDSubquery(lsq.subquery, lsq.start, i, lsq.write_subquery),)
            _subqueries += tuple(
                TDSubquery(sq.subquery, i, i, sq.write_subquery)
                for sq in self._subqueries[lidx + 1 : ridx]
            )
            _subqueries += (TDSubquery(rsq.subquery, i, rsq.stop, rsq.write_subquery),)
            _columns += tuple(
                TDColumn(c.column, ridx, c.conditions, c.alias)
                for c in self._columns[i + 1 : j]
            ) + (TDColumn(self._columns[i][0], ridx, *self._columns[i][2:]),)
        _columns += self._columns[j + 1 : rsq.stop]

        # RIGHT
        _columns += self._columns[j + 1 :]
        _subqueries += self._subqueries[ridx + 1 :]

        kwargs = {}
        if not self.is_readonly():
            kwargs["_write_target"] = self.write_target
            kwargs["_write_permutation"] = (
                ndtd.Permutation.swap(i, j) + self.write_permutation
            )

        return self.build_from(
            self, _subqueries=_subqueries, _columns=_columns, **kwargs
        )

    def insert_constant_column(self, value, index=0, alias=None):
        """
        Returns a new TupleDictSchema with columns "self._columns[:index]+(value,)+self._columns[index:]"
        +	index:
                the index where to insert the column. Should be less than `self.height`.
        +	value:
                the constant value to insert.
        +	alias:
                an optional alias for the column.
        """
        emptycond = self.dialect.conditions.EmptyCondition()

        _columns = self._columns
        _subqueries = self._subqueries
        joins = self.joins

        sqidx = _columns[index].subquery_index
        sq = _subqueries[sqidx]

        if hasattr(value, "qformat"):
            newcol = value
        else:
            newcol = self.dialect.columns.ValueColumn(value, name=alias)

        # BEFORE
        new_columns = _columns[:index]
        new_subqueries = tuple(sq for sq in _subqueries[: sqidx - int(bool(sqidx))])
        new_joins = joins[:sqidx]

        # OVER
        # TODO: what to do on `write_subquery`? Drop constant rekey function?
        if index > sq.start:
            oldsq = _subqueries[sqidx]
            sq = TDSubquery(
                oldsq.subquery, oldsq.start, oldsq.stop + 1, oldsq.write_subquery
            )
            afterisq = True
            addsubq = False
        elif sqidx:
            oldsq = _subqueries[sqidx - 1]
            sq = TDSubquery(
                oldsq.subquery, oldsq.start, oldsq.stop + 1, oldsq.write_subquery
            )
            afterisq = False
            addsubq = False
        elif _subqueries[sqidx].subquery.is_dummy():
            oldsq = _subqueries[sqidx]
            sq = TDSubquery(
                oldsq.subquery, oldsq.start, oldsq.stop + 1, oldsq.write_subquery
            )
            afterisq = True
            addsubq = False
        else:
            # we introduce a dummy new subquery, as first tupleDict subquery
            dsq = self.dialect.queries.DualQuery()
            sq = TDSubquery(dsq, 0, 1, dsq)
            new_joins += (joins[0],)
            afterisq = False
            addsubq = True
        new_columns += (TDColumn(newcol, len(new_subqueries), (), alias),)
        new_subqueries += (sq,)
        new_joins += (joins[sqidx],)

        # AFTER
        if addsubq:
            new_columns += tuple(
                TDColumn(c.column, c.subquery_index + 1, c.conditions, c.alias)
                for c in _columns[index:]
            )
        else:
            new_columns += _columns[index:]
        if afterisq:
            new_subqueries += tuple(
                TDSubquery(sq.subquery, sq.start + 1, sq.stop + 1, sq.write_subquery)
                for sq in _subqueries[sqidx + 1 :]
            )
        else:
            new_subqueries += tuple(
                TDSubquery(sq.subquery, sq.start + 1, sq.stop + 1, sq.write_subquery)
                for sq in _subqueries[sqidx:]
            )
        new_joins += joins[sqidx + 1 :]

        return self.build_from(
            self, _subqueries=new_subqueries, _columns=new_columns, joins=new_joins
        )

    @functools.lru_cache(maxsize=None)
    def truncate(self, up_to):
        """
        Drop all but the `up_to` first columns to likely form a new
        tupleDict. The result might be an invalid tupleDict.
        """
        new = super().truncate(up_to)
        state = new.__getstate__()
        _columns = tuple(c for c in state["_columns"] if c.subquery_index < up_to)
        _subqueries = state["_subqueries"][:up_to]
        return new.build_from(new, _columns=_columns, _subqueries=_subqueries)

    def union_all(self, *others, shared=None):
        """
        +	self, others
                tupleDicts of same arity
        +	shared
                either `None` (default) or a column index. If not `None`
                the `shared` leftmost column of each tupleDicts shall
                originate from the same subqueries, and union is performed
                on rightmost columns only.
        """
        # outline
        # (1) truncate `self` and `others` keeping the `shared` leftmost columns only
        # (2) insert constant column with distinct value in each of the above-truncated tupleDict
        # (3) takes union of all tupleDict (notice that, due to the inserted column, the result is a valid tupleDict)
        # (4) left overlap the resulting tupleDict with `self` up to `shared`
        raise NotImplementedError()

    def filter_from_column(self, col, cond, write_target=None):
        """
        +	col:
                a column specification.
        +	cond:
                either a specification of mapping, from subquery index to
                conditions, or a conditions.
        +	write_target:
                if None, toggle the new tupleDict to readonly, otherwise set its write_target to the provided one.
        """
        if not write_target:
            self = self.to_readonly()
        emptycond = self.dialect.conditions.EmptyCondition()
        if not cond:
            return self
        elif hasattr(cond, "qformat"):
            sq, _ = self.get_index_of_condition(cond)
            cond = tuple(emptycond for i in range(sq)) + (cond,)
        if not any(cond):
            return self
        col = self.exposed_external_columns.index(col)

        def f(colcond):
            colcond = tuple(
                emptycond & cc & nc for cc, nc in itertools.zip_longest(colcond, cond)
            )
            if len(colcond) > 1:
                colcond = (emptycond, colcond[0] & colcond[1], *colcond[2:])
            return colcond

        g = lambda _col: TDColumn(*_col[:2], f(_col.conditions), *_col[3:])
        _columns = self._columns[:col] + tuple(map(g, self._columns[col:]))
        return self.build_from(self, _columns=_columns, _write_target=write_target)

    def filter_column(self, col, condition):
        """
        Like `filter_from_condition` but assuming that condition can
        be expressed at the joining subquery level of the column
        specified by specification `col`.
        """
        col = self.exposed_external_columns.index(col)
        sbqidx = self._columns[col].subquery_index
        emptycond = self.dialect.conditions.EmptyCondition()
        cond = (emptycond,) * sbqidx + (condition,)
        return self.filter_from_column(col, cond)


@subdialect.register(True)
class ReadWriteTupleDictSchema(ReadOnlyTupleDictSchema):
    @functools.wraps(ReadOnlyTupleDictSchema.__init__)
    def __init__(
        self,
        *args,
        write_target=None,
        write_permutation=ndtd.Permutation.identity(),
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if write_target:
            self._write_target = write_target.write_target
            self._write_permutation = write_permutation + write_target.write_permutation
        else:
            self._write_target = None
            self._write_permutation = write_permutation

    @property
    def write_target(self):
        return self._write_target or self

    @property
    def write_permutation(self):
        return self._write_permutation

    def is_readonly(self):
        return False

    def __getstate__(self):
        state = super().__getstate__()
        state.update(
            _write_target=self._write_target, _write_permutation=self._write_permutation
        )
        return state

    def to_readonly(self):
        state = super().__getstate__()
        new = object.__new__(self.dialect.tupledict.ReadOnlyTupleDictSchema.func)
        new.__setstate__(state)
        return new

    def insert_infix_query(self, row_prefix, condition=None):
        """
        Inserts the maximal suffix of a row prefix in its corresponding
        rightmost subquery (expected to be a container).

        PARAMETERS
        ----------

        row_prefix: tuple or SelectQuery
                the nonempty row prefix from which to extract the suffix to insert.

        condition: condition
                additional condition or `None` (default).
        """
        # TODO: treat the case where row_prefix is a SELECT query.
        self = self.write_target
        query = None
        if type(row_prefix) is int:
            row_prefix = (self.dialect.constants.Placeholder,) * row_prefix
        elif hasattr(row_prefix, "qformat"):
            query = row_prefix
            row_prefix = (self.dialect.constants.Placeholder,) * len(query)
        elif self.write_permutation:
            row_prefix = self.write_permutation(row_prefix)
        condition = condition or self.dialect.conditions.EmptyCondition()
        col_idx = len(row_prefix) - 1
        col = self._columns[col_idx]
        sbq_idx = col.subquery_index
        sbq = self._subqueries[sbq_idx]
        start = sbq.start
        stop = len(row_prefix)
        columns = self[start:stop]
        if not sbq_idx and not condition:
            if query:
                return self.subqueries[0].insert_query(query, columns=columns)
            else:
                return self.subqueries[0].insert_values(row_prefix, columns=columns)
        joinpairs = self.joins[sbq_idx].pairs
        selcols = tuple(map(lambda e: e[0], joinpairs))
        columns = tuple(map(lambda e: e[1], joinpairs)) + columns
        if query:
            q = self.select_row_query(selcols + self[:start])
            if len(q.subqueries) > 1:
                q = q.name_query("td_prefix")
            else:
                q = q.subqueries[0]
            if not hasattr(query, "name"):
                query = query.name_query("td_insert")
            on = zip(query[:start], (q[c] for c in selcols + self[:start]))
            q = query.inner_join_query(q, *on)
            q = q.select_query(columns=selcols + q[start:stop])
        else:
            selcols += tuple(
                self.dialect.columns.ValueColumn(v, for_column=self[i])
                for i, v in enumerate(row_prefix[start:stop], start=start)
            )
            condition = self.row_prefix_condition(row_prefix, stop=start) & condition
            q = self.select_row_query(selcols, condition=condition)
        target = self._subqueries[sbq_idx].write_subquery
        return target.insert_query(q, columns=columns)

    def insert_row_script(self, row_prefix, condition=None, shift=0):
        self = self.write_target
        if type(row_prefix) is int:
            row_prefix = (self.dialect.constants.Placeholder,) * row_prefix
        if self.write_permutation:
            row_prefix = self.write_permutation(row_prefix)
        firstcont = self._columns[shift].subquery_index
        lastcont = self._columns[len(row_prefix) - 1].subquery_index
        return (
            self.insert_infix_query(
                row_prefix[: self._subqueries[i].stop], condition=condition
            )
            for i in range(firstcont, lastcont + 1)
        )

    @functools.lru_cache(maxsize=None)
    def delete_prefix_query(
        self, row_prefix, subquery_index=None, prefcondition=None, suffcondition=None
    ):
        """
        Deletes the rows infixes from `subquery_index`-indexed
        subquery (expected to be a container) that correspond to
        rows having `row_prefix` as prefix. If `subquery_index` is
        `None` (default), then the subquery storing the last
        coordinate of `row_prefix` (or the first subquery if empty)
        is taken.

        Arguments:
        +	row_prefix:
                the nonempty row prefix from which to extract the suffix
                to delete.
        +	subquery_index:
                either `None` (default) or a subquery index.
        +	prefcondition:
                additional condition on the subqueries preceding the
                subquery in which delete is performed or `None` (default).
        +	suffcondition:
                additional condition on the subquery in which delete is
                performed, or `None` (default).
        """
        self = self.write_target
        if type(row_prefix) is int:
            row_prefix = (self.dialect.constants.Placeholder,) * row_prefix
        if self.write_permutation:
            row_prefix = self.write_permutation(row_prefix)
        sbq_idx = subquery_index
        if sbq_idx is None:
            lastcol = max(0, len(row_prefix) - 1)
            col = self._columns[lastcol]
            sbq_idx = col.subquery_index
            cond = col.conditions
            sq = self._subqueries[sbq_idx]
        else:
            sq = self._subqueries[sbq_idx]
            col = self._columns[q.stop - 1]
            cond = col.conditions
        start = sq.start
        suffcondition = (
            self.row_prefix_condition(row_prefix, start=start) & suffcondition
        )
        for c in cond[sbq_idx:]:
            suffcondition &= c
        joinpairs = self.joins[sbq_idx].pairs
        if sbq_idx and joinpairs and all(joinpairs):
            l_joinids = tuple(map(lambda e: e[0], joinpairs))
            r_joinids = tuple(map(lambda e: e[1], joinpairs))
            if len(r_joinids) == 1:
                r_joinids = r_joinids[0]
            prefcondition = (
                self.row_prefix_condition(row_prefix, stop=start) & prefcondition
            )
            q = self.select_row_query(l_joinids, condition=prefcondition)
            suffcondition &= self.dialect.conditions.InQuerySetCondition(r_joinids, q)
        target = self._subqueries[sbq_idx].write_subquery
        return target.delete_query(condition=suffcondition)

    @functools.lru_cache(maxsize=None)
    def delete_row_script(
        self, row_prefix, shift=0, suffcondition=None, prefcondition=None
    ):
        """
        delete suffix `row_prefix[shift:]` of rows starting with
        `row_prefix`.
        """
        # TODO
        raise NotImplementedError("We should Implement that")


class BaseRowStore(ndtd.BaseAbstractRowStore, DataClass):
    __attributes__ = Attributes(
        "master", "tupleDictSchema", lazy=False, cascade=True, cache_level=0
    )

    @property
    def helper(self):
        return self.master.helper

    @property
    def height(self):
        return self.tupleDictSchema.height

    @property
    def key_coordinate_checkers(self):
        return tuple(ndutls.functions.hashable_checker for _ in range(self.height))

    # GET
    @functools.wraps(ndtd.ReadWriteAbstractRowStore.select.__call__)
    def iter_bunch(
        self,
        key_prefix=(),
        start=None,
        stop=None,
        count=None,
        ordered=False,
        condition=None,
        distinct=False,
        **kwargs,
    ):
        """
        This is the core method for select queries on the SQL
        TupleDict. It allows thin control on what is selected and
        what is returned, through its arguments:
        +	start/stop: allows to slice the tuplekeys to return
        +	count: count the number of returned results (cannot be used together with aggregate optional parameter)
        +	condition: add a condition to the where-clause
        + ordered: whether to order the result. Could be a Boolean or the special keywords 'desc' or 'asc'.
        +	kwargs: additional optional parameters to be passed to the `select_row_query` method of `TupleDictSchema`. They include:
                +	satisfying: an iterable of constraints (see, `ndsql.constraints`)
                +	aggregate: an SQL function to aggregate results
        """
        tds = self.tupleDictSchema
        if count and start is None and stop is None:
            cols = None
        else:
            start = len(key_prefix) if start is None else start
            start, stop, _ = slice(start, stop).indices(self.height + 1)
            cols = tds[start:stop]
        condition = tds.row_prefix_condition(key_prefix) & condition
        q = tds.select_row_query(
            cols=cols, condition=condition, count=count, distinct=distinct, **kwargs
        )
        return tds.dialect.helper.IterableQuery(self.helper, q)

    @functools.wraps(ndtd.ReadWriteAbstractRowStore.select.__call__)
    def select(self, *args, count=None, **kwargs):
        res = self.iter_bunch(*args, count=count, **kwargs)
        if count:
            return next(iter(res))[0]
        return res

    def to_readonly(self):
        return self

    def filter(self, condition, col=None):
        if col is None:
            _, col = self.tupleDictSchema.get_index_of_condition(condition)
        return self.to_readonly().build_from(
            self, tupleDictSchema=self.tupleDictSchema.filter_column(col, condition)
        )

    def left_projection(self, *args, keep_column=False, **kwargs):
        return self.to_readonly().build_from(
            self,
            tupleDictSchema=self.tupleDictSchema.left_projection_tupledict(
                *args, keep_column=keep_column, **kwargs
            ),
        )

    def filter_from_column(self, col, condition):
        return self.to_readonly().build_from(
            self,
            tupleDictSchema=self.tupleDictSchema.filter_from_column(col, condition),
        )


class ReadWriteRowStore(BaseRowStore, ndtd.ReadWriteAbstractRowStore):
    _RO = BaseRowStore

    @property
    def _ReadOnlyRowStore(self):
        return BaseRowStore

    @property
    def _contextmanager(self):
        return self.helper.transaction

    # INSERT
    def bulk_insert_onepass(self, bunch, shift=0):
        """
        Parameters
        ----------
        bunch: iterable
                an iterator of (unfolded, tuples) row prefixes.

        shift: int
                indicates that the `shift` first values of the tuples from bunch
                correspond to tuplekey prefix that already exist in the tupleDict.
        """
        tds = self.tupleDictSchema.write_target
        if tds.write_permutation:
            bunch = map(tds.write_permutation, bunch)
        cut_cont = tds._columns[shift].subquery_index
        start_tbl, stop_tbl = (
            tds._subqueries[cut_cont].start,
            tds._subqueries[cut_cont].stop,
        )
        bunch = itertools.groupby(bunch, key=len)
        with self._contextmanager:
            for elen, elen_bunch in bunch:
                if elen < start_tbl:
                    continue
                elen_tbl_index = tds._columns[elen - 1].subquery_index
                elen_tbl_start = tds._subqueries[elen_tbl_index].start
                if elen > stop_tbl:
                    # insertion in more than one container
                    def grouping(edgedef):
                        e_slices = [
                            edgedef[
                                slice(tds._subqueries[i].start, tds._subqueries[i].stop)
                            ]
                            for i in range(elen_tbl_index)
                        ]
                        return e_slices

                    elen_bunch = itertools.groupby(elen_bunch, key=grouping)
                    for kpref_by_slice, kpref_bunch in elen_bunch:
                        # 1. Insert tuplekey part from grouping
                        kpref = ()
                        preflen = 0
                        for tbl_idx, kinf in enumerate(kpref_by_slice):
                            if kinf:
                                kpref += kinf
                                preflen += len(kinf)
                                if tbl_idx < cut_cont:
                                    continue
                                q = tds.insert_infix_query(len(kpref))
                            else:
                                subq = tds._subqueries[tbl_idx].write_subquery
                                jpairs = tds.joins[tbl_idx].pairs
                                cols = tuple(p[0] for p in jpairs)
                                rpcond = tds.row_prefix_condition(kpref)
                                selq = tds.select_row_query(cols=cols, condition=rpcond)
                                cols = tuple(p[1] for p in jpairs)
                                q = subq.insert_query(selq, columns=cols)
                            column_map = tuple(c.name for c in tds[: len(kpref)])
                            self.helper.execute(
                                q, args=kpref, column_map=column_map, rekey=tds.rekey
                            )

                        # 2. Insert bunch suffixes of kpref from bunch
                        args = (tds.dialect.constants.Placeholder,) * (
                            elen + len(kpref) - elen_tbl_start
                        )
                        q = tds.insert_infix_query(args)
                        column_map = tuple(c.name for c in tds[:elen])
                        kpref_bunch = map(lambda e: e[elen_tbl_start:elen], kpref_bunch)
                        self.helper.executemany(
                            q,
                            I=kpref_bunch,
                            args=kpref,
                            column_map=column_map,
                            rekey=tds.rekey,
                        )
                else:
                    q = tds.insert_infix_query(elen)
                    column_map = tuple(c.name for c in tds[:elen])
                    self.helper.executemany(
                        q, I=elen_bunch, column_map=column_map, rekey=tds.rekey
                    )

    def bulk_insert_reiterable(self, bunch, shift=0):
        """
        Parameters:
        -----------
        bunch: reiterable
                The iterable of tuplekey prefixes to insert.  It is expected to allow
                more than one pass, namely `iter(bunch)` should return an iterator on
                `bunch` that always start from the first element, even if call
                several time.  Indeed, reiterability is tested according to whether
                `iter(bunch)` is different from `bunch` or not.

        shift: int, default=0
                Indicates that the first `shift` coordinates of each tuplekey prefix
                given in `bunch` are already present in the rowstore, whence do not
                require any insertion.  Only the suffix part from `shift` of theses
                prefixes should be inserted.
        """
        if hasattr(bunch, "query"):
            return self.bulk_insert_from_query(bunch.query, shift=shift)
        tds = self.tupleDictSchema.write_target
        # first pass to see the tuplekey lengths
        lengths = set(map(len, iter(bunch)))
        lengths = [i in lengths for i in range(len(tds) + 1)]
        with self._contextmanager:
            for tbl_idx, sq in enumerate(tds._subqueries):
                if sq.stop < shift:
                    continue
                if not any(lengths[sq.start + 1 :]):
                    break
                # one pass for each tuplekey length and each container in which to insert
                b = iter(bunch)
                if sq.start:
                    b = filter(lambda t: len(t) >= sq.start, b)
                if tds.write_permutation:
                    b = map(tds.write_permutation, b)
                f = lambda t: ndtd.padd(t[: sq.stop], sq.stop)
                b = map(f, b)
                if sq.start == sq.stop:
                    subq = sq.write_subquery
                    jpairs = tds.joins[tbl_idx].pairs
                    cols = tuple(p[0] for p in jpairs)
                    phs = tuple(
                        tds.dialect.columns.PlaceholderColumn(for_column=tds[i])
                        for i in range(sq.start)
                    )
                    rpcond = tds.row_prefix_condition(phs)
                    selq = tds.select_row_query(cols=cols, condition=rpcond)
                    cols = tuple(p[1] for p in jpairs)
                    q = subq.insert_query(selq, columns=cols)
                    column_map = tuple(c.name for c in tds[: sq.start])
                    self.helper.executemany(
                        q, I=b, column_map=column_map, rekey=tds.rekey
                    )
                else:
                    self.bulk_insert_onepass(b, shift=sq.start)

    def bulk_insert_from_query(self, query, shift=0):
        tds = self.tupleDictSchema.write_target
        if tds.write_permutation:
            selcols = map(tds.write_permutation, query)
        else:
            selcols = query.external_columns
        aliases = {
            c: tds[i].name for i, c in enumerate(query) if not hasattr(c, "name")
        }
        query = query.set_columns(selcols, aliases=aliases)
        with self._contextmanager:
            for sq in tds._subqueries:
                if sq.stop < shift:
                    continue
                if sq.start > len(query):
                    break
                q = query.set_columns(query[: sq.stop])
                q = tds.insert_infix_query(q)
                self.helper.execute(q)

    def insert(self, kpref, shift=0):
        self.bulk_insert_reiterable((kpref,), shift=shift)

    # CLEANING
    def clean_prefixes(self):
        """Clean the rowstore from tuplekeys prefixing others.

        In order for a rowstore to correctly implement a tupleDict, it is
        required that no incomplete tuplekey (i.e., tuplekey with a nonempty
        `None` prefix) is a prefix of another tuplekey.  In other words, if a
        row is, for instance, `(a, b, None, None)` with `a` and `b` not being
        `None`, then there couldn't be a row of the form `(a, b, c, d)`.  Yet,
        for performance purpose, some methods (e.g., `bulk_insert_from_query`)
        do not care about this constraint when operation, but rather clean the
        rowstore after having altered the store.  This cleaning is the purpose
        of the present method.  Namely, it deletes all partial tuplekey that
        is a prefix of another tuplekey.

        For each subquery `t` of the underlying tupleDict schema, a Delete
        query, in the spirit of the following, is built, where `a`, `b`, `c`,
        and `d` are the tupleDict columns originating from `t`, in order.

                DELETE FROM t
                        WHERE d IS NULL AND (a, b, c) IN (SELECT a, b, c FROM t WHERE d IS NOT NULL)
                        OR c IS NULL AND (a, b) IN (SELECT a, b FROM t WHERE c IS NOT NULL)
                        OR b IS NULL AND a IN (SELECT a FROM t WHERE b IS NOT NULL)
                        OR a IS NULL

        Often, the last condition component `OR a IS NULL` is useless, as not
        having rows with `a` being `NULL` can be enforced as a SQL schema `NOT
        NULL` constraint.  However, we add it so that the cleaning works for
        any schema.

        The method does not checks that the `None` values of each tuplekey
        form a suffix of the tuplekey.  It does not check neither that the
        tuplekeys uniquely determine the `value`.
        """
        tds = self.tupleDictSchema.write_target
        with self._contextmanager:
            for sbq in tds._subqueries:
                condition = tds.dialect.conditions.EmptyCondition()
                start = sbq.start + 1
                stop = sbq.stop if sbq.stop <= tds.height else sbq.stop - 1
                if start >= stop:
                    continue
                for i in range(start, stop):
                    jpairs = tds.joins[tds._columns[sbq.start].subquery_index].pairs
                    jids = tuple(c[0] for c in jpairs)
                    jfids = tuple(c[1] for c in jpairs)
                    tplcol = tds.dialect.columns.TupleColumn(
                        *jfids, *tds[sbq.start : i]
                    )
                    extendings = sbq.subquery.select_query(
                        columns=tplcol, condition=tds[i].isnotnull()
                    )
                    condition &= tds[i].isnull() & tplcol.inset(extendings)
                q = sbq.subquery.delete_query(condition=condition)
                self.helper.execute(q)

    # DELETE
    def bulk_delete(self, bunch, no_reinsert=0):
        # src: nd.tupledict.tupledict.ReadWriteAbstractRowStore.delete
        if isinstance(no_reinsert, int):
            no_reinsert = set(range(no_reinsert + 1))
        elif no_reinsert is True:
            no_reinsert = set(range(self.depth))
        elif no_reinsert is False:
            no_reinsert = set()
        no_reinsert.add(self.height)
        #
        tds = self.tupleDictSchema.write_target
        if tds.write_permutation:
            bunch = map(tds.write_permutation, bunch)
        bunch = itertools.groupby(bunch, key=len)
        with self._contextmanager:
            for elen, subbunch in bunch:
                if not elen:
                    q = tds.delete_prefix_query(())
                    self.helper.execute(q)
                    return
                args = (tds.dialect.constants.Placeholder,) * elen
                tbl_idx = tds._columns[elen - 1].subquery_index
                pref_tbl_idx = tds._columns[elen - 2].subquery_index
                if not self.cascade and tbl_idx < len(self.subqueries) - 1:
                    for t in subbunch:
                        for cidx in range(len(self.subqueries) - 1, tbl_idx, -1):
                            q = tds.delete_prefix_query(t, subquery_index=cidx)
                            self.helper.execute(q)
                elif tbl_idx == pref_tbl_idx and any(
                    elen - i not in no_reinsert for i in range(1, elen)
                ):
                    i = 0
                    while elen - i in no_reinsert:
                        i -= 1
                    subbunch = itertools.groupby(subbunch, key=lambda e: e[:-i])
                    for kpref, subsubbunch in subbunch:
                        q = tds.delete_prefix_query(args)
                        column_map = tuple(c.name for c in tds[:elen])
                        self.helper.executemany(
                            q, I=subsubbunch, column_map=column_map, rekey=tds.rekey
                        )
                        if kpref and not self.is_keyprefix(kpref):
                            self.insert(kpref, shift=len(kpref) - 1)
                else:
                    q = tds.delete_prefix_query(args)
                    column_map = tuple(c.name for c in tds[:elen])
                    self.helper.executemany(
                        q, I=subbunch, column_map=column_map, rekey=tds.rekey
                    )

    def delete(self, kpref, no_reinsert=0):
        self.bulk_delete((kpref,), no_reinsert=no_reinsert)

    def to_readonly(self):
        return self._RO.build_from(self)


ReadOnlyTupleDict = ndtd.tupleDictFactory(BaseRowStore)
ReadWriteTupleDict = ndtd.tupleDictFactory(ReadWriteRowStore)

subdialect.register(
    dialectable=False,
    ReadOnlyTupleDict=ReadOnlyTupleDict,
    ReadWriteTupleDict=ReadWriteTupleDict,
)
