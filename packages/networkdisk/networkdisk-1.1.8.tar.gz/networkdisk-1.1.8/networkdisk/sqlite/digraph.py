from networkdisk.sqlite.dialect import sqlitedialect as dialect
from networkdisk import sql as ndsql
from networkdisk import sqlite as ndsqlite


@dialect.register(False)
class DiGraph(dialect.DiGraph, dialect.Graph):
    pass
