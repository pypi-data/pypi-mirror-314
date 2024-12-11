from .schemata import ungraph, digraph
from .dialect import sqldialect as dialect
from networkdisk.exception import NetworkDiskSQLError

__all__ = ["DiGraphSchema", "GraphSchema", "ungraph", "digraph", "setup_graph_columns"]

dialect = dialect.provide_submodule(__name__)
dialect.register(False, "JSON", name="_default_node_type")
dialect.register(False, "JSON", name="_default_datakey_type")
dialect.register(False, "JSON", name="_default_datavalue_type")


@dialect.register(True)
class DiGraphSchema:
    """
    A `DiGraphSchema` is basically a collection of 5
    `TupleDictSchema`: nodes, edgestore, adj, graph (c.f.
    documentation of `GraphSchema`), and:
    +	pred: of depth 3, storing the reversed edges. It a
            view on `edgestore` for seeing graph predecessor relation.
            Alterations are performed directly on `edgestore`.

    The `edgestore` attribute provides a direct access to `edges`
    which is not required to admit every node as first coordinate
    (aka column), unlike `nx.Graph.adj`. It is initially set to
    the `edges` argument of the constructor. It is the preferred
    way to access edges, both for reading and altering them.

    The object has a further attribute, `schema`, just as
    `GraphSchema` objects.
    """

    def __init__(
        self,
        dialect,
        nodes,
        edges,
        graph,
        schema=None,
        readonly=None,
        refresh_not_unique_node=True,
        node_cascade_on_delete=True,
        schema_trace=(),
    ):
        """
        The constructor requires 3 TupleDictSchema arguments:
        +	nodes: of height 2, that store the nodes and their data;
        +	edges: of height 3, that store the edges and their data;
        +	graph: of height 1, that store the graph data.

        Optional arguments are the following:
        +	schema: an `ndsql.Schema` that gather the SQL structures
                to be created (if creation is requested). If not given,
                an `ndsql.Schema` is automatically built by inspecting the
                various `TupleDictSchema`.
        + refresh_node_unique a Boolean indicating if the refresh_node_script should refresh without taking care of duplicates
        (if False) or insert only new node (if True).
        """
        if readonly:
            nodes, edges, graph = (
                nodes.to_readonly(),
                edges.to_readonly(),
                graph.to_readonly(),
            )
        d = dict(
            dialect=dialect.name,
            nodes=nodes,
            edgestore=edges,
            graph=graph,
            schema=schema,
            readonly=readonly,
            refresh_not_unique_node=refresh_not_unique_node,
        )
        d.update(
            node_cascade_on_delete=node_cascade_on_delete,
            schema_trace=dict(schema_trace),
        )
        self.__setstate__(d)
        self.set_schema(schema)

    def set_schema(self, schema=None):
        if schema:
            assert all(
                cont.name in schema
                for tds in self.tupledictrows
                for cont in tds.get_schema_containers()
            )
        else:
            schema = self.dialect.schema.Schema()
            for tds in self.tupledictrows:
                for cont in tds.get_schema_containers():
                    schema.add_existing_container(cont)
        self.schema = schema

    def __getstate__(self):
        d = dict(
            dialect=self.dialect.name,
            nodes=self.nodes,
            edgestore=self.edgestore,
            graph=self.graph,
            schema=self.schema,
            readonly=self.readonly,
        )
        d.update(
            refresh_not_unique_node=self.refresh_not_unique_node,
            node_cascade_on_delete=self.node_cascade_on_delete,
            schema_trace=self.schema_trace,
        )
        return d

    def __setstate__(self, state):
        for k, v in state.items():
            if k == "dialect":
                v = dialect._dialects[v]
            setattr(self, k, v)
        self.adj = self.edgestore.left_overlap(self.nodes)
        self.revedgestore = revedgestore = self.edgestore.swap(0, 1)
        self.pred = revedgestore.left_overlap(self.nodes)

    @property
    def tupledictrows(self):
        return [
            self.nodes,
            self.adj,
            self.edgestore,
            self.graph,
            self.pred,
            self.revedgestore,
        ]

    @property
    def indices(self):
        yield from (
            e
            for e in self.schema.values()
            if isinstance(e, self.dialect.schema.SchemaIndex.func)
        )

    @property
    def tables(self):
        yield from (
            e
            for e in self.schema.values()
            if isinstance(e, self.dialect.schema.SchemaTable.func)
        )

    def is_directed(self):
        return True

    def is_readonly(self):
        ms = int(bool(self.readonly))
        ns = self.nodes.is_readonly()
        es = self.edgestore.is_readonly()
        gs = self.graph.is_readonly()
        return (((ms << 1) + ns << 1) + es << 1) + gs

    @classmethod
    def loads(cls, state):
        self = object.__new__(cls)
        self.__setstate__(state)
        return self

    def to_readonly(self):
        if self.is_readonly():
            return self
        cls = type(self)
        return cls(
            self.dialect,
            self.nodes,
            self.edgestore,
            self.graph,
            schema=self.schema,
            schema_trace=dict(self.schema_trace, readonly=True),
            readonly=True,
        )

    def to_directed(self):
        return self

    def to_undirected(self, reciprocal=False):
        if not self.is_directed():
            return self
        # TODO: what about edgestore.rekey? assert it is "identity"?
        edgestore = self.edgestore
        if reciprocal:
            # TODO: improve the following:
            q1 = edgestore.select_row_query(cols=(1, 0))
            reciprocond = edgestore[0].tuple_with(edgestore[1]).inset(q1)
            q2 = edgestore.select_row_query(condition=reciprocond).name_query("right")
            symedges = self.dialect.tupledict.ReadOnlyTupleDictSchema(
                q2, rekey=edgestore.rekey
            )
        else:
            con_idx = edgestore._columns[2].subquery_index
            if con_idx > edgestore._columns[1].subquery_index:
                join = edgestore.joins[con_idx]
                jcols = tuple(
                    e[0] for e in join.pairs if e[0] not in (edgestore[0], edgestore[1])
                )  # otherwise we duplictate them.
                jpairs = list(join.pairs)
                jcond = join.other_condition
            else:
                jpairs = None
                jcols = ()
                jcond = None
            qsucc = edgestore.select_row_query(
                cols=(edgestore[0], edgestore[1], *jcols)
            )
            qpred = edgestore.select_row_query(
                cols=(edgestore[1], edgestore[0], *jcols)
            )
            qsym = qsucc.union_query(qpred).name_query("symmetric_edges")
            if jpairs:
                jpairs = [
                    (
                        qsym.external_columns.get_external_column_from_origin(
                            e[0], context=qsym.internal_columns
                        ),
                        e[1],
                    )
                    for e in jpairs
                ]
            symedges = self.dialect.tupledict.ReadOnlyTupleDictSchema(
                qsym,
                *edgestore.subqueries[con_idx:],
                columns=(qsym[0], qsym[1], edgestore[2], edgestore[3]),
                joinpairs=(jpairs,)
                + tuple(list(j.pairs) for j in edgestore.joins[con_idx + 1 :]),
                joinconds=(jcond,)
                + tuple(j.other_condition for j in edgestore.joins[con_idx + 1 :]),
                rekey=edgestore.rekey,
            )
        return self.dialect.graph_schema.GraphSchema(
            self.nodes, symedges, self.graph, symmode=False, readonly=True
        )

    def reverse(self):
        edgestore = self.edgestore
        try:
            columns = map(edgestore.__getitem__, (1, 0, 2, 3))
            edgestore = self.dialect.tupledict.ReadOnlyTupleDictSchema(
                edgestore, columns=columns
            )
        except NetworkDiskSQLError:
            query = edgestore.select_row_query(cols=(1, 0, 2, 3))
            edgestore = self.dialect.tupledict.ReadOnlyTupleDictSchema(query)
        return self.dialect.graph_schema.DiGraphSchema(
            self.nodes, edgestore, self.graph, schema=self.schema, readonly=True
        )

    def __eq__(self, other):
        if not self.__class__ == other.__class__:
            return False
        return self.__getstate__() == other.__getstate__()

    def __hash__(self):
        return hash(tuple(self.__getstate__().items()) + (self.__class__,))

    def creation_script(self, ifnotexists=False):
        """
        Generate SQL creation scripts for the schema.
        Results is an iterator of SQL statements.
        """
        return self.schema.create_script(ifnotexists=ifnotexists)

    def refresh_nodes_query(self):
        """
        Generate a query that update nodes table from edge table.
        The query is useful when bulk inserting edges without
        trigger for performance tuning.
        """
        nodes = getattr(self.nodes, "_write_target", self.nodes) or self.nodes
        node_cont = nodes.subqueries[0]
        condition = self.dialect.conditions.EmptyCondition()
        if not self.refresh_not_unique_node:
            condition &= -self.edgestore[1].inset(self.nodes.select_row_query((0,)))
        qTRGT = self.edgestore.select_row_query(cols=(1,), condition=condition)
        condition = self.dialect.conditions.EmptyCondition()
        if not self.refresh_not_unique_node:
            condition &= -self.edgestore[0].inset(self.nodes.select_row_query((0,)))
        qSRC = self.edgestore.select_row_query(cols=(0,), condition=condition)
        qInsrt = qSRC.union_all_query(qTRGT)
        qN = node_cont.insert_query(qInsrt, columns=(nodes[0],))
        return qN


@dialect.register(True)
class GraphSchema(DiGraphSchema):
    """
    A `GraphSchema` is basically a collection of at least 4
    `tupleDictRows`:
    +	nodes: of depth 3, for storing nodes with associated data.
    +	edgestore: of depth 4, for storing edges with associated
            data. This is the preferred access for reading edges. The
            store is always assumed to be symmetric, meaning that for
            any edge `(u,v)` in the store, the reversed edge `(v, u)`
            is as well in the store. However, symmetric alteration of
            the store can be manage in several, considering the
            attributes `asymedges` and `symmetrized`.
    + graph: of depth 2, for storing graph data.
    +	`adj`: of depth 2, for storing node adjacency. The tupleDict
            coincides with the `nodes` tupleDict on its first coordinate
            and with `edgestore` on the further ones.

    Additionally, another `tupleDictRows` might be stored:
    +	asymedges: of depth 4, for storing asymmetric edges with
            associated data. This is the preferred access for editing
            edges. If unset, the attribute has value `None`.

    The object has two other attributes:
    +	symmetrized: a Boolean that indicates whether the access to
            edges allows to alter an edge by considering it only one way
            (if `True`), or whether both ways should be considered (if
            `False`). Standard alterations are insertions, deletions,
            and updates.
    +	schema: a `Schema` which gather the SQL structures (namely,
            tables, views, indices, and triggers) used by the various
            `TupleDictSchema`, for being created if requested. This schema
            is either passed at initialization, or computed using the
            structures of the `TupleDictSchema`.
    """

    def __init__(
        self,
        dialect,
        nodes,
        edges,
        graph,
        symmode=False,
        schema=None,
        readonly=None,
        refresh_not_unique_node=True,
        node_cascade_on_delete=True,
        schema_trace=(),
    ):
        """
        The constructor requires 3 TupleDictSchema arguments:
        +	nodes: of height 2, that store the nodes and their data;
        +	edges: of height 3, that store the edges and their data;
        +	graph: of height 1, that store the graph data.

        Unlike `nx.Graph._adj` recursive dictionary, the tupleDict
        `edges` is not supposed to admit every node from `nodes` as
        first coordinate (aka column).

        Here, the tupleDict `edges` is assumed to contain symmetric
        edges, namely, for each tupleDict row `(s, t, k, v)` in
        `edges` there is `(t, s, k, v)` in `edges` as well. However
        modification of the edges (insertion, deletion, update), may
        be handled differently. The way it is handled is the purpose
        of the keyworded argument `symmode` (see below). By default,
        these alteration should be repeated on both the edge and its
        reverse.


        Optional arguments are the following:
        +	symmode:
                either a Boolean, indicating whether the edges represented
                by `edges` are symmetrized on back-side when altered or
                not, or a further `TupleDictSchema`, which is an asymmetric
                representation of the edges. This additional access is
                preferred when altering (inserting, deleting, updating)
                edges. When possible, it is recommended for optimization
                purpose, to provide both accesses. The default value of
                `symmode` is `False`.
        + schema:
                an `ndsql.Schema` that gathers the SQL structures (tables,
                views, indices, triggers) used by the `TupleDictSchema`, for
                creation. If not given, a `ndsql.Schema` is automatically
                created by inspecting the `TupleDictSchema`.


        Typically, the `edges` `TupleDictSchema` refers to an SQL VIEW
        on symmetrized edges stored in a table pointed by the
        `TupleDictSchema` given as `symmode`. This table stores the
        edges in one way (for instance, in increasing order, see the
        `rekey` parameter of `TupleDictSchema`), but they can be
        accessed both ways using the `edges` view.
        """
        if readonly:
            nodes, edges, graph = (
                nodes.to_readonly(),
                edges.to_readonly(),
                graph.to_readonly(),
            )
            if hasattr(symmode, "to_readonly"):
                symmode = symmode.to_readonly()
        d = dict(
            dialect=dialect.name,
            nodes=nodes,
            edgestore=edges,
            graph=graph,
            symmode=symmode,
            readonly=readonly,
            refresh_not_unique_node=refresh_not_unique_node,
            node_cascade_on_delete=node_cascade_on_delete,
            schema_trace=dict(schema_trace),
        )
        self.__setstate__(d)
        self.set_schema(schema)

    def __getstate__(self):
        state = super().__getstate__()
        state["symmode"] = self.asymedges or self.symmetrized
        return state

    def __setstate__(self, state):
        symmode = state.pop("symmode")
        for k, v in state.items():
            if k == "dialect":
                v = dialect._dialects[v]
            setattr(self, k, v)
        self.adj = self.edgestore.left_overlap(self.nodes)
        self.symmetrized = bool(symmode)
        if isinstance(symmode, self.dialect.tupledict.ReadOnlyTupleDictSchema.func):
            self.asymedges = symmode
        else:
            self.asymedges = None

    @property
    def tupledictrows(self):
        tupledictrows = [self.nodes, self.adj, self.edgestore, self.graph]
        if self.asymedges:
            tupledictrows.append(self.asymedges)
        return tupledictrows

    def is_directed(self):
        return False

    def refresh_nodes_script(self):
        """
        Generate a query that update nodes table from edge table.
        The query is useful when bulk inserting edges without
        trigger for performance tuning.
        """
        nodes = self.nodes
        node_cont = nodes.subqueries[0]
        qSRC = self.edgestore.select_row_query(cols=(0,), distinct=True)
        qN = node_cont.insert_query(qSRC, columns=(nodes[0],))
        # qTRGT = self.edgestore.select_row_query(cols=(1,), distinct=True)
        # qN = node_cont.insert_query(qSRC.union_query(qTRGT), columns=(nodes[0],))
        ##no need to make UNION as edgestore is assumed symmetric
        return qN

    def to_directed(self):
        return self.dialect.graph_schema.DiGraphSchema(
            self.nodes,
            self.edgestore,
            self.graph,
            schema=self.schema,
            readonly=self.readonly,
        )

    def to_undirected(self):
        return self


@dialect.register(True)
def setup_graph_columns(
    dialect,
    node=None,
    datakey=None,
    datavalue=None,
    node_datakey=None,
    node_datavalue=None,
    edge_datakey=None,
    edge_datavalue=None,
    graph_datakey=None,
    graph_datavalue=None,
):
    """Tool function to setup default type and encoding of graph columns.

    Parameters
    ----------
    dialect : Dialect
            The SQL dialect to use.  It is expected to offer, in its `schemata`
            subdialect, the default values keyed by `'_default_node_type'`,
            `_default_datakey_type`, and `'_default_datavalue_type'`.

    node : None or str or pair
            The specification for the type and the encoder of the node name column.
            If `None`, the default value comes from the dialect.

    datakey : None or str or pair
            The specification for the default type and the default encoder of the
            datakey columns.  If `None`, the default value comes from `dialect`.

    datavalue : None or str or pair
            The specification for the default type and the default encoder of the
            datavalue columns.  If `None`, the default value comes from `dialect`.

    node_datakey : None or str or pair
            The specification for the type and the encoder of the node datakey
            column.  If `None`, a default value is taken.

    node_datavalue : None or str or pair
            The specification for the type and the encoder of the node datavalue
            column.  If `None`, a default value is taken.

    edge_datakey : None or str or pair
            The specification for the type and the encoder of the edge datakey
            column.  If `None`, a default value is taken.

    edge_datavalue : None or str or pair
            The specification for the type and the encoder of the edge datavalue
            column.  If `None`, a default value is taken.

    graph_datakey : None or str or pair
            The specification for the type and the encoder of the graph datakey
            column.  If `None`, a default value is taken.

    graph_datavalue : None or str or pair
            The specification for the type and the encoder of the graph datavalue
            column.  If `None`, a default value is taken.

    Notes
    -----
    The goal of the function is to associate each column with a type/encoder
    specification.  Such a specification is a pair, whose first coordinate is
    a string (the SQL type, e.g., "TEXT", "INT", "JSON") and the second one
    is either a string (the encoder key, e.g., "TEXT", "INT", "JSON") or the
    special value `None`.  In the latter case, the default encoder will be
    handled by the column constructor.

    The value for node, edge, or graph datakey (resp. datavalue) columns are
    obtained as follows.  If the value (other than `None`) is provided as
    parameter, then it is used.  Otherwise, namely when the corresponding
    parameter has value `None`, the default value is the value of `datakey`
    (resp `datavalue`) if provided, or it is obtained from the subdialect
    `dialect.graph_schema` if proposed, or it is taken from the default value
    of the `datakey` (resp. `datavalue`) parameter (itself obtained from
    the subdialect).

    Returns
    -------
    dict
            A formatted canonical mapping for column setting, with keys `'node'`,
            `'datakey'`, `'datavalue'`, `'node_datakey'`, `'node_datavalue'`,
            `'edge_datakey'`, `'edge_datavalue'`, `'graph_datakey'`, and
            `'graph_datavalue'` and associated pairs of column type and encoder.
            An unspecified encoder is represented by `None`, to be handled by the
            column constructor (typically, the provided type will be used as
            encoder).
    """
    subdial = dialect.graph_schema
    column_setup = dict(
        node=node,
        datakey=datakey,
        datavalue=datavalue,
        node_datakey=node_datakey,
        node_datavalue=node_datavalue,
        edge_datakey=edge_datakey,
        edge_datavalue=edge_datavalue,
        graph_datakey=graph_datakey,
        graph_datavalue=graph_datavalue,
    )
    default_datakey = (
        subdial._default_datakey_type,
        subdial.get("_default_datakey_encoder", None),
    )
    default_datavalue = (
        subdial._default_datavalue_type,
        subdial.get("_default_datavalue_encoder", None),
    )
    for n, t in column_setup.items():
        if n.endswith("_datakey") and datakey and t is None:
            t = datakey
        elif n.endswith("_datavalue") and datavalue and t is None:
            t = datavalue
        if isinstance(t, str):
            column_setup[n] = t, None
        elif not t:
            ktype = f"_default_{n}_type"
            kencd = f"_default_{n}_encoder"
            if n.endswith("datakey"):
                column_setup[n] = (
                    subdial.get(ktype, default_datakey[0]),
                    subdial.get(kencd, default_datakey[1]),
                )
            elif n.endswith("datavalue"):
                column_setup[n] = (
                    subdial.get(ktype, default_datavalue[0]),
                    subdial.get(kencd, default_datavalue[1]),
                )
            else:
                column_setup[n] = subdial[ktype], subdial.get(kencd, None)
        else:
            column_setup[n] = t
    return column_setup
