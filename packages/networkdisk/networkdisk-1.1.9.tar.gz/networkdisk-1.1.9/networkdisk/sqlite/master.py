"""SQLite variant of SQL MasterGraph

This variant deal with threading of MasterGraph, which is the
primary access to the helper for Graph/DiGraph.

It will attempt to regenerate a new helper for each threads
which should allowed concurrent access to the Graph objects.
"""

import threading
from networkdisk.sqlite.dialect import sqlitedialect as dialect

subdialect = dialect.provide_submodule(__name__)


@subdialect.register(True)
class MasterGraphs(dialect.master.MasterGraphs.func):
    def __init__(self, dialect, db, **kwargs):
        self.threads_id = {}
        super().__init__(dialect, db, **kwargs)

    @property
    def helper(self):
        helper = self.threads_id.get(threading.get_ident(), None)
        if helper is None:
            helper = self.helper = self.get_helper(self.db_constructor)
        return helper

    @helper.setter
    def helper(self, h):
        self.threads_id[threading.get_ident()] = h

    def get_helper(self, db):
        if isinstance(db, self.dialect.helper.Helper.func):
            if db.dbpath == ":memory:" or db.temporary_table_count:
                return db
        return super().get_helper(db)
