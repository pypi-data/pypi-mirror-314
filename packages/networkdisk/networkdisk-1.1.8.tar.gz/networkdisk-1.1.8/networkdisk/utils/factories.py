"""Is a factory necessarily a type, or could it be just a callable returning an instance of the right class?

We think the second choice is perfectly fine, but some networx's tests rely on the first choice.
Hence, the present module introduces a function decorator `to_typefactory`
which wraps a factory function in a type factory.
This allows to successfully test `isinstance(something, factory)`.
"""

from abc import ABC
from functools import wraps
from types import UnionType
from typing import Callable, Optional, TypeVar, overload

T = TypeVar("T")


@overload
def to_typefactory(
    func: Callable[..., T], /, types: type[T] | UnionType | tuple[type] | None = None
) -> type[T]: ...


@overload
def to_typefactory(
    func: None = None, /, types: type[T] | UnionType | tuple[type] | None = None
) -> Callable[[Callable[..., T]], type[T]]: ...


def to_typefactory(
    func: Callable[..., T] | None = None,
    /,
    types: type[T] | UnionType | tuple[type] | None = None,
) -> Callable[[Callable[..., T]], type[T]] | type[T]:
    """Either create a type factory from a function factory, or such a parametrized decorator.

    Parameters
    ----------
    func: Callable[..., T] | None = None
        the function factory to decorate.  If None, a parametrized decorator is return instead.
    types: Optional[type[T]] = None
        the return type of the factory, for allowing testing instance against the returned type
        factory with `isinstance` builtin.  If `None`, the return type is expected in the
        annoations of the function to decorate.

    Examples
    --------
    >>> @to_typefactory
    ... def factory(E=(), /, **F) -> dict:
    ...     return dict(E, **F)
    >>> isinstance(factory, type)
    True
    >>> isinstance(factory(), dict)
    True
    >>> isinstance({}, factory)
    True
    >>> isinstance(set(), factory)
    False
    >>> class MyDict(dict): ...
    >>> @to_typefactory(types=MyDict)
    ... def factory2(E=(), /, **F):
    ...     return MyDict(E, **F)
    >>> isinstance(factory2, type)
    True
    >>> isinstance(factory2(), MyDict)
    True
    >>> isinstance({}, factory2)
    False
    """

    def decorator(builder: Callable[..., T], /) -> type[T]:
        __types: type[T] | UnionType | tuple[type] = (
            types if types else builder.__annotations__["return"]
        )

        @wraps(builder.__call__)  # type: ignore #(got surprising '"Callable[..., T]" not callable' error)
        def __new__(cls, *args, **kwargs) -> T:
            return cls.__builder(*args, **kwargs)

        def __subclasshook__(cls, subclass: type) -> bool:
            return issubclass(subclass, cls.__types)

        name = f"_{builder.__name__}_typefactory"
        bases = (ABC,)
        namespace = dict(
            __new__=staticmethod(__new__),
            __subclasshook__=classmethod(__subclasshook__),
            __types=__types,
            __builder=builder,
            __doc__=f"Type factory wrapping {builder!r}",
        )

        t: type[T] = type(name, bases, namespace)
        return t

    if func:
        return decorator(func)
    return decorator
