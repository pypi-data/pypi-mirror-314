import abc, functools
from .dialect import sqldialect as dialect
import networkdisk.sql.scope

dialect = dialect.provide_submodule(__name__)

__all__ = [
    "DefaultConstraint",
    "NotnullConstraint",
    "UniqueConstraint",
    "PrimarykeyConstraint",
    "ForeignkeyConstraint",
    "TablePrimarykeyConstraint",
    "TableUniqueConstraint",
    "TableForeignkeyConstraint",
]


@dialect.register(True)
class SchemaConstraint(abc.ABC):
    def __init__(self, dialect, name=None):
        self.name = name
        self.dialect = dialect

    def __init_subclass__(cls):
        orig_qformat = cls.qformat

        @functools.wraps(orig_qformat)
        def decored_qformat(self, *args, **kwargs):
            if self.name:
                return f"CONSTRAINT {self.name} {orig_qformat(self, *args, **kwargs)}"
            return orig_qformat(self, *args, **kwargs)

        setattr(cls, "qformat", decored_qformat)

    @abc.abstractmethod
    def qformat(self):
        pass

    def get_schema_containers(self):
        yield from ()

    def get_subargs(self):
        return scope.ScopeValueColumns()

    def get_with_queries(self):
        return {}

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.qformat()}>"

    def __getstate__(self):
        return dict(dialect=self.dialect.name, name=self.name)

    def __setstate__(self, state):
        for k, v in state.items():
            if k == "dialect":
                v = dialect._dialects[v]
            setattr(self, k, v)

    def __hash__(self):
        return hash(
            tuple(sorted(self.__getstate__().items())) + (self.__class__.__name__,)
        )

    def __eq__(self, other):
        try:
            return hash(self) == hash(other)
        except TypeError:
            return False


@dialect.register(True)
class CheckConstraint(SchemaConstraint):
    def __init__(self, dialect, condition, name=None):
        super().__init__(dialect, name=name)
        self.condition = condition

    def __getstate__(self):
        d = super().__getstate__()
        d.update(dict(condition=self.condition))
        return d

    def qformat(self):
        return f"CHECK ({self.condition.qformat()})"

    def get_schema_containers(self):
        yield from super().get_schema_containers()
        yield from self.condition.get_schema_containers()

    def get_subargs(self):
        return self.condition.get_subargs()

    def get_with_queries(self):
        return condition.get_with_queries()

    def get_schema_containers(self):
        yield from super().get_schema_containers()
        yield from self.condition.get_schema_containers()


@dialect.register(True)
class ConflictableConstraint(SchemaConstraint):
    base_constraint = ""

    def __init__(self, dialect, on_conflict=None, name=None):
        super().__init__(dialect, name=name)
        self.on_conflict = on_conflict

    def __getstate__(self):
        d = super().__getstate__()
        d.update(dict(on_conflict=self.on_conflict))
        return d

    def on_conflict_format(self):
        if self.on_conflict:
            return f"ON CONFLICT {self.on_conflict}"
        else:
            return ""


@dialect.register(True)
class OnColumnsConstraint(SchemaConstraint):
    base_constraint = ""

    def __init__(self, dialect, *columns, name=None):
        if not columns:
            raise NetworkDiskSQLError(
                f"At least one column expected for {self.__class__.__name__}"
            )
        super().__init__(dialect, name=name)
        self.columns = columns

    def on_column_format(self):
        return (
            f"{self.base_constraint} ({', '.join(c.qformat() for c in self.columns)})"
        )

    def __getstate__(self):
        d = super().__getstate__()
        d.update(dict(columns=self.columns))
        return d


# COLUMN SPECIFIC CONSTRAINTS


class ColumnSpecificConstraint(ConflictableConstraint):
    def qformat(self):
        return " ".join(filter(bool, (self.base_constraint, self.on_conflict_format())))


@dialect.register(True)
class DefaultConstraint(SchemaConstraint):
    def __init__(self, dialect, default, name=None):
        super().__init__(dialect, name=name)
        self.default = default

    def qformat(self):
        return f"DEFAULT ({self.default.qformat()})"

    def get_subargs(self):
        return self.default.get_subargs()


@dialect.register(True)
class NotnullConstraint(ColumnSpecificConstraint):
    base_constraint = "NOT NULL"


@dialect.register(True)
class UniqueConstraint(ColumnSpecificConstraint):
    base_constraint = "UNIQUE"


@dialect.register(True)
class PrimarykeyConstraint(ColumnSpecificConstraint):
    base_constraint = "PRIMARY KEY"

    def __init__(
        self, dialect, order=None, on_conflict=None, autoincrement=False, name=None
    ):
        super().__init__(dialect, on_conflict=on_conflict, name=name)
        if order:
            self.base_constraint += f" {order}"
        self.autoincrement = autoincrement

    def qformat(self):
        frmt = super().qformat()
        if self.autoincrement:
            return f"{frmt} AUTOINCREMENT"
        return frmt

    def __getstate__(self):
        d = super().__getstate__()
        d.update(
            dict(base_constraint=self.base_constraint, autoincrement=self.autoincrement)
        )
        return d


@dialect.register(True)
class ForeignkeyConstraint(SchemaConstraint):
    def __init__(
        self,
        dialect,
        *references,
        container=None,
        on_delete=None,
        on_update=None,
        deferrable=None,
        initially_deferred=None,
        name=None,
    ):
        super().__init__(dialect, name=name)
        self.references = references
        self.container = container
        self.on_delete = on_delete
        self.on_update = on_update
        if initially_deferred is None and deferrable is not None:
            initially_deferred = False
        self.initially_deferred = initially_deferred
        if initially_deferred is not None and deferrable is None:
            deferrable = True
        self.deferrable = deferrable

    def __getstate__(self):
        d = super().__getstate__()
        d.update(
            dict(
                references=self.references,
                container=self.container,
                on_delete=self.on_delete,
                on_update=self.on_update,
                deferrable=self.deferrable,
                initially_deferred=self.initially_deferred,
            )
        )
        return d

    def qformat(self):
        l = []
        l.append("REFERENCES")
        cols = ", ".join(ref.qformat() for ref in self.references)
        if self.container:
            cont = getattr(self.container, "name", self.container)
            if cols:
                l.append(f"{cont}({cols})")
            else:
                l.append(cont)
        elif cols:
            l.append(f"({cols})")
        if self.on_delete:
            l.append(f"ON DELETE {self.on_delete}")
        if self.on_update:
            l.append(f"ON UPDATE {self.on_update}")
        # TODO: NOT IMPLEMENTED: "MATCH name"
        if self.deferrable is not None:
            if self.deferrable is False:
                l.append("NOT")
            l.append("DEFERRABLE")
            if self.initially_deferred is not None:
                l.append("INITIALLY")
                if self.initially_deferred:
                    l.append("DEFERRED")
                else:
                    l.append("IMMEDIATE")
        return " ".join(l)


# TABLE SPECIFIC CONSTRAINTS
@dialect.register(True)
class TablePrimarykeyConstraint(OnColumnsConstraint, ConflictableConstraint):
    base_constraint = "PRIMARY KEY"

    def __init__(self, dialect, *columns, on_conflict=None, name=None):
        dialect.constraints.OnColumnsConstraint.func.__init__(
            self, dialect, *columns, name=name
        )
        dialect.constraints.ConflictableConstraint.func.__init__(
            self, dialect, on_conflict=on_conflict, name=name
        )

    def qformat(self):
        l = []
        l.append(self.on_column_format())
        l.append(self.on_conflict_format())
        return " ".join(filter(bool, l))


@dialect.register(True)
class TableUniqueConstraint(TablePrimarykeyConstraint):
    base_constraint = "UNIQUE"


@dialect.register(True)
class TableForeignkeyConstraint(ForeignkeyConstraint, OnColumnsConstraint):
    base_constraint = "FOREIGN KEY"

    def __init__(self, dialect, *references, container=None, name=None, **kwargs):
        columns = tuple(ref[0] for ref in references)
        references = tuple(ref[1] for ref in references)
        dialect.constraints.ForeignkeyConstraint.func.__init__(
            self, dialect, *references, container=container, name=name, **kwargs
        )
        dialect.constraints.OnColumnsConstraint.func.__init__(
            self, dialect, *columns, name=name
        )

    def qformat(self):
        return f"{self.on_column_constraint} {super().qformat()}"
