import functools
from .dialect import sqlitedialect as dialect

subdialect = dialect.provide_submodule(__name__)


@subdialect.register(True)
class ReadOnlyTupleDictSchema(dialect.tupledict.ReadOnlyTupleDictSchema.func):
    @functools.wraps(dialect.tupledict.ReadOnlyTupleDictSchema.func.select_row_query)
    def select_row_query(self, cols=None, count=False, distinct=False, **kwargs):
        if not count or cols is None or len(cols) < 2:
            return super().select_row_query(
                cols=cols, count=count, distinct=distinct, **kwargs
            )
        else:
            q = super().select_row_query(cols=cols, distinct=distinct, **kwargs)
            q = self.dialect.queries.SelectQuery(
                q,
                columns=self.dialect.columns.CountColumn(
                    self.dialect.columns.ValueColumn(1)
                ),
            )
        return q


@subdialect.register(True)
class ReadWriteTupleDictSchema(
    ReadOnlyTupleDictSchema, dialect.tupledict.ReadWriteTupleDictSchema.func
):
    pass
