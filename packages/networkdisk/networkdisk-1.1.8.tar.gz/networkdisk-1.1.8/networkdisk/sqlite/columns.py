from .dialect import sqlitedialect as dialect
import sqlite3

dialect = dialect.provide_submodule(__name__)


@dialect.register(True)
def IfNullColumn(dialect, column, value):
    if not isinstance(value, dialect.columns.AbstractColumn.func):
        value = dialect.columns.ValueColumn(value, for_column=column)
    return dialect.columns.TransformColumn(
        "IFNULL", column, value, sqltype=column.sqltype, decoder=column.encoder
    )


if tuple(map(int, sqlite3.sqlite_version.split("."))) >= (3, 32, 0):

    @dialect.register(True)
    def IIFColumn(dialect, expression, left, right):
        if not isinstance(left, dialect.columns.AbstractColumn.func):
            left = dialect.columns.ValueColumn(left)
        if not isinstance(right, dialect.columns.AbstractColumn.func):
            right = dialect.columns.ValueColumn(right)
        return dialect.columns.TransformColumn("IIF", expression, left, right)
else:

    @dialect.register(True)
    def IIFColumn(dialect, expression, left, right):
        if not isinstance(left, dialect.columns.AbstractColumn.func):
            left = dialect.columns.ValueColumn(left)
        if not isinstance(right, dialect.columns.AbstractColumn.func):
            right = dialect.columns.ValueColumn(right)
        return dialect.columns.CaseColumn((expression, left), right)


@dialect.register(True)
class TupleColumn(dialect.TupleColumn.func):
    def inset(self, first, *other):
        """Override TupleColumn.inset for sqlite.

        In Sqlite "(a, b) IN ((1, 2), (3, 4))" is incorrect, so we need to use
        "(a, b) IN (VALUES (1, 2), (3, 4))" instead.
        """
        if not other:
            return super().inset(first)
        values = self.dialect.queries.ValuesQuery(first, *other)
        return super().inset(values)
