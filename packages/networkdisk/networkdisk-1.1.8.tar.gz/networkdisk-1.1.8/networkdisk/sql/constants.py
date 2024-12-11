"""Module containing SQL constants

An SQL-constant is a symbol that can be used with-in queries
constructions. Typically, NULL/* or the variable placeholder.

"""

import abc
from networkdisk.sql.dialect import sqldialect as dialect
from networkdisk.utils import Singletons

dialect = dialect.provide_submodule(__name__)

__all__ = ["Null", "Star", "Placeholder"]


class SQLConstant(abc.ABC):
    @abc.abstractmethod
    def sqlize(self):
        pass

    def __str__(self):
        return self.sqlize()

    def __repr__(self):
        return f"{self.__class__}<{self}>"

    def __call__(self, *args):
        return self

    def __getstate__(self):
        return {}

    def __setstate__(self, state):
        pass

    def __eq__(self, other):
        return self.sqlize() == other.sqlize()

    def __hash__(self):
        return hash((self.__class__.__name__, self.sqlize()))


class SQLNull(SQLConstant):
    def sqlize(self):
        return "NULL"


class SQLStar(SQLConstant):
    def sqlize(self):
        return "*"


class SQLPlaceholder(SQLConstant):
    def sqlize(self):
        #'?' is the default db paramater substitution
        # see `sqlite3.paramstyle`…
        # https://www.python.org/dev/peps/pep-0249/#paramstyle
        return "?"


class SQLNow(SQLConstant):
    def sqlize(self):
        return "'now'"


Null = SQLNull()
Star = SQLStar()
Placeholder = SQLPlaceholder()
Now = SQLNow()

dialect.register(False, Null=Null, Star=Star, Placeholder=Placeholder, Now=Now)
