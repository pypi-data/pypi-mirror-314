import collections, itertools
# TODO: see dataclass (that requires python 3.7)


class Attributes:
    def __new__(cls, *attrnames, **attrdefaults):
        self = super().__new__(cls)
        self.names = attrnames + tuple(k for k in attrdefaults if k not in attrnames)
        self.defaults = attrdefaults
        return self

    @classmethod
    def build_from(cls, *args, **kwargs):
        names = []
        defaults = {}
        for x in args:
            # x is either an instance or an required attribute name
            xnames = getattr(x, "required", (x,))
            xdefaults = getattr(x, "defaults", {})
            for n in xnames:
                if n not in names:
                    names.append(n)
            for n, v in xdefaults.items():
                defaults[n] = v
        defaults.update(kwargs)
        return cls.__new__(cls, *names, **defaults)

    @property
    def required(self):
        return tuple(n for n in self.names if n not in self.defaults)

    def __repr__(self):
        defaults = (f"{k}={v}" for k, v in self.defaults.items())
        args = ", ".join(itertools.chain(self.required, defaults))
        return f"{self.__class__.__name__}<{args}>"


class DataClass:
    """Naive and minimal implementation of dataclass-ish.

    Introduced in Python 3.7, dataclass are convenient
    interface to store some attributes either as dict
    or with object notation.

    See ``here <https://docs.python.org/3.7/library/dataclasses.html>``_
    for more informations.

    Overloading `__attributes__` allows to defined required and optional
    arguments.

    Example:
    --------
    >>> class MyClass(nd.utils.DataClass):
    ...		__attributes__ = nd.utils.Attributes("Age", "Name", status="Happy")
    >>> M = MyClass(18, "Smith")
    >>> M
    MyClass〈Age=10, Name=Smith, status=Unhappy >
    >>> M.Age
    10
    >>> M.Name
    'Smith'

    """

    __attributes__ = Attributes()

    def __init__(self, *args, **kwargs):
        state = dict(self.__attributes__.defaults)
        required = self.__attributes__.required
        missing = [n for n in self.__attributes__.defaults if n not in kwargs]
        for i, a in enumerate(args):
            if i < len(required):
                state[required[i]] = a
            else:
                state[missing.pop(0)] = a
        state.update(kwargs)
        self.__setstate__(state)
        self.__post_init__()

    def __setstate__(self, state):
        for k in self.__attributes__.names:
            v = state.pop(k)
            object.__setattr__(self, k, v)
        if state:
            raise ValueError(
                f"Unexpected attribute {', '.join(state)} for {self.__class__.__name__}"
            )

    def __getstate__(self):
        return {k: getattr(self, k) for k in self.__attributes__.names}

    def hash(self):
        return tuple(sorted(self.__getstate__().items()) + (self.__class__.__name__,))

    @classmethod
    def build_from(cls, *instances, **kwargs):
        state = {}
        for inst in instances:
            state.update(inst.__getstate__())
        state = {k: v for k, v in state.items() if k in cls.__attributes__.names}
        state.update(kwargs)
        return cls(**state)

    def __post_init__(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}〈{', '.join(f'{k}={getattr(self, k)}' for k in self.__attributes__.names)} 〉"
