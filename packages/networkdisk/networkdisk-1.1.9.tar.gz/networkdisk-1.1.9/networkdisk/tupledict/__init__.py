"""TupleDict: nested mapping representation.

A TupleDict is a representation of a dict-of-dict...-of-dict, or a
*recursive dict* of a given depth as a table of tuples, padded with None
values.

Typically, we want to represent the following recursive dictionary:

>>> dictofdict = {"a":{"b":{}, "c":{"d":3}}, "d":{}}

As the following dictionary:

>>> tupledict = {
... ("a", "b", None): None,
... ("a", "c", "d"): 3,
... ("d", None, None): None
... }

Such a transformation allows a simple representation of dict-(of-dict)*
within a tabular data-store.  Supporting all dict-like operations requires some
maintenance work that is provided in this current module.
"""

from .currying import fold, unfold, shorten_tuples, extend_tuple
from .condition import *
from .tools import tuple_sorted, padd, trim
from .permutations import Permutation
from .rekey_functions import SortFirstTwo, Identity
from .tupledict import BaseAbstractRowStore, ReadWriteAbstractRowStore
from .tupledict import ReadOnlyTupleDictView, ReadWriteTupleDictView, tupleDictFactory
