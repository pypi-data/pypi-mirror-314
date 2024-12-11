from networkdisk.sql.dialect import Dialect, dialect as sqldialect

dialect = Dialect("Oracle")
dialect.import_dialect(sqldialect)
