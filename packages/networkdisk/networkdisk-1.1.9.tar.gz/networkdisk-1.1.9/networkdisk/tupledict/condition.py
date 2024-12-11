import abc, collections, functools, itertools
from networkdisk.exception import NetworkDiskSQLError
from networkdisk.utils.constants import SymDict, IdentityFunction


class ConditionObject(collections.abc.Callable):
    def columns(self):
        return ()

    def __repr__(self):
        return f"{self.__class__.__name__}〈{self}〉"

    @abc.abstractmethod
    def __str__(self):
        pass

    def __or__(self, other):
        if isinstance(other, TrueCondition):
            return other
        elif other is None or isinstance(other, FalseCondition):
            return self
        return DisjunctionCondition(self, other)

    def __and__(self, other):
        if isinstance(other, FalseCondition):
            return other
        elif other is None or isinstance(other, TrueCondition):
            return self
        return ConjunctionCondition(self, other)

    def __neg__(self):
        return NegationCondition(self)

    __pos__ = functools.partialmethod(IdentityFunction)

    def __getstate__(self):
        return {}

    def __setstate__(self, state):
        for k, v in state.items():
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
        return hash(tuple(sorted(self.__getstate__().items())))

    @abc.abstractmethod
    def __call__(self, t):
        pass


class EmptyCondition(ConditionObject):
    def __bool__(self):
        return False

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __str__(self):
        return "ε"

    def __and__(self, other):
        return other or self

    def __or__(self, other):
        return other or self

    def __neg__(self):
        return self

    def __call__(self, t):
        return True


class TrueCondition(ConditionObject):
    def __str__(self):
        return "⊤"

    def __and__(self, other):
        return other or self

    def __or__(self, other):
        return self

    def __neg__(self):
        return FalseCondition()

    def __call__(self, t):
        return True


class FalseCondition(ConditionObject):
    def __str__(self):
        return "⊥"

    def __and__(self, other):
        return self

    def __or__(self, other):
        return other or self

    def __neg__(self):
        return TrueCondition()

    def __call__(self, t):
        return False


class BinaryCondition(ConditionObject):
    """
    A `BinaryCondition` is an abstract condition that involves two
    selected columns (instances of `AbstractColumns`), referred as
    `left` and `right`.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __getstate__(self):
        state = super().__getstate__()
        state.update(left=self.left, right=self.right)
        return state


class CompareCondition(BinaryCondition):
    _operators = SymDict({"=": "!=", "<=": ">", ">=": "<", "is": "is not"})

    def __init__(self, left, right, operator="="):
        super().__init__(left, right)
        self.operator = operator

    @property
    def columns(self):
        return (self.left, self.right)

    def __neg__(self):
        negop = self._operators.get(self.operator, None)
        if negop is None:
            return super().__neg__()
        return self.build_from(operator=negop)

    def __getstate__(self):
        state = super().__getstate__()
        state.update(operator=self.operator)
        return state

    def __str__(self):
        return f"{self.left}{self.operator}{self.right}"

    def __call__(self, t):
        l, r = t[self.left], t[self.right]
        if self.operator == "=":
            return l == r
        if self.operator == "!=":
            return l != r
        if self.operator == "<":
            return l < r
        if self.operator == ">":
            return l > r
        if self.operator == "<=":
            return l <= r
        if self.operator == ">=":
            return l >= r
        if self.operator == "is":
            return l is r
        if self.operator == "is not":
            return l is not r
        else:
            raise ValueError(
                f"Unknown operator {self.operator} in {self.__class__.__name__}"
            )


def NullCondition(left):
    return CompareCondition(left, None, operator="is")


def NotNullCondition(left):
    return CompareCondition(left, None, operator="is not")


class InSetCondition(CompareCondition):
    """
    A variant of `CompareCondition` whose right column is replaced
    by a query. This condition express the `left` column value
    membership to the rows of the `right` query using the operator
    "IN".
    """

    _operators = SymDict({"in": "not in"})

    def __init__(self, left, container, negate=False):
        """
        +	left:
                tuple of indices or an index;
        +	container:
                any instance of a class implementing `__contains__`.
        +	negate:
                a Boolean that specifies whether the operator should be
                negated or not. If `False` (default) the operator is "in",
                otherwise it is "not in".
        """
        operator = "not in" if negate else "in"
        super().__init__(left, container, operator)

    @property
    def columns(self):
        return (self.left,)

    def __call__(self, t):
        l = t[self.left]
        return (self.operator == "in") == (l in self.right)

    def __str__(self):
        if self.operator == "in":
            return f"{self.left}∈{self.right}"
        return f"{self.left}∉{self.right}"


class NegationCondition(ConditionObject):
    def __init__(self, condition):
        self.subcondition = condition

    def __bool__(self):
        return bool(self.subcondition)

    @property
    def columns(self):
        return self.subcondition.columns

    def __neg__(self):
        return self.subcondition

    def __getstate__(self):
        state = super().__getstate__()
        state["subcondition"] = self.subcondition
        return state

    def __str__(self):
        return f"¬{super()}"

    def __call__(self, t):
        return not super().__call__(t)


class MultipleCondition(ConditionObject):
    """
    An abstract `ConditionObject` that involves an arbitrary
    number of sub-conditions, referred as `subconditions`.
    """

    def __init__(self, subconditions):
        self.subconditions = tuple(subconditions)

    def __getstate__(self):
        state = super().__getstate__()
        state["subconditions"] = self.subconditions
        return state


class ConjunctionCondition(MultipleCondition):
    _combinator = "AND"

    def __init__(self, *conditions):
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
        super().__init__(subconditions)

    @property
    def columns(self):
        return sum((subcond.columns for subcond in self.subconditions), ())

    def __neg__(self):
        return DisjunctionCondition(*(-sc for sc in self.subconditions))

    def __bool__(self):
        return bool(self.subconditions)

    def __str__(self):
        return f"{' ∧ '.join(f'({sc})' for sc in self.subconditions)}"

    def __call__(self, t):
        return all(sc(t) for sc in self.subconditions)


class DisjunctionCondition(ConjunctionCondition):
    _combinator = "OR"

    def __neg__(self):
        return ConjunctionCondition(*(-sc for sc in self.subconditions))

    def __str__(self):
        return f"{' ∨ '.join(f'({sc})' for sc in self.subconditions)}"

    def __call__(self, t):
        return any(sc(t) for sc in self.subconditions)
