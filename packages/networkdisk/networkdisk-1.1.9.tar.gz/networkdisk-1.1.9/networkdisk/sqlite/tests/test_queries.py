from networkdisk.sql.tests.test_queries import (
    TestColumn as SQLColumn,
    TestQuery as SQLQuery,
)
from networkdisk.sqlite import sqlitedialect


class TestColumn(SQLColumn):
    dialect = sqlitedialect


class TestQuery(SQLQuery):
    dialect = sqlitedialect
