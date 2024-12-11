import sqlite3, functools
from networkdisk.exception import NetworkDiskBackendTypeError, NetworkDiskBackendError
from networkdisk import sql as ndsql
from networkdisk import sqlite as ndsqlite
from networkdisk.utils import Attributes
from networkdisk.sqlite.dialect import sqlitedialect as dialect

sqlite_masters = []
for sqlite_table in ("sqlite_master", "sqlite_temp_master"):
    table = dialect.schema.SchemaTable(sqlite_table)
    table.add_column("type", sqltype="TEXT", encoder="identity")
    table.add_column("name", sqltype="TEXT", encoder="identity")
    table.add_column("tbl_name", sqltype="TEXT", encoder="identity")
    table.add_column("rootpage", sqltype="INTEGER")
    table.add_column("sql", sqltype="TEXT", encoder="identity")
    sqlite_masters.append(table)

get_pragma_fk_query = dialect.queries.GetPragmaQuery("foreign_keys", "BOOL")
get_case_sensitive_like_query = dialect.queries.GetPragmaQuery(
    "case_sensitive_like", "BOOL"
)

subdialect = dialect.provide_submodule(__name__)


@subdialect.register(True)
class Helper(dialect.helper.Helper.func):
    # TODO: change property pragma_fk into get_pragma_fk/set_pragma_fk to emphasize immutability
    __attributes__ = Attributes.build_from(
        dialect.helper.Helper.func.__attributes__,
        sqlite_master=sqlite_masters[0],
        sqlite_temp_master=sqlite_masters[1],
    )
    BackendException = (
        sqlite3.OperationalError,
        sqlite3.IntegrityError,
        sqlite3.InterfaceError,
    )

    def table_exists(self, table):
        m = self.sqlite_master
        q = m.select_query(
            columns=(1,), condition=m["type"].eq("table") & m["name"].eq(table.name)
        )
        res = self.execute(q)
        try:
            next(res)
        except StopIteration:
            return False
        return True

    def connect(self):
        if not self.db:
            self.db = sqlite3.connect(self.dbpath)
        super().connect()

    def __setstate__(self, state):
        super().__setstate__(state)
        self.pragma_fk = True
        self.case_sensitive_like = True

    @property
    def pragma_fk(self):
        res = self.execute(get_pragma_fk_query)
        return next(res)[0]

    @pragma_fk.setter
    def pragma_fk(self, value):
        with self.transaction(oncontext=0):
            q = self.dialect.queries.SetPragmaQuery(get_pragma_fk_query, value)
            res = self.execute(q, commit=False)

    @property
    def case_sensitive_like(self):
        res = self.execute(get_case_sensitive_like_query)
        return next(res)[0]

    @case_sensitive_like.setter
    def case_sensitive_like(self, value):
        with self.transaction(oncontext=0):
            q = self.dialect.queries.SetPragmaQuery(
                get_case_sensitive_like_query, value
            )
            res = self.execute(q, commit=False)

    def generate_temporary_table_name(self, suffix=""):
        cond = self.sqlite_temp_master["name"].like(f"nd_{suffix}%")
        conflictings = {
            e[0]
            for e in self.execute(
                self.sqlite_temp_master.select_query(columns=("name",), condition=cond)
            )
        }
        conflictings.add(None)
        name = None
        while name in conflictings:
            name = super().generate_temporary_table_name(suffix=suffix)
        return name

    @functools.wraps(dialect.helper.Helper.func.execute)
    def execute(self, *args, **kwargs):
        try:
            return super().execute(*args, **kwargs)
        except sqlite3.InterfaceError as e:
            raise NetworkDiskBackendTypeError() from e
        except self.BackendException as e:
            raise NetworkDiskBackendError() from e

    @functools.wraps(dialect.helper.Helper.func.executemany)
    def executemany(self, *args, **kwargs):
        try:
            return super().executemany(*args, **kwargs)
        except sqlite3.InterfaceError as e:
            raise NetworkDiskBackendTypeError() from e
        except self.BackendException as e:
            raise NetworkDiskBackendError() from e
