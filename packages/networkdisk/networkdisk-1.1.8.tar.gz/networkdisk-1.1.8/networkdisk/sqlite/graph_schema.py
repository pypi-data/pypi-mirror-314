"""SQLite subdialect override.

In sqlite3, the connector automatically decodes some value according to the
SQL type of its origin column.  This yields to unexpected behavior when
dealing with JSON-encoded columns.
>>> import sqlite3
>>> db = sqlite3.connect(':memory:')

In the following example, the TEXT-typed column is decoded as string (as
expected):
>>> _ = db.execute("CREATE TABLE A(t TEXT)")
>>> _ = db.executemany("INSERT INTO A(t) VALUES (?)", [(0,), ('0',), ('"0"',)])
>>> list(db.execute("SELECT t FROM A ORDER BY t"))
[('"0"',), ('0',), ('0',)]

In the following example, the JSON-typed column is decoded as int, when
possible, or as string otherwise:
>>> _ = db.execute("CREATE TABLE B(j JSON)")
>>> _ = db.executemany("INSERT INTO B(j) VALUES (?)", [(0,), ('0',), ('"0"',)])
>>> list(db.execute("SELECT j FROM B ORDER BY j"))
[(0,), (0,), ('"0"',)]

To avoid this weird uncontrolled behavior, we set the default type for node
column to "TEXT" but using a "JSON" encoder, rather than setting the column
type to "JSON".
"""

from .dialect import sqlitedialect as dialect

dialect = dialect.provide_submodule(__name__)

dialect.register(False, "TEXT", name="_default_node_type")
dialect.register(False, "JSON", name="_default_node_encoder")
dialect.register(False, "TEXT", name="_default_datakey_type")
dialect.register(False, "JSON", name="_default_datakey_encoder")
dialect.register(False, "TEXT", name="_default_datavalue_type")
dialect.register(False, "JSON", name="_default_datavalue_encoder")
