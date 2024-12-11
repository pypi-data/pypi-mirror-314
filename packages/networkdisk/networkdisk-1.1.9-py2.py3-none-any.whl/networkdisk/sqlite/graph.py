import os, functools
from .dialect import sqlitedialect as dialect
from networkdisk.utils import notProvidedArg
import networkx as nx
import networkdisk.exception as ndexc

SQLGraph = dialect.Graph


@dialect.register(False)
class Graph(SQLGraph):
    _doc_format = dict(
        SQLGraph._doc_format,
        short_description="SQLite Graph class",
        db_parameter="""db : MasterGraphs or Helper or DB connect information or None, default=None
		The db to connect, or an already connected Master or Helper.  Special
		keys `':memory:'`, `':tempfile:'`, and `':autofile:'` may in particular
		be used to create the graph in-memory, in a new temporary file, or in
		a file whose name is automatically determined according to the graph
		type and name -- see tutorials for further details.""",
    )
    default_dbpath = ":memory:"

    @property
    def dialect(self):
        return dialect

    @functools.wraps(SQLGraph.__pre_init__)
    def __pre_init__(self, *args, db=None, create=None, **kwargs):
        """
        +	db: a path to a datafile (str) or the ":memory:" (str), or `None` for using the `self.default_dbpath` or an `Helper`;
        +	create: a Boolean (or None) indicating whether to create the schemas in the data store or not;
        """
        db = self.default_dbpath if db is None else db
        if isinstance(db, str):
            if db == ":memory:" or (
                db not in [":autofile:", ":tempfile:"] and not os.path.isfile(db)
            ):
                create = True
        return super().__pre_init__(*args, db=db, create=create, **kwargs)

    def __setstate__(self, state):
        if state["helper"].dbpath == ":memory:":
            raise ndexc.NetworkDiskBackendError(
                "cannot restore transient in-memory database"
            )
        self.__unsafe_setstate__(state)

    def __unsafe_setstate__(self, state):
        super().__setstate__(state)

    def copy(self, as_view=False):
        if as_view or self.helper.dbpath == ":memory:":
            return nx.Graph.copy(self, as_view=as_view)
        return super().copy(as_view=as_view)

    def copy_to_memory(self, **kwargs):
        # TODO: replace incoming_graph_data with ATTACH DATABASE !!! OR NOT !!!
        H = self.__class__(incoming_graph_data=self, dbpath=":memory:", **kwargs)
        return H
