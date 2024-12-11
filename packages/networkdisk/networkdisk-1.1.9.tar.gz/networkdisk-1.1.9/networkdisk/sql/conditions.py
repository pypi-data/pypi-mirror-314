import abc, functools, itertools
from networkdisk.sql.dialect import sqldialect as dialect
from collections import namedtuple
import collections
from networkdisk.exception import NetworkDiskSQLError
from networkdisk.utils.constants import SymDict, IdentityFunction
from networkdisk.sql import scope as ndscope

dialect = dialect.provide_submodule(__name__)

__all__ = [
    "ConditionObject",
    "EmptyCondition",
    "BinaryCondition",
    "CompareCondition",
    "NegationCondition",
    "MultipleCondition",
    "ConjunctionCondition",
    "DisjunctionCondition",
    "NullCondition",
    "NotNullCondition",
    "InQuerySetCondition",
    "InValueSetCondition",
]


@dialect.register(True)
class ConditionObject(abc.ABC):
    def __init__(self, dialect):
        self.dialect = dialect

    @abc.abstractmethod
    def qformat(self, grouped=False, context=None, force=None):
        pass

    @property
    def columns(self):
        return ()

    @property
    def is_emptycondition(self):
        return False

    def substitute_column(self, old, new):
        return self.build_from()

    def get_subargs(self):
        return ndscope.ScopeValueColumns()

    def get_with_queries(self):
        return {}

    def get_schema_containers(self):
        yield from ()

    def get_subcolumns(self):
        return ()

    def __repr__(self):
        return f"{self.__class__.__name__}〈{self.qformat()}〉"

    def __or__(self, other):
        dcond = self.dialect.conditions
        if other is None or isinstance(
            other, (dcond.EmptyCondition.func, dcond.FalseCondition.func)
        ):
            return self
        elif isinstance(other, dcond.TrueCondition.func):
            return other
        else:
            return self.dialect.conditions.DisjunctionCondition(self, other)

    def __and__(self, other):
        dcond = self.dialect.conditions
        if other is None or isinstance(
            other, (dcond.EmptyCondition.func, dcond.TrueCondition.func)
        ):
            return self
        elif isinstance(other, dcond.FalseCondition.func):
            return other
        else:
            return dcond.ConjunctionCondition(self, other)

    def __neg__(self):
        return self.dialect.conditions.NegationCondition(self)

    __pos__ = functools.partialmethod(IdentityFunction)

    def __getstate__(self):
        return dict(dialect=self.dialect.name)

    def __setstate__(self, state):
        for k, v in state.items():
            if k == "dialect":
                v = dialect._dialects[v]
            setattr(self, k, v)

    def build_from(self, **kwargs):
        cls = self.__class__
        state = self.__getstate__()
        for k in state.keys():
            if k in kwargs:
                state[k] = kwargs[k]
        new = object.__new__(cls)
        new.__setstate__(state)
        return new

    def __hash__(self):
        return hash(
            tuple(sorted(self.__getstate__().items())) + (self.__class__.__name__,)
        )

    def __eq__(self, other):
        return self.__class__ == other.__class__

    def iff(self, left, right):
        return self.dialect.columns.IIFColumn(self, left, right)


@dialect.register(True)
class FalseCondition(ConditionObject):
    constant = False

    @property
    def column(self):
        if not hasattr(self, "_col"):
            self._col = self.dialect.columns.ValueColumn(self.constant)
        return self._col

    def qformat(self, grouped=False, context=None, force=None):
        return f"{self.column.qformat()}"

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __and__(self, other):
        return self

    def __or__(self, other):
        if other is None or isinstance(
            other, self.dialect.conditions.EmptyCondition.func
        ):
            return self
        return other

    def __neg__(self):
        return self.dialect.conditions.TrueCondition()

    def get_subargs(self):
        return self.column.get_subargs()

    def get_subcolumns(self):
        return (self.column,)


@dialect.register(True)
class TrueCondition(FalseCondition):
    constant = True

    def __and__(self, other):
        if other is None or isinstance(
            other, self.dialect.conditions.EmptyCondition.func
        ):
            return self
        return other

    def __or__(self, other):
        return self

    def __neg__(self):
        return self.dialect.conditions.FalseCondition()


@dialect.register(True)
class EmptyCondition(ConditionObject):
    def qformat(self, grouped=False, context=None, force=None):
        raise NetworkDiskSQLError(f"EmptyCondition is not formattable")

    @property
    def is_emptycondition(self):
        return True

    def __bool__(self):
        return False

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __and__(self, other):
        if other is None:
            return self
        return other

    def __or__(self, other):
        return other or self

    def __neg__(self):
        return self


@dialect.register(True)
class BinaryCondition(ConditionObject):
    """
    A `BinaryCondition` is an abstract condition that involves two
    selected columns (instances of `AbstractColumns`), referred as
    `left` and `right`.
    """

    def get_subargs(self):
        return self.left.get_subargs() + self.right.get_subargs()

    def __getstate__(self):
        state = super().__getstate__()
        state.update(left=self.left, right=self.right)
        return state

    def __eq__(self, other):
        return (
            super().__eq__(other)
            and self.left == other.left
            and self.right == other.right
        )

    def __hash__(self):
        return super().__hash__()


@dialect.register(True)
class CompareCondition(BinaryCondition):
    """
    A `CompareCondition` is a binary condition (`BinaryCondition`)
    that compares the two columns `left` and `right` using an
    operator `operator`. These operators typically belong to (but
    are not limited to) the key set of the class attribute
    `_operators`. This dictionary defines the negation of each
    operator, if any. This allows flat-negation of instances of
    `CompareCondition`. An class instance that uses an operator
    which is not a key of the `_operators` dictionary, or which is
    associated with `None` in that dictionary, cannot be
    flat-negated. Its negation thus default to the instantiation
    of a `ConditionNegation` object.
    """

    _operators = SymDict(
        {"=": "!=", "<=": ">", ">=": "<", "IS": "IS NOT", "LIKE": "NOT LIKE"}
    )

    def __init__(self, dialect, left, right, operator="=", parameters=()):
        """
        +	left, right:
                either two column definitions, or two tuples of column
                definitions. Here, column definitions are either columns
                or any values, from which to build a `ValueColumn`. In
                case of real columns in one side, the encoders of the
                built `ValueColumn`s of the other side are inferred. If
                only one of the two arguments is a tuple, then it is
                considered as a value.
        +	operator:
                a string (`str`), considered as an plain-SQL comparison
                operator (e.g., "=", "<", "!="). Typically it is a key of
                the class dict attribute `_operators` that provides
                negations of operators (e.g., "!=" is mapped to "=" in
                that symmetric dictionary). The parameter defaults to
                `"="`.
        """
        super().__init__(dialect)
        AbstrCol = dialect.columns.AbstractColumn.func
        if isinstance(left, tuple) and isinstance(right, tuple):
            L, R = [], []
            for l, r in zip(left, right):
                if not hasattr(l, "qformat"):
                    l = self.dialect.columns.ValueColumn(
                        l, for_column=r if isinstance(r, AbstrCol) else None
                    )
                L.append(l)
                if not hasattr(r, "qformat"):
                    r = self.dialect.columns.ValueColumn(r, for_column=l)
                R.append(r)
            left = self.dialect.columns.TupleColumn(*L)
            right = self.dialect.columns.TupleColumn(*R)
        else:
            if not hasattr(left, "qformat"):
                if isinstance(left, tuple) and (
                    isinstance(right, tuple) or hasattr(right, "target")
                ):
                    left = self.dialect.columns.TupleValueColumn(
                        *left, for_column=right if isinstance(right, AbstrCol) else None
                    )
                else:
                    left = self.dialect.columns.ValueColumn(
                        left, for_column=right if isinstance(right, AbstrCol) else None
                    )
            if not hasattr(right, "qformat"):
                if isinstance(right, tuple) and hasattr(left, "target"):
                    right = self.dialect.columns.TupleValueColumn(
                        *right, for_column=left
                    )
                else:
                    right = self.dialect.columns.ValueColumn(right, for_column=left)
        self.left = left
        self.right = right
        self.operator = operator
        self.parameters = tuple(parameters)

    @property
    def columns(self):
        return (self.left, self.right)

    def substitute_column(self, old, new):
        kwargs = {}
        if self.left is old:
            kwargs["left"] = new
        if self.right is old:
            kwargs["right"] = new
        return self.build_from(**kwargs)

    def qformat(self, grouped=False, context=None, force=None):
        frmt = f"{self.left.qformat(context=context)} {self.operator} {self.right.qformat(context=context)}"
        if self.parameters:
            frmt = f"{frmt} {' '.join(self.parameters)}"
        return frmt

    def __neg__(self):
        negop = self._operators.get(self.operator, None)
        if negop is None:
            return super().__neg__()
        return self.build_from(operator=negop)

    def __getstate__(self):
        state = super().__getstate__()
        state.update(operator=self.operator, parameters=self.parameters)
        return state

    def __eq__(self, other):
        return (
            super().__eq__(other)
            and self.operator == other.operator
            and self.parameters == other.parameters
        )

    def __hash__(self):
        return super().__hash__()


@dialect.register(True)
def LikeCondition(dialect, left, right, insensitive=False, escape=None):
    if insensitive:
        left = dialect.columns.TransformColumn("lower", left)
        if isinstance(right, str):
            right = right.lower()
        elif isinstance(right, dialect.columns.ValueColumn.func) and isinstance(
            right.value, str
        ):
            state = right.__getstate__()
            state[value] = state[value].lower()
            right = object.__new__(type(right))
            right.__setstate__(state)
        else:
            right = dialect.columns.TransformColumn("lower", right)
    parameters = (f'ESCAPE "{escape}"',) if escape else ()
    return dialect.conditions.CompareCondition(
        left, right, operator="LIKE", parameters=parameters
    )


@dialect.register(True)
def ILikeCondition(dialect, left, right, escape=None):
    return dialect.conditions.LikeCondition(
        left, right, insensitive=True, escape=escape
    )


@dialect.register(True)
def NullCondition(dialect, left):
    return dialect.conditions.CompareCondition(
        left, dialect.columns.NullColumn(), operator="IS"
    )


@dialect.register(True)
def NotNullCondition(dialect, left):
    return dialect.conditions.CompareCondition(
        left, dialect.columns.NullColumn(), operator="IS NOT"
    )


@dialect.register(True)
class InQuerySetCondition(CompareCondition):
    """
    A variant of `CompareCondition` whose right column is replaced
    by a query. This condition expresses the `left` column value
    membership to the rows of the `right` query using the operator
    "IN".
    """

    _operators = SymDict({"IN": "NOT IN"})

    def __init__(self, dialect, col, query, negate=False):
        """
        +	col:
                a column specification as accepted by the initializer of
                `CompareCondition`.
        +	query:
                a query.
        +	negate:
                a Boolean that specifies whether the operator should be
                negated or not. If `False` (default) the operator is "IN",
                otherwise it is "NOT IN".
        +	with_query_name:
                either `None` (default) or an nonempty name (`str`). In
                the latter case, the `right` query is replaced by a
                `WithQuery` on `right` named `with_query_name`.
        """
        ConditionObject.__init__(self, dialect)
        operator = self._operators["IN"] if negate else "IN"
        if not isinstance(query, self.dialect.queries.ReadQuery.func):
            raise NetworkDiskSQLError(
                f"InQuerySetCondition expects a query, got {type(query)}"
            )
        if isinstance(col, collections.abc.Sequence):
            T = []
            if len(query) != len(col):
                raise NetworkDiskSQLError(
                    f"comparing tuple of columns and query rows of different size, got {len(col)} and {len(query)}"
                )
            for tcol, fcol in zip(col, query):
                if not hasattr(tcol, "qformat"):
                    tcol = self.dialect.columns.ValueColumn(tcol, for_column=fcol)
                T.append(tcol)
            col = self.dialect.columns.TupleColumn(*T)
        else:
            if len(query) != 1:
                raise NetworkDiskSQLError(
                    f"comparing tuple of columns and query rows of different size, got {1} and {len(query)}"
                )
            if not hasattr(col, "qformat"):
                col = self.dialect.columns.ValueColumn(col, for_column=query[0])
        self.left = col
        self.right = query
        self.operator = operator
        self.parameters = ()

    @property
    def columns(self):
        return (self.left,) + tuple(self.right.external_columns)  # ???

    def get_with_queries(self):
        return self.right.get_with_queries()

    def get_schema_containers(self):
        yield from super().get_schema_containers()
        yield from self.right.get_schema_containers()

    def qformat(self, grouped=False, context=None, force=None):
        # TODO: Query subformat should have context?
        return f"{self.left.qformat(context=context)} {self.operator} {self.right.subformat(scoped=True)}"


@dialect.register(True)
class InValueSetCondition(CompareCondition):
    _operators = SymDict({"IN": "NOT IN"})

    def __init__(self, dialect, left, *values, negate=False):
        """
        +	dialect
                an SQL dialect.
        +	left
                a column, which might be simple or tuple.
        +	values
                a tuple whose elements are value specifications if left is
                a single column, or tuple column or tuples of value
                specifications otherwise. Here, a value specification is
                a value or a column.
        +	negate
                a Boolean indicating whether the `left` column value
                membership to the set of values specified by `values`
                should be negated or not.
        """
        operator = self._operators["IN"] if negate else "IN"
        lsubcols = list(left.get_subcolumns())
        AbstrCol = dialect.columns.AbstractColumn.func
        right = []
        for i, v in enumerate(values):
            if not i and isinstance(left, tuple):
                if isinstance(v, tuple):
                    target = v
                else:
                    assert isinstance(v, dialect.columns.TupleColumn.func)
                    target = v.target
                L, R = [], []
                for l, r in zip(left, target):
                    if not isinstance(l, AbstrCol):
                        l = dialect.columns.ValueColumn(
                            l, for_column=r if isinstance(r, AbstrCol) else None
                        )
                    L.append(l)
                    if not isinstance(w, AbstrCol):
                        r = dialect.columns.ValueColumn(r, for_column=l)
                    R.append(r)
                left = dialect.columns.TupleColumn(*L)
                right.append(dialect.columns.TupleColumn(*R))
            elif not isinstance(v, AbstrCol):
                if len(lsubcols) != 1:
                    assert isinstance(v, tuple) and len(v) == len(lsubcols)
                    t = []
                    for l, w in zip(lsubcols, v):
                        if not isinstance(w, AbstrCol):
                            w = dialect.columns.ValueColumn(w, for_column=l)
                        t.append(w)
                    v = dialect.columns.TupleColumn(*t)
                else:
                    v = dialect.columns.ValueColumn(v, for_column=lsubcols[0])
            right.append(v)
        right = dialect.columns.TupleColumn(*right)
        self.right = right
        super().__init__(dialect, left, right, operator=operator)


@dialect.register(True)
class NegationCondition(ConditionObject):
    def __init__(self, dialect, condition):
        super().__init__(dialect)
        self.subcondition = condition

    def __bool__(self):
        return bool(self.subcondition)

    @property
    def columns(self):
        return self.subcondition.columns

    def substitute_column(self, old, new):
        return self.build_from(subcondition=subcondition.substitute_column(old, new))

    def qformat(self, grouped=False, context=None, force=None):
        return f"NOT {self.subcondition.qformat(grouped=True, context=context)}"

    def __neg__(self):
        return self.subcondition

    def get_subargs(self):
        return self.subcondition.get_subargs()

    def get_with_queries(self):
        return self.subcondition.get_with_queries()

    def get_schema_containers(self):
        yield from self.subcondition.get_schema_containers()

    def __getstate__(self):
        state = super().__getstate__()
        state["subcondition"] = self.subcondition
        return state

    def __eq__(self, other):
        return super().__eq__(other) and self.subcondition == other.subcondition

    def __hash__(self):
        return super().__hash__()


@dialect.register(True)
class MultipleCondition(ConditionObject):
    """
    An abstract `ConditionObject` that involves an arbitrary
    number of sub-conditions, referred as `subconditions`.
    """

    def __init__(self, dialect, subconditions):
        super().__init__(dialect)
        self.subconditions = tuple(subconditions)

    @property
    def columns(self):
        return sum((subcond.columns for subcond in self.subconditions), ())

    def substitute_column(self, old, new):
        return self.build_from(
            subconditions=tuple(
                subcond.substitute_column(old, new) for subcond in self.subconditions
            )
        )

    def get_subargs(self):
        return sum(
            (e.get_subargs() for e in self.subconditions), ndscope.ScopeValueColumns()
        )

    def get_with_queries(self):
        return dict(
            itertools.chain.from_iterable(
                map(lambda sc: sc.get_with_queries().items(), self.subconditions)
            )
        )

    def get_schema_containers(self):
        yield from super().get_schema_containers()
        for sc in self.subconditions:
            yield from sc.get_schema_containers()

    def __getstate__(self):
        state = super().__getstate__()
        state["subconditions"] = self.subconditions
        return state

    def __eq__(self, other):
        return super().__eq__(other) and self.subconditions == other.subconditions

    def __hash__(self):
        return super().__hash__()


@dialect.register(True)
class ConjunctionCondition(MultipleCondition):
    _combinator = "AND"

    def __init__(self, dialect, *conditions):
        subconditions = []
        for cons in conditions:
            if not cons:
                continue
            if (
                hasattr(cons, "subconditions")
                and getattr(cons, "_combinator", None) == self._combinator
            ):
                subconditions.extend(cons.subconditions)
            else:
                subconditions.append(cons)
        super().__init__(dialect, subconditions)

    def qformat(self, grouped=False, context=None, force=None):
        if not self:
            raise NetworkDiskSQLError(
                f"Empty {self.__class__.__name__} are not formattable"
            )
        res = f" {self._combinator} ".join(
            sc.qformat(grouped=True, context=context) for sc in self.subconditions
        )
        if grouped:
            res = f"({res})"
        return res

    def __neg__(self):
        return self.dialect.conditions.DisjunctionCondition(
            *(-sc for sc in self.subconditions)
        )

    def __bool__(self):
        return bool(self.subconditions)


@dialect.register(True)
class DisjunctionCondition(ConjunctionCondition):
    _combinator = "OR"

    def __neg__(self):
        return self.dialect.conditions.ConjunctionCondition(
            *(-sc for sc in self.subconditions)
        )
