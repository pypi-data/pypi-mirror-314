import abc, functools
from networkdisk import sql as ndsql
from networkdisk import sqlite as ndsqlite
from networkdisk.sql.schema import *


class SchemaTableColumn(ndsql.schema.SchemaTableColumn):
    typesMatching = {"date": "INTEGER"}


class Schema(ndsql.schema.Schema):
    @functools.wraps(ndsql.schema.Schema)
    def __init__(self, *args, sql=ndsqlite, **kwargs):
        super().__init__(*args, sql=sql, **kwargs)

    def add_schema(self, name, dbpath):
        if name in self.children:
            raise NetworkDiskSQLError(f"Conflict on schema name {name}")
        newsch = self.SchemaChildClasses["schema"](name, dbpath)
        self.children[name] = newsch
        return newsch

    @property
    def SchemaChildClasses(self):
        scc = super().SchemaChildClasses
        scc["schema"] = AttachedSchema
        return scc


class AttachedSchema(Schema):
    def __init__(self, name, dbpath, sql=ndsqlite):
        super().__init__(name=name, sql=sql)
        self.dbpath = dbpath

    def create_query(self):
        return self.dialect.queries.AttachDatabaseQuery(self.name, self.dbpath)

    def get_dependency_graph(self):
        dag = super().get_dependency_graph()
        deps = list(dag.nodes)
        dag.add_edges_from(((v, self) for v in deps))
        return dag

    @functools.wraps(Schema.add_table)
    def add_table(self, *args, **kwargs):
        tbl = super().add_table(*args, **kwargs)
        tbl.name = f"{self.name}.{tbl.name}"
        return tbl
