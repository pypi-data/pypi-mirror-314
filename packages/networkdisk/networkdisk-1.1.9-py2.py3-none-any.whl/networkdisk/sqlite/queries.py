import functools
import networkdisk.sql as ndsql
from .dialect import sqlitedialect as dialect
from networkdisk.sql.scope import ScopeValueColumns, InternalColumns, ExternalColumns

dialect = dialect.provide_submodule(__name__)

# added to ndsql.__all__
__all__ = [
    "SelectQuery",
    "GetPragmaQuery",
    "SetPragmaQuery",
    "AttachDatabaseQuery",
    "BeginTransactionQuery",
    "CommitTransactionQuery",
    "RollbackTransactionQuery",
    "SavepointQuery",
    "ReleaseSavepointQuery",
]


@dialect.register(True)
class SelectQuery(ndsql.queries.SelectQuery):
    def offset_subformat(self):
        return ""

    def limit_subformat(self):
        q = ""
        if self.limit:
            q = f"LIMIT {self.limit}"
            if self.offset:
                q += f" OFFSET {self.offset}"
        return q


# PRAGMAS
@dialect.register(True)
class GetPragmaQuery(ndsql.queries.ReadQuery):
    def __init__(self, dialect, key, sqltype):
        super().__init__(dialect)
        self.pragma = self.dialect.columns.QueryColumn(
            key, index_in_container=0, encoder=sqltype
        )

    def __getstate__(self):
        state = super().__getstate__()
        state.update(pragma=self.pragma)
        return state

    @property
    def external_columns(self):
        return ndsql.scope.ExternalColumns((self.pragma,))

    @ndsql.queries.nonscopable
    def subformat(self):
        return f"PRAGMA {self.pragma.qformat()}"


@dialect.register(True)
class SetPragmaQuery(ndsql.queries.AbstractQuery):
    def __init__(self, dialect, key, value, sqltype=None):
        super().__init__(dialect)
        if not isinstance(key, GetPragmaQuery):
            key = ReadPragmaQuery(key, sqltype)
        self.container = key
        self.value = self.dialect.columns.ValueColumn(
            value, for_column=self.container.pragma
        )

    def __getstate__(self):
        state = super().__getstate__()
        state.update(container=self.container, value=self.value)
        return state

    @ndsql.queries.nonscopable
    def subformat(self):
        # CANNOT PASS value AS ARGS
        value = self.value.encode(self.value.value)
        return f"{self.container.subformat()} = {value}"


# ATTACH
@dialect.register(True)
class AttachDatabaseQuery(ndsql.queries.AbstractQuery):
    def __init__(self, dialect, name, dbpath):
        super().__init__(dialect)
        self.name = name
        self.dbpath = dbpath

    def __getstate__(self):
        state = super().__getstate__()
        state.update(name=self.name, dbpath=self.dbpath)
        return state

    @ndsql.queries.nonscopable
    def subformat(self):
        return f'ATTACH DATABASE "{self.dbpath}" AS {self.name}'


# TRANSACTION
@dialect.register(True)
class BeginTransactionQuery(ndsql.queries.AbstractQuery):
    def __init__(self, dialect, mode=None):
        super().__init__(dialect)
        self.mode = mode

    def __getstate__(self):
        state = super().__getstate__()
        state.update(mode=self.mode)
        return state

    @ndsql.queries.nonscopable
    def subformat(self):
        mode = f" {self.mode}" if self.mode else ""
        return f"BEGIN{mode} TRANSACTION"


@dialect.register(True)
class CommitTransactionQuery(ndsql.queries.AbstractQuery):
    @ndsql.queries.nonscopable
    def subformat(self):
        return "COMMIT TRANSACTION"


@dialect.register(True)
class RollbackTransactionQuery(ndsql.queries.AbstractQuery):
    def __init__(self, dialect, to_savepoint=None):
        super().__init__(dialect)
        self.to_savepoint = to_savepoint

    def __getstate__(self):
        state = super().__getstate__()
        state.update(to_savepoint=self.to_savepoint)
        return state

    @ndsql.queries.nonscopable
    def subformat(self):
        to_savepoint = f" TO SAVEPOINT {self.to_savepoint}" if self.to_savepoint else ""
        return f"ROLLBACK TRANSACTION{to_savepoint}"


@dialect.register(True)
class SavepointQuery(ndsql.queries.AbstractQuery):
    def __init__(self, dialect, name):
        super().__init__(dialect)
        self.name = name

    def __getstate__(self):
        state = super().__getstate__()
        state.update(name=self.name)
        return state

    @ndsql.queries.nonscopable
    def subformat(self):
        return f"SAVEPOINT {self.name}"


@dialect.register(True)
class ReleaseSavepointQuery(SavepointQuery):
    @ndsql.queries.nonscopable
    def subformat(self):
        return f"RELEASE SAVEPOINT {self.name}"


# JSON1 related functions
@dialect.register(True)
class JsonEach(ndsql.queries.ReadQuery, ndsql.queries.FromQueryQuery):
    name = "json_each"

    def __init__(self, dialect, subquery, colspec, pattern=None):
        super().__init__(dialect, subquery)
        self.col = subquery.external_columns.unambiguous_get(colspec)
        self.pattern = pattern
        QC = dialect.columns.QueryColumn
        self._external_columns = ExternalColumns(
            [
                QC(
                    name="key",
                    index_in_container=0,
                    container_name=self.name,
                    sqltype="TEXT",
                ),
                QC(
                    name="value",
                    index_in_container=1,
                    container_name=self.name,
                    sqltype="TEXT",
                ),
                QC(
                    name="type",
                    index_in_container=2,
                    container_name=self.name,
                    encoder="IDENTITY",
                    sqltype="TEXT",
                ),
                QC(
                    name="atom",
                    index_in_container=3,
                    container_name=self.name,
                    encoder="IDENTITY",
                    sqltype="TEXT",
                ),
                QC(
                    name="id",
                    index_in_container=4,
                    container_name=self.name,
                    sqltype="INT",
                ),
                QC(
                    name="parent",
                    index_in_container=5,
                    container_name=self.name,
                    sqltype="INT",
                ),
                QC(
                    name="fullkey",
                    index_in_container=5,
                    container_name=self.name,
                    sqltype="INT",
                ),
                QC(
                    name="path",
                    index_in_container=5,
                    container_name=self.name,
                    sqltype="INT",
                ),
                QC(
                    name="json",
                    index_in_container=6,
                    container_name=self.name,
                    sqltype="JSON",
                ),
                QC(
                    name="text",
                    index_in_container=6,
                    container_name=self.name,
                    sqltype="TEXT",
                ),
            ]
        )

    @property
    def external_columns(self):
        return self._external_columns

    @functools.lru_cache(maxsize=None)
    @ndsql.queries.nonscopable
    def subformat(self, context=None):
        args = self.col.qformat(context=context)
        if self.pattern:
            args += f", {self.pattern}"
        return f"{self.name}({args})"

    def providing_subquery(self):
        return self.subquery

    def __getstate__(self):
        state = super().__getstate__()
        state.update(col=self.col, pattern=self.pattern)
        return state

    def select_query(self, *args, **kwargs):
        q = self.dialect.queries.SelectQuery(self, *args, **kwargs)
        q = q.add_subquery(self.providing_subquery())
        return q


class JsonTree(JsonEach):
    name = "json_tree"
