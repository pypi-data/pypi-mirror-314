import importlib
import sys
import inspect
from types import ModuleType, FunctionType
import networkx as nx
import networkdisk as nd
from functools import wraps


class nxmock:
    to_mock = {
        "Graph": [nx, nx.classes, nx.classes.graph],
        "DiGraph": [nx, nx.classes, nx.classes.digraph],
    }

    def __init__(
        self, path=":memory:", ndClass=None, silence=True, lazy=False, reload=None
    ):
        if ndClass is None:
            ndClass = nd.sqlite
        self.path = path
        self.ndclass = ndClass
        self.oldGraph = nx.Graph
        self.oldDiGraph = nx.DiGraph

        class mockGraph(ndClass.Graph):
            def __init__(self, *args, **kwargs):
                lpath = kwargs.pop("path", path)
                llazy = kwargs.pop("lazy", lazy)
                super().__init__(*args, db=lpath, lazy=llazy, **kwargs)

        class mockDiGraph(ndClass.DiGraph):
            def __init__(self, *args, **kwargs):
                lpath = kwargs.pop("path", path)
                llazy = kwargs.pop("lazy", lazy)
                super().__init__(*args, db=lpath, lazy=llazy, **kwargs)

        self.Graph = mockGraph
        self.DiGraph = mockDiGraph
        self.silence = silence
        self.reload = reload

    def __enter__(self):
        for k, v in self.to_mock.items():
            for path in v:
                setattr(path, k, getattr(self, k))
        nx.empty_graph.__defaults__ = (0, None, self.Graph)
        if self.reload:
            importlib.reload(sys.modules[self.reload])

    def __exit__(self, *args):
        for k, v in self.to_mock.items():
            for path in v:
                setattr(path, k, getattr(self, "old" + k))
        nx.empty_graph.__defaults__ = (0, None, self.oldGraph)
        if self.reload:
            importlib.reload(sys.modules[self.reload])


def nxmockFun(nxfun, path=":memory:", ndClass=None, silence=True, lazy=False):
    @wraps(nxfun)
    def mocked(*args, **kwargs):
        lpath = kwargs.pop("path", path)
        llazy = kwargs.pop("lazy", lazy)
        with nxmock(
            path=lpath,
            ndClass=ndClass,
            silence=silence,
            lazy=llazy,
            reload=nxfun.__module__,
        ):
            return nxfun(*args, **kwargs)

    return mocked


def nxmockClass(cls, path=":memory:", ndClass=None, silence=True, lazy=False):
    for name, m in inspect.getmembers(cls, inspect.isfunction):
        decorator = lambda e: e
        if name in cls.__dict__ and isinstance(cls.__dict__[name], staticmethod):
            decorator = staticmethod
        setattr(
            cls,
            name,
            decorator(
                nxmockFun(m, path=path, ndClass=ndClass, silence=silence, lazy=lazy)
            ),
        )
    return cls


def nxmockModule(module, path=":memory:", ndClass=None, silence=True, lazy=False):
    attrs = {}
    for name, m in inspect.getmembers(module, inspect.isfunction):
        attrs[name] = staticmethod(
            nxmockFun(m, path=path, ndClass=ndClass, silence=silence, lazy=lazy)
        )
    return type(f"mock_{module.__name__}", (object,), attrs)
