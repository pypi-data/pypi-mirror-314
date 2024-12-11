from networkdisk.sql.tests.test_schema import Schema, SchemaHelper
from networkdisk.sqlite import sqlitedialect


class TestSchema(Schema):
    dialect = sqlitedialect


class TestSchemaHelper(SchemaHelper):
    path = ":memory:"
    dialect = sqlitedialect
