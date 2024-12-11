import functools
import networkx.classes.reportviews as nxrv
import networkdisk.tupledict as ndtd
import networkdisk.exception as ndexc

NetworkDiskError = ndexc.NetworkDiskError


class View:
    repr_limit = 3


# === NODES === #


class NodeView(View, nxrv.NodeView):
    def __repr__(self):
        res = self._nodes.rowstore.select(
            stop=1, notnull=True, limit=self.repr_limit + 1
        )
        res = list(map(lambda t: t[0], res))
        if len(res) <= self.repr_limit:
            suff = "," if len(res) == 1 else ""
        else:
            res = res[:-1]
            suff = ", …"
        return f"{self.__class__.__name__}(({', '.join(map(repr, res))}{suff}))"

    def __call__(self, data=False, default=None):
        if data is False and default is None:
            return self
        return NodeDataView(self._nodes, data, default)

    def data(self, data=True, default=None):
        if data is False:
            return self
        return NodeDataView(self._nodes, data, default)

    @property
    def dialect(self):
        return self._graph.dialect


class NodeDataView(View, nxrv.NodeDataView):
    def __repr__(self):
        res = self._nodes.rowstore.select(
            stop=1, notnull=True, limit=self.repr_limit + 1
        )
        res = list(map(lambda t: t[0], res))
        if len(res) < self.repr_limit:
            suff = ""
        else:
            res = res[:-1]
            suff = ", …"
        if self._data is False:
            opening = "("
            closing = ")"
            res = map(repr, res)
        elif self._data is True:
            res = map(lambda u: f"{repr(u)}: {repr(self._nodes[u].fold())}", res)
            opening = "{"
            closing = "}"
        else:
            res = map(
                lambda u: f"{repr(u)}: {repr(self._nodes[u].get(self._data, self._default))}",
                res,
            )
            opening = "{"
            closing = f"}}, data={self._data}"
        return f"{self.__class__.__name__}({opening}{', '.join(map(str, res))}{suff}{closing})"

    @property
    def dialect(self):
        return self._nodes.rowstore.tupleDictSchema.dialect

    def iterable_query(self):
        rs = self._nodes.rowstore
        if self._data is False:
            res = rs.select(stop=1, distinct=True, notnull=True)
        elif self._data is True:
            res = rs.partial_fold(1, maxfolddepth=1, distinct=True)
            res = res.map(lambda t: t[0] + (t[1],))
        else:
            td = rs.tupleDictSchema
            td = td.left_projection_tupledict(1, self._data)
            ifnullC = self.dialect.columns.IfNullColumn(
                rs.tupleDictSchema[2], self._default
            )
            q = td.select_row_query(cols=(0, ifnullC), distinct=True, notnull=False)
            res = self.dialect.helper.IterableQuery(rs.helper, q)
        return res

    def __iter__(self):
        return iter(self.iterable_query())


# === EDGES === #


class OutEdgeDataView(View, nxrv.OutEdgeDataView):
    def __init__(self, viewer, nbunch=None, data=False, default=None):
        # The nbunch management is changed with respect those of the `nxrv.OutEdgeDataView` constructor.
        super().__init__(viewer, nbunch=None, data=data, default=default)
        self._target = target = viewer._target
        base_condition = viewer._base_condition
        rs = target.rowstore
        if nbunch is not None:
            nbunch = viewer._graph.nbunch_iter(nbunch)
            node_domain = nbunch.query.with_query("node_domain")
            base_condition &= rs.tupleDictSchema[0].inset(node_domain)
        if not base_condition:
            self._nodes_nbrs = target.items
        else:
            self._nodes_nbrs = lambda: (
                (u[0], target[u])
                for u in rs.select(
                    stop=1, notnull=True, distinct=True, condition=base_condition
                )
            )
        self._base_condition = base_condition
        self._nbunch = nbunch

    @property
    def dialect(self):
        return self._viewer.dialect

    def __len__(self):
        return self._target.rowstore.select(
            stop=2,
            distinct=True,
            notnull=True,
            count=True,
            condition=self._base_condition,
        )

    def iterable_query(self):
        rs = self._target.rowstore
        if self._data is False:
            res = rs.select(
                stop=2, distinct=True, notnull=True, condition=self._base_condition
            )
        elif self._data is True:
            res = rs.partial_fold(
                2, maxfolddepth=1, distinct=True, condition=self._base_condition
            )
            res = res.map(lambda t: t[0] + (t[1],))
        else:
            td = rs.tupleDictSchema
            td = td.left_projection_tupledict(2, self._data)
            lcond = self._base_condition
            ifnullC = self.dialect.columns.IfNullColumn(
                rs.tupleDictSchema[3], self._default
            )
            q = td.select_row_query(
                cols=(0, 1, ifnullC), distinct=True, notnull=1, condition=lcond
            )
            res = self.dialect.helper.IterableQuery(rs.helper, q)
        return res

    def __contains__(self, e):
        if self._viewer._graph.is_directed():
            rs = self._target.rowstore
        else:
            rs = self._viewer._graph.edgestore.rowstore
        if self._data is False:
            if len(e) != 2:
                return False
            res = rs.select(
                key_prefix=e[:2],
                stop=0,
                count=True,
                distinct=True,
                notnull=True,
                limit=1,
                condition=self._base_condition,
            )
            return bool(res)
        elif self._data is True:
            if len(e) != 3:
                return False
            return rs.view(e[:2]) == e[2]
        else:
            if len(e) != 3:
                return False
            res = rs.view((e[0], e[1])).get(self._data, self._default)
            return res == e[2]

    def __iter__(self):
        return iter(self.iterable_query())

    def __contains__(self, e):
        if self._viewer._graph.is_directed():
            rs = self._target.rowstore
        else:
            rs = self._viewer._graph.edgestore.rowstore
        if self._data is False:
            if len(e) != 2:
                return False
            res = rs.select(
                key_prefix=e[:2],
                stop=0,
                count=True,
                distinct=True,
                notnull=True,
                limit=1,
                condition=self._base_condition,
            )
            return bool(res)
        elif self._data is True:
            if len(e) != 3:
                return False
            return rs.view(e[:2]) == e[2]
        else:
            if len(e) != 3:
                return False
            res = rs.view((e[0], e[1])).get(self._data, self._default)
            return res == e[2]

    def __repr__(self):
        limit = self.repr_limit + 1
        rs = self._target.rowstore
        res = rs.select(
            stop=2,
            distinct=True,
            notnull=True,
            condition=self._base_condition,
            limit=limit,
        )
        res = list(res)
        if len(res) < self.repr_limit:
            suff = ""
        else:
            res = res[:-1]
            suff = ", …"
        if self._data is False:
            pass
        elif self._data is True:
            res = map(lambda t: t + (rs.view(t).fold(),), res)
        else:
            res = map(lambda t: t + (rs.view(t).get(self._data, self._default),), res)
        return "{0.__class__.__name__}([{1}{2}])".format(
            self, ", ".join(map(repr, res)), suff
        )


class EdgeDataView(OutEdgeDataView, nxrv.EdgeDataView):
    @functools.wraps(OutEdgeDataView.__init__)
    def __init__(self, viewer, nbunch=None, *args, **kwargs):
        super().__init__(viewer, nbunch, *args, **kwargs)
        if nbunch is None:
            return
        # Override base_condition
        nbunch = self._nbunch
        target = self._target
        base_condition = viewer._base_condition
        rs = target.rowstore
        node_domain = nbunch.query.with_query("node_domain")

        # Avoid having edges between selected nodes listed twice
        condition = rs.tupleDictSchema[0].inset(node_domain)
        condition |= -condition & rs.tupleDictSchema[1].inset(node_domain)
        base_condition &= condition
        self._nodes_nbrs = lambda: (
            (u[0], target[u])
            for u in rs.select(
                stop=1, notnull=True, distinct=True, condition=base_condition
            )
        )
        self._base_condition = base_condition

    # Divergence: __iter__ list the edges without ensuring that first coordinates are selected nodes
    # (but one of source or target should be)


class InEdgeDataView(OutEdgeDataView, nxrv.InEdgeDataView):
    def __init__(self, viewer, nbunch=None, data=False, default=None):
        super().__init__(viewer, nbunch=nbunch, data=data, default=default)
        if nbunch is None:
            return
        base_condition = viewer._base_condition
        nbunch = self._nbunch
        base_condition &= self._target.rowstore.tupleDictSchema[1].inset(nbunch.query)
        target = self._target
        rs = target.rowstore
        self._nodes_nbrs = lambda: (
            (u[0], target[u])
            for u in rs.select(
                stop=1, notnull=True, distinct=True, condition=base_condition
            )
        )
        self._base_condition = base_condition


class OutEdgeView(View, nxrv.OutEdgeView):
    # Checked: networkx uses OutEdgeView's only in DiGraphs and Graphviews (or, as base class of EdgeView's)
    dataview = OutEdgeDataView

    def __init__(self, G):
        super().__init__(G)
        self._target = G.edgestore
        self._base_condition = G.dialect.conditions.EmptyCondition()

    @property
    def dialect(self):
        return self._graph.dialect

    def __len__(self):
        return self._target.rowstore.select(
            stop=2,
            distinct=True,
            notnull=True,
            count=True,
            condition=self._base_condition,
        )

    def __iter__(self):
        return iter(
            self._target.rowstore.select(
                stop=2, distinct=True, notnull=True, condition=self._base_condition
            )
        )

    def __contains__(self, e):
        if self._graph.is_directed():
            target = self._target
        else:
            target = self._graph.edgestore
        return bool(
            target.rowstore.select(key_prefix=e, stop=len(e), count=1)
        )  # no base condition here

    def __repr__(self):
        res = self._target.rowstore.select(
            stop=2,
            distinct=True,
            notnull=True,
            condition=self._base_condition,
            limit=self.repr_limit + 1,
        )
        res = list(res)
        if len(res) < self.repr_limit:
            suff = ""
        else:
            res = res[:-1]
            suff = ", …"
        return "{0.__class__.__name__}([{1}{2}])".format(
            self, ", ".join(map(repr, res)), suff
        )


class EdgeView(OutEdgeView, nxrv.EdgeView):
    dataview = EdgeDataView

    def __init__(self, G):
        super().__init__(G)
        if not G.is_directed() and G.asymedges is not None:
            self._target = G.asymedges
        else:
            rs = self._target.rowstore
            self._base_condition &= rs.tupleDictSchema[0].le(rs.tupleDictSchema[1])


class InEdgeView(OutEdgeView, nxrv.InEdgeView):
    dataview = InEdgeDataView


# === DEGREES === #


class DiDegreeView(View, nxrv.DiDegreeView):
    @functools.wraps(nxrv.DiDegreeView.__init__)
    def __init__(
        self, G, nbunch=None, weight=None, default=1.0, *args, condition=None, **kwargs
    ):
        """
        +	G:
                the graph whose degrees should be viewed
        +	nbunch, args, condition, kwargs:
                c.f. `G.nbunch_iter` arguments
        +	weight:
                a edgestore tupleDict key for considering their associated
                values as edge weights.
        +	default:
                the default weight for edges missing the specified key
                `weight`. The argument is ignored when `weight` is left
                undefined (`None`).
        """
        super().__init__(G)
        self._weight = weight
        self._default = default
        emptycond = G.dialect.conditions.EmptyCondition()
        sch = G.schema
        tds = [sch.nodes, sch.edgestore, sch.adj]
        tds_using_nodes = [True, False, True]
        tds_storing_edges = [False, True, True]
        if sch.is_directed():
            tds.extend([sch.revedgestore, sch.pred])
            tds_using_nodes.extend([False, True])
            tds_storing_edges.extend([True, True])
        elif sch.asymedges:
            tds.append(sch.asymedges)
            tds_using_nodes.append(False)
            tds_storing_edges.append(True)

        if nbunch is not None:
            if hasattr(nbunch, "__len__") and len(nbunch) == 1:
                node_filter = lambda c: c.eq(next(iter(nbunch)))
            else:
                wq = G.nbunch_iter(nbunch, condition=condition).query.with_query(
                    "node_domain"
                )
                node_filter = lambda c: c.inset(wq)
            for i, td in enumerate(tds):
                if tds_using_nodes[i]:
                    tds[i] = td.filter_from_column(0, node_filter(td[0]))
        if weight is None:
            for i, td in enumerate(tds):
                if tds_storing_edges[i]:
                    tds[i] = td.drop_columns(2, 3)
        else:
            for i, td in enumerate(tds):
                if tds_storing_edges[i]:
                    tds[i] = td.left_projection_tupledict(2, weight)
        self.nodes, self.edges, self.adj = tds[:3]
        if sch.is_directed():
            self.revedges, self.pred = tds[3:]
        elif sch.asymedges:
            self.asymedges = tds[3]

    @property
    def all_degree_query(self):
        if not hasattr(self, "_all_degree_query"):
            qdir = self.edges.select_row_query(
                notnull=1,
                aliases=tuple(
                    enumerate(
                        ("node", "neighbor", "weight"),
                    )
                ),
            )
            notloop = self.revedges[1].neq(self.revedges[0])
            qrev = self.revedges.select_row_query(
                notnull=1,
                aliases=tuple(
                    enumerate(
                        ("node", "neighbor", "weight"),
                    )
                ),
            )
            qedges = qdir.union_all_query(qrev).name_query("alledges")
            qnodes = self.nodes.select_row_query(cols=(0,)).name_query("nodes")
            q = qnodes.left_join_query(qedges, (0, 0))
            if self._weight is None:
                col = qedges[1].count()
            else:
                # takes default weight when weight value is NULL
                wcol = qedges[2].ifnull(self._default).cast("NUMERIC")
                # takes weight 0 when target is NULL, otherwise, takes wcol
                col = qedges[1].isnotnull().iff(wcol, 0).sum()
            q = q.select_query(
                columns=(q[0], col), groupby=(0,), aliases=((1, "degree"),)
            )
            self._all_degree_query = q
        return self._all_degree_query

    @property
    def item_degree_query(self):
        if not hasattr(self, "_item_degree_query"):
            q1 = self._item_degree_query_from_td(self.adj)
            q2 = self._item_degree_query_from_td(self.pred)
            self._item_degree_query = q1.union_all_query(q2).select_query(
                columns=(q1[0].sum(),)
            )
        return self._item_degree_query

    def _item_degree_query_from_td(self, td, name=None):
        ph = self._graph.dialect.constants.Placeholder
        if self._weight is None:
            c1 = td[1].count()
        else:
            c1 = (
                td[1]
                .isnotnull()
                .iff(td[2].ifnull(self._default).cast("NUMERIC"), 0)
                .sum()
            )
        q = td.select_row_query(
            (c1,), condition=td[0].eq(ph), aliases=((0, "value"),), notnull=1
        )
        if name:
            q = q.name_query(name)
        return q

    def check_node(self, key):
        if not hasattr(self, "_check_node_query"):
            dialect = self._graph.dialect
            ph = dialect.constants.Placeholder
            adj = self.adj
            self._check_node_query = adj.select_row_query(
                cols=(dialect.columns.ValueColumn(1).count(),), condition=adj[0].eq(ph)
            )
        return bool(next(self._graph.helper.execute(self._check_node_query, (key,)))[0])

    def __repr__(self):
        res = self.all_degree_query.set_limit(self.repr_limit + 1)
        res = self._graph.helper.execute(res)
        res = list(res)
        if len(res) < self.repr_limit:
            suff = ""
        else:
            res = res[:-1]
            suff = ", …"
        res = map(lambda t: f"{t[0]}: {t[1]}", res)
        return f"{self.__class__.__name__}({{{', '.join(map(str, res))}{suff}}})"

    def __call__(self, nbunch=None, weight=None, default=1.0):
        r = super().__call__(nbunch=nbunch, weight=weight)
        if isinstance(r, self.__class__):
            r._default = default
        return r

    def __iter__(self):
        return self._graph.helper.execute(self.all_degree_query)

    def __getitem__(self, key):
        if not self.check_node(key):
            # TODO: avoid double check after contains (e.g. self(0))
            raise KeyError(key)
        return next(self._graph.helper.execute(self.item_degree_query, (key, key)))[0]


class LateralDegreeView:
    _target = "None"

    @property
    def target(self):
        return getattr(self, self._target)

    @property
    def all_degree_query(self):
        if not hasattr(self, "_all_degree_query"):
            self._all_degree_query = self._all_degree_from_td(self.target)
        return self._all_degree_query

    def _all_degree_from_td(self, td, name=None):
        if self._weight is None:
            col = td[1].count()
        else:
            # takes default weight when weight value is NULL
            wcol = td[2].ifnull(self._default).cast("NUMERIC")
            # takes weight 0 when target is NULL, otherwise, takes wcol
            col = td[1].isnotnull().iff(wcol, 0).sum()
        q = td.select_row_query((0, col), groupby=(0,), aliases=((1, "degree"),))
        if name:
            q = q.name_query(name)
        return q

    @property
    def item_degree_query(self):
        if not hasattr(self, "_item_degree_query"):
            ph = self._graph.dialect.constants.Placeholder
            target = self.target
            if self._weight is None:
                c1 = target[1].count()
            else:
                c1 = (
                    target[1]
                    .isnotnull()
                    .iff(target[2].ifnull(self._default).cast("NUMERIC"), 0)
                    .sum()
                )
            self._item_degree_query = target.select_row_query(
                (c1,), condition=target[0].eq(ph), notnull=1
            )
        return self._item_degree_query


class DegreeView(LateralDegreeView, DiDegreeView, nxrv.DegreeView):
    _target = "adj"

    def _all_degree_from_td(self, td, name=None):
        if self._weight is None:
            col = td[1].count()
        else:
            col = (
                td[1]
                .isnotnull()
                .iff(td[2].ifnull(self._default).cast("NUMERIC"), 0)
                .sum()
            )
        q = td.select_row_query(
            (0, col),
            groupby=(0,),
            aliases=((1, "degree"),),
            condition=td[0].neq(td[1]),
            notnull=1,
        )
        loops = td.select_row_query(
            (0, col.multiply(2)),
            groupby=(0,),
            aliases=((1, "degree"),),
            condition=td[0].eq(td[1]),
        )
        q = q.union_all_query(loops)
        q = q.name_query("partial_aggregate")
        q = q.select_query(columns=(0, q[1].sum()), groupby=(0,))
        if name:
            q = q.name_query(name)
        return q

    @property
    def item_degree_query(self):
        if not hasattr(self, "_item_degree_query"):
            ph = self._graph.dialect.constants.Placeholder
            target = self.target
            if self._weight is not None:
                c1 = (
                    target[1]
                    .isnotnull()
                    .iff(target[2].ifnull(self._default).cast("NUMERIC"), 0)
                    .sum()
                )
            else:
                c1 = target[1].count()
            q0 = target.select_row_query(
                (c1,),
                condition=target[0].eq(ph) & target[0].neq(target[1]),
                aliases=((0, "degree"),),
            )
            q = q0.union_all_query(
                target.select_row_query(
                    (c1.multiply(2),),
                    condition=target[0].eq(ph) & target[0].eq(target[1]),
                    aliases=((0, "degree"),),
                )
            )
            self._item_degree_query = q.select_query(columns=(q0[0].sum(),))
        return self._item_degree_query


class OutDegreeView(LateralDegreeView, DiDegreeView, nxrv.DegreeView):
    _target = "adj"


class InDegreeView(LateralDegreeView, DiDegreeView, nxrv.DegreeView):
    _target = "pred"
