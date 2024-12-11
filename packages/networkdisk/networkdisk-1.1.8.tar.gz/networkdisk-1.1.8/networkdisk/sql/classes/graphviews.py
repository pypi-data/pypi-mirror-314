import networkx as nx
import functools


@functools.wraps(nx.classes.graphviews.generic_graph_view)
def generic_graph_view(G, create_using=None):
    # TODO: minimal implementation using networkx implementation
    # used for to_directed/to_undirected…
    H = nx.classes.graphviews.generic_graph_view(G, create_using=create_using)
    return H


@functools.wraps(nx.classes.graphviews.subgraph_view)
def subgraph_view(
    G,
    filter_node=None,
    filter_edge=None,
    restrict_edge_endpoints=True,
    temporary_table=False,
):
    """Create a view on graph by filtering nodes and/or edges.

    PARAMETERS
    ----------
    G: Graph
            the graph or graph view to filter.

    filter_node: condition or None, default=None
            a condition applicable on `G._node`, to filter nodes.  The condition
            will filter the first column (name) of the `_node` and `_adj`
            tupledicts of the created Graph view, as well as the first two columns
            (source and target) of the `edgestore` and, possibly, `asymedges`
            tupledicts unless the parameter `restrict_edge_endpoints` is `False`
            and the parameter `temporary_table` is `True`.

    filter_edge: condition or None, default=None
            a condition on `G.edgestore` tupledict, to filter edges.

    restrict_edge_endpoints: bool, default=True
            Whether to enforce edge endpoints (source and target) to match the
            given `node_filter` or not.  If set to `False`, the generated view
            might be an invalid graph (e.g., some listed edges might have source
            and/or target not belonging to the graph view nodes).  Thus, this
            parameter should be used with care, when the given `edge_filter`
            already restrict the edge endpoints to match the given `filter_node`.
            If `temporary_table` is `True`, the parameter is ignored, as the
            `filter_node` filtering is not any longer dynamic contrary to the
            `filter_edge` filtering which always is.

    temporary_table: bool, default=False
            If `True`, the function creates a temporary table, which contains all
            the nodes of `G` that match the given `filter_node` **at the time of
            the view creation**.  This parameter should be used with care, as it
            makes part of the view static.  Indeed, after alteration, a node
            belonging to `G` will be seen in the view, if and only if it matches
            `filter_node` and it was already a node of `G` at the time the view
            has been created.

    """
    restrict_edge_endpoints = temporary_table or restrict_edge_endpoints
    if restrict_edge_endpoints:
        filter_edge_endpoints = filter_node
    else:
        filter_edge_endpoints = None

    H = G
    if hasattr(G, "_NODE_FILTER"):
        filter_node = G._NODE_FILTER & filter_node
        filter_edge = G._EDGE_FILTER & filter_edge
        H = G._graph

    # filtering nodes
    nodes = H.schema.nodes
    if filter_node:
        node_domain_query = H.schema.nodes.select_row_query(
            condition=filter_node, cols=(0,)
        )
        if temporary_table:
            wq = G.schema.schema.add_table(
                G.helper.generate_temporary_table_name(suffix="node_domain"),
                node_domain_query,
                temporary=True,
            )
            G.helper.execute(wq.create_query())
            G.helper.execute(wq.create_index_query((0,)))
        else:
            wq = node_domain_query.with_query("node_domain")
        filter_node2 = H.schema.nodes[0].inset(wq)
        nodes = H.schema.nodes.filter_from_column(0, filter_node2)

    # filtering edges
    filter_edge = filter_edge or H.dialect.conditions.EmptyCondition()
    edges = H.schema.edgestore
    if filter_edge:
        edges = edges.filter_from_column(0, filter_edge)
    if filter_edge_endpoints:
        source_filter = H.schema.edgestore[0].inset(wq)
        target_filter = H.schema.edgestore[1].inset(wq)
        edges = edges.filter_from_column(0, source_filter)
        edges = edges.filter_from_column(0, target_filter)

    # readonlize graph
    graph = H.schema.graph.to_readonly()

    # filtering asymmetric edges, if needed
    asymedges = getattr(H, "asymedges", None)
    if not filter_edge and asymedges is not None:
        asymedges = H.schema.asymedges
        if filter_edge:
            asymedges = asymedges.filter_from_column(1, filter_edge)
        if filter_edge_endpoints:
            source_filter = asymedges[0].inset(wq)
            target_filter = asymedges[1].inset(wq)
            asymedges = asymedges.filter_from_column(0, source_filter)
            asymedges = asymedges.filter_from_column(0, target_filter)
        gs = type(H.schema)(
            H.dialect,
            nodes,
            edges,
            graph,
            symmode=asymedges,
            schema=H.schema.schema,
            readonly=True,
        )
    else:
        gs = type(H.schema)(
            H.dialect, nodes, edges, graph, schema=H.schema.schema, readonly=True
        )

    J = type(G)(db=H.helper, schema=gs, create=False, insert_schema=False, lazy=H.lazy)
    J._graph = H
    J._NODE_FILTER = filter_node
    J._EDGE_FILTER = filter_edge

    return J


@functools.wraps(nx.classes.graphviews.reverse_view)
@nx.utils.not_implemented_for("undirected")
def reverse_view(G):
    schema = G.schema.reverse()
    H = type(G)(
        db=G.helper, schema=schema, create=False, insert_schema=False, lazy=G.lazy
    )
    H._graph = G
    return H
