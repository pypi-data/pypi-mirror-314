import networkdisk as nd
import networkx.classes.tests.test_reportviews
from networkx.classes.tests.test_reportviews import TestNodeView as nxTestNodeView
from networkx.classes.tests.test_reportviews import (
    TestNodeDataView as nxTestNodeDataView,
)
from networkx.classes.tests.test_reportviews import (
    TestEdgeDataView as nxTestEdgeDataView,
)
from networkx.classes.tests.test_reportviews import (
    TestOutEdgeDataView as nxTestOutEdgeDataView,
)
from networkx.classes.tests.test_reportviews import (
    TestInEdgeDataView as nxTestInEdgeDataView,
)
from networkx.classes.tests.test_reportviews import TestEdgeView as nxTestEdgeView
from networkx.classes.tests.test_reportviews import TestOutEdgeView as nxTestOutEdgeView
from networkx.classes.tests.test_reportviews import TestInEdgeView as nxTestInEdgeView
from networkx.classes.tests.test_reportviews import TestDegreeView as nxTestDegreeView
from networkx.classes.tests.test_reportviews import (
    TestDiDegreeView as nxTestDiDegreeView,
)
from networkx.classes.tests.test_reportviews import (
    TestOutDegreeView as nxTestOutDegreeView,
)
from networkx.classes.tests.test_reportviews import (
    TestInDegreeView as nxTestInDegreeView,
)

glob = globals()
__all__ = []

# TODO test for other schema,
nxTestClasses = [
    nxTestNodeView,
    nxTestNodeDataView,
    nxTestEdgeDataView,
    nxTestOutEdgeDataView,
    nxTestInEdgeDataView,
    nxTestEdgeView,
    nxTestOutEdgeView,
    nxTestInEdgeView,
    nxTestDegreeView,
    nxTestDiDegreeView,
    nxTestOutDegreeView,
    nxTestInDegreeView,
]


def override_setup_method(cls):
    cls.mro()[1].setup_class()
    if cls.G.is_directed():
        ndG = cls.ndDiGraph(cls.G, lazy=True)
    else:
        ndG = cls.ndGraph(cls.G, lazy=True)
    cls.G = ndG


def avoid(self):
    pass


overload = dict(
    ndDiGraph=nd.sqlite.DiGraph,
    ndGraph=nd.sqlite.Graph,
    setup_class=classmethod(override_setup_method),
    test_pickle=avoid,
    test_repr=avoid,
    test_str=avoid,
)
for C in nxTestClasses:
    ndC = type(f"{C.__name__}", (C,), overload)
    glob[ndC.__name__] = ndC
    __all__.append(ndC.__name__)
