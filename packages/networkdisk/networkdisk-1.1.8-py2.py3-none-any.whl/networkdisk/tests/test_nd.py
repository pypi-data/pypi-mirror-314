import functools, pickle, pytest, tempfile, os
from networkx.classes.tests.test_graph import TestGraph as nxTestGraph
from networkx.classes.tests.test_digraph import TestDiGraph as nxTestDiGraph
from networkx.utils import nodes_equal
import networkx.exception as nxexcept
from networkdisk.tupledict import ReadWriteAbstractRowStore
from networkdisk.sql import SQL_logger
from networkdisk.sqlite import Graph, DiGraph, sqlitedialect as dialect
from networkdisk.exception import NetworkDiskBackendError, NetworkDiskError
from networkdisk.tests import test_nd as ndtest

ungraph = dialect.schemata.ungraph
digraph = dialect.schemata.digraph

glob = globals()
__all__ = []
__module__ = ndtest.__name__
os.makedirs("/tmp/networkdisk", exist_ok=True)
tmpdir = tempfile.mkdtemp(prefix="tests_", dir="/tmp/networkdisk")
tmp = lambda suffix=".db": tempfile.mkstemp(suffix=suffix, dir=tmpdir)


# Graph.default_schema =
Graph.default_lazy = False
DiGraph.default_lazy = False
# ReadWriteAbstractRowStore._updateondelvalue = True


class OverloadTestGraph:
    def test_shallow_copy(self):
        pass

    def test_graph_attr(self):
        G = self.K3.copy()
        G.graph["foo"] = "bar"
        assert G.graph["foo"] == "bar"
        del G.graph["foo"]
        assert G.graph == G.graph_attr_dict_factory()
        H = self.Graph(foo="bar")
        assert H.graph["foo"] == "bar"

    def test_update(self):
        # specify both edges and nodes
        G = self.K3.copy()
        G.update(nodes=[3, (4, {"size": 2})], edges=[(4, 5), (6, 7, {"weight": 2})])
        nlist = [
            (0, {}),
            (1, {}),
            (2, {}),
            (3, {}),
            (4, {"size": 2}),
            (5, {}),
            (6, {}),
            (7, {}),
        ]
        assert sorted(G.nodes.data()) == nlist
        if G.is_directed():
            elist = [
                (0, 1, {}),
                (0, 2, {}),
                (1, 0, {}),
                (1, 2, {}),
                (2, 0, {}),
                (2, 1, {}),
                (4, 5, {}),
                (6, 7, {"weight": 2}),
            ]
        else:
            elist = [
                (0, 1, {}),
                (0, 2, {}),
                (1, 2, {}),
                (4, 5, {}),
                (6, 7, {"weight": 2}),
            ]
            assert sorted(G.edges.data()) == elist
            assert G.graph == G.graph_attr_dict_factory()

            # no keywords -- order is edges, nodes
            G = self.K3.copy()
            G.update([(4, 5), (6, 7, {"weight": 2})], [3, (4, {"size": 2})])
            assert sorted(G.nodes.data()) == nlist
            assert sorted(G.edges.data()) == elist
            assert G.graph == G.graph_attr_dict_factory()

            # update using only a graph
            G = self.Graph()
            G.graph["foo"] = "bar"
            G.add_node(2, data=4)
            G.add_edge(0, 1, weight=0.5)
            GG = G.copy()
            H = self.Graph()
            GG.update(H)
            self.graphs_equal(G, GG)
            H.update(G)
            self.graphs_equal(H, G)

            # update nodes only
            H = self.Graph()
            H.update(nodes=[3, 4])
            assert H.nodes ^ {3, 4} == set()
            assert H.size() == 0

            # update edges only
            H = self.Graph()
            H.update(edges=[(3, 4)])
            assert sorted(H.edges.data()) == [(3, 4, {})]
            assert H.size() == 1

            # No inputs -> exception
            with pytest.raises(nxexcept.NetworkXError):
                self.Graph().update()

    def shallow_copy_graph_attr(self, *args):
        pass

    def shallow_copy_attrdict(self, *args):
        pass

    def shallow_copy_node_attr(self, *args):
        pass

    def shallow_copy_edge_attr(self, *args):
        pass

    def graphs_equal(self, G, H):
        assert G._adj == H._adj
        assert G._node == H._node
        assert G.graph == H.graph
        assert G.name == H.name

    def same_attrdict(self, H, G):
        if H.is_readonly() or G.is_readonly():
            pass
        else:
            super().same_attrdict(H, G)

    def is_deepcopy(self, H, G):
        if H.is_readonly() or G.is_readonly():
            if H.is_view() or G.is_view():
                return getattr(H, "_graph", H) == getattr(G, "_graph", G)
            raise NotImplementedError
        return super().is_deepcopy(H, G)

    def test_nbunch_iter(self):
        G = self.K3
        assert nodes_equal(G.nbunch_iter(), self.k3nodes)  # all nodes
        assert nodes_equal(G.nbunch_iter(0), [0])  # single node
        assert nodes_equal(G.nbunch_iter([0, 1]), [0, 1])  # sequence
        assert nodes_equal(G.nbunch_iter([-1]), [])
        assert nodes_equal(G.nbunch_iter("foo"), [])
        with pytest.raises(nxexcept.NetworkXError):
            bunch = G.nbunch_iter(-1)
        with pytest.raises(nxexcept.NetworkXError):
            bunch = G.nbunch_iter([0, 1, 2, {}])


# GRAPHS
class BaseTestGraph(OverloadTestGraph, nxTestGraph):
    Default_Graph = None
    insert_schema = True

    def setup_method(self):
        getattr(self.Default_Graph.default_dbpath, "commit", lambda: None)()
        self.Graph = self.Default_Graph
        self.K3 = self.Graph(
            [(0, 1), (0, 2), (1, 2)], masterid=1, insert_schema=self.insert_schema
        )
        self.P3 = self.Graph(
            [(0, 1), (1, 2)], masterid=2, insert_schema=self.insert_schema
        )
        self.k3edges = [(0, 1), (0, 2), (1, 2)]
        self.k3nodes = [0, 1, 2]
        type(self).insert_schema = False

    def test_pickle(self):
        if self.K3.helper.dbpath == ":memory:":
            d = pickle.dumps(self.K3)
            with pytest.raises(NetworkDiskBackendError):
                l = pickle.loads(d)
        elif self.K3.helper.dbpath is None:
            d = pickle.dumps(self.K3)
            with pytest.raises(TypeError):
                l = pickle.loads(d)
        else:
            super().test_pickle()


def copy_method(cls):
    def copy(self, as_view=False):
        try:
            return cls.copy(self, as_view=as_view)
        except NetworkDiskError:
            return self.copy_to_networkx()

    return copy


symmode2name = {
    True: "symmetric",
    False: "asymmetric",
    None: "both",
    "auto": "both_triggered",
}
# TODO: dbpathes (as for DiGraphs)
for symmode, name in symmode2name.items():
    _, logfile = tmp(suffix=f"_Graph_{name}.log")
    logger = SQL_logger(file=logfile)
    schema = functools.partial(ungraph, symmode=symmode)

    @functools.wraps(DiGraph.__init__)
    def __init__(self, *args, sql_logger=logger, **kwargs):
        Graph.__init__(self, *args, sql_logger=sql_logger, **kwargs)

    DG = type(
        f"Graph_{name}",
        (Graph,),
        dict(
            default_schema=staticmethod(schema),
            copy=copy_method(Graph),
            __module__=__module__,
            __init__=__init__,
        ),
    )
    glob[DG.__name__] = DG
    TG = type(
        f"TestGraph_{name}",
        (BaseTestGraph,),
        {"Default_Graph": DG, "__module__": __module__},
    )
    glob[TG.__name__] = TG
    __all__.append(TG.__name__)


# DIGRAPHS
class BaseTestDiGraph(BaseTestGraph, nxTestDiGraph):
    # TODO: why not directly defining Graph?
    Default_Graph = None

    def setup_method(self):
        if hasattr(self.Default_Graph.default_dbpath, "db"):
            self.Default_Graph.default_dbpath.db.commit()
        nxTestDiGraph.setup_method(self)
        self.Graph = self.Default_Graph
        self.K3 = self.Graph(
            incoming_graph_data=self.K3,
            masterid=1,
            insert_schema=self.insert_schema,
            create=self.insert_schema,
        )
        self.P3 = self.Graph(
            incoming_graph_data=self.P3,
            masterid=2,
            insert_schema=self.insert_schema,
            create=self.insert_schema,
        )
        type(self).insert_schema = False


digraph2name = {
    digraph: "default",
    dialect.schemata.digraph_one_table: "onetable",
    dialect.schemata.digraph_splitted: "splitted",
}
_, logfile = tmp(suffix=f"_DiGraph.log")
logger = SQL_logger(file=logfile)
dbpathes = {
    "default": None,
    "memory": dialect.helper.Helper(":memory:", sql_logger=logger),
    "path": tmp()[1],
}
for schema, name in digraph2name.items():
    for i, dbpath in dbpathes.items():

        @functools.wraps(DiGraph.__init__)
        def __init__(
            self,
            *args,
            create=True,
            insert_schema=True,
            autocommit=True,
            sql_logger=logger,
            **kwargs,
        ):
            Graph.__init__(
                self,
                *args,
                create=create,
                insert_schema=insert_schema,
                autocommit=autocommit,
                sql_logger=sql_logger,
                **kwargs,
            )

        cdict = dict(
            default_schema=staticmethod(schema),
            copy=copy_method(Graph),
            __module__=__module__,
            __init__=__init__,
        )
        if dbpath is not None:
            cdict["default_dbpath"] = dbpath
        DG = type(f"DiGraph_{name}_{i}", (DiGraph,), cdict)
        glob[DG.__name__] = DG
        TG = type(
            f"TestDiGraph_{name}_{i}",
            (BaseTestDiGraph,),
            {"Default_Graph": DG, "__module__": __module__},
        )
        glob[TG.__name__] = TG
        __all__.append(TG.__name__)
