import pytest
from networkdisk.sql import sqldialect as dialect

PH_f = dialect.constants.Placeholder.sqlize()


class Test_ConditionClasses:
    def setup_method(self):
        self.vcolumns = list(map(dialect.columns.ValueColumn, range(4)))
        self.ec = dialect.conditions.EmptyCondition()

    def test_compare(self):
        vcols = self.vcolumns
        cond = dialect.conditions.CompareCondition(vcols[0], vcols[1])
        assert list(cond.columns) == vcols[0:2]
        out = f"{PH_f} = {PH_f}"
        assert cond.qformat() == out
        for operator in dialect.conditions.CompareCondition.func._operators:
            cond = dialect.conditions.CompareCondition(
                vcols[0], vcols[1], operator=operator
            )
            assert list(cond.columns) == vcols[0:2]
            out = f"{PH_f} {operator} {PH_f}"
            assert cond.qformat() == out
        cond = dialect.conditions.CompareCondition(
            vcols[0], vcols[1], operator="myoperator"
        )
        assert list(cond.columns) == vcols[0:2]
        out = f"{PH_f} myoperator {PH_f}"
        assert cond.qformat() == out

    def test_negation(self):
        pass

    def test_empty(self):
        ec = self.ec
        assert not ec and not -ec and not ec & ec and not ec | ec

    def test_conjunction(self):
        pass
        # with None

    def test_disjunction(self):
        pass
        # with None

    def test_inSet(self):
        pass
        # WITH QUERY

    def test_complex(self):
        # TODO: one nested complex condition
        pass

    # Class initializer wrappers
    def test_null(self):
        pass

    def test_inValueSet(self):
        pass


class Test_ConditionOperations:
    def setup_method(self):
        self.vcolumns = list(map(dialect.columns.ValueColumn, range(4)))

    def test_and(self):
        pass

    def test_or(self):
        pass

    def test_neg(self):
        """
        Unlike `test_negation`, this does not specifically test the
        `NegationCondition` objects, but tests all condition objects
        against the `__neg__` operation.
        Notice that `__neg__` follows an “as flat as possible”
        philosophy whence over unnecessarily-deep conditions, it is
        not a involution (but some of its iteration is). Indeed,
        `-(-Cond)` is not more complex (≡ deep) than `-Cond`. Hence,
        applying an even number of times the `__neg__` operation on
        a condition might simplify it.
        """
        vcols = self.vcolumns

        def _aux_negation(
            condPos, condNeg=dialect.conditions.EmptyCondition(), hard_involution=False
        ):
            condNeg = condNeg or -condNeg
            condNegNeg = -condNeg
            assert condPos is not condNeg  # negation does not intersect hard identity
            if hard_involution:
                # negation is hardly involutive
                assert condNegNeg is condPos
            elif hard_involution is not None:
                # negation is softly involutive
                assert type(condNegNeg) is type(condPos)
                assert list(condNegNeg.columns) == list(condPos.columns)
                assert condNegNeg.qformat() == condPos.qformat()
            else:
                # negation is not (even softly) involutive, but negationⁿ is softly involutive for some n
                i = 0
                pos = condPos
                neg = condNeg
                negneg = condNegNeg
                while negneg.qformat() != pos.qformat():
                    i += 1
                    assert negneg.columns == pos.columns
                    pos = neg
                    neg = negneg
                    negneg = -negneg
                assert type(negneg) is type(pos)
                assert negneg.columns == condPos.columns
            assert condPos.columns == condNeg.columns  # negation preserves columns
            assert (
                condPos.qformat() != condNeg.qformat()
            )  # qformat∘negation does not intersect soft identity

        # CompareCondition
        def _aux_negation_compare(
            condPos, condNeg=dialect.conditions.EmptyCondition(), right=PH_f, **kwargs
        ):
            condNeg = condNeg or -condPos
            _aux_negation(condPos, condNeg, **kwargs)
            opPos = condPos.operator
            outPos = f"{PH_f} {opPos} {right}"
            assert condPos.qformat() == outPos
            if opPos in condPos._operators:
                # flat negation, using negated operator
                opNeg = condNeg.operator
                assert type(condPos) is type(condNeg)
                assert opPos != opNeg
                assert opPos == condNeg._operators[opNeg]
                assert opNeg == condPos._operators[opPos]
                outNeg = f"{PH_f} {opNeg} {right}"
            else:
                # deep negation, using NegationCondition class
                assert type(condNeg) is dialect.conditions.NegationCondition.func
                outNeg = f"NOT {outPos}"
            assert condNeg.qformat() == outNeg

        condPos = dialect.conditions.CompareCondition(
            vcols[0], vcols[1]
        )  # default operator
        _aux_negation_compare(condPos)
        for operator in dialect.conditions.CompareCondition.func._operators:
            condPos = dialect.conditions.CompareCondition(
                vcols[0], vcols[1], operator=operator
            )  # operator from class _operators
            _aux_negation_compare(condPos)
        compPos = dialect.conditions.CompareCondition(
            vcols[0], vcols[1], operator="myNewOperator"
        )  # “unknown” operator
        compNeg = -compPos  # for later use
        _aux_negation_compare(compPos, compNeg, hard_involution=True)
        # InQuerySetCondition
        vq = dialect.queries.ValuesQuery(*vcols[1:])
        condPos = dialect.conditions.InQuerySetCondition(vcols[0], vq)
        _aux_negation_compare(condPos, right=vq.subformat(scoped=True))
        # ConjunctionCondition
        condPos = dialect.conditions.ConjunctionCondition(compNeg, compPos)
        condNeg = -condPos
        _aux_negation(condPos, condNeg)
        assert (
            type(condNeg) is dialect.conditions.DisjunctionCondition.func
        )  # flat negation
        assert condPos.qformat() == f"{compNeg.qformat()} AND {compPos.qformat()}"
        assert condNeg.qformat() == f"{compPos.qformat()} OR {compNeg.qformat()}"
        # DisjunctionCondition
        condPos = dialect.conditions.DisjunctionCondition(compNeg, compPos)
        condNeg = -condPos
        _aux_negation(condPos, condNeg)
        assert (
            type(condNeg) is dialect.conditions.ConjunctionCondition.func
        )  # flat negation
        assert condPos.qformat() == f"{compNeg.qformat()} OR {compPos.qformat()}"
        assert condNeg.qformat() == f"{compPos.qformat()} AND {compNeg.qformat()}"
        # NegationCondition
        condPos = dialect.conditions.NegationCondition(compPos)
        condNeg = -condPos
        _aux_negation(condPos, condNeg, hard_involution=None)
        assert condPos.qformat() == f"NOT {compPos.qformat()}"
        assert condNeg.qformat() == f"{compPos.qformat()}"
