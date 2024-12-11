import networkdisk.sql as ndsql
from .dialect import dialect

dialect = dialect.provide_submodule(__name__)

__all__ = ["DummyQuery"]


@dialect.register(True)
class DummyQuery(ndsql.queries.DummyQuery):
    def __init__(self, dialect):
        super().__init__(dialect)
        self.name = "dual"
        dummycol = dialect.schema.SchemaTableColumn(
            "dummy", self.name, 0, sqltype="VARCHAR2", encoder="TEXT"
        )
        self._external_columns = ExternalColumns((dummycol,))

    def is_dummy(self):
        return False
