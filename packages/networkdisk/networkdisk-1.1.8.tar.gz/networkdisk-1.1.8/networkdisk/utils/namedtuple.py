import collections


def custom_namedtuple(typename, field_names, defaults=(), module=None):
    T = collections.namedtuple(typename, field_names, module=module)
    T.__new__.__defaults__ = (None,) * len(T._fields)
    if isinstance(defaults, collections.Mapping):
        prototype = T(**defaults)
    else:
        prototype = T(*defaults)
    T.__new__.__defaults__ = tuple(prototype)
    return T


if "defaults" not in collections.namedtuple.__kwdefaults__:
    namedtuple = custom_namedtuple
else:
    namedtuple = collections.namedtuple
