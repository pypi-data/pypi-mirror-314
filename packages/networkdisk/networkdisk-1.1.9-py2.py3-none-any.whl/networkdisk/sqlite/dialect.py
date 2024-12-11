from networkdisk.sql.dialect import Dialect, sqldialect

sqlitedialect = Dialect("SQLite")
sqlitedialect.import_dialect(sqldialect)
