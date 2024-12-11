from networkdisk.sql.tests.test_tupledict import TupleDictSchema, TupleDict
from networkdisk.sqlite import sqlitedialect


class TestTupleDictSchema(TupleDictSchema):
    dialect = sqlitedialect


class TestTupleDict(TupleDict):
    path = ":memory:"
    dialect = sqlitedialect
