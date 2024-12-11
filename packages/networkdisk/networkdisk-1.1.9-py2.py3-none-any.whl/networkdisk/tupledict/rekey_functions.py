from collections.abc import Callable


class RekeyFunction(Callable):
    def __getstate__(self):
        return {}

    def __setstate__(self, state):
        pass

    def __hash__(self):
        return hash(("RekeyFunction", self.__class__.__name__))


class SortFirstTwo(RekeyFunction):
    def __call__(self, t):
        return (*sorted(t[:2]), *t[2:])


class Identity(RekeyFunction):
    def __call__(self, t):
        return t
