import itertools
from collections.abc import Mapping
from .constants import notProvidedArg
from networkdisk.exception import NetworkDiskError


class Scope(Mapping):
    """
    In `networkdisk.sql`, a `Scope` is an ordered structure that
    store hashable objects such that columns or queries. It is
    basically composed by a list and its inverse (from object to
    index) mapping, and another mapping, from object name to
    object tuples. The object `__getitem__` resolves keys,
    considering them, in order, as an object, an index, or an
    object name. Unnamed objects are associated to the pseudo
    name `unnamed_key` (which defaults to `'__unnamed'`).

    Class attribute:
    +	unnamed_key
            the pseudo name under which unnamed objects are classified;
            default is `'__unnamed'`.

    Instance attributes:
    +	byindex:
            a list of objects.
    +	byvalue:
            a mapping from objects to index, inverting `byindex`.
    +	byname:
            a mapping from object names to object tuples.
    """

    unnamed_key = "__unnamed"

    def __init__(self, objects):
        """
        +	objects
                iterable of objects
        """
        byindex = []
        byvalue = {}
        byname = {}
        for res in objects:
            byvalue.setdefault(res, [])
            byvalue[res].append(len(byindex))
            name = getattr(res, "name", self.unnamed_key)
            byname.setdefault(name, [])
            byname[name].append(res)
            byindex.append(res)
        self.byindex = tuple(byindex)
        self.byname = {k: tuple(v) for k, v in byname.items()}
        self.byvalue = {k: tuple(v) for k, v in byvalue.items()}

    def __getstate__(self):
        return dict(byindex=self.byindex, byvalue=self.byvalue, byname=self.byname)

    def __setstate__(self, state):
        for k, v in state.items():
            setattr(self, k, v)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.byindex[key]
        elif key in self.byvalue:
            return (key,)
        elif isinstance(key, int):
            try:
                return (self.byindex[key],)
            except IndexError as e:
                raise KeyError(key) from e
        else:
            return self.byname[key]

    def __len__(self):
        return len(self.byindex)

    def __iter__(self):
        return iter(self.byindex)

    def unambiguous_get(self, key, default=notProvidedArg):
        r = self.get(key, ())
        if len(r) > 1:
            raise NetworkDiskError(f"Ambiguous selection of {key} in scope")
        if r:
            return r[0]
        elif default is notProvidedArg:
            raise KeyError(key)
        else:
            return default

    def index(self, key):
        res = self.byvalue[self.unambiguous_get(key)]
        if len(res) > 1:
            raise NetworkDiskError(f"Ambiguous index for {key} in scope")
        return res[0]

    def indices(self, key):
        return sum((self.byvalue[c] for c in self[key]), ())

    def __hash__(self):
        if not hasattr(self, "_hash"):
            self._hash = hash(self.byindex)
        return self._hash

    def __add__(self, other):
        return self.__class__(itertools.chain(self, other))

    def __repr__(self):
        return f"{self.__class__.__name__}<{', '.join(map(str, self))}>"
