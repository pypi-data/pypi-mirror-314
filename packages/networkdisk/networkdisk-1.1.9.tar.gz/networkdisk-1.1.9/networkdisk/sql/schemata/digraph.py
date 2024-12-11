from networkdisk.sql.dialect import sqldialect as dialect

dialect = dialect.provide_submodule("schemata")


## Defining default undirected graph schema
@dialect.register(True)
def digraph(dialect, table_suffix="", readonly=False, index=True, **columns):
    """Generates a DiGraphSchema.

    Returns a valid, sqlite-optimized DiGraphSchema that uses five tables,
    as described in Notes, below.

    Parameters
    ----------
    dialect : Dialect
            The SQL dialect to use.

    columns : dictable, default=()
            Mapping to be passed to `dialect.graph_schema.setup_graph_columns`
            function as keyworded parameters.  Accepted keys are `'node'`,
            `'datakey'`, `'datavalue'`, and the two former ones prefixed by one of
            `'node_'`, `'edge_'`, or `'graph_'`.  Accepted values are `None` (same
            as missing key), string (the SQL type to use, e.g., `'INT'`, `'TEXT'`,
            `'JSON'`), or type/encoder pairs.

    table_suffix : string, default=""
            A suffix to append to each TABLE and VIEW name.

    readonly : bool, default=False
            Whether the generated schema is read only.

    index : bool, default=True
            Whether to add useful INDEX to the schema.

    Notes
    -----

    Schema TABLES and VIEWS:
    ^^^^^^^^^^^^^^^^^^^^^^^^
    +	TABLE nodes
            stores the vertex ids in its single column 'name' of type
            `node_type`, which is a PRIMARY KEY.
    +	TABLE node_data
            stores in two columns 'key' and 'value' the data of each
            vertex. The table has a third column 'name' which references
            the column 'name' of TABLE 'nodes'. The pair ('name', 'key')
            has the UNIQUE constraint. The 'key' column is indexed.
    +	TABLE edges
            stores the edges in two columns, named 'source' and 'target'
            respectively, which are both references to the column 'name'
            of the TABLE 'nodes'. Each pair ('source', 'target') is
            UNIQUE. There is a third column 'id' that stores an
            AUTOINCREMENTed integer id for the edge. There is a reversed
            index on pairs ('target', 'source').
    +	TABLE edge_data
            stores the edge data in two columns 'key' and 'value'. The
            third column 'id' references the column 'id' of TABLE
            'nodes'. The pair ('id', 'key') is UNIQUE. The 'key' column
            is indexed.
    +	TABLE graph_info
            stores the graph data in two columns 'key' and 'value'. The
            column 'key' is a PRIMARY KEY for the table, and the column
            'value' does not accept the NULL value.
    """
    columns = dialect.graph_schema.setup_graph_columns(**columns)
    table_suffix = str(table_suffix)
    trace = dict(
        method="digraph",
        columns=columns,
        table_suffix=table_suffix,
        readonly=readonly,
        index=index,
    )

    schema = dialect.schema.Schema("digraphs")
    # NODES
    nodesT = schema.add_table("nodes" + table_suffix)
    sqltype, encoder = columns["node"]
    nnamC = nodesT.add_column(
        "name", sqltype=sqltype, encoder=encoder, primarykey="IGNORE", notnull="IGNORE"
    )
    consfk = dialect.constraints.ForeignkeyConstraint(
        nnamC,
        container=nnamC.container_name,
        on_delete="CASCADE",
        on_update="CASCADE",
        deferrable=True,
        initially_deferred=True,
    )
    # NODE DATA
    nodeDataT = schema.add_table("node_data" + table_suffix)
    nfidC = nodeDataT.add_column(
        "name", references=nnamC, constraints=(consfk,), notnull="IGNORE"
    )
    sqltype, encoder = columns["node_datakey"]
    nkeyC = nodeDataT.add_column(
        "key", sqltype=sqltype, encoder=encoder, notnull="IGNORE"
    )
    sqltype, encoder = columns["node_datavalue"]
    nvalC = nodeDataT.add_column(
        "value", sqltype=sqltype, encoder=encoder, notnull=True
    )
    nodeDataT.add_constraint(
        dialect.constraints.TableUniqueConstraint(nfidC, nkeyC, on_conflict="REPLACE")
    )
    if index:
        schema.add_index(nodeDataT, columns=(nkeyC, nvalC))
    # EDGES
    edgesT = schema.add_table("edges" + table_suffix)
    eidC = edgesT.add_column(
        "id", sqltype="INTEGER", primarykey=True, autoincrement=True, notnull=True
    )
    esrcC = edgesT.add_column(
        "source", sqltype=nnamC, references=nnamC, constraints=(consfk,), notnull=True
    )
    etrgtC = edgesT.add_column(
        "target",
        sqltype=nnamC,
        references=nnamC,
        constraints=(consfk,),
        notnull="IGNORE",
    )
    edgesT.add_constraint(
        dialect.constraints.TableUniqueConstraint(esrcC, etrgtC, on_conflict="IGNORE")
    )
    if index:
        schema.add_index(edgesT, columns=(etrgtC, esrcC))
    # EDGE DATA
    edgeDataT = schema.add_table("edge_data" + table_suffix)
    efidC = edgeDataT.add_column(
        "id", references=eidC, on_delete="CASCADE", on_update="CASCADE", notnull=True
    )
    sqltype, encoder = columns["edge_datakey"]
    ekeyC = edgeDataT.add_column("key", sqltype=sqltype, encoder=encoder, notnull=True)
    sqltype, encoder = columns["edge_datavalue"]
    evalC = edgeDataT.add_column(
        "value", sqltype=sqltype, encoder=encoder, notnull=True
    )
    edgeDataT.add_constraint(
        dialect.constraints.TableUniqueConstraint(efidC, ekeyC, on_conflict="REPLACE")
    )
    if index:
        schema.add_index(edgeDataT, columns=(ekeyC, evalC))
    # GRAPH DATA
    graphT = schema.add_table("graph_info" + table_suffix)
    sqltype, encoder = columns["graph_datakey"]
    gkeyC = graphT.add_column(
        "key", sqltype=sqltype, encoder=encoder, primarykey="REPLACE", notnull=True
    )
    sqltype, encoder = columns["graph_datavalue"]
    gvalC = graphT.add_column("value", sqltype=sqltype, encoder=encoder, notnull=True)
    if index:
        schema.add_index(graphT, columns=(gkeyC, gvalC))
    # TUPLEDICTSCHEMA
    if readonly:
        TupleDictSchema = dialect.tupledict.ReadOnlyTupleDictSchema
    else:
        TupleDictSchema = dialect.tupledict.ReadWriteTupleDictSchema
    nodesTDS = TupleDictSchema(
        nodesT, nodeDataT, columns=(nnamC, nkeyC, nvalC), joinpairs=[(nnamC, nfidC)]
    )
    edgesTDS = TupleDictSchema(
        edgesT,
        edgeDataT,
        columns=[esrcC, etrgtC, ekeyC, evalC],
        joinpairs=[(eidC, efidC)],
    )
    graphTDS = TupleDictSchema(graphT, columns=[gkeyC, gvalC])
    # GRAPHSCHEMA
    gS = dialect.graph_schema.DiGraphSchema(
        nodesTDS, edgesTDS, graphTDS, schema=schema, schema_trace=trace
    )
    return gS


@dialect.register(True)
def digraph_one_table(dialect, table_suffix="", readonly=False, index=True, **columns):
    """Generates a DiGraphSchema.

    Returns a valid, sqlite-optimized DiGraphSchema that uses only one table.

    Parameters
    ----------
    dialect : Dialect
            The SQL dialect to use.

    columns : dictable, default=()
            Mapping to be passed to `dialect.graph_schema.setup_graph_columns`
            function as keyworded parameters.  Accepted keys are `'node'`,
            `'datakey'`, `'datavalue'`, and the two former ones prefixed by one of
            `'node_'`, `'edge_'`, or `'graph_'`.  Accepted values are `None` (same
            as missing key), string (the SQL type to use, e.g., `'INT'`, `'TEXT'`,
            `'JSON'`), or type/encoder pairs.

    table_suffix : string, default=""
            A suffix to append to each TABLE and VIEW name.

    readonly : bool, default=False
            Whether the generated schema is read only.

    index : bool, default=True
            Whether to add useful INDEX to the schema.
    """
    columns = dialect.graph_schema.setup_graph_columns(**columns)
    table_suffix = str(table_suffix)
    trace = dict(
        method="digraph",
        columns=columns,
        table_suffix=table_suffix,
        readonly=readonly,
        index=index,
    )

    schema = dialect.schema.Schema("digraphs")
    # NODES
    nodesT = schema.add_table("nodes" + table_suffix)
    sqltype, encoder = columns["node"]
    nnamC = nodesT.add_column(
        "name", sqltype=sqltype, encoder=encoder, primarykey="IGNORE", notnull="IGNORE"
    )
    consfk = dialect.constraints.ForeignkeyConstraint(
        nnamC,
        container=nnamC.container_name,
        on_delete="CASCADE",
        on_update="CASCADE",
        deferrable=True,
        initially_deferred=True,
    )
    # NODE DATA
    nodeDataT = schema.add_table("node_data" + table_suffix)
    nfidC = nodeDataT.add_column(
        "name", references=nnamC, constraints=(consfk,), notnull="IGNORE"
    )
    sqltype, encoder = columns["node_datakey"]
    nkeyC = nodeDataT.add_column(
        "key", sqltype=sqltype, encoder=encoder, notnull="IGNORE"
    )
    sqltype, encoder = columns["node_datavalue"]
    nvalC = nodeDataT.add_column(
        "value", sqltype=sqltype, encoder=encoder, notnull=True
    )
    nodeDataT.add_constraint(
        dialect.constraints.TableUniqueConstraint(nfidC, nkeyC, on_conflict="REPLACE")
    )
    if index:
        schema.add_index(nodeDataT, columns=(nkeyC, nvalC))
    # EDGES
    edgesT = schema.add_table("edges" + table_suffix)
    eidC = edgesT.add_column(
        "id", sqltype="INTEGER", primarykey=True, autoincrement=True, notnull=True
    )
    esrcC = edgesT.add_column(
        "source", sqltype=nnamC, references=nnamC, constraints=(consfk,), notnull=True
    )
    etrgtC = edgesT.add_column(
        "target",
        sqltype=nnamC,
        references=nnamC,
        constraints=(consfk,),
        notnull="IGNORE",
    )
    edgesT.add_constraint(
        dialect.constraints.TableUniqueConstraint(esrcC, etrgtC, on_conflict="IGNORE")
    )
    if index:
        schema.add_index(edgesT, columns=(etrgtC, esrcC))
    # EDGE DATA
    edgeDataT = schema.add_table("edge_data" + table_suffix)
    efidC = edgeDataT.add_column(
        "id", references=eidC, on_delete="CASCADE", on_update="CASCADE", notnull=True
    )
    sqltype, encoder = columns["edge_datakey"]
    ekeyC = edgeDataT.add_column("key", sqltype=sqltype, encoder=encoder, notnull=True)
    sqltype, encoder = columns["edge_datavalue"]
    evalC = edgeDataT.add_column(
        "value", sqltype=sqltype, encoder=encoder, notnull=True
    )
    edgeDataT.add_constraint(
        dialect.constraints.TableUniqueConstraint(efidC, ekeyC, on_conflict="REPLACE")
    )
    if index:
        schema.add_index(edgeDataT, columns=(ekeyC, evalC))
    # GRAPH DATA
    graphT = schema.add_table("graph_info" + table_suffix)
    sqltype, encoder = columns["graph_datakey"]
    gkeyC = graphT.add_column(
        "key", sqltype=sqltype, encoder=encoder, primarykey="REPLACE", notnull=True
    )
    sqltype, encoder = columns["graph_datavalue"]
    gvalC = graphT.add_column("value", sqltype=sqltype, encoder=encoder, notnull=True)
    if index:
        schema.add_index(graphT, columns=(gkeyC, gvalC))
    # TUPLEDICTSCHEMA
    if readonly:
        TupleDictSchema = dialect.tupledict.ReadOnlyTupleDictSchema
    else:
        TupleDictSchema = dialect.tupledict.ReadWriteTupleDictSchema
    nodesTDS = TupleDictSchema(
        nodesT, nodeDataT, columns=(nnamC, nkeyC, nvalC), joinpairs=[(nnamC, nfidC)]
    )
    edgesTDS = TupleDictSchema(
        edgesT,
        edgeDataT,
        columns=[esrcC, etrgtC, ekeyC, evalC],
        joinpairs=[(eidC, efidC)],
    )
    graphTDS = TupleDictSchema(graphT, columns=[gkeyC, gvalC])
    # GRAPHSCHEMA
    gS = dialect.graph_schema.DiGraphSchema(
        nodesTDS, edgesTDS, graphTDS, schema=schema, schema_trace=trace
    )
    return gS


@dialect.register(True)
def digraph_splitted(dialect, table_suffix="", readonly=False, index=True, **columns):
    """Generates a DiGraphSchema.

    Returns a valid, sqlite-optimized DiGraphSchema that uses nine tables.

    Parameters
    ----------
    dialect : Dialect
            The SQL dialect to use.

    columns : dictable, default=()
            Mapping to be passed to `dialect.graph_schema.setup_graph_columns`
            function as keyworded parameters.  Accepted keys are `'node'`,
            `'datakey'`, `'datavalue'`, and the two former ones prefixed by one of
            `'node_'`, `'edge_'`, or `'graph_'`.  Accepted values are `None` (same
            as missing key), string (the SQL type to use, e.g., `'INT'`, `'TEXT'`,
            `'JSON'`), or type/encoder pairs.

    table_suffix : string, default=""
            A suffix to append to each TABLE and VIEW name.

    readonly : bool, default=False
            Whether the generated schema is read only.

    index : bool, default=True
            Whether to add useful INDEX to the schema.
    """
    columns = dialect.graph_schema.setup_graph_columns(**columns)
    table_suffix = str(table_suffix)
    trace = dict(
        method="digraph_splitted",
        columns=columns,
        table_suffix=table_suffix,
        readonly=readonly,
        index=index,
    )

    schema = dialect.schema.Schema("digraphs")

    def tdref(col, cont=None):
        return dialect.constraints.ForeignkeyConstraint(
            col,
            container=cont,
            on_delete="CASCADE",
            on_update="CASCADE",
            deferrable=True,
            initially_deferred=True,
        )

    # NODES
    nNT = schema.add_table("node_names" + table_suffix)
    sqltype, encoder = columns["node"]
    nNC = nNT.add_column(
        "name", sqltype=sqltype, encoder=encoder, primarykey="IGNORE", notnull="IGNORE"
    )
    refNname = tdref(nNC, nNT)
    # NODE KEYS
    nKT = schema.add_table("node_keys" + table_suffix)
    nKidC = nKT.add_column(
        "id", sqltype="INTEGER", primarykey=True, autoincrement=True, notnull=True
    )
    nKfidC = nKT.add_column(
        "node", references=nNC, notnull="IGNORE", constraints=(refNname,)
    )
    sqltype, encoder = columns["node_datakey"]
    nKC = nKT.add_column("key", sqltype=sqltype, encoder=encoder, notnull="IGNORE")
    nKT.add_constraint(
        dialect.constraints.TableUniqueConstraint(nKfidC, nKC, on_conflict="REPLACE")
    )
    if index:
        schema.add_index(nKT, columns=(nKfidC, nKC))
    refNkey = tdref(nKidC, nKT)
    # NODE VALUES
    nVT = schema.add_table("node_values" + table_suffix)
    nVfidC = nVT.add_column(
        "id", references=nKidC, notnull="IGNORE", constraints=(refNkey,)
    )
    sqltype, encoder = columns["node_datavalue"]
    nVC = nVT.add_column("value", sqltype=sqltype, encoder=encoder, notnull=True)
    nVT.add_constraint(
        dialect.constraints.TableUniqueConstraint(nVfidC, nVC, on_conflict="REPLACE")
    )
    if index:
        schema.add_index(nVT, columns=(nVfidC, nVC))

    # EDGE SOURCES
    eST = schema.add_table("edge_sources" + table_suffix)
    eSC = eST.add_column(
        "source",
        references=nNC,
        primarykey="IGNORE",
        notnull="IGNORE",
        constraints=(refNname,),
    )
    refEsource = tdref(eSC, eST)
    # EDGE TARGETS
    eTT = schema.add_table("edge_targets" + table_suffix)
    eTidC = eTT.add_column(
        "id", sqltype="INTEGER", primarykey=True, autoincrement=True, notnull=True
    )
    eTfidC = eTT.add_column(
        "source", references=eSC, notnull="IGNORE", constraints=(refEsource,)
    )
    eTC = eTT.add_column(
        "target", references=nNC, constraints=(refNname,), notnull="IGNORE"
    )
    eTT.add_constraint(
        dialect.constraints.TableUniqueConstraint(eTfidC, eTC, on_conflict="IGNORE")
    )
    if index:
        schema.add_index(eTT, columns=(eTC, eTfidC))
    refEedge = tdref(eTidC, eTT)
    # EDGE KEYS
    eKT = schema.add_table("edge_keys" + table_suffix)
    eKidC = eKT.add_column(
        "id", sqltype="INTEGER", primarykey=True, autoincrement=True, notnull=True
    )
    eKfidC = eKT.add_column(
        "edge", references=eTidC, notnull="IGNORE", constraints=(refEedge,)
    )
    sqltype, encoder = columns["edge_datakey"]
    eKC = eKT.add_column("key", sqltype=sqltype, encoder=encoder, notnull=True)
    eKT.add_constraint(
        dialect.constraints.TableUniqueConstraint(eKfidC, eKC, on_conflict="REPLACE")
    )
    refEkey = tdref(eKidC, eKT)
    # EDGE VALUES
    eVT = schema.add_table("edge_values" + table_suffix)
    eVfidC = eVT.add_column(
        "fid", references=eKidC, notnull=True, constraints=(refEkey,)
    )
    sqltype, encoder = columns["edge_datavalue"]
    eVC = eVT.add_column("value", sqltype=sqltype, encoder=encoder, notnull=True)
    eVT.add_constraint(
        dialect.constraints.TableUniqueConstraint(eVfidC, eVC, on_conflict="REPLACE")
    )
    if index:
        schema.add_index(eVT, columns=(eVfidC, eVC))

    # GRAPH KEYS
    gKT = schema.add_table("graph_keys" + table_suffix)
    sqltype, encoder = columns["graph_datakey"]
    gKC = gKT.add_column(
        "key", sqltype=sqltype, encoder=encoder, primarykey="REPLACE", notnull=True
    )
    refGkey = tdref(gKC, gKT)
    # GRAPH VALUES
    gVT = schema.add_table("graph_values" + table_suffix)
    gVfidC = gVT.add_column(
        "key", references=gKC, notnull=True, primarykey=True, constraints=(refGkey,)
    )
    sqltype, encoder = columns["graph_datavalue"]
    gVC = gVT.add_column("value", sqltype=sqltype, encoder=encoder, notnull=True)
    if index:
        schema.add_index(gVT, columns=(gVfidC, gVC))
    # TUPLEDICTSCHEMA
    if readonly:
        TupleDictSchema = dialect.tupledict.ReadOnlyTupleDictSchema
    else:
        TupleDictSchema = dialect.tupledict.ReadWriteTupleDictSchema

    nodesTDS = TupleDictSchema(
        nNT,
        nKT,
        nVT,
        columns=(nNC, nKC, nVC),
        joinpairs=[(nNC, nKfidC), (nKidC, nVfidC)],
    )
    edgesTDS = TupleDictSchema(
        eST,
        eTT,
        eKT,
        eVT,
        columns=(eSC, eTC, eKC, eVC),
        joinpairs=[(eSC, eTfidC), (eTidC, eKfidC), (eKidC, eVfidC)],
    )
    edgesTDS = edgesTDS.filter_from_column(eSC, eTC.isnotnull(), write_target=edgesTDS)
    graphTDS = TupleDictSchema(gKT, gVT, columns=(gKC, gVC), joinpairs=[(gKC, gVfidC)])
    gS = dialect.graph_schema.DiGraphSchema(
        nodesTDS, edgesTDS, graphTDS, schema=schema, schema_trace=trace
    )
    return gS


methods = dict(
    digraph=dialect.digraph,
    digraph_one_table=dialect.digraph_one_table,
    digraph_splitted=dialect.digraph_splitted,
)


@dialect.register(True)
def load_digraph(dialect, **state):
    method = state.pop("method", "digraph")
    methods = dialect.schemata
    if method in methods:
        method = methods[method]
        columns = state.pop("columns", {})
        return method(**state, **columns)
    elif method is not None:
        raise ValueError(f"Unknown digraph schema generator method {method}")
    raise ValueError(f"Unknown digraph schema dump {state}")
