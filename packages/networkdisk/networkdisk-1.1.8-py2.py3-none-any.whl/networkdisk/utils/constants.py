import functools, itertools
from collections.abc import MutableMapping, Mapping, MutableSet
from networkdisk.exception import NetworkDiskSQLError


class Singletons(type):
    _instances = {}

    @functools.wraps(type.__call__)
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singletons, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class NotProvidedArg(metaclass=Singletons):
    pass


notProvidedArg = NotProvidedArg()


class DeactivatedFunctionReturn(metaclass=Singletons):
    pass


deactivatedFunctionReturn = DeactivatedFunctionReturn()


def IdentityFunction(e):
    return e


Projection0 = lambda e: e[0]
Projection1 = lambda e: e[1]
Projection2 = lambda e: e[2]
Projection3 = lambda e: e[3]


def IgnoreFunction(*args, **kwargs):
    pass


def TrueChecker(o):
    return True


def FalseChecker(o):
    return False


# Deactivate decorator
class Deactivate:
    def __init__(self, f, activated=False):
        self._function = f
        self._activated = activated

    # @functools.wraps(f)
    def __call__(self, *args, **kwargs):
        if self._activated:
            return f(*args, **kwargs)
        else:
            return deactivatedFunctionReturn


def activate(f, activated=True):
    if hasattr(f, "_activated"):
        f._activated = activate
    else:
        f = Deactivate(f, activated=activated)
    return f


def deactivate(f, activated=False):
    return activate(f, activated=activated)


class SymDict(MutableMapping):
    """
    A symmetric dictionary. Requires both keys and values to be
    hashable.
    """

    def __init__(self, E=(), **F):
        self.mapping = {}
        self.update(E, **F)

    def __getitem__(self, k):
        return self.mapping[k]

    def __setitem__(self, k, v):
        hash(v)
        self.mapping[k] = v
        self.mapping[v] = k

    def __delitem__(self, k):
        del self.mapping[k]

    def __len__(self):
        return len(self.mapping)

    def __iter__(self):
        return iter(self.mapping)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.mapping})"


class ProtectedDict(Mapping):
    def __init__(self):
        self.map = {}

    def __getitem__(self, k):
        return self.map[k]

    def __len__(self):
        return len(self.map)

    def __iter__(self):
        return iter(self.map)

    def __repr__(self):
        return f"{repr(self.map)}ₚ"


class BinRel(Mapping, MutableSet):
    def __init__(self, *E):
        self.left = ProtectedDict()
        self.right = ProtectedDict()
        self.update(*E)

    def __contains__(self, leftNright):
        left, right = leftNright
        return right in self.left.get(left, ())

    def __len__(self):
        return sum(map(len, self.left.values()))

    def __iter__(self):
        for k, v in self.left.items():
            for w in v:
                yield (k, w)

    def __getitem__(self, key):
        left = self.left.get(key, ())
        right = self.right.get(key, ())
        if not left and not right:
            raise KeyError(key)
        return left, right

    def __delitem__(self, key):
        target = (self.left, self.right)
        for i in range(2):
            res = target[i].map.pop(key, ())
            for r in res:
                s = target[i - 1][r]
                s.remove(key)
                if not s:
                    target[i - 1].map.pop(r)

    def add(self, leftNright):
        left, right = leftNright
        self.left.map.setdefault(left, set())
        self.left.map[left].add(right)
        self.right.map.setdefault(right, set())
        self.right.map[right].add(left)

    def discard(self, leftNright):
        left, right = leftNright
        if left not in self.left or right not in self.right:
            return
        self.left.map[left].discard(right)
        if not self.left.map[left]:
            del self.left.map[left]
        self.right.map[right].discard(left)
        if not self.right.map[right]:
            del self.right.map[right]

    def update(self, *E):
        for it in E:
            for k, v in it:
                self.add((k, v))

    def __repr__(self):
        return f"{{{', '.join('↔'.join(map(str, e)) for e in self)}}}"

    def union(self, other):
        # TODO: optimize?
        return BinRel(self, other)

    def keys(self):
        yield from self.left
        yield from filter(lambda k: k not in self.left, self.right)
