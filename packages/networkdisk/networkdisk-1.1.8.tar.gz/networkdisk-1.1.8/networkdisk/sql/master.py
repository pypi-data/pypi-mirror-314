import functools, json, collections
from .dialect import sqldialect as dialect
from networkdisk.exception import (
    NetworkDiskError,
    NetworkDiskBackendError,
    NetworkDiskMetaError,
)
import networkdisk as nd

dialect = dialect.provide_submodule(__name__)


@dialect.register(True)
def mastertable(dialect):
    """Function creating the MasterTable

    The master table is an SQL Table, which is used to store graph master
    information. Typically, it will store a dump of the graph schema
    (:py:class:networkdisk.sql.graph.SchemaGraphSchema) together with the
    graph name (if provided), and possibly additional data.

    Notes
    -----
    The master table is an SQL Table, which is used to store
    graph master information. Typically, it will store a dump of the
    graph schema (networkdisk.sql.graph.SchemaGraphSchema)
    together with the graph name (if provided), and possibly
    additional data. The table has the following columns:

    - ID INTEGER PRIMARY KEY:
       the graph id, wich is an automatically incremented integer;
    - NAME TEXT UNIQUE
       the graph name, which is optional;
    - TYPE TEXT NOT NULL
       the graph type, which should be one of "SQLGraph",  "SQLDiGraph";
    - SCHEMA TEXT NOT NULL
       the graph schema dump;
    - CREATION_DATE INTEGER NOT NULL
       the graph creation date;
    - LAST_ACCESS_DATE INTEGER NOT NULL
       the graph last modification date;
    - LAST_ALTERATION_DATE INTEGER NOT NULL
       the graph last access date;
    - INFO TEXT
       some additional graph information (optional).

    Each row correspond to a distinct graph, which can be either
    identified by its name, if given, or by its id.
    """
    table = dialect.schema.SchemaTable("networkdisk_master")
    table.add_column(
        "id", sqltype="INTEGER", primarykey=True
    )  # , constraints=["AUTOINCREMENT"])
    table.add_column("name", sqltype="TEXT")
    table.add_column("type", sqltype="TEXT")
    table.add_column("schema", sqltype="BLOB")
    table.add_column("networkdisk_version", sqltype="TEXT")
    table.add_column(
        "creation_date",
        sqltype="DATE",
        default=dialect.columns.DateColumn(dialect.constants.Now),
    )
    table.add_column(
        "last_access_date",
        sqltype="DATE",
        default=dialect.columns.DateColumn(dialect.constants.Now),
    )
    table.add_column(
        "last_alteration_date",
        sqltype="DATE",
        default=dialect.columns.DateColumn(dialect.constants.Now),
    )
    table.add_column("info", sqltype="TEXT")
    return table


@dialect.register(True)
class MasterGraphs(collections.abc.Mapping):
    """A class to manipulate the MasterTable

    PARAMETERS
    ----------
    db: str or Helper or db connector
            Information to initialize the Helper

    kwargs:
            Any keyword arguments that can be fed to the Helper class
            to initialize it.

    The MasterTable stores Graph Schema, some type information and some metadata information.
    Any entry can have any name without restriction, but id is unique.
    """

    def __init__(self, dialect, db, autoinitialize=True, **kwargs):
        self.dialect = dialect
        self.helper = self.get_helper(db, **kwargs)
        self.db_constructor = db
        self.mastertable = self.dialect.master.mastertable()
        if autoinitialize and not self.is_initialized:
            self.initialize(safe=False)

    def get_helper(self, db, **kwargs):
        if isinstance(db, self.dialect.helper.Helper.func):
            if db.dbpath is not None:
                helper = db.build_from(db, dbpath=db.dbpath, db=None, **kwargs)
            else:
                helper = db.build_from(db, db=db.db, **kwargs)
        elif hasattr(db, "execute"):
            helper = self.dialect.helper.Helper(dbpath=None, db=db, **kwargs)
        else:
            helper = self.dialect.helper.Helper(dbpath=db, **kwargs)
        return helper

    @property
    def is_initialized(self):
        """Property returning whether the master table has been created or not"""
        return self.helper.table_exists(self.mastertable)

    @property
    def name_column(self):
        """Property returning the name column of the master table"""
        return self.mastertable["name"]

    @property
    def masterid_column(self):
        """Property returning the id column of the master table"""
        return self.mastertable["id"]

    @property
    def type_column(self):
        """Property returning the type column of the master table"""
        return self.mastertable["type"]

    def __getitem__(self, key):
        if isinstance(key, int):
            try:
                return self.load_graph(masterid=key)
            except KeyError:
                pass
        return self.load_graph(name=key)

    def __iter__(self):
        yield from self.list_graphs(columns="name")

    def __len__(self):
        return len(self.list_graphs())

    def __repr__(self):
        prefix = f"{self.__class__.__name__}<{self.dialect.name}({self.helper.dbpath})>"
        return f"{prefix}\n{self._pretty_print_str()}"

    def _pretty_print_str(self):
        suffix = ""
        infix = ""
        l = [tuple(map(str, e)) for e in self.list_graphs()]
        if l:
            m = [max(map(lambda t: len(t[i]), l)) + 3 for i in range(3)]
            padd = lambda ie: ie[1] + (" " * (m[ie[0]] - len(ie[1])))
            l = [("id", "name", "type"), ("—" * m[0], "—" * m[1], "—" * m[2])] + l
            l = [tuple(map(padd, enumerate(e))) for e in l]
            infix = "\n" if l else " ø "
            suffix = "\n".join("|" + "|".join(e) + "|" for e in l)
        return f"{infix}{suffix}"

    def pretty_print(self):
        print(self._pretty_print_str())

    def initialize(self, safe=True):
        """Initialize the MasterTable

        Raises
        ------
        NetworkDiskError
                if the master table is already initialized
        """
        if safe and self.is_initialized:
            raise NetworkDiskError("Database already initialized")
        else:
            self.helper.executescript(self.mastertable.create_script())

    def _condition(self, name=None, masterid=None, directed=None):
        """Helper to build condition for filtering the master table contents"""
        condition = self.dialect.conditions.EmptyCondition()
        if name is not None:
            condition &= self.name_column.eq(name)
        if masterid is not None:
            condition &= self.masterid_column.eq(masterid)
        if directed:
            condition &= self.type_column.eq(self.dialect.DiGraph.__name__)
        elif directed is not None:
            condition &= self.type_column.eq(self.dialect.Graph.__name__)
        return condition

    def list_graphs(
        self, columns=("id", "name", "type"), name=None, masterid=None, directed=None
    ):
        """Lists all Graph and/or DiGraph stored in the DB"""
        condition = self._condition(name=name, masterid=masterid, directed=directed)
        project = not isinstance(columns, tuple)
        if project:
            columns = (columns,)
        res = list(
            self.helper.execute(
                self.mastertable.select_query(columns=columns, condition=condition)
            )
        )
        if project:
            return [e[0] for e in res]
        return res

    list_ungraphs = functools.partialmethod(list_graphs, directed=False)
    list_digraphs = functools.partialmethod(list_graphs, directed=True)

    # Copied from Graph
    def load_graph_schema(
        self, name=None, masterid=None, directed=None, to_directed=None
    ):
        """Loads the Graph schema

        Parameters
        ----------
        name:	non-mutable value, optional
                The name of the graph schema to fetch

        masterid:	int, optional
                The id of the graph schema to fetch

        directed: bool, optional
                If True, will fetch only DiGraph schema, if False only Graph schema

        to_directed: bool, optional
                If given, the parameter has two effects: (1) it will allow to resolve
                possible ambiguity in some cases; (2) it will convert a loaded schema
                to the desired type.  Indeed, if True (resp. False) then, in case of
                multiple graph schemas in the master table, the graph schema of the
                desired type is preferred, if it is unique (otherwise an error on
                ambiguity is raised).  When the directed parameter is also given (see
                above), only the second effect applies.

        Notes
        -----
        If `name` is not provided, then the method loads one (TODO: the last?)
        graph schema of the master table, or raises a `NetworkDiskMetaError` if
        the master table is empty or nonexistent.  Otherwise, a schema of the
        given name is returned if found, or the `NetworkDiskMetaError` is
        raised, otherwise.

        Returns
        -------
        GraphSchema

        Raises
        ------
        NetworkDiskMetaError
                if no or several graphs corresponding to the given criteria are found
        """
        condition = self._condition(name=name, masterid=masterid, directed=directed)
        if directed is None and to_directed is not None:
            orderby = dict(orderby=(self.mastertable["type"],), desc=not to_directed)
        else:
            orderby = {}
        query = self.mastertable.select_query(condition=condition, **orderby)
        graphtype = {None: "", True: "di", False: "un"}
        try:
            res = self.helper.execute(query)
            row = next(res)
            masterid = row[0]
            gcls = row[2]
            if isinstance(row[3], tuple):
                sch = nd.utils.serialize.dedictify(*row[3])
            else:
                sch = json.loads(row[3])
                sch = self.dialect.schemata.load_graph(
                    gcls == self.dialect.DiGraph.__name__, sch
                )
            ndvrs = row[4]
        except NetworkDiskBackendError as e:
            raise NetworkDiskMetaError("No master table found") from e
        except StopIteration:
            graphtype = f"{graphtype[directed]}graph"
            if masterid:
                if name:
                    raise NetworkDiskMetaError(
                        f"No {graphtype} with masterid '{masterid}' and name '{name}' found"
                    )
                else:
                    raise NetworkDiskMetaError(
                        f"No {graphtype} with masterid '{masterid}' found"
                    )
            elif name:
                raise NetworkDiskMetaError(f"No {graphtype} with name '{name}' found")
            else:
                raise NetworkDiskMetaError(f"No {graphtype} found")
        try:
            next(res)
            if to_directed is None or gcls == res[2]:
                graphtype = f"{graphtype[to_directed]}graph"
                if name:
                    raise NetworkDiskMetaError(
                        f"Ambiguous selection of {graphtype} with name '{name}'"
                    )
                else:
                    raise NetworkDiskMetaError(f"Ambiguous selection of {graphtype}")
        except StopIteration:
            pass
        if to_directed is True:
            sch = sch.to_directed()
        elif to_directed is False:
            sch = sch.to_undirected()
        return sch, masterid

    load_ungraph_schema = functools.partialmethod(load_graph_schema, directed=False)
    load_digraph_schema = functools.partialmethod(load_graph_schema, directed=True)

    def save_graph(self, G, masterid=None, name=None):
        """Save the Graph Schema in the Master Table

        Parameters
        ----------
        name:	non-mutable value
                The name of the graph schema to fetch

        masterid:	int
                The id of the graph schema to fetch

        directed: bool or None
                If True, will fetch only DiGraph schemas, if False
                only Graph schemas and if None, both.
        """
        if not hasattr(G, "schema"):
            schemadump = json.dumps(None)
        elif getattr(G.schema, "schema_trace", None):
            schemadump = json.dumps(G.schema.schema_trace)
        else:
            schemadump = nd.utils.serialize.dictify(getattr(G, "schema", None))
        graph_master = dict(type=G.__class__.__name__, schema=schemadump)
        if name:
            graph_master["name"] = name
        if masterid:
            graph_master["id"] = masterid
        graph_master["networkdisk_version"] = nd.__version__
        query = self.mastertable.insert_values(replace=bool(masterid), **graph_master)
        curs = self.helper.execute(query)
        return curs.lastrowid

    def delete_graph(self, name=None, masterid=None, directed=None):
        """Delete the Graph Schema in the Master Table

        Parameters
        ----------
        name:	non-mutable value
                The name of the graph schema to fetch

        masterid:	int
                The id of the graph schema to fetch

        directed: bool or None
                If True, will fetch only DiGraph schema, if False
                only Graph schema and if None, both.
        """
        condition = self._condition(name=name, masterid=masterid, directed=directed)
        return self.helper.execute(self.mastertable.delete_query(condition=condition))

    delete_ungraph = functools.partialmethod(delete_graph, directed=False)
    delete_digraph = functools.partialmethod(delete_graph, directed=True)

    def get_graph_class(self, name=None, masterid=None, directed=None):
        """Get the graph Class associated to the Schema

        Parameters
        ----------
        name:	non-mutable value
                The name of the graph schema to fetch

        masterid:	int
                The id of the graph schema to fetch

        directed: bool or None
                If True, will fetch only DiGraph schema, if False
                only Graph schema and if None, both.
        """

        condition = self._condition(name=name, masterid=masterid, directed=directed)
        q = self.mastertable.select_query(
            columns=("type",), condition=condition, distinct=True, limit=2
        )
        gtypes = list(self.helper.execute(q))
        if len(gtypes) > 1:
            raise NetworkDiskError(f"Ambiguous graph class for name {name}")
        elif not gtypes:
            raise KeyError(name)
        gtype = gtypes[0][0]
        return getattr(self.dialect, gtype)

    def load_graph(self, name=None, masterid=None, directed=None):
        """Load the Graph

        Parameters
        ----------
        name:	non-mutable value
                The name of the graph schema to fetch

        masterid:	int
                The id of the graph schema to fetch

        directed: bool or None
                If True, will fetch only DiGraph schemas, if False
                only Graph schemas and if None, both.
        """
        cls = self.get_graph_class(name, masterid, directed=directed)
        return cls(db=self.helper, name=name, masterid=masterid)

    load_ungraph = functools.partialmethod(load_graph, directed=False)
    load_digraph = functools.partialmethod(load_graph, directed=True)

    def new_ungraph(self, incoming_graph_data=None, name=None, schema=None):
        return self.dialect.Graph(
            incoming_graph_data=incoming_graph_data,
            db=self.helper,
            name=name,
            create=True,
            insert_schema=True,
            schema=schema,
        )

    def new_diGraph(self, incoming_graph_data=None, name=None, schema=None):
        return self.dialect.DiGraph(
            incoming_graph_data=incoming_graph_data,
            db=self.helper,
            name=name,
            create=True,
            insert_schema=True,
            schema=schema,
        )


@dialect.register(True)
def load_graph(dialect, db, *args, name=None, masterid=None, directed=None, **kwargs):
    master = dialect.master.MasterGraphs(db, *args, **kwargs)
    return master.load_graph(name=name, masterid=masterid, directed=directed)


dialect.register(True, load_ungraph=functools.partial(load_graph, directed=False))
dialect.register(True, load_digraph=functools.partial(load_graph, directed=True))


@dialect.register(True)
def list_graphs(dialect, db, *args, name=None, masterid=None, directed=None, **kwargs):
    master = dialect.master.MasterGraphs(db, *args, **kwargs)
    return master.list_graphs(name=name, masterid=masterid, directed=directed)


dialect.register(True, list_ungraphs=functools.partial(list_graphs, directed=False))
dialect.register(True, list_digraphs=functools.partial(list_graphs, directed=True))
