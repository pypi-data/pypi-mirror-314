"""Module for SQL column constructors."""

import abc, functools, collections.abc, itertools
from .dialect import sqldialect as dialect
from networkdisk.exception import NetworkDiskSQLError
from networkdisk.utils.serialize import encoderFunctions
from .constants import Star, Null, Placeholder
from .scope import ScopeValueColumns

dialect = dialect.provide_submodule(__name__)


def aliasable(f):
    @functools.wraps(f)
    def decored(self, *args, alias=None, **kwargs):
        if alias is None or (hasattr(self, "name") and alias == self.name):
            return f(self, *args, **kwargs)
        else:
            return f"{f(self, *args, **kwargs)} AS {alias}"

    return decored


def nonaliasable(f):
    @functools.wraps(f)
    def decored(self, *args, alias=None, **kwargs):
        return f(self, *args, **kwargs)

    return decored


class decorate_encoder:
    def __init__(self, encode):
        self.encode = encode

    def __call__(self, e):
        sqlize = getattr(e, "sqlize", None)
        return sqlize() if sqlize else self.encode(e)


class TupleEncoder:
    def __init__(self, target):
        self.target = target

    def __call__(self, t):
        t = list(t)
        encoded = []
        for trgt in self.target:
            if hasattr(trgt, "encode"):
                encoded.append(trgt.encode(t.pop(0)))
        assert not t
        return tuple(encoded)


# ABSTRACT COLUMN OBJECTS
@dialect.register(True)
class AbstractColumn(abc.ABC):
    """An abstract SQL column.

    Parameters
    ----------
    dialect : Dialect
            The SQL dialect to use, represented as a Dialect object for finding
            dialect-wise classes.
    sqltype : str or None, default=None
            The type (e.g. "int", "text" of the column).
    container_name : str or None, default=None
            The name of the container (_e.g._, table, view, query) containing the
            column, if any, or `None` (default) otherwise.

    Attributes
    ----------
    dialect : Dialect
            The SQL dialect to use, represented as a Dialect object for finding
            dialect-wise classes.
    container_name : str or None, default=None
            The name of the container (_e.g._, table, view, query) containing the
            column, if any, or `None` (default) otherwise.

    Methods
    -------
    qformat(context=None, force=None)
    """

    def __init__(self, dialect, sqltype=None, container_name=None):
        self.dialect = dialect
        self.container_name = container_name
        self.sqltype = sqltype

    @abc.abstractmethod
    def qformat(self, context=None, force=False):
        pass

    #
    # Conditions
    # TODO: functools.partialmethod
    def eq(self, other):
        return self.dialect.conditions.CompareCondition(self, other, operator="=")

    def neq(self, other):
        return self.dialect.conditions.CompareCondition(self, other, operator="!=")

    def lt(self, other):
        return self.dialect.conditions.CompareCondition(self, other, operator="<")

    def le(self, other):
        return self.dialect.conditions.CompareCondition(self, other, operator="<=")

    def gt(self, other):
        return self.dialect.conditions.CompareCondition(self, other, operator=">")

    def ge(self, other):
        return self.dialect.conditions.CompareCondition(self, other, operator=">=")

    def isnull(self):
        return self.dialect.conditions.NullCondition(self)

    def isnotnull(self):
        return self.dialect.conditions.NotNullCondition(self)

    def inset(self, first, *other):
        if not other:
            if hasattr(first, "qformat"):
                return self.dialect.conditions.InQuerySetCondition(self, first)
            return self.eq(first)
        return self.dialect.conditions.InValueSetCondition(self, first, *other)

    def like(self, other, escape=None):
        return self.dialect.conditions.LikeCondition(self, other, escape=escape)

    def ilike(self, other, escape=None):
        return self.dialect.conditions.ILikeCondition(self, other, escape=escape)

    #
    def count(self):
        return self.dialect.columns.CountColumn(self)

    def sum(self):
        return self.dialect.columns.SumColumn(self)

    def min(self):
        return self.dialect.columns.MinColumn(self)

    def max(self):
        return self.dialect.columns.MaxColumn(self)

    def add(self, other):
        return self.dialect.columns.AddColumn(self, other)

    def sub(self, other):
        return self.dialect.columns.SubstractColumn(self, other)

    def multiply(self, other):
        return self.dialect.columns.MulColumn(self, other)

    def divides(self, other):
        return self.dialect.columns.DivColumn(self, other)

    def ifnull(self, default):
        # TODO: define IfNullColumn in sql!
        return self.dialect.columns.IfNullColumn(self, default)

    def cast(self, sqltype):
        return self.dialect.columns.CastColumn(sqltype, self)

    #
    def tuple_with(self, *others):
        return self.dialect.columns.TupleColumn(self, *others)

    #
    def __str__(self):
        return self.qformat()

    def __repr__(self):
        return f"{self.__class__.__name__}<{self}>"

    def get_subargs(self):
        return ScopeValueColumns()

    def __getstate__(self):
        return dict(
            dialect=self.dialect.name,
            container_name=self.container_name,
            sqltype=self.sqltype,
        )

    def __setstate__(self, state):
        for k, v in state.items():
            if k == "dialect":
                v = dialect._dialects[v]
            setattr(self, k, v)

    def __hash__(self):
        return hash(
            tuple(sorted(self.__getstate__().items())) + (self.__class__.__name__,)
        )

    def __eq__(self, other):
        return self.__class__ is other.__class__ and hash(self) == hash(other)

    def get_subcolumns(self):
        yield self


@dialect.register(True)
class EncodedColumn(AbstractColumn):
    """An abstract SQL column with associated encoding.

    PARAMETERS
    ----------
    dialect : Dialect
            The SQL dialect to use.
    sqltype : str or None, default=None
            The type (e.g. "int", "text" of the column).
    encoder : str or None
            A key of the `encoderFunctions` mapping.
    container_name: str or None
            The name of the column container.

    ATTRIBUTES
    ----------
    encode
    decode
    encoder : str or None, default=None
            The key of the `encoderFunctions` mapping that defines the encoder and
            the decoder.  The `None` key (default) correspond to identity encoding.


    NOTES
    -----
    Only the two above properties are relevant for this extension of
    `AbstractColumn`.  However, for serialization motivations, the encoder is
    specified as a key of the `encoderFunctions` mapping.

    """

    def __init__(self, dialect, encoder=None, container_name=None, sqltype=None):
        super().__init__(dialect, container_name=container_name, sqltype=sqltype)
        encoder = encoder or sqltype
        if isinstance(encoder, tuple):
            encoder = list(encoder)
            for i, enc in enumerate(encoder):
                encoder[i] = enc = enc and enc.upper()
                encoderFunctions[enc]
            encoder = tuple(encoder)
        else:
            encoder = encoder and encoder.upper()
            encoderFunctions[encoder]
        self.encoder = encoder

    @property
    def encode(self):
        return decorate_encoder(encoderFunctions[self.encoder][0])

    @property
    def decode(self):
        return encoderFunctions[self.encoder][1]

    def __getstate__(self):
        state = super().__getstate__()
        state["encoder"] = self.encoder
        return state


# REAL COLUMNS
@dialect.register(True)
class ConstantColumn(AbstractColumn):
    """A concrete SQL constant column (_e.g._, NULL, 1, \*).

    PARAMETERS
    ----------
    dialect : Dialect
            The SQL dialect to use.
    sqltype : str or None, default=None
            The type (e.g. "int", "text" of the column).
    constant : any
            The value of the constant.

    ATTRIBUTES
    ----------
    constant : any
            The value of the constant.

    """

    # Cannot both extend `AbstractColumn` and be a `Singletons` (metaclass)
    def __init__(self, dialect, constant, sqltype=None):
        super().__init__(dialect, sqltype=sqltype)
        self.constant = constant

    def __getstate__(self):
        state = super().__getstate__()
        state["constant"] = self.constant
        return state

    @nonaliasable
    def qformat(self, context=None, force=False):
        return self.constant.sqlize()


@dialect.register(True)
class NullColumn(ConstantColumn):
    """The special NULL constant column.

    Notes
    -----
    This class should be a singleton class.
    """

    def __init__(self, dialect):
        super().__init__(dialect, dialect.constants.Null, sqltype=None)


@dialect.register(True)
class StarColumn(ConstantColumn):
    """The special * (STAR) constant pseudo-column.

    Notes
    -----
    This class should be a singleton class.
    """

    def __init__(self, dialect):
        super().__init__(dialect, dialect.constants.Star, sqltype=None)


@dialect.register(True)
class QueryColumn(EncodedColumn):
    """A concrete SQL encoded column with a name.

    PARAMETERS
    ----------
    dialect : Dialect
            The SQL dialect to use.
    name : str
            The column name.
    index_in_container : int
            The index of the column in the container query.
    sqltype : str or None, default=None
            The type (e.g. "int", "text" of the column).
    encoder : str or None
            A key of the `encoderFunctions` mapping.
    container_name: str or None
            The name of the column container.

    ATTRIBUTES
    ----------
    name: str
            The column name.
    index_in_container:
            The container index.

    METHODS
    -------
    qformat(query, alias=None, context=None, force=False)

    """

    def __init__(
        self,
        dialect,
        name,
        index_in_container,
        encoder=None,
        container_name=None,
        sqltype=None,
    ):
        # TODO: add for_column parameter
        super().__init__(
            dialect, encoder=encoder, container_name=container_name, sqltype=sqltype
        )
        self.name = name
        self.index_in_container = index_in_container

    @aliasable
    def qformat(self, context=None, force=False):
        """
        +	context:
                either `None` or a `InternalColumns` scope from which to
                recover the context of `self` and name conflicts using
                the `__getitem__` and  `sources.get` methods. If `None`
                the name of `self` only is returned (`self.name`) without
                checking ambiguity. Otherwise, the context query name (if
                any) is prepended followed by a dot to `self` name, e.g.
                "table.col", when needed. More precisely, this query name
                is prepended if there exists another column in the scope
                presented by `context` has same name. An `NetworkDiskError`
                exception is raised when this happen and one of the two
                following cases hold: `self` does not have a source query
                in `context`, `self` context query does not have a name.
        """
        name = self.name
        if not context:
            return name
        samename = context.byname[name]
        if not samename:
            raise NetworkDiskSQLError(f"No internal column named {name} in context")
        elif len(samename) == 1:
            if not self in context.origin_columns[samename[0]]:
                raise NetworkDiskSQLError(
                    f"No internal column corresponding to {self} in context"
                )
            if not force:
                return name
        selforig = context.origin_query.get(self, None)
        if not hasattr(selforig, "name"):
            if force and len(samename) == 1:
                return name
            raise NetworkDiskSQLError(f"Ambiguous selection of internal column {self}")
        return f"{selforig.name}.{name}"

    def __getstate__(self):
        state = super().__getstate__()
        state.update(name=self.name, index_in_container=self.index_in_container)
        return state


@dialect.register(True)
class TupleColumn(EncodedColumn, collections.abc.Sequence):
    """An SQL tuple column formed by a tuple of SQL columns.

    PARAMETERS
    ----------
    dialect : Dialect
            The SQL dialect to use.
    sqltype : str or None, default=None
            The type (e.g. "int", "text" of the column).
    *target : iterable
            The columns to gather in the tuple.  Elements which are not columns
            (_i.e._, which do not implement the `qformat` method) are considered
            as values, and thus replaced by the corresponding `ConstantColumn`
            within the tuple.
    sqltype : str or None, default=None
            The sql type of the column.

    ATTRIBUTES
    ----------
    encode
    decode
    encoder : tuple
            A tuple of keys (`str` or `None`) of the `encoderFunctions` mapping.
    target : tuple
            The tuple of gathered columns.

    METHODS
    -------
    qformat(context=None, force=False, distinct=False)
    """

    def __init__(self, dialect, *target, sqltype=None):
        EncodedColumn.__init__(self, dialect)
        target = tuple(
            c
            if hasattr(c, "qformat")
            else (
                dialect.columns.ConstantColumn(c)
                if hasattr(c, "sqlize")
                else dialect.columns.ValueColumn(c)
            )
            for c in target
        )
        if callable(sqltype):
            sqltype = sqltype(target)
        self.sqltype = sqltype
        self.encoder = tuple(getattr(c, "encoder", None) for c in target)
        self.target = target

    @property
    def encode(self):
        return TupleEncoder(self.target)

    @property
    def decode(self):
        raise TypeError(f"Should not decode {self.__class__.__name__} columns")

    def get_subargs(self):
        return ScopeValueColumns(
            incolumns=itertools.chain(
                super().get_subargs(), *(c.get_subargs() for c in self.target)
            )
        )

    @nonaliasable
    def qformat(self, context=None, force=False, distinct=False):
        distinct = "DISTINCT " if distinct else ""
        return f"({distinct}{', '.join(c.qformat(context=context, force=force) for c in self.target)})"

    def __getstate__(self):
        state = super().__getstate__()
        state["target"] = self.target
        return state

    def __len__(self):
        return len(self.target)

    def __getitem__(self, k):
        return self.target[k]

    def get_subcolumns(self):
        return itertools.chain.from_iterable(c.get_subcolumns() for c in self.target)


@dialect.register(True)
class CaseColumn(TupleColumn):
    """An SQL filter column: "CASE [col] [WHEN col THEN col]⁺ [ELSE col]".

    PARAMETERS
    ----------
    dialect : Dialect
            The SQL dialect to use.
    first : AbstractColumn or tuple
            A single column `col` (yielding "CASE [col]…") or a pair `(cond, col)`
            where `cond` is a condition and `col` is a column (yielding
            "CASE WHEN [cond] THEN [col]…").
    conditions_and_targets : iterable
            An iterable of pairs `(cond, col)` where `col` is a column and `cond` is
            a condition.  If `first` is a single column, then `cond` might be
            substituted with a value, to be replace by the condition `col.eq(cond)`.
            Each element yields a "WHEN [cond] THEN [col]" statement.
    last : AbstractColumn or tuple
            A single column (yielding "… ELSE [col]") or a element of the same kind as
            condition and `col` is a column (yielding "… WHEN [cond] THEN [col]" as if
            it were at the end of the `conditions_and_targets` iterable).
    sqltype : str or None, default=None
            The type (e.g. "int", "text" of the column).

    ATTRIBUTES
    ----------
    conditions : tuple
            The tuple of condition on which to filter.
    on_target : AbstractColumn or None
            The column to filter (if of the form "CASE [col] …") or `None` otherwise.
    else : AbstractColumn or None
            The default column to use if no filter matched (in the case "ELSE [col]")
            or `None` otherwise.

    """

    def __init__(
        self, dialect, first, *conditions_and_targets, last=None, sqltype=None
    ):
        """
        +	dialect
        + first
                either a pair `(cond, col)` with `cond` a condition and
                `col` a column, or a single column `col`. In the former
                case, a _searched_ CASE column is built and the pair is
                prepended to the `conditions_and_target` tuple, in the
                latter case a _simple_ CASE on `first` is built.
        +	conditions_and_target
                a tuple of pairs. If the CASE is `simple` (which is
                determined from the nature of `first`), then the pairs
                should be pairs of columns or values. Otherwise, the pairs
                are formed by a condition `cond` and a column `col`. In
                both cases, a CASE statement "WHEN {left} THEN {right}" is
                defined.
        +	last
                Either a pair of same kind as those of the given
                `conditions_and_target` (the kind is determined according
                to the value of `first`, namely according to whether the
                built CASE is simple or searched), or a single columns.
                In the former case, the pair is appended to the tuple
                `conditions_and_target`, thus defining a further CASE
                statement "WHEN {left} THEN {right}". In the latter case
                the CASE statement "ELSE {last}" is defined.

        If `last` has its default value `None` then the last item
        of `conditions_and_targets` which is not required to satisfy
        the form of the pairs in `conditions_and_targets` is taken
        instead. In this case, it is assumed that this last item
        exists.
        """
        if last is None:
            last = conditions_and_targets[-1]
            conditions_and_targets = conditions_and_targets[:-1]
        ConditionObject = dialect.conditions.ConditionObject.func
        #
        is_searched_case = (
            isinstance(first, tuple)
            and len(first) == 2
            and isinstance(first[0], ConditionObject)
        )
        if is_searched_case:
            conditions_and_targets = (first,) + conditions_and_targets
            first = None
        #
        has_else = (
            not isinstance(last, tuple)
            or len(last) != 2
            or (is_searched_case and not isinstance(last[0], ConditionObject))
        )
        if not has_else:
            conditions_and_targets = conditions_and_targets + (last,)
            last = None
        #
        col_or_val = (
            lambda c: c if hasattr(c, "qformat") else dialect.columns.ValueColumn(c)
        )
        conditions = map(lambda ct: ct[0], conditions_and_targets)
        targets = map(lambda ct: ct[1], conditions_and_targets)
        targets = map(col_or_val, targets)
        if not is_searched_case:
            first = col_or_val(first)
            targets = itertools.chain((first,), targets)
            conditions = map(col_or_val, conditions)
        if has_else:
            last = col_or_val(last)
            targets = itertools.chain(targets, (last,))
        #
        super().__init__(dialect, *targets, sqltype=sqltype)
        self.conditions = tuple(conditions)
        self.on_target = first
        self.else_target = last

    @aliasable
    def qformat(self, context=None, force=False):
        cases = []
        conds, trgts = iter(self.conditions), iter(self.target)
        kwforce = {}
        if self.on_target:
            t = next(trgts)  # assert t is self.on_target
            cases.append(f"{t.qformat(context=context, force=force)}")
            kwforce["force"] = force
        cases.extend(
            f"WHEN {left.qformat(context=context, **kwforce)} THEN {right.qformat(context=context, force=force)}"
            for left, right in zip(conds, trgts)
        )
        if self.else_target:
            t = next(trgts)  # assert t is self.else_target and not list(trgts)
            cases.append(f"ELSE {t.qformat(context=context, force=force)}")
        return f"CASE {' '.join(cases)} END"

    def __getstate__(self):
        state = super().__getstate__()
        state["conditions"] = self.conditions
        state["on_target"] = self.on_target
        state["else_target"] = self.else_target
        return state

    def get_subargs(self):
        for cond, trgt in itertools.zip_longest(
            self.conditions, self.target, fillvalue=None
        ):
            if cond is not None:
                yield from cond.get_subargs()
            if trgt is not None:
                yield from trgt.get_subargs()
        yield from self.dialect.columns.AbstractColumn.func.get_subargs(self)

    def get_subcolumns(self):
        for cond, trgt in itertools.zip_longest(
            self.conditions, self.target, fillvalue=None
        ):
            if cond is not None:
                yield from cond.get_subcolumns()
            if trgt is not None:
                yield from trgt.get_subcolumns()


@dialect.register(True)
class TriggerColumn(TupleColumn):
    """A column referencing another to be used in triggers (_e.g._, `NEW.c`).

    PARAMETERS
    ----------
    dialect : Dialect
            The SQL dialect to use.
    target : AbstractColumn
            The referenced column.
    new : bool, default=True
            Whether the trigger column is a NEW or OLD column (default is NEW).

    ATTRIBUTES
    ----------
    target : AbstractColumn
            The referenced column.
    new : bool, default=True
            Whether the trigger column is a NEW or OLD column (default is NEW).

    """

    def __init__(self, dialect, target, new=True):
        super().__init__(dialect, target, sqltype=target.sqltype)
        self.encoder = target.encoder
        self.new = new

    def qformat(self, context=None, force=False):
        if self.new:
            return f"NEW.{self.target[0].name}"
        else:
            return f"OLD.{self.target[0].name}"

    def __getstate__(self):
        state = super().__getstate__()
        state["new"] = self.new
        return state


dialect.register_partial_dialectable(TriggerColumn, "TriggerNewColumn", new=True)
dialect.register_partial_dialectable(TriggerColumn, "TriggerOldColumn", new=False)


@dialect.register(True)
class TransformColumn(TupleColumn):
    """An SQL column resulting from the transformation of another column.

    PARAMETERS
    ----------
    dialect : Dialect
            The SQL dialect to use.
    transform : str
            The plain SQL function to apply (_e.g._, "LOWER", "COUNT", "SUM").
    *target : iterable
            The referenced columns on which to apply the transformation.
    decoder : str or None, default=None
            A key of `encoderFunctions` mapping that allows to specify how the
            values of this column can be decoded.  Notice that values are never
            encoded for this column.
    sqltype : str or None, default=None
            The type (e.g. "int", "text" of the column).
    distinct : bool, default=False
            Whether the transformation should be applied on distinct values of
            the columns from `target`.

    ATTRIBUTES
    ----------
    decode
    name : str
            The name of the column, which equals the transformation function.
    encoder : str or None
            A key of `encoderFunctions` mapping that allows to specify how the
            values of this column can be decoded.  Notice that values are never
            encoded for this column.
    distinct : bool, default=False
            Whether the transformation should be applied on distinct values of
            the columns from `target`.

    """

    def __init__(
        self, dialect, transform, *target, decoder=None, distinct=False, sqltype=None
    ):
        """
        The column name is its transform function name, in a postgre
        spirit (notice that SQLite append the names of the columns
        on which the function is applied).
        +	transform:
                an SQL function (`str`), e.g., `"lower"`;
        +	target:
                a tuple of `AbstractColumn`'s.
        +	encoder:
                a key of the global `encoderFunctions` dictionary. These
                include the default value `None`.
        """
        super().__init__(dialect, *target, sqltype=sqltype)
        decoder = decoder or self.sqltype
        self.name = transform
        self.encoder = decoder
        self.distinct = distinct

    @property
    def decode(self):
        return encoderFunctions[self.encoder][1]

    @aliasable
    def qformat(self, context=None, force=False):
        return f"{self.name}{super().qformat(context=context, force=force, distinct=self.distinct)}"

    def __getstate__(self):
        state = super().__getstate__()
        state["name"] = self.name
        state["encoder"] = self.encoder
        state["distinct"] = self.distinct
        return state


dialect.register_partial_dialectable(
    TransformColumn, "CountColumn", "COUNT", sqltype="INT"
)
dialect.register_partial_dialectable(TransformColumn, "SumColumn", "SUM")
dialect.register_partial_dialectable(
    TransformColumn, "MinColumn", "MIN", distinct=False
)  # or distinct=True?
dialect.register_partial_dialectable(
    TransformColumn, "MaxColumn", "MAX", distinct=False
)  # or distinct=True?
dialect.register_partial_dialectable(
    TransformColumn, "DateColumn", "DATE", distinct=False
)


@dialect.register(True)
def CoalesceColumn(dialect, *columns, value, sqltype=None, decoder=None):
    if not isinstance(value, dialect.columns.AbstractColumn.func):
        value = dialect.columns.ValueColumn(value, for_column=column)
    return dialect.columns.TransformColumn(
        "COALESCE", *columns, value, distinct=False, sqltype=sqltype, decoder=decoder
    )


@dialect.register(True)
def IfNullColumn(dialect, column, value):
    return dialect.columns.CoalesceColumn(
        column, value, sqltype=column.sqltype, decoder=column.encoder
    )


def common_type_in_tuple(targets):
    if not targets:
        return
    sqltype = targets[0].sqltype
    if any(t.sqltype != sqltype for t in targets[1:]):
        return
    return sqltype


@dialect.register(True)
class OperatorColumn(TransformColumn):
    """An SQL column resulting from operations on columns.

    PARAMETERS
    ----------
    dialect : Dialect
            The SQL dialect to use.
    transform : str
            The plain SQL function to apply (_e.g._, "LOWER", "COUNT", "SUM").
    *target : iterable
            The referenced columns on which to apply the transformation.

    ATTRIBUTES
    ----------
    decode
    name : str
            The operation to perform on target columns (_e.g._, "+", "-", "*", "/").

    """

    __init__ = functools.partialmethod(
        TransformColumn.__init__, sqltype=common_type_in_tuple, distinct=False
    )

    @aliasable
    def qformat(self, context=None, force=False):
        left = self.target[0].qformat(context=context, force=force)
        right = self.target[1].qformat(context=context, force=force)
        return self.name.join(
            c.qformat(context=context, force=force) for c in self.target
        )


dialect.register_partial_dialectable(OperatorColumn, "AddColumn", "+")
dialect.register_partial_dialectable(OperatorColumn, "SubColumn", "-")
dialect.register_partial_dialectable(OperatorColumn, "MulColumn", "*")
dialect.register_partial_dialectable(OperatorColumn, "DivColumn", "/")

aggregation_transformators = lambda dialect: dict(
    {True: dialect.columns.CountColumn},
    min=dialect.columns.MinColumn,
    max=dialect.columns.MaxColumn,
    count=dialect.columns.CountColumn,
    sum=dialect.columns.SumColumn,
)


@dialect.register(True)
def aggregate_column(dialect, agg, *target, **kwargs):
    agg = aggregation_transformators(dialect).get(agg, agg)
    if type(agg) is type:
        return agg(*target, **kwargs)
    return dialect.columns.TransformColumn(agg, *target, **kwargs)


@dialect.register(True)
class CastColumn(TransformColumn):
    """An SQL cast column ("CAST([col] AS [type])").

    PARAMETERS
    ----------
    dialect : Dialect
            The SQL dialect to use.
    sqltype : str
            The type to which to cast.  This type is used as encoder key as well.
    target : AbstractColumn
            The column to cast.

    """

    def __init__(self, dialect, sqltype, target):
        super().__init__(dialect, "CAST", target, sqltype=sqltype)

    @aliasable
    def qformat(self, context=None, force=False):
        return f"{self.name}({self.target[0].qformat(context=context, force=force, alias=self.encoder)})"


@dialect.register(True)
class ValueColumn(EncodedColumn):
    """An SQL encoded column with a value.

    PARAMETERS
    ----------
    dialect : Dialect
            The SQL dialect to use.
    value : any
            The value associated with the column.  Any object is accepted, although
            it should be encodable according to the encode function associated with
            the `encoder` parameter (see below).
    sqltype : str or None, default=None
            The type (e.g. "int", "text" of the column).
    for_column : AbstractColumn or None, default=None
            A column targetted by the value column (_e.g._, when the intention is
            to insert the given value in a table, the corresponding table column is
            referenced here) or `None`.  If given, its "encoder" attribute, if any,
            is taken as fallback if the parameter `encoder` has value `None`.  In
            the same way, the value column is using the `for_column` "name"
            attribute, if any and if the parameter `name` has value `None`.
    encoder : str or None
            A key of `encoderFunctions` to get the associated encoder and decoder.
            If not given, the parameter value might be taken from the attribute
            'encoder' of `for_column`, if given, if any.
    name : str or None
            The name of the value column.  If not given, the parameter value might be
            taken from the attribute 'name' of `for_column`, if given, if any.

    ATTRIBUTES
    ----------
    value : any
            The value associated with the column.
    for_column : AbstractColumn or None
            A related column or `None`.

    METHODS
    -------
    __eq__(other)

    NOTES
    -----
    The difference with the `ConstantColumn` class is that here the value is
    not hard coded within queries using the column, but a placeholder is used
    instead.  This allows in particular to perform 'executemany' queries with
    different values for the column.
    """

    def __init__(
        self, dialect, value, for_column=None, sqltype=None, encoder=None, name=None
    ):
        sqltype = sqltype or getattr(for_column, "sqltype", sqltype)
        encoder = encoder or getattr(for_column, "encoder", encoder) or sqltype
        name = name or getattr(for_column, "name", name)
        super().__init__(dialect, encoder=encoder, sqltype=sqltype)
        self.value = value
        self.for_column = for_column
        if name:
            self.name = name

    @aliasable
    def qformat(self, context=None, force=False):
        return self.dialect.constants.Placeholder.sqlize()

    def get_subargs(self):
        return ScopeValueColumns((self,))

    def __repr__(self):
        return f"{self.__class__.__name__}<{self}>"

    def __str__(self):
        name = f"{self.name}:" if hasattr(self, "name") else ""
        return f"{name}{self.qformat()}:{self.value}"

    def __getstate__(self):
        state = super().__getstate__()
        state["value"] = self.value
        state["for_column"] = self.for_column
        if hasattr(self, "name"):
            state["name"] = self.name
        return state

    def __hash__(self):
        try:
            return super().__hash__()
        except TypeError:
            state = self.__getstate__()
            state["value"] = id(self.value)
            return hash(tuple(sorted(tuple(state.items()))))

    def __eq__(self, other):
        return hash(self) == hash(other)


@dialect.register(True)
def TupleValueColumn(dialect, *values, for_column=None, encoder=None, names=None):
    if for_column:
        assert hasattr(for_column, "target") and len(for_column.target) == len(values)
    if encoder:
        assert len(encoder) == len(values)
    if names:
        assert len(names) == len(values)
    values = list(values)
    for i, v in enumerate(values):
        if not isinstance(v, AbstractColumn):
            values[i] = dialect.columns.ValueColumn(
                v,
                for_column=for_column[i] if for_column else None,
                encoder=encoder[i] if encoder else None,
                name=names[i] if names else None,
            )
    return dialect.columns.TupleColumn(*values)


@dialect.register(True)
class PlaceholderColumn(ValueColumn):
    """A placeholder, namely an SQL value column with implicit value.

    PARAMETERS
    ----------
    dialect : Dialect
            The SQL dialect to use.
    for_column : AbstractColumn or None, default=None
            A column targetted by the value column (_e.g._, when the intention is
            to insert the given value in a table, the corresponding table column is
            referenced here) or `None`.  If given, its "encoder" attribute, if any,
            is taken as fallback if the parameter `encoder` has value `None`.  In
            the same way, the value column is using the `for_column` "name"
            attribute, if any and if the parameter `name` has value `None`.
    sqltype : str or None, default=None
            The type (e.g. "int", "text" of the column).
    encoder : str or None
            A key of `encoderFunctions` to get the associated encoder and decoder.
            If not given, the parameter value might be taken from the attribute
            'encoder' of `for_column`, if given, if any.
    name : str or None
            The name of the value column.  If not given, the parameter value might be
            taken from the attribute 'name' of `for_column`, if given, if any.

    """

    def __init__(self, dialect, for_column=None, sqltype=None, encoder=None, name=None):
        super().__init__(
            dialect,
            dialect.constants.Placeholder,
            for_column=for_column,
            sqltype=sqltype,
            encoder=encoder,
            name=name,
        )
