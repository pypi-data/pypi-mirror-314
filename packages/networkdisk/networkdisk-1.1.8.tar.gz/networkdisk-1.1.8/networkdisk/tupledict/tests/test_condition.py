import pytest
import networkdisk.tupledict as ndtd


class Test_condition:
    def test_empty(self):
        cond = ndtd.EmptyCondition()
        assert cond((3, 4, 5))
        assert cond(())
        assert cond((0, 0, 1))
        assert cond(("Dark", "side", "of", "the", "Moon"))
        assert (-cond) is cond
        assert (cond & None) is cond
        assert (cond | None) is cond
        assert (cond & cond) is cond
        assert (cond | cond) is cond

    def test_compare(self):
        cond = ndtd.CompareCondition(0, 1, "=")
        assert cond((0, 0, 1, 2))
        assert cond((1, 1, 1))
        assert cond((42, 42, 0, "foo", "bar"))
        assert cond((None, None, True))
        assert cond((True, 1, False, True, 3))
        assert cond(("a" * 42, "aa" * 21, None))
        assert not cond((0, 1, "foo", "bar"))
        assert not cond((1, 0, "bem", "bing"))
        assert not cond((False, True, 3))
        #
        cond = ndtd.CompareCondition(1, 2, "<=")
        assert cond((0, 0, 1, 2))
        assert cond((1, 1, 1))
        assert not cond((42, 42, 0, "foo", "bar"))
        with pytest.raises(TypeError):
            cond((None, None, True))
        assert cond((3, "a" * 42, "aa" * 21, None))
        assert cond((None, True, 1, False, True, 3))
        assert cond((0, "1", "foo", "bar"))
        assert cond((0, "5", "foo", "bar"))
        with pytest.raises(TypeError):
            cond((8, 12, "foo", "bar"))
        assert cond((1, 0, 3, "bem", "bing"))
        assert not cond((1, 0, -1, "bem", "bing"))
        assert cond((False, True, 3))
        #
        # …

    def test_inset(self):
        cond = ndtd.InSetCondition(2, range(3, 8))
        assert cond((0, 1, 4, 7, True, [False, "foo", "bar"]))
        assert cond((0, 0, 4))
        assert not cond((0, 1, 2))
        with pytest.raises(IndexError):
            cond((0, 1))
        with pytest.raises(IndexError):
            cond(())

    def test_negation(self):
        pass

    def test_and(self):
        pass

    def test_or(self):
        pass

    def test_boolean_combination(self):
        pass
