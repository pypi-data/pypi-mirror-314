"""Module providing the Graph SQL class.

A SQL Graph is a undirected Graph overloading the
networkx Graph class. Ir overrides some of its methods
for optimization purpose.

At Graph instantiation, it is possible to relatively efficiency
controls the behavior of the Graph creation/loading.
"""

import itertools, functools, abc, os, tempfile
import networkdisk as nd
import networkx as nx
import networkx.classes as nxclasses
from networkdisk.tupledict.currying import shorten_tuples
from networkdisk.tupledict.tupledict import ReadOnlyTupleDictView
from networkdisk.sql import classes as ndclasses
from networkdisk.sql.dialect import sqldialect as dialect
from networkdisk.exception import (
    NetworkDiskError,
    NetworkDiskException,
    NetworkDiskMetaError,
    NetworkDiskBackendError,
)
from networkdisk.utils import notProvidedArg, to_typefactory
from networkdisk.mock import copymock

__all__ = ["Graph"]


@dialect.register(False)
class Graph(nxclasses.graph.Graph, abc.ABC):
    """{short_description}

    The class inherit from `nx.Graph` class and override some of the methods
    for performance purpose.  Two constructors are possible to obtain a SQL
    Graph: :meth:`__load_graph_init__` and :meth:`__create_graph_init__`
    depending on whether the graph has to be created on disk or simply loaded
    from the database.

    Depending on the chosen parameters for initializing the graph, the first
    or second methods will be called.

    PARAMETERS
    ----------
    incoming_graph_data : graph data or None, default=None
            Possibly, graph data to import, as for NetworkX graphs.

    {db_parameter}

    sql_logger : callable or bool or None or notProvidedArg, default=notProvidedArg
            Whether and how to log SQL queries.  Value `None` means “do not log
            anything”, value `True` means “use a fresh instance of the default
            logger and set it active”, value `False` means “use a fresh instance
            of the default logger and set it inactive”, value `notProvidedArg`
            means “use the shared instance of the default logger”, and `callable`
            values allow to set the logger to a user-defined logger.

    autocommit : bool, default=True
            Whether to connect to the db with autocommit flag (ignored if `db` is
            an already connected object).

    schema : GraphSchema or bool or mapping or None, default=None
            The `GraphSchema` to use for the graph.  `True` indicates that the
            default schema should be generated through according to the
            `default_schema` property, while `False` enforces to load the schema
            from DB.  If a mapping, the schema is generated (as with `True`)
            using the mapping items as keyworded parameters for the generation.  In
            particular, the key `method` indicates which function should be used to
            generate the schema (`default_schema` is used if missing).  The value
            associated with the `method` key should be a key of the sub-dialect
            `dialect.schemata`.  Finally, if the parameter has value `None`, a
            default behavior is chosen according to the other parameters and the
            contents of the master table of the connected DB, if present.

    insert_schema : bool or None, default=None
            Whether to insert the schema in the master table.  If `None` the value
            is determined according to the given parameters in a very smart way.

    lazy : bool or None, default=None
            Whether the tupledicts living in the graph schema should be lazy or not
            for increasing performance.  `Graph` with lazy attributes set to `True`
            will not raise `KeyError` in some situation where normal
            `networkx.Graph` would.  See `TupleDict` documentation for details.

    static : bool, default=False
            Whether the graph is assumed to be static.  Declaring a graph as static
            has two effects: (1) the graph schema is automatically turn into the
            corresponding read-only schema; (2) node/edge caching (see parameters
            node_cache_level and edge_cache_level below) is allowed.  It is up to
            the programmer to ensure that the graph backend is not altered.

    node_cache_level: None or integer, default=None
            A value indicating how deep should node caching be performed.  Value 0
            means that no caching is performed.  Caching is allowed only if the
            graph has been declared as static (see static parameter above) — an
            error is raised otherwise.  If None, then the value is set to the value
            of the cache_level parameter (see below).

    edge_cache_level: None or integer, default=None
            A value indicating how deep should edge caching be performed.  Value 0
            means that no caching is performed.  Caching is allowed only if the
            graph has been declared as static (see static parameter above) — an
            error is raised otherwise.  If None, then the value is set to the value
            of the cache_level parameter (see below).

    cache_level: integer, default=0
            A value for both node_cache_level and edge_cache_level, which both take
            precedence over cache_level in case they are given.

    masterid : str or None, default=None
            If given with one of `schema`, or `insert_schema`, then set the Graph
            masterid to `masterid`.  Otherwise, load the graph schema of the graph
            of masterid `masterid` from master table.  In the latter case, an error
            is raised if no such graph is found.

    name : str or None, default=None
            Without `schema` and `insert_schema` parameters, attempt to load a
            `name`-named graph from the master table.  If failing, or with `schema`
            or `insert_schema` parameters, set the graph name.

    attr : mapping
            Additional data to add to the graph (as for NetworkX graphs).
    """

    _doc_format = dict(
        short_description="SQL abstract Graph class",
        db_parameter="""db : MasterGraphs or Helper or DB connect information or None, default=None
		The DB connector specification.  Connect information format depends on
		backend.""",
    )
    __unformated_doc__ = __doc__
    __doc__ = __unformated_doc__.format(**_doc_format)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "__doc__" not in cls.__dict__:
            cls.__doc__ = cls.__unformated_doc__.format(**cls._doc_format)

    default_lazy = True
    nx_variant = nxclasses.graph.Graph
    autofile_dir = "_networkdisk_graphs"
    tempfile_dir = "/tmp/networkdisk/graphs"

    @property
    @abc.abstractmethod
    def dialect(self):
        return dialect

    @property
    def helper(self):
        return self.master.helper

    # Constructors
    def __init__(
        self,
        incoming_graph_data=None,
        db=None,
        sql_logger=notProvidedArg,
        autocommit=False,
        schema=None,
        create=None,
        insert_schema=None,
        lazy=None,
        static=False,
        node_cache_level=None,
        edge_cache_level=None,
        cache_level=0,
        masterid=None,
        name=None,
        **attr,
    ):
        """Smart graph initializer.

        The initialized graph by be loaded from DB (by calling `load_graph`) or
        created (by calling `create_graph`) depending on provided parameters.
        The whole method behaves as a pipeline, passing parameters through the
        following initializing submethods:
        1.	__pre_init__ (initialize the helper and the master)
        2.	__graph_init__ (initialize the graph schema, by either calling
                        `load_graph` or `__create_graph`)
        3.	__super_init__ (import data as done in NetworkX)
        4.	__post_init__ (post initialization)

        Parameters
        ----------
        db: DB-connector information
                c.f., `__pre_init__`.

        sql_logger: SQL-logger information
                c.f., `__pre_init__`.

        autocommit: bool
                c.f., `__pre_init__`.

        incoming_graph_data: None or graph-data
                c.f., `__super_init__` and `networkx.Graph.__init__`.

        schema: None or GraphSchema or bool or mapping
                The graph schema to use, or whether to create one (`True` or mapping)
                or load one (`False`) schema.  If `None`, the behavior is chosen
                according to the other.  C.f., `__create_graph__`.

        lazy: None or bool
                c.f., both `create_graph` and `load_graph`.

        name: None or str
                the graph name or `None`.  If not `None`, the name is used for
                attempting to find the graph within the database, and it is finally
                added to the graph data `attr`.

        attr: mapping
                graph data, c.f. `__super_init__` and  `networkx.Graph.__init__`.
        """
        node_cache_level = cache_level if node_cache_level is None else node_cache_level
        edge_cache_level = cache_level if edge_cache_level is None else edge_cache_level
        args, kwargs = (
            (),
            dict(
                incoming_graph_data=incoming_graph_data,
                db=db,
                sql_logger=sql_logger,
                autocommit=autocommit,
                schema=schema,
                create=create,
                insert_schema=insert_schema,
                lazy=lazy,
                static=static,
                node_cache_level=node_cache_level,
                edge_cache_level=edge_cache_level,
                masterid=masterid,
                name=name,
                **attr,
            ),
        )
        args, kwargs = self.__pre_init__(*args, **kwargs)
        with self.helper.transaction(oncontext=1):
            args, kwargs = self.__graph_init__(*args, **kwargs)
            args, kwargs = self.__super_init__(*args, **kwargs)
            args, kwargs = self.__post_init__(*args, **kwargs)

    def __pre_init__(
        self, *args, db=None, sql_logger=notProvidedArg, autocommit=False, **kwargs
    ):
        if isinstance(db, self.dialect.master.MasterGraphs.func):
            self.master = db
        else:
            if isinstance(db, self.dialect.helper.Helper.func):
                autoinitialize = kwargs.get("insert_schema", None) is not False
                helper = db
            elif hasattr(db, "execute"):
                autoinitialize = kwargs.get("insert_schema", None) is not False
                helper = self.dialect.helper.Helper(
                    dbpath=None, db=db, sql_logger=sql_logger, autocommit=autocommit
                )
            else:
                if db == ":tempfile:":
                    # automatically generated new DB-file
                    tempdir = self.tempfile_dir
                    if not os.path.isdir(tempdir):
                        os.makedirs(tempdir)
                    prefix = (
                        f"{type(self).__name__}_{kwargs.get('name') or '-anonymous-'}_"
                    )
                    suffix = ".db"
                    _, db = tempfile.mkstemp(prefix=prefix, suffix=suffix, dir=tempdir)
                elif db == ":autofile:":
                    # automatically generated DB-file name, possibly existing
                    tempdir = self.autofile_dir
                    if not os.path.isdir(tempdir):
                        os.makedirs(tempdir)
                    db = f"{tempdir}/{type(self).__name__}_{kwargs.get('name') or '-anonymous-'}.db"
                autoinitialize = kwargs.get("insert_schema", None)
                autoinitialize = (
                    not os.path.isfile(db) if autoinitialize is None else autoinitialize
                )
                create = kwargs.get("create", None)
                if create is None and not os.path.isfile(db):
                    kwargs["create"] = create = True
                helper = self.dialect.helper.Helper(
                    dbpath=db, sql_logger=sql_logger, autocommit=autocommit
                )
            with helper.transaction():
                self.master = self.dialect.master.MasterGraphs(
                    helper, autoinitialize=autoinitialize
                )
        return args, kwargs

    def __graph_init__(
        self,
        *args,
        schema=None,
        create=None,
        insert_schema=None,
        masterid=None,
        name=None,
        static=False,
        node_cache_level=0,
        edge_cache_level=0,
        **kwargs,
    ):
        kwargs.update(
            schema=schema,
            create=create,
            insert_schema=insert_schema,
            masterid=masterid,
            name=name,
            static=static,
            node_cache_level=node_cache_level,
            edge_cache_level=edge_cache_level,
        )
        if schema is None:
            # decide whether to create or attempt to load graph schema
            if insert_schema or (not masterid and name is None and create):
                schema = True
            elif not self.helper.table_exists(self.master.mastertable):
                schema = True
                insert_schema = kwargs.get("insert_schema")
                insert_schema = False if insert_schema is None else insert_schema
                kwargs["insert_schema"] = insert_schema
            else:
                try:
                    thename = None if masterid else name
                    kwargs["schema"], masterid = self.master.load_graph_schema(
                        masterid=masterid, name=thename
                    )
                    schema = False
                    if "create" in kwargs:
                        kwargs["create"] = create = False
                    if "insert_schema" in kwargs:
                        kwargs["insert_schema"] = insert_schema = False
                except NetworkDiskException as e:
                    if masterid and insert_schema is None:
                        raise e
                    schema = True
            kwargs["schema"] = schema

        if schema or hasattr(schema, "keys"):
            args, kwargs = self.__create_graph_init__(*args, **kwargs)
        else:
            kwargs.pop("insert_schema", None)
            args, kwargs = self.__load_graph_init__(*args, **kwargs)
        return args, kwargs

    def __load_graph_init__(
        self,
        *args,
        create=False,
        lazy=None,
        masterid=None,
        name=None,
        schema=None,
        static=False,
        node_cache_level=0,
        edge_cache_level=0,
        **kwargs,
    ):
        """Load a graph from database.

        +	incoming_graph_data:
        +	db:
                either a DB helper, or a DB file path (`str`).
                The default value `None` will result in an error.
        +	sql_logger, autocommit:
                c.f. `set_helper` method.
        +	create:
                a Boolean (default is `False`) indicating whether the
                found graph schema structure should be created. In a
                common situation, a graph schema which has been saved in
                the master table, is an existing schema, namely, its
                structure (TABLE, VIEW…) exists within the database whence
                the default parameter value `False` should be used.
                However, in some cases, a graph schema whose structure
                does not exist in the database could have been saved in
                the master table. In which case, one might want to specify
                `create=True` so that the structure is created.
        +	lazy:
                a Boolean or `None` indicating the tupledict lazyness.
                If `None` the default value is taken.
        +	name:
                the name of the graph to find, or `None`.
        +	masterid:
                the id of the graph to find, or `None`.
        +	schema:
                the graph schema to load. If provided together with
                masterid, then it used without reading the master table.
        +	attr:
        """
        if not schema or masterid is None:
            schema, masterid = self.master.load_graph_schema(
                masterid=masterid, name=name, to_directed=self.is_directed()
            )
        elif not self.master.is_initialized:
            raise NetworkDiskError(
                "Cannot find graph schema in database without master table"
            )
        self.setsignature(
            schema,
            masterid,
            lazy=lazy,
            create=create,
            static=static,
            node_cache_level=node_cache_level,
            edge_cache_level=edge_cache_level,
        )
        return args, kwargs

    def __create_graph_init__(
        self,
        *args,
        schema=True,
        lazy=None,
        create=None,
        insert_schema=None,
        masterid=None,
        name=None,
        static=False,
        node_cache_level=0,
        edge_cache_level=0,
        **kwargs,
    ):
        """An SQL Graph constructor.

        Parameters
        ----------
        schema: GraphSchema or True or mapping
                The `GraphSchema` to use or how to generate it.  If `True`, the
                default graph schema is generated according to `self.default_schema`.
                If a mapping, then the generation is controlled by the mapping items,
                namely, the value of the special key `method` indicate which schema
                generating function to use (the `self.default_schema` one if missing)
                and the other parameters are passed as keyworded parameters to the
                specified function.  Hence, an empty mapping is equivalent to `True`.
                The value associated with the `method` special key should be a key of
                the sub-dialect `self.dialect.schemata`.

        lazy: bool or None
                a Boolean setting tupleDicts lazyness, or `None` for the default
                lazyness.

        create: bool or None
                a Boolean or `None` (default) indicating whether to create the graph
                structure (TABLE, VIEW, INDEX, TRIGGER) within DB or not.  If `False`
                each structure occurring within the (possibly generated) schema, is
                assumed to exist.  If `None` then the flag takes the value `True` if
                the schema has been generated (namely, if the `schema` argument was
                not a `GraphSchema` instance) and `False` otherwise.

        insert_schema: bool or None
                a Boolean or `None` (default) indicating whether to save the schema
                in the master table (for future importation) or not.  If `None`, then
                the parameter takes the value `True` if the schema is created and
                `False` otherwise (c.f. `create` parameter documentation above).

        name:
                one of the graph data, namely its name, that is stored in the master
                table when the graph is inserted.

        args : tuple
        kwargs : dict
                further ignored parameters to be passed in the initialization pipe.

        The master table is **created** when it does not exist and
        `insert_schema` is `True` or is changed from `None` to `True`
        as above explained.
        """
        # Set default behavior
        if schema is True or schema is None:
            schema, schema_gen = None, {}
        elif hasattr(schema, "keys"):
            schema, schema_gen = None, schema
        if create is None:
            if insert_schema is False:
                create = None
            else:
                create = not schema
        if insert_schema is None:
            insert_schema = create
        if insert_schema and not self.master.is_initialized:
            self.master.initialize()

        if schema:
            # A schema has been given
            if self.is_directed():
                schema = schema.to_directed()
            else:
                schema = schema.to_undirected()
            if static:
                schema = schema.to_readonly()
            self.schema = schema
            if insert_schema:
                masterid = self.master.save_graph(self, masterid=masterid, name=name)
        else:
            if static:
                schema_gen["readonly"] = True
            if insert_schema:
                # Generate default schema and insert it in mastertable
                with self.helper.transaction():
                    masterid = self.master.save_graph(self, name=name)
                    schema_gen.setdefault("table_suffix", masterid)
                    self.schema = schema = self.default_schema(**schema_gen)
                    self.master.save_graph(self, masterid=masterid, name=name)
            else:
                # Generate default schema
                schema = self.default_schema(**schema_gen)
                masterid = None

        self.setsignature(
            schema,
            masterid,
            lazy=lazy,
            create=create,
            static=static,
            node_cache_level=node_cache_level,
            edge_cache_level=edge_cache_level,
        )

        if name is not None:
            kwargs["name"] = name
        return args, kwargs

    def __super_init__(self, incoming_graph_data=None, **attr):
        """
        This is a wrapper of `super().__init__`.
        """
        if self.is_readonly():
            if incoming_graph_data:
                raise NetworkDiskError(
                    f"Cannot import data from {incoming_graph_data} in read-only graph"
                )
            if attr:
                raise NetworkDiskError(
                    f"Cannot add attributes from {attr} to read-only graph"
                )
            # dirty trick for avoiding the self.graph.update of nx.Graph.__init__ on readonly TupleDict
            graph_attr_dict_factory = self.graph_attr_dict_factory
            self.graph_attr_dict_factory = dict
            super().__init__(incoming_graph_data=incoming_graph_data, **attr)
            self.graph_attr_dict_factory = graph_attr_dict_factory
            super().__setattr__(
                "graph", graph_attr_dict_factory()
            )  # avoid overloaded self.__setattr__
        else:
            # Fix of NetworkX testing instance membership to dict instead of collections.abc.Mapping
            if hasattr(incoming_graph_data, "fold"):
                incoming_graph_data = incoming_graph_data.fold()
            with self.helper.transaction(
                oncontext=1 if (incoming_graph_data or attr) else 0
            ):
                super().__init__(incoming_graph_data=incoming_graph_data, **attr)
        return (), {}

    def __post_init__(self):
        if self.is_readonly():
            nxclasses.freeze(self)
        if self.helper.transaction.active:
            self.helper.transaction.commit()
        return (), {}

    def setsignature(
        self,
        schema,
        masterid,
        lazy=None,
        create=None,
        static=False,
        node_cache_level=0,
        edge_cache_level=0,
    ):
        """Internal initialization of Graph.

        Parameters
        ----------
        schema: GraphSchema
                The graph schema to use.

        masterid: int or None
                The graph id in master table if any, or `None` otherwise.

        lazy: bool or None, default=None
                The underlying tupledicts lazyness.

        create: bool or None, default=None
                Whether the creation script of the given schema (that creates the
                schema tables, views, index, and triggers) should be executed or not.
                If `None`, then it is executed with the SQL `IF NOT EXISTS` flag.
        """
        if static:
            schema = schema.to_readonly()
        elif edge_cache_level > 0 or node_cache_level > 0:
            raise ValueError("Node/edge caching is possible only for static Graphs")
        self._static = static
        helper = self.helper
        master = self.master
        if create is not False:
            with self.helper.transaction():
                helper.sql_logger("Begin graph's schema creation")
                helper.executescript(schema.creation_script(ifnotexists=create is None))
                helper.sql_logger("End graph's schema creation")
        if schema.is_readonly():
            TupleDict = self.dialect.tupledict.ReadOnlyTupleDict
        else:
            TupleDict = self.dialect.tupledict.ReadWriteTupleDict
        lazy = self.default_lazy if lazy is None else lazy
        self.schema = schema
        self.masterid = masterid
        self.node_dict_factory = to_typefactory(
            lambda: TupleDict(
                master, schema.nodes, lazy=lazy, cache_level=node_cache_level
            ),
            ReadOnlyTupleDictView,
        )
        self.node_attr_dict_factory = dict
        self.adjlist_outer_dict_factory = to_typefactory(
            lambda: TupleDict(
                master, schema.adj, lazy=lazy, cache_level=edge_cache_level
            ),
            ReadOnlyTupleDictView,
        )
        self.adjlist_inner_dict_factory = to_typefactory(
            dict, dict | ReadOnlyTupleDictView
        )
        self.edge_attr_dict_factory = dict
        # Lazyness of graphs attributes does not make much sense.
        self.graph_attr_dict_factory = to_typefactory(
            lambda: TupleDict(master, schema.graph, lazy=lazy), ReadOnlyTupleDictView
        )
        self.edgestore = TupleDict(
            master, schema.edgestore, lazy=lazy, cache_level=edge_cache_level
        )
        if self.is_directed():
            self.pred_dict_factory = to_typefactory(
                lambda: TupleDict(
                    master, schema.pred, lazy=lazy, cache_level=edge_cache_level
                ),
                ReadOnlyTupleDictView,
            )
            self.write_edge_target = self.edgestore
            self.revedgestore = TupleDict(
                master, schema.revedgestore, lazy=lazy, cache_level=edge_cache_level
            )
        elif schema.asymedges is None:
            self.asymedges = None
            self.write_edge_target = self.edgestore
        else:
            self.asymedges = TupleDict(
                master, schema.asymedges, lazy=lazy, cache_level=edge_cache_level
            )
            self.write_edge_target = self.asymedges

    # Constructors
    @classmethod
    @functools.wraps(__create_graph_init__)
    def create_graph(cls, *args, **kwargs):
        self = object.__new__(cls)
        args, kwargs = self.__pre_init__(*args, **kwargs)
        args, kwargs = self.__create_graph_init__(*args, **kwargs)
        args, kwargs = self.__super_init__(*args, **kwargs)
        args, kwargs = self.__post_init__(*args, **kwargs)
        return self

    @classmethod
    @functools.wraps(__load_graph_init__)
    def load_graph(cls, *args, **kwargs):
        self = object.__new__(cls)
        args, kwargs = self.__pre_init__(*args, **kwargs)
        args, kwargs = self.__load_graph_init__(*args, **kwargs)
        args, kwargs = self.__super_init__(*args, **kwargs)
        args, kwargs = self.__post_init__(*args, **kwargs)
        return self

    def __getstate__(self):
        return dict(
            helper=self.helper,
            schema=self.schema,
            masterid=self.masterid,
            lazy=self.lazy,
            static=self.static,
        )

    def __setstate__(self, state):
        self.__pre_init__(db=state.pop("helper"))
        state["static"] = state.pop("_static", False)
        self.setsignature(**state)
        super().__init__()
        self.__post_init__()

    def __unsafe_setstate__(self, state):
        self.__setstate__(state)

    @property
    def schema_class(self):
        return self.dialect.graph_schema.GraphSchema.func

    @property
    def default_schema(self):
        return self.dialect.schemata.load_ungraph

    @property
    def static(self):
        return self._static

    def __setattr__(self, k, v):
        """
        Override `__setattr__` of networkx graphs, in order to
        prevent tupleDicts to be replaced by simple dictionaries
        (c.f., `networkx.classes.tests.test_graph`).
        """
        if k in ("_adj", "_pred", "_succ", "_node", "graph"):
            attr = self.__dict__.get(k, None)
            if attr is None:
                # If it is not a dict-like, I don't know what to do, gives it to networkx.
                super().__setattr__(k, v)
            else:
                with self.helper.transaction():
                    attr.rowstore.delete(())  # Truncate tupleDict
                    attr.update(v)  # Update tupleDict
        else:
            super().__setattr__(k, v)

    def is_readonly(self):
        return getattr(self, "frozen", False) or self.schema.is_readonly()

    def is_static(self):
        return self.static

    def is_view(self):
        return hasattr(self, "_graph")

    def _get_all_tupleDicts(self):
        yield self._node
        yield self._adj
        yield self.graph
        if self.edgestore is not None:
            yield self.edgestore

    @property
    def lazy(self):
        return all(map(lambda td: td.lazy, self._get_all_tupleDicts()))

    @lazy.setter
    def lazy(self, lazy):
        list(map(lambda td: setattr(td, "lazy", lazy), self._get_all_tupleDicts()))

    @property
    def nodes(self):
        nodes = ndclasses.NodeView(self)
        self.__dict__["nodes"] = nodes
        return nodes

    @property
    def adj(self):
        return ndclasses.AdjacencyView(self._adj)

    @property
    def edges(self):
        return ndclasses.EdgeView(self)

    @property
    def degree(self):
        return ndclasses.DegreeView(self)

    @nxclasses.graph.Graph.name.setter
    def name(self, s):
        if self.masterid is None:
            self.graph["name"] = s
            return
        condition = self.master.mastertable["id"].eq(self.masterid)
        with self.helper.transaction():
            query = self.master.mastertable.update_query(condition=condition, name=s)
            self.helper.execute(query)
            self.graph["name"] = s

    def get_edge_data(self, u, v, default=None, lazy=False):
        if lazy:
            return super().get_edge_data(u, v, default=default)
        else:
            # overload networkx method, to return loaded dictionary
            try:
                return self[u][v].fold()
            except KeyError:
                return default

    def get_node_data(self, u, default=None, lazy=False):
        try:
            nd = self._node[u]
            if lazy:
                return nd
            else:
                return nd.fold()
        except KeyError:
            return default

    # Node insertion/deletion
    def _allow_none_node(self, node):
        if node is None:
            # according to networkx 2.6, raise
            raise ValueError("None cannot be a node")
        # return node to allow use in map
        return node

    def add_node_without_data(self, u):
        self.add_nodes_without_data_from([u])

    def add_node_data(self, u, **attr):
        """
        Add data from `attr` (update) to node `u` which is supposed
        to exist, but **never checked**. If `u` is not a vertex of
        `self`, then nothing is inserted silently.
        """
        # TODO: couldn't we always use add_node_data_from now?
        if self.schema.node_cascade_on_delete:
            self.add_node_data_from([(u,)], **attr)
        else:
            self._node[u].update(attr)

    def add_node(self, node_for_adding, **attr):
        """
        For code concision and optimization we reduce
        to add_nodes_from. nx version work but perform
        unnecessary operation.
        """
        self._allow_none_node(node_for_adding)
        with self.helper.transaction():
            # TODO: couldn't we always use add_node_data_from now?
            if self.schema.node_cascade_on_delete:
                if node_for_adding not in self._node:
                    self._node[node_for_adding] = attr
                else:
                    self._node[node_for_adding].update(
                        attr
                    )  # We have to manually deal with deletion of old values
            else:
                self.add_node_without_data(node_for_adding)
                self.add_node_data(node_for_adding, **attr)

    def remove_node(self, node, cascade=None):
        """Remove a node.

        If cascade is True, suppose edges refering to nodes
        have the "ON DELETE CASCADE". Hence, constraints
        are done on SQLite side. If cascade is False,
        we user the nx version to ensure structure.
        """
        cascade = cascade or self.schema.node_cascade_on_delete
        if cascade:
            try:
                with self.helper.transaction():
                    del self._node[node]
            except KeyError as e:
                raise NetworkDiskError(f"The node {node} is not in the graph.") from e
        else:
            with self.helper.transaction():
                try:
                    del self._node[node]
                    tds = self.write_edge_target.rowstore.tupleDictSchema
                    self.helper.execute(
                        tds.delete_prefix_query((), suffcondition=tds[1].eq(node))
                    )
                    # TODO: this should be easier with  self.write_edge_target.delete(()) but condition on delete unsupported
                except KeyError as e:
                    raise NetworkDiskError(
                        f"The node {node} is not in the graph."
                    ) from e

    def add_nodes_without_data_from(self, nodes_for_adding, tuples=False):
        target = self._node.rowstore
        bunch = nodes_for_adding
        if not tuples:
            bunch = map(lambda n: (n,), bunch)
        bunch = map(lambda t: tuple(map(self._allow_none_node, t)), bunch)
        target.bulk_insert(bunch)

    def add_node_data_from(self, nodes_for_adding, **attr):
        if iter(nodes_for_adding) is nodes_for_adding:
            raise NetworkDiskError(
                "Impossible to use `add_node_data_from` with an iterable. Use `add_node_from` instead"
            )
        target = self._node.rowstore
        bunch = nodes_for_adding

        def format_node_data(nodedef):
            d = dict(attr)
            u = nodedef[0] if isinstance(nodedef, tuple) else nodedef
            if isinstance(nodedef, tuple) and len(nodedef) > 1:
                d.update(nodedef[1])
            if d:
                for k, v in d.items():
                    yield (u, k, v)

        with self.helper.transaction:
            if not self.schema.node_cascade_on_delete:
                nbunch = map(format_node_data, bunch)
                nbunch = itertools.chain.from_iterable(nbunch)
                target.bulk_delete(map(lambda e: e[:2], nbunch))
            nbunch = map(format_node_data, bunch)
            nbunch = itertools.chain.from_iterable(nbunch)
            target.bulk_insert(nbunch, shift=1)

    def add_nodes_from(self, nodes_for_adding, **attr):
        """Add nodes to the graph

        Respect the NetworkX variant but optimize.

        Notes
        -----
        Using the networkx implementation of the method is correct,
        but for optimization purpose, it is better to overload it.
        Two algorithms will be performed depending if nodes_for_adding
        is an iterator or an iterable which is not an iterator.
        In the first case, we assume only one pass over the data is possible
        and will perform many more queries to update the database to insert
        data values.
        In the later we will first do one pass to insert nodes and then another
        to insert their data values. The algorithm is choose by testing
        if iter(nodes_for_adding) is nodes_for_adding.
        """
        bunch = nodes_for_adding
        with self.helper.transaction():
            if iter(bunch) is bunch:
                target = self._node.rowstore
                if self.schema.node_cascade_on_delete:
                    bunch = map(
                        lambda ndef: (ndef, {})
                        if not isinstance(ndef, tuple)
                        else ndef,
                        bunch,
                    )
                    for node, d in bunch:
                        self.add_node(node, **d, **attr)
                else:

                    def format_node_data(nodedef):
                        d = dict(attr)
                        if type(nodedef) is not tuple:
                            u = self._allow_none_node(nodedef)
                        else:
                            u = self._allow_none_node(nodedef[0])
                            if len(nodedef) > 1:
                                d.update(nodedef[1])
                        if d:
                            for k, v in d.items():
                                yield (u, k, v)
                        else:
                            yield (u,)

                    bunch = map(format_node_data, bunch)
                    bunch = itertools.chain.from_iterable(bunch)
                    target.bulk_insert(bunch)
            else:
                n_bunch = iter(bunch)
                n_bunch = map(
                    lambda ndef: ndef[0] if isinstance(ndef, tuple) else ndef, n_bunch
                )
                self.add_nodes_without_data_from(n_bunch)
                self.add_node_data_from(bunch, **attr)

    def remove_nodes_from(self, nodes, cascade=None):
        """Remove multiple nodes.

        If cascade is True, suppose edges refering to nodes
        have the "ON DELETE CASCADE". Hence, constraints
        are done on SQLite side. If cascade is False,
        we user the nx version to ensure structure.

        Parameters
        ----------
        nodes : iterable container
                A container of nodes (list, dict, set, etc.). If a node
                in the container is not in the graph it is silently
                ignored.

        See Also
        --------
        remove_node
        """
        cascade = cascade or self.schema.node_cascade_on_delete
        with self.helper.transaction():
            if cascade:
                self._node.rowstore.bulk_delete(map(lambda e: (e,), nodes))
            else:
                if iter(nodes) is nodes:
                    for node in nodes:
                        self.remove_node(node)
                else:
                    self._node.rowstore.bulk_delete(map(lambda e: (e,), nodes))
                    tds = self.write_edge_target.rowstore.tupleDictSchema
                    ph = self.dialect.constants.Placeholder
                    self.helper.executemany(
                        tds.delete_prefix_query((), suffcondition=tds[1].eq(ph)),
                        map(lambda e: (e,), nodes),
                    )

    # Edge insertion
    def add_edge_without_data(self, u_of_edge, v_of_edge, refresh_nodes=True):
        self.add_edges_without_data_from(
            [(u_of_edge, v_of_edge)], refresh_nodes=refresh_nodes
        )

    def add_edge_data(self, u_of_edge, v_of_edge, **attr):
        self.add_edge_data_from([(u_of_edge, v_of_edge)], **attr)

    def add_edge(self, u_of_edge, v_of_edge, refresh_nodes=True, **attr):
        """
        Overload networkx.Graph.add_edge.
        + u_of_edge: source of edge
        + v_of_edge: target of edge
        + attr: keyworded list of additional edge attributes

        Should update edge (u,v) with attributes from attr, after,
        possibly, inserting the edge (u,v).

        Actually reduce to add_edges_from for code simplicity.
        """
        with self.helper.transaction():
            self.add_edge_without_data(
                u_of_edge, v_of_edge, refresh_nodes=refresh_nodes
            )
            self.add_edge_data(u_of_edge, v_of_edge, **attr)

    def remove_edge(self, u, v):
        try:
            with self.helper.transaction():
                if not self.lazy and not (u, v) in self.edges:
                    raise KeyError
                self.write_edge_target.rowstore.delete((u, v), no_reinsert=1)
                if not self.is_directed() and not self.schema.symmetrized:
                    self.write_edge_target.rowstore.delete((v, u))
        except KeyError as e:
            raise NetworkDiskError(f"The edge {u}-{v} is not in the graph.") from e
        # self.remove_edges_from([(u, v)])

    def add_edges_without_data_from(self, ebunch_to_add, refresh_nodes=True):
        """Add edges without data

        Notes
        -----
        Add edges from iterable `ebunch_to_add` of tuples. Each
        tuple should have length 2 or 3. In the latter case, the
        third component, which typically stores data of the edge,
        is dropped.
        """
        schema = self.schema
        target = self.write_edge_target.rowstore
        bunch = ebunch_to_add

        def format_edge(edgedef):
            if len(edgedef) < 2 or len(edgedef) > 3:
                raise NetworkDiskError(
                    f"Edge tuple {edgedef} must be a 2-tuple or 3-tuple"
                )
            edgedef = tuple(map(self._allow_none_node, edgedef[:2]))
            return edgedef

        bunch = map(format_edge, bunch)
        # Symmetrize edges if required
        if not self.is_directed() and not schema.symmetrized:
            if iter(bunch) is bunch:
                symmetrize = lambda e: (e, tuple(reversed(e)))
                bunch = map(symmetrize, bunch)
                bunch = itertools.chain.from_iterable(bunch)
            else:
                symmetrize = lambda e: tuple(reversed(e))
                symedge_bunch = iter(bunch)
                symedge_bunch = map(symmetrize, symedge_bunch)
                bunch = itertools.chain(bunch, symedge_bunch)
        # insert edges
        with self.helper.transaction():
            target.bulk_insert(bunch)
            # refresh nodes
            if refresh_nodes:
                self.__refresh_nodes()

    def add_edge_data_from(self, ebunch_to_add, **attr):
        """
        Parameters
        ----------
        ebunch_to_add:
                iterator of tuple of length 2 (u,v) or 3 (u, v, d) with
                (u,v) an existing edge of the graph, and d a dictionary
                to update the edge data.
        **attr:
                a keyworded list of optional arguments, to be added to
                all edge data from ebunch_to_add.
        """
        schema = self.schema
        target = self.write_edge_target.rowstore
        bunch = ebunch_to_add
        # Format, symmetrize (if needed), and check edges
        if not self.is_directed() and not schema.symmetrized:
            # symmetrizing needed
            def format_edge_data(edgedef):
                if len(edgedef) < 2 or len(edgedef) > 3:
                    raise NetworkDiskError(
                        f"Edge tuple {edgedef} must be a 2-tuple or 3-tuple."
                    )
                d = dict(attr)
                uv = tuple(map(self._allow_none_node, edgedef[:2]))
                if len(edgedef) > 2:
                    d.update(edgedef[2])
                for kv in d.items():
                    yield uv + kv
                # symmetrize edges
                for kv in d.items():
                    yield tuple(reversed(uv)) + kv
        else:

            def format_edge_data(edgedef):
                if len(edgedef) < 2 or len(edgedef) > 3:
                    raise NetworkDiskError(
                        f"Edge tuple {edgedef} must be a 2-tuple or 3-tuple."
                    )
                d = dict(attr)
                uv = tuple(map(self._allow_none_node, edgedef[:2]))
                if len(edgedef) > 2:
                    d.update(edgedef[2])
                for kv in d.items():
                    yield uv + kv

        bunch = map(format_edge_data, bunch)
        bunch = itertools.chain.from_iterable(bunch)
        with self.helper.transaction():
            target.bulk_insert(bunch, shift=2)

    def add_edges_from(self, ebunch_to_add, refresh_nodes=True, **attr):
        """Add edges in bulk to self

        Respect the NetworkX signature.

        Notes
        -----
        Using the networkx implementation of the method is correct,
        but for optimization purpose, it is better to overload it.
        For better performance, one should drop and add triggers. We
        perform two different strategy depending on whether the
        argument `ebunch_to_add` is an 'Iterable' or an 'Iterator'.
        The case is determined determined by testing the pointer
        equality of `iter(ebunch_to_add)` to `ebunch_to_add`. If the
        two object are the same, then `ebunch_to_add` is assumed to
        be an 'Iterator' over which only one pass is allowed. In
        this case, edges and their associated data will be inserted
        simultaneously, while nodes are inserted after using the
        `refresh_nodes` method. It requires to perform many queries.
        In this other case, `ebunch_to_add` is assumed to be an
        'Iterable' over which several passes are possible. Hence, a
        more efficient implementation is used, in which first edges
        are inserted, and then their data. Performance are vastly
        improve.
        """
        # ebunch_to_add is an iterable of (u, v) or (u, v, d), referenced as edgedef below
        # ⟶ we format them by setting default values of edge dictionary from attr, popping off it if empty, and ordering vertices
        schema = self.schema
        target = self.write_edge_target.rowstore
        bunch = ebunch_to_add
        if iter(bunch) is bunch:
            symmetrize = not self.is_directed() and not schema.symmetrized

            def format_edge_data(edgedef):
                if len(edgedef) < 2 or len(edgedef) > 3:
                    raise NetworkDiskError(
                        f"Edge tuple {edgedef} must be a 2-tuple or 3-tuple."
                    )
                d = dict(attr)
                uv = tuple(map(self._allow_none_node, edgedef[:2]))
                if len(edgedef) > 2:
                    d.update(edgedef[2])
                prefs = [uv]
                if symmetrize:
                    prefs.append(tuple(reversed(uv)))
                for pref in prefs:
                    if d:
                        for kv in d.items():
                            yield pref + kv
                    else:
                        yield pref

            # Unfold each provided data
            bunch = map(format_edge_data, bunch)
            bunch = itertools.chain.from_iterable(bunch)
            with self.helper.transaction():
                # insert
                target.bulk_insert(bunch)
                # refresh nodes
                if refresh_nodes:
                    self.__refresh_nodes()
        else:
            # First add edges without data
            edge_bunch = iter(bunch)
            with self.helper.transaction():
                self.add_edges_without_data_from(
                    edge_bunch, refresh_nodes=refresh_nodes
                )
                # Second add edge data
                self.add_edge_data_from(bunch, **attr)

    def remove_edges_from(self, ebunch):
        with self.helper.transaction():
            if not self.is_directed() and not self.schema.symmetrized:
                # no direct access to symmetric edge store
                if iter(ebunch) is ebunch:
                    symmetrize = lambda e: (e, tuple(reversed(e)))
                    ebunch = map(symmetrize, ebunch)
                    ebunch = itertools.chain.from_iterable(ebunch)
                else:
                    symmetrize = lambda e: tuple(reversed(e))
                    symedge_bunch = iter(ebunch)
                    symedge_bunch = map(symmetrize, symedge_bunch)
                    ebunch = itertools.chain(ebunch, symedge_bunch)
            self.write_edge_target.rowstore.bulk_delete(ebunch, no_reinsert=1)

    def __refresh_nodes(self):
        """
        Update nodes table with all edge endpoints occurring in the
        edges table. Methods useful when performing bulk insert or
        where data between nodes and edges are inconsistent.
        """
        self.helper.execute(self.schema.refresh_nodes_query())

    def size(self, weight=None, default=1.0):
        if not weight:
            condition = self.dialect.conditions.EmptyCondition()
            if not self.is_directed():
                condition &= self.source_column.le(self.target_column)
            return self.edgestore.rowstore.select(
                stop=2, count=True, condition=condition
            )
        else:
            etds = self.schema.edgestore
            res = etds.left_projection_tupledict(2, weight)
            valCol = res[2].ifnull(default).cast("NUMERIC").sum()
            res = res.select_row_query(cols=(valCol,))
        return next(iter(self.helper.execute(res)))[0]

    def nbunch_iter(
        self,
        nbunch=None,
        *mandatory_keys,
        data=False,
        default=None,
        limit=None,
        condition=None,
        **if_key_then_value,
    ):
        """Iter over nodes according to filtering conditions

        Parameters
        ----------
        nbunch: iterable or None or Graph node
                either a Graph node, or an iterable of elements. If in the
                former case, an iterator-query with `nbunch` as unique
                element is returned. Otherwise (in the latter case), an
                iterable query with all nodes of `self` that belong to the
                iterable `nbunch` are returned. Alternatively, the
                parameter can be set to `None` (default), in which case,
                all the graph nodes are taken.

        mandatory_keys: tuple[mapping or key or function]
                Intuitively, the list of keys that selected nodes should have.  Yet,
                some of the items may be mappings.  These mapping items are initially
                extracted from the list, and use to populate the `if_key_then_value`
                mapping, not overwriting already specified items.  In this way, it is
                possible to specify `if_key_then_value` keys that are not keywordable
                (e.g., `True` or `'a key with spaces'`), as well as keys that are
                reserved keywords of the function (e.g., `'data'` or `'condition'`).
                It may also be a boolean function that should be matched by at least one key.

        data: bool or str
                If `False` (the default), then nodes are returned without data.  If
                `True`, then they are returned with data.  If a string, then pairs
                `(n, d)` are returned where `n` is a selected node and `d` is either
                the value associated with key `data`, if any, or `default`,
                otherwise.

        default: any
                The default data to return if `data` is a key (`str`), for nodes not
                having this key.

        if_key_then_value: mapping
                a k/v mapping.  A node is taken if and only if one of the two
                following condition is met: either the node does not have the given
                key k, or the value associated with the given key k matches v.
                Notice that the former condition is avoided by giving the same key
                within the `mandatory_keys` tuple.  Concerning the latter condition,
                the matching is defined as follows.  If v is callable, then it should
                take one column parameter and return a condition.  In this case the
                condition obtained by its call on the node value column is taken.
                Otherwise, v is considered as a value, and the equality condition
                with the value v is taken instead.  Therefore, passing `key=3` is
                equivalent to passing `key=lambda c: c.eq(3)`.

        condition: condition or None
                a condition to add in every filter.

        limit: int or None
                the number of answers that should be returned
                or None if every answer should be returned

        Returns
        -------
        An iterable query representing the selected nodes.  The iterable
        elements may be nodes `v` (if `data` is `False`), or pairs `(n, d)`
        with `d` the value associated with key `data` (if a string) in the data
        of node `n`, or triples `(n, k, v)` with `k`/`v` be pairs key/value of
        the data of node `n` (if `data` is `True`).
        """
        namecol, keycol, valcol = self.schema.nodes
        apply_fct = None
        if data is True:
            apply_fct = lambda it: shorten_tuples(it, 1, maxdepth=2)

        def ib(condition, nonstrict=None):
            rs = self._node.rowstore
            if nonstrict:
                rs = rs.filter_from_column(0, nonstrict)
                notnull = 0
            else:
                notnull = False
            return rs.iter_bunch(
                stop=1, condition=condition, notnull=notnull, distinct=True
            )

        # sorts and prepares the key/values arguments
        kwargs_if_key_then_value = {}
        args_mandatory_keys = set()
        kwargs_keys_and_values = {}

        # merges the positional and keyworded if_key_then_value arguments
        for d in mandatory_keys:
            if hasattr(d, "keys"):
                for k, v in dict.items(d):
                    if_key_then_value.setdefault(k, v)
            else:
                args_mandatory_keys.add(d)

        for k, v in if_key_then_value.items():
            # turns all if_key_then_value arguments into conditions
            if not callable(v):
                v = (lambda v: (lambda c: c.eq(v)))(v)

            # creates a new dict for keys that are both mandatory
            # AND whose value should be checked
            if k in args_mandatory_keys:
                args_mandatory_keys.remove(k)
                kwargs_keys_and_values[k] = v
            else:
                kwargs_if_key_then_value[k] = v

        common_condition = condition or self.dialect.conditions.EmptyCondition()
        condition = common_condition
        nonstrict = None

        # initialises condition using the "first" argument of the function
        if kwargs_keys_and_values:
            k, v = kwargs_keys_and_values.popitem()
            condition &= self.nodes_satisfying_condition(k, v)
        elif args_mandatory_keys:
            k = args_mandatory_keys.pop()
            condition &= self.nodes_satisfying_condition(k)
        elif not condition and kwargs_if_key_then_value:
            k, v = kwargs_if_key_then_value.popitem()
            condition &= self.nodes_satisfying_condition(k, v, strict=False)
            nonstrict = self.nodes_satisfying_condition(k, strict=True)

        # initialises a minimal iterative query iq
        # using nbunch and condition
        if nbunch is None:
            if not condition and data is not False:
                rs = self._node.rowstore
                if data is True:
                    d_iq = rs.iter_bunch(stop=3, notnull=0, orderby=(0,))
                else:
                    condition = rs.tupleDictSchema[1].eq(data)
                    rs = rs.filter_from_column(0, condition)
                    d_iq = rs.iter_bunch(stop=3, notnull=0)
                    q = d_iq.query
                    c = q[2]
                    if default is not None:
                        c = q.external_columns.sources.get(c, c)
                        c = c.ifnull(default)
                    q = q.set_columns((0, c))
                    d_iq = type(d_iq)(d_iq.helper, q)
                if apply_fct:
                    d_iq = d_iq.apply(apply_fct)
                return d_iq
            else:
                iq = ib(condition, nonstrict=nonstrict)
        elif nbunch in self:
            iq = ib(namecol.eq(nbunch) & condition, nonstrict=nonstrict)
        elif hasattr(
            nbunch, "external_columns"
        ):  # nbunch is an iterable query, but a query above all
            iq = ib(namecol.inset(nbunch) & condition, nonstrict=nonstrict)
        elif not hasattr(nbunch, "__iter__"):
            error = NetworkDiskError("nbunch is not a node or a sequence of nodes.")
            raise error
        elif hasattr(
            nbunch, "query"
        ):  # nbunch is an iterable query, but a query above all
            iq = ib(namecol.inset(nbunch.query) & condition, nonstrict=nonstrict)
        else:
            nbunch = filter(self._node.coordinate_checker, nbunch)
            try:
                nbunch = tuple(nbunch)
            except TypeError as e:
                raise NetworkDiskError(*e.args) from e
            iq = ib(namecol.inset(*nbunch) & condition, nonstrict=nonstrict)

        # applies the remaining arguments to iq
        for k in args_mandatory_keys:
            iq = iq.intersection(
                ib(
                    common_condition & self.nodes_satisfying_condition(k),
                    nonstrict=nonstrict,
                )
            )
        for k, v in kwargs_keys_and_values.items():
            iq = iq.intersection(
                ib(
                    common_condition & self.nodes_satisfying_condition(k, v),
                    nonstrict=nonstrict,
                )
            )
        for k, v in kwargs_if_key_then_value.items():
            nonstrict = self.nodes_satisfying_condition(k, strict=True)
            iq = iq.intersection(
                ib(
                    common_condition
                    & self.nodes_satisfying_condition(k, v, strict=False),
                    nonstrict=nonstrict,
                )
            )

        if limit:
            iq = iq.limit(limit)

        if data is not False:
            rs = self._node.rowstore
            if data is True:
                d_iq = rs.iter_bunch(stop=3, notnull=0, orderby=(0,))
            else:
                condition = rs.tupleDictSchema[1].eq(data)
                rs = rs.filter_from_column(0, condition)
                d_iq = rs.iter_bunch(stop=3, notnull=0)
                q = d_iq.query
                c = q[2]
                if default is not None:
                    c = q.external_columns.sources.get(c, c)
                    c = c.ifnull(default)
                q = q.set_columns((0, c))
                d_iq = type(d_iq)(d_iq.helper, q)
            ql = iq.query.name_query("node_selection")
            qr = d_iq.query.name_query("data_selection")
            jq = ql.left_join_query(qr, (0, 0))
            q = jq.select_query(columns=(ql[0], *qr[1:]))
            d_iq = type(d_iq)(d_iq.helper, q)
            if apply_fct:
                d_iq = d_iq.apply(apply_fct)
            return d_iq

        return iq.project(0)

    def nodes_satisfying_condition(self, key, value=notProvidedArg, strict=True):
        """Simple builder of condition on node data.

        PARAMETERS
        ----------
        key: str or callable
                The node data key to filter.  If callable, then it is expected to
                return a condition when called with a column parameter.  In that
                case the 'key-condition' is the condition returned when the column
                parameter is the node data key column.  Otherwise, it is the key
                name to filter against equality.  E.g., `key=3` is equivalent to
                `key=lambda c: c.eq(3)`.

        value: any
                If provided, a condition is built in addition to the one resulting
                from the treatment of the `key` parameter, as follows.  If the given
                `value` is callable, then it is expected to take one column argument,
                namely the node data value column, and return a condition.  Otherwise
                it is considered as a (any-type but callable) value indicating the
                value to be matched by the node data value column.  E.g., `value=3`
                is equivalent to `value=lambda c: c.eq(3)`.

        strict: Boolean = True
                This flag is aimed for internal use only.  It allows to construct a
                different condition when the intention is to filter only nodes that
                do admit the corresponding key `key`, thus keeping all nodes not
                admitting it.
        """
        tds = self.schema.nodes
        if value is notProvidedArg:
            cond = None
        elif callable(value):
            cond = value(tds[2])
        else:
            cond = tds[2].eq(value)
        if strict:
            if callable(key):
                cond = key(tds[1]) & cond
            else:
                cond = tds[1].eq(key) & cond
        else:
            cond = tds[1].isnull() | cond
        return cond

    def find_all_nodes(
        self, *mandatory_keys, condition=None, limit=None, **if_key_then_value
    ):
        """A wrapper of nbunch_iter, to filter node by condition but not by bunch.

        Returns
        -------
        Return an iterable query that fetches the nodes found with the condition.

        EXAMPLES
        --------
        >>> G = nd.sqlite.Graph()
        >>> G.add_node(0, foo="bar", color="red", shape="circle")
        >>> G.add_node(1, foo="bar", color="yellow", shape="rectangle")
        >>> G.add_node(2, foo="not bar", color="brown", shape="circle")
        >>> G.add_node(3, foo="bar", shape="diamond")
        >>> G.add_node(4, color="purple")
        >>> sorted(G.find_all_nodes("foo"))
        [0, 1, 2, 3]
        >>> sorted(G.find_all_nodes("foo", limit=2))
        [0, 1]
        >>> sorted(G.find_all_nodes(foo="bar")) #observe that 4 is listed
        [0, 1, 3, 4]
        >>> sorted(G.find_all_nodes("foo", foo="bar")) #combining both
        [0, 1, 3]
        >>> sorted(G.find_all_nodes("foo", "color", foo="bar"))
        [0, 1]
        >>> sorted(G.find_all_nodes("color", foo="bar"))
        [0, 1, 4]
        >>> sorted(G.find_all_nodes("color", color=lambda c: c.gt("purple")))
        [0, 1]
        >>> sorted(G.find_all_nodes(lambda e: e.like("%o%")))
        [0, 1, 2, 3, 4]
        """
        return self.nbunch_iter(
            None, *mandatory_keys, condition=condition, limit=limit, **if_key_then_value
        )

    def find_one_node(self, *args, condition=None, **kwargs):
        """Find one node satisfying some condition. This is a wrapper of find_all_nodes method.

        Returns
        -------
        Return one node found with the condition.
        """
        try:
            return next(
                iter(self.find_all_nodes(*args, limit=1, condition=condition, **kwargs))
            )
        except StopIteration as e:
            raise NetworkDiskError("No node corresponding to criteria found") from e

    def ebunch_iter(
        self,
        ebunch=None,
        *mandatory_keys,
        data=False,
        default=None,
        condition=None,
        limit=None,
        **if_key_then_value,
    ):
        """Iter over edges according to filtering conditions

        Parameters
        ----------
        ebunch: iterable or None or Graph edge
                either a Graph edge, or an iterable of elements.  If in the former
                case, an iterator-query with `ebunch` as unique element is returned.
                Otherwise (in the latter case), an iterable query with all nodes of
                `self` that belong to the iterable `ebunch` are returned.
                Alternatively, the parameter can be set to `None` (default), in which
                case, all the graph edges are taken.

        mandatory_keys: tuple[mapping or key]
                Intuitively, the list of keys that selected edges should have.  Yet,
                some of the items may be mappings.  These mapping items are initially
                extracted from the list, and use to populate the `if_key_then_value`
                mapping, not overwriting already specified items.  In this way, it is
                possible to specify `if_key_then_value` keys that are not keywordable
                (e.g., `True` or `'a key with spaces'`), as well as keys that are
                reserved keywords of the function (e.g., `'data'` or `'condition'`).
                It may also be a boolean function that should be matched by at least one key.

        data: bool or str
                If `False` (the default), then edges are returned without data.  If
                `True`, then they are returned with data.  If a string, then triples
                `(s, t, d)` are returned where `s, t` is a selected edge and `d` is
                either the value associated with key `data`, if any, or `default`,
                otherwise.

        default: any
                The default data to return if `data` is a key (`str`), for edges not
                having this so-specified key.

        if_key_then_value: mapping
                a k/v mapping.  An edge is taken if and only if one of the two
                following condition is met: either the edge does not have the given
                key k, or the value associated with the given key k matches v.
                Notice that the former condition is avoided by giving the same key
                within the `mandatory_keys` tuple.  Concerning the latter condition,
                the matching is defined as follows.  If v is callable, then it should
                take one column parameter and return a condition.  In this case the
                condition obtained by its call on the node value column is taken.
                Otherwise, v is considered as a value, and the equality condition
                with the value v is taken instead.  Therefore, passing `key=3` is
                equivalent to passing `key=lambda c: c.eq(3)`.

        condition: condition or None
                a condition to add in every filter.

        limit: int or None
                the number of answers that should be returned
                or None if every answer should be returned

        Returns
        -------
        An iterable query representing the selected edges.  The iterable
        elements may be edges `(s, t)` (if `data` is `False`), or triples
        `(s, t, d)` with `d` the value associated with key `data` (if a string)
        in the data of edge `s, t`, or quadruples `(s, t, k, v)` with `k`/`v`
        be pairs key/value of the data of edge `s, t` (if `data` is `True`).
        """
        srccol, trgtcol, keycol, valcol = self.schema.edgestore

        def ib(condition, nonstrict=None):
            if self.is_directed():
                rs = self.edgestore.rowstore
            else:
                if self.asymedges is not None:
                    rs = self.asymedges.rowstore
                else:
                    # TODO: check this!
                    rs = self.edgestore.rowstore
                    nonstrict = rs[0].lt(rs[1]) & nonstrict
            if nonstrict:
                rs = rs.filter_from_column(0, nonstrict)
                notnull = 1
            else:
                notnull = False
            return rs.iter_bunch(
                condition=condition, notnull=notnull, stop=2, distinct=True
            )

        kwargs_keys_and_values = {}
        args_mandatory_keys = set()
        kwargs_if_key_then_value = {}
        for d in mandatory_keys:
            if hasattr(d, "keys"):
                for k, v in dict.items(d):
                    if_key_then_value.setdefault(k, v)
            else:
                args_mandatory_keys.add(d)
        for k, v in if_key_then_value.items():
            if not callable(v):
                v = (lambda v: (lambda c: c.eq(v)))(v)
            if k in mandatory_keys:
                kwargs_keys_and_values[k] = v
            else:
                kwargs_if_key_then_value[k] = v
        common_condition = condition or self.dialect.conditions.EmptyCondition()
        condition = common_condition
        nonstrict = None

        if kwargs_keys_and_values:
            k, v = kwargs_keys_and_values.popitem()
            condition &= self.edges_satisfying_condition(k, v)
        elif args_mandatory_keys:
            k = args_mandatory_keys.pop()
            condition &= self.edges_satisfying_condition(k)
        elif not condition and kwargs_if_key_then_value:
            k, v = kwargs_if_key_then_value.popitem()
            condition &= self.edges_satisfying_condition(k, v, strict=False)
            nonstrict = self.edges_satisfying_condition(k, strict=True)

        if ebunch is None:
            if not condition and data is not False:
                rs = self.edgestore.rowstore
                if data is True:
                    d_iq = rs.iter_bunch(stop=4, notnull=0)
                else:
                    condition = rs.tupleDictSchema[2].eq(data)
                    rs = rs.filter_from_column(0, condition)
                    d_iq = rs.iter_bunch(stop=4, notnull=0)
                    q = d_iq.query
                    c = q[3]
                    if default is not None:
                        c = q.external_columns.sources.get(c, c)
                        c = c.ifnull(default)
                    q = q.set_columns((0, 1, c))
                    d_iq = type(d_iq)(d_iq.helper, q)
                return d_iq
            else:
                iq = ib(condition, nonstrict=nonstrict)
        elif isinstance(ebunch, tuple) and len(ebunch) == 2 and ebunch in self.edges:
            iq = ib(
                srccol.eq(ebunch[0]) & trgtcol.eq(ebunch[1]) & condition,
                nonstrict=nonstrict,
            )
        elif hasattr(ebunch, "external_columns"):
            etplcol = self.dialect.columns.TupleColumn(srccol, trgtcol)
            iq = ib(etplcol.inset(ebunch) & condition, nonstrict=nonstrict)
        elif not hasattr(ebunch, "__iter__"):
            error = NetworkDiskError("ebunch is not an edge or a sequence of edges.")
            raise error
        elif hasattr(ebunch, "query"):
            etplcol = self.dialect.columns.TupleColumn(srccol, trgtcol)
            iq = ib(etplcol.inset(nbunch.query) & condition, nonstrict=nonstrict)
        else:
            ebunch = filter(self._node.coordinate_checker, ebunch)
            try:
                ebunch = tuple(ebunch)
            except TypeError as e:
                raise NetworkDiskError() from e
            etplcol = self.dialect.columns.TupleColumn(srccol, trgtcol)
            iq = ib(etplcol.inset(*ebunch) & condition, nonstrict=nonstrict)

        for k, v in kwargs_keys_and_values.items():
            condition = common_condition & self.edges_satisfying_condition(k, v)
            iq = iq.intersection(ib(condition))
        for k in args_mandatory_keys:
            condition = common_condition & self.edges_satisfying_condition(k)
            iq = iq.intersection(ib(condition))
        for k, v in kwargs_if_key_then_value.items():
            condition = common_condition & self.edges_satisfying_condition(
                k, v, strict=False
            )
            nonstrict = self.edges_satisfying_condition(k, strict=True)
            iq = iq.intersection(ib(condition, nonstrict=nonstrict))

        if limit:
            iq = iq.limit(limit)

        if data is not False:
            rs = self.edgestore.rowstore
            if data is True:
                d_iq = rs.iter_bunch(stop=4, notnull=1)
            else:
                condition = rs.tupleDictSchema[2].eq(data)
                rs = rs.filter_from_column(0, condition)
                d_iq = rs.iter_bunch(stop=4, notnull=1)
                q = d_iq.query
                c = q[3]
                if default is not None:
                    c = q.external_columns.sources.get(c, c)
                    c = c.ifnull(default)
                q = q.set_columns((0, 1, c))
                d_iq = type(d_iq)(d_iq.helper, q)
            ql = iq.query.name_query("edge_selection")
            qr = d_iq.query.name_query("data_selection")
            jq = ql.left_join_query(qr, (0, 0), (1, 1))
            q = jq.select_query(columns=(ql[0], ql[1], *qr[2:]))
            iq = type(d_iq)(d_iq.helper, q)
        return iq

    def edges_satisfying_condition(self, key, value=notProvidedArg, strict=True):
        """Simple builder of condition on edge data.

        Parameters
        ----------
        key: str or callable
                The edge data key to filter.  If callable, then it is expected to
                return a condition when called with a column parameter.  In that
                case the 'key-condition' is the condition returned when the column
                parameter is the edge data key column.  Otherwise, it is the key
                name to filter against equality.  E.g., `key=3` is equivalent to
                `key=lambda c: c.eq(3)`.

        value: any
                If provided, a condition is built in addition to the one resulting
                from the treatment of the `key` parameter, as follows.  If the given
                `value` is callable, then it is expected to take one column argument,
                namely the edge data value column, and return a condition.  Otherwise
                it is considered as a (any-type but callable) value indicating the
                value to be matched by the edge data value column.  E.g., `value=3`
                is equivalent to `value=lambda c: c.eq(3)`.

        strict: Boolean = True
                This flag is aimed for internal use only.  It allows to construct a
                different condition when the intention is to filter only edges that
                do admit the corresponding key `key`, thus keeping all edges not
                admitting it.

        Returns
        -------
        Return an object representing the condition adapted to the graph schema.
        """
        if self.is_directed():
            tds = self.schema.edgestore
        else:
            # TODO: check this
            tds = self.schema.asymedges
        if value is notProvidedArg:
            cond = None
        elif callable(value):
            cond = value(tds[3])
        else:
            cond = tds[3].eq(value)
        if strict:
            if callable(key):
                cond = key(tds[2]) & cond
            else:
                cond = tds[2].eq(key) & cond
        else:
            cond = tds[2].isnull() | cond
        return cond

    def find_all_edges(
        self, *mandatory_keys, condition=None, limit=None, **if_key_then_value
    ):
        """A wrapper of ebunch_iter, to filter edges by condition but not by bunch.

        Returns
        -------
        Return an iterable query that fetches the edges found with the condition.

        EXAMPLES
        --------
        >>> G = nd.sqlite.DiGraph()
        >>> G.add_edge(0, 1, foo="bar", color="red", shape="circle")
        >>> G.add_edge(1, 2, foo="bar", color="yellow", shape="rectangle")
        >>> G.add_edge(2, 3, foo="not bar", color="brown", shape="circle")
        >>> G.add_edge(3, 4, foo="bar", shape="diamond")
        >>> G.add_edge(4, 0, color="purple")
        >>> sorted(G.find_all_edges("foo"))
        [(0, 1), (1, 2), (2, 3), (3, 4)]
        >>> sorted(G.find_all_edges("foo", limit=2))
        [(0, 1), (1, 2)]
        >>> sorted(G.find_all_edges(foo="bar")) #observe that (4, 0) is listed
        [(0, 1), (1, 2), (3, 4), (4, 0)]
        >>> sorted(G.find_all_edges("foo", foo="bar")) #combining both thus avoiding (0, 4)
        [(0, 1), (1, 2), (3, 4)]
        >>> sorted(G.find_all_edges("foo", "color", foo="bar"))
        [(0, 1), (1, 2)]
        >>> sorted(G.find_all_edges("color", foo="bar"))
        [(0, 1), (1, 2), (4, 0)]
        >>> sorted(G.find_all_edges("color", color=lambda c: c.gt("purple")))
        [(0, 1), (1, 2)]
        >>> sorted(G.find_all_edges(lambda e: e.like("%o%")))
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]

        >>> G = nd.sqlite.Graph()
        >>> G.add_edge(0, 1, foo="bar", color="red", shape="circle")
        >>> G.add_edge(1, 2, foo="bar", color="yellow", shape="rectangle")
        >>> G.add_edge(2, 3, foo="not bar", color="brown", shape="circle")
        >>> G.add_edge(3, 4, foo="bar", shape="diamond")
        >>> G.add_edge(4, 0, color="purple")
        >>> sorted(G.find_all_edges("foo"))
        [(0, 1), (1, 2), (2, 3), (3, 4)]
        >>> sorted(map(tuple, map(sorted, G.find_all_edges(foo="bar")))) #observe that (0, 4) is listed
        [(0, 1), (0, 4), (1, 2), (3, 4)]
        >>> sorted(map(tuple, map(sorted, G.find_all_edges("foo", foo="bar")))) #combining both thus avoiding (0, 4)
        [(0, 1), (1, 2), (3, 4)]
        >>> sorted(map(tuple, map(sorted, G.find_all_edges("foo", "color", foo="bar"))))
        [(0, 1), (1, 2)]
        >>> sorted(map(tuple, map(sorted, G.find_all_edges("color", foo="bar"))))
        [(0, 1), (0, 4), (1, 2)]
        >>> sorted(map(tuple, map(sorted, G.find_all_edges("color", color=lambda c: c.gt("purple")))))
        [(0, 1), (1, 2)]
        """
        return self.ebunch_iter(
            None, *mandatory_keys, condition=condition, limit=limit, **if_key_then_value
        )

    def find_one_edge(self, *args, condition=None, **kwargs):
        """Find one edge satisfying some condition. This is a wrapper of find_all_edges method.

        Returns
        -------
        Return one edge found with the condition.
        """
        try:
            return next(
                iter(self.find_all_edges(*args, limit=1, condition=condition, **kwargs))
            )
        except StopIteration as e:
            raise NetworkDiskError("No edge corresponding to criteria found") from e

    @functools.wraps(nxclasses.graph.Graph.copy)
    def copy(self, as_view=False):
        """
        +	if `as_view` is `True`:
                ⇒ dbpath and table_suffix are ignored
        +	otherwise
                + dbpath or table_suffix should be provided or G.helper.dbpath should be memory
                +	otherwise NetworkDiskError is raised
        """
        if as_view:
            return super().copy(as_view=as_view)
        raise NetworkDiskError(
            "impossible to copy database-stored graph (use copy_to_* methods instead)"
        )

    def copy_to_networkx(
        self, data=True, node_data=None, edge_data=None, graph_data=None
    ):
        node_data = data if node_data is None else node_data
        edge_data = data if edge_data is None else edge_data
        graph_data = data if graph_data is None else graph_data
        stop = None if edge_data else 2
        H = self.nx_variant()
        if node_data:
            H.add_nodes_from(self._node.fold().items())
        else:
            H.add_nodes_from(self._node)
        H.add_edges_from(self.edges(data=edge_data))
        # Performance issue dirty fixed here.
        if graph_data:
            H.graph.update(self.graph.fold())
        return H

    def copy_to_database(self, dbpath):
        raise NotImplementedError

    @functools.wraps(nxclasses.graph.Graph.to_directed)
    def to_directed(self, as_view=True):
        if not as_view:
            raise NetworkDiskError(f"Cannot perform deepcopy of {self.__class__} in DB")
        dischema = self.schema.to_directed()
        G = self.dialect.DiGraph(
            db=self.helper, schema=dischema, create=False, insert_schema=False
        )
        G._graph = self
        nd.sql.freeze(G)
        return G

    @functools.wraps(nxclasses.graph.Graph.to_undirected)
    def to_undirected(self, as_view=True):
        if not as_view:
            raise NetworkDiskError(f"Cannot perform deepcopy of {self.__class__} in DB")
        unschema = self.schema.to_undirected()
        G = self.dialect.Graph(
            db=self.helper, schema=unschema, create=False, insert_schema=False
        )
        G._graph = self
        nd.sql.freeze(G)
        return G

    def subgraph(self, nodes, temporary_table=False):
        """Return a subgraph view or a static subgraph of the subgraph induced by `nodes`

        The induced subgraph of the graph contains the nodes in `nodes`
        and the edges between those nodes.

        Parameters
        ----------
        nodes: iterable or node or condition
                The nodes to select for the subgraph.  If an `IterableQuery`, a
                specific optimized condition is built.  If a condition, it should
                be a `filter_node` condition as accepted by the function
                `nd.sql.classes.subgraph_view`.

        temporary_table: bool, default=False
                If `True`, then the selected nodes will be stored in a temporary
                table on disk.  It will have much better performance but will not
                provide a view but a semi-static subgraph instead (edges are
                maintained but not nodes).  Ignored if `filter_node` is `False`.

        Returns
        -------
                A networkdisk Graph based on the same helper than self (DB-connector) and exposing the desired subgraph.

        Examples
        --------
        >>> G = nd.sqlite.Graph()
        >>> G.add_edges_from([(0, 1), (1, 2), (2, 3)])
        >>> K = G.subgraph([1, 2, 3])
        >>> sorted(K.edges)
        [(1, 2), (2, 3)]
        >>> sorted(K.nodes)
        [1, 2, 3]

        To increase performance, we can use temporary table for storing the
        node domain on disk:
        >>> J = G.subgraph([1, 2, 3], temporary_table=True)
        >>> sorted(J.edges)
        [(1, 2), (2, 3)]
        >>> sorted(J.nodes)
        [1, 2, 3]

        But `J` is not a view anylonger, `K` is a view:
        >>> G.remove_node(3)
        >>> sorted(K.nodes)
        [1, 2]
        >>> sorted(J.nodes)
        [1, 2, 3]

        However, `J` does follows correctly edges of `G`:
        >>> sorted(J.edges)
        [(1, 2)]
        >>> sorted(K.edges)
        [(1, 2)]
        """
        if hasattr(nodes, "__iter__"):
            if hasattr(nodes, "query"):
                nodes = self.node_column.inset(nodes.query)
            else:
                nodes = list(nodes)
                if not nodes:
                    nodes = self.dialect.conditions.FalseCondition()
                else:
                    nodes = self.node_column.inset(*(e for e in nodes))
        elif not hasattr(nodes, "qformat"):
            nodes = self.node_column.eq(nodes)
        return ndclasses.subgraph_view(
            self, filter_node=nodes, temporary_table=temporary_table
        )

    def edge_subgraph(self, edges, restrict_node_domain=True, temporary_table=False):
        """Returns a view of the subgraph induced by the specified edges.

        The induced subgraph of the graph contains the edges in `edges`.  By
        default, only nodes that are incident to some of these edges are in
        the induced subgraph.

        Parameters
        ----------
        edges: iterable
                The edges to select.

        restrict_node_domain: bool, default=True
                Whether to filter nodes so that only nodes incident to some selected
                edges are kept.  The default behavior is the `networkx.edge_subgraph`
                behavior.

        temporary_table: bool, default=False
                If `True`, then the selected nodes will be stored in a temporary
                table on disk.  It will have much better performance but will not
                provide a view but a semi-static subgraph instead (edges are
                maintained but not nodes).  Ignored if `filter_node` is `False`.

        Returns
        -------
                A networkdisk (Di)Graph view based on the same helper than self
                (DB-connection) and exposing the desired subgraph.

        Examples
        --------
        >>> G = nd.sqlite.Graph()
        >>> G.add_edges_from([(0, 1), (1, 2), (2, 3)])
        >>> K = G.edge_subgraph([(1, 2), (2, 3)])
        >>> sorted(K.edges)
        [(1, 2), (2, 3)]
        >>> sorted(K.nodes)
        [1, 2, 3]

        We can choose to keep all nodes:
        >>> H = G.edge_subgraph([(0, 1), (1, 2), (2, 3)], restrict_node_domain=False)
        >>> sorted(H.edges)
        [(1, 2), (2, 3)]
        >>> sorted(H.nodes)
        [0, 1, 2, 3]

        To increase performance, we can use temporary table for storing the
        node domain on disk:
        >>> J = G.edge_subgraph([(0, 1), (1, 2), (2, 3)], temporary_table=True)
        >>> sorted(J.edges)
        [(1, 2), (2, 3)]
        >>> sorted(J.nodes)
        [1, 2, 3]

        But `J` is not a view anylonger, `K` is a view:
        >>> G.remove_edge(2, 3)
        >>> sorted(J.edges)
        [(1, 2)]
        >>> sorted(J.nodes)
        [1, 2, 3]
        >>> sorted(K.edges)
        [(1, 2)]
        >>> sorted(K.nodes)
        [1, 2]
        """
        filter_node = None
        if hasattr(edges, "query"):
            edges = edges.query
            if not self.is_directed():
                edges = edges.union_query(edges.set_columns((edges[1], edges[0])))
            filter_edge = self.edge_tuplecolumn.inset(edges)
            if restrict_node_domain:
                nodes = edges.set_columns(edges[0])
                if self.is_directed():
                    # on undirected graphs, edges has been symmetrized
                    nodes = nodes.union_query(edges.set_columns(edges[1]))
                filter_node = self.node_column.inset(nodes)
        else:
            edges = set(edges)
            if not edges:
                filter_edge = self.dialect.conditions.FalseCondition()
                if restrict_node_domain:
                    filter_node = filter_edge
            else:
                if restrict_node_domain:
                    filter_node = self.node_column.inset(*set(sum(edges, ())))
                if not self.is_directed():
                    edges.update(map(tuple, map(reversed, list(edges))))
                    filter_edge = self.edge_tuplecolumn.inset(*edges)
                elif (
                    isinstance(edges, tuple)
                    and len(edges) == 2
                    and (
                        not hasattr(edges[0], "__iter__")
                        or not hasattr(edges[1], "__iter__")
                        or (hasattr(edges[0], "__len__") and len(edges[0]) != 2)
                        or (hasattr(edges[1], "__len__") and len(edges[1]) != 2)
                    )
                ):
                    # edges is considered as a single edge
                    filter_edge = self.edge_tuplecolumn.eq(edges)
                else:
                    filter_edge = self.edge_tuplecolumn.inset(*edges)
        return ndclasses.subgraph_view(
            self,
            filter_node=filter_node,
            filter_edge=filter_edge,
            restrict_edge_endpoints=temporary_table,
            temporary_table=temporary_table,
        )

    @property
    def node_column(self):
        return self.schema.nodes[0]

    @property
    def source_column(self):
        return self.schema.edgestore[0]

    @property
    def target_column(self):
        return self.schema.edgestore[1]

    @property
    def edge_tuplecolumn(self):
        return self.source_column.tuple_with(self.target_column)

    def drop_index(self):
        """
        Remove indexation. Can be useful in case of bulk insert where reindexing
        post insertion is faster than indexing during insertion.
        """
        for i in self.schema.indices:
            self.helper.execute(i.drop_query())
        pass

    def reindex(self):
        """
        Restore indices present in the schema.
        """
        for i in self.schema.indices:
            self.helper.execute(i.create_query())

    # @functools.wraps(nxclasses.graph.Graph.clear_edges)
    # Wrapping bug with nx < 2.5
    # TODO: the function will not work with **all** schemas.
    def clear_edges(self):
        self.edgestore.clear()
