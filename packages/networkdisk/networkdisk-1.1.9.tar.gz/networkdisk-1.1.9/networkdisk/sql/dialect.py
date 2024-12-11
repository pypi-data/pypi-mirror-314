"""Module providing the `Dialect` class and an instance of the SQL Dialect.

A (SQL) Dialect is a representation of the SQL language.
The instance object `dialect` define in this module will be use
to register classes and functions useful to define complex SQL Queries.

The dialect can be forked to be adapted to specific SQL Dialect (SQLite, PostgreSQL).
See the module `sqlite/dialect.py` for an adaptation to SQLite.

NOTES
-----
        The order of import of in the super module is important.
        The object dialect have to be imported before the modules
        using it.

"""

import functools, itertools
import networkdisk.utils as ndutls


class Dialect(ndutls.AttrDict):
    """A mapping class to gather dialect-aware SQL constructors.

    This class inherit from `AttrDict` (see `networkdisk.utils.AttrDict`).
    An AttrDict object allows to switch between mapping and object notation.
    The main methods of the Dialect class is the possibility to registers
    new elements to it. See the ``register`` method for details.
    A dialect can have sub-dialect (which are dialect themself). It should
    be think as a tree-shape datastructure to store SQL Builders methods.

    PARAMETERS
    ----------
    name: str
            The name of the dialect, will be used for serialization and to find the
            dialect.

    dialect: Dialect or None
            The parent Dialect. If None, the dialect is the root Dialect.

    ATTRIBUTES
    ----------
    reserved_names
    name: str
            The name of the dialect, will be used for serialization and to find the
            dialect.
    dialect: Dialect
            The parent Dialect or the dialect itself if root.

    EXAMPLES
    --------
    We can registers functions, class or object. It is often the case
    that the function we want to register depends them self of the dialect.
    We then say that they are dialectable.

    The basic usage is the following.

    >>> dialect = Dialect('foo')
    >>> def f(*args):
    ...		print(*args)
    >>> f2 = dialect.register(True, f) # return the decored function

    The function `f2` is actually simply the function itself

    >>> f2 == f
    True

    >>> dialect.f(1, 2, 3)
    Dialect(foo)<f> 1 2 3

    The function `dialect.f` is a decored variant of `f` if the function
    is dialectable.

    >>> dialect.f == f
    False

    We can access the original function:

    >>> dialect.f.func == f
    True


    >>> decored_f = dialect.register(False, f)
    >>> f2 = dialect.f(1, 2, 3)
    1 2 3

    In this case, the function in the dialect is exactly the initial function:

    >>> dialect.f == f
    True

    We can name the function as we want:

    >>> decored_f = dialect.register(False, f, name="bar")
    >>> dialect.bar(1, 2, 3)
    1 2 3

    The dialect pretty print its methods:

    >>> print(dialect)
    Dialect(foo)<f, bar>

    If no object is provided, it returns a function decorator.
    Thus we can use:

    >>> @dialect.register(True)
    ... def g(*args):
    ...		print(*args)
    >>> dialect.g(1, 2, 3)
    Dialect(foo)<f, bar, g> 1 2 3

    We can also set the function as not dialectable
    with the decorator:

    >>> @dialect.register(False)
    ... def h(*args):
    ...		print(*args)
    >>> dialect.h(1, 2, 3)
    1 2 3

    NOTES
    -----------
    Subdialect.

    """

    _dialects = {}

    @functools.wraps(ndutls.AttrDict.__init__)
    def __init__(self, name, dialect=None):
        if dialect is None:
            if name in self._dialects:
                raise ValueError(f"Dialect named '{name}' already exists")
            self._dialects[name] = self
        super().__init__()
        self.name = name
        self.dialect = dialect

    def import_dialect(self, dialect):
        root_dialect = self.get_root_dialect()
        for k in dialect:
            v = dialect[k]
            if isinstance(v, Dialect):
                subdialect = self.__class__(v.name, dialect=self)
                subdialect.import_dialect(v)
                v = subdialect
            elif isinstance(v, functools.partial) and v.args:
                v = functools.partial(v.func, root_dialect, *v.args[1:], **v.keywords)
            self[k] = v

    def register(self, dialectable=None, *objects, name=None, **kwargs):
        """Registers objects or returns a decorator for registering an object at its definition.

        The main method of the dialect.

        Parameters
        ----------
        dialectable: None | bool
                Either `None` or a Boolean indicating whether the objects
                to register are callable and expect the dialect as first
                argument. In this case, the resulting object pointed by
                the dialect is a partial (`functools.partial`), in which
                the first argument is set to `self`, namely the dialect.
                Otherwise the object might be any python object, not
                necessarily callable. If `None`, then the parameter value
                defaults to `True` if all given objects (from `objects`
                and `kwargs`) are callable, or to `False` otherwise.

        name: str
                specify the name of the objects to register. When given
                many positional objects (within `objects`), all will be
                associate with the same name, whence only the last one
                will be saved. This is thus not an interesting case.
                However, when given one positional argument only, the name
                for that positional argument is set to `name` instead of
                its `'__name__'` attribute, which possibly does not exist.
                This behavior can be obtained using a keyworded argument.
                Above all, the parameter `name` is useful, when using the
                method as a class or function decorator, as it allows to
                save the defined object under a different name. Default
                value is `None`, meaning that the `'__name__'` attribute
                value of each objects from `object` or decorated is taken.

        objects, kwargs:
                the objects to decorate. If none are given then the method
                returns a decorator, for decorating an single object.
                Otherwise, each object is registered within the dialect.
                Unnamed objects (namely, from `objects`) are either named
                by `name`, if given, or by their respective `'__name__'`
                attribute value otherwise. On contrast, named objects
                (namely, from `kwargs`) are named according to their key.
                This in particular allows to register objects that do not
                have the `'__name__'` attribute.


        """
        root_dialect = self.get_root_dialect()
        if dialectable is None:
            dialectable = all(map(callable, itertools.chain(objects, kwargs.values())))

        def decorator(obj, name=name):
            if dialectable:
                over = functools.partial(obj, root_dialect)
                over.__doc__ = obj.__doc__
            else:
                over = obj
            oname = name or obj.__name__
            self[oname] = over
            return obj

        if objects or kwargs:
            kwargs.update((name or o.__name__, o) for o in objects)
            for name, obj in kwargs.items():
                decorator(obj, name=name)
            return obj
        return decorator

    def provide_submodule(self, submodule_name):
        submodule_name = submodule_name.rsplit(".", maxsplit=1)[-1]
        if self.is_reserved_name(submodule_name):
            raise ValueError(
                f"Cannot register submodule of reserved name {submodule_name}"
            )
        self.setdefault(submodule_name, self.__class__(submodule_name, dialect=self))
        return self[submodule_name]

    def register_partial_dialectable(self, callable_obj, name, *args, **kwargs):
        over = functools.partial(callable_obj, self, *args, **kwargs)
        over.__doc__ = callable_obj.__doc__
        self[name] = over

    def is_reserved_name(self, name):
        return name in self.reserved_names or hasattr(self.__class__, name)

    def get_root_dialect(self):
        if self.dialect:
            return self.dialect.get_root_dialect()
        else:
            return self

    def __repr_name__(self):
        n = [self.name]
        d = self
        while d.dialect:
            d = d.dialect
            n.append(d.name)
        return ".".join(reversed(n))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__repr_name__()})<{', '.join(self)}>"

    def __iter__(self):
        return (k for k in super().__iter__() if not self.is_reserved_name(k))

    def __setitem__(self, k, v):
        if self.is_reserved_name(k):
            raise ValueError(f"Cannot set item with reserved key {k}")
        super().__setitem__(k, v)

    def __delitem__(self, k):
        if self.is_reserved_name(k):
            raise ValueError(f"Cannot delete item with reserved key {k}")
        super().__delitem__(k)

    @property
    def reserved_names(self):
        return ("name", "dialect")

    def __hash__(self):
        return hash(self.__repr_name__())


sqldialect = Dialect("SQL")
