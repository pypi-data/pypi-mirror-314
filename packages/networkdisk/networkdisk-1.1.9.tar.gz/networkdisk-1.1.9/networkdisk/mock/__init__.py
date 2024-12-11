from networkdisk.mock.nxmock import nxmock, nxmockFun, nxmockClass, nxmockModule
from networkdisk.mock.copymock import copymock

"""
This submodule provide a context manager
that overload networkx modules and replace
them by networkdisk.

Example:
	>>> import networkdisk as nd
	>>> nd.silence()
	>>> import networkx as nx
	>>> with nxmock(":memory:"):
		G = nx.random_regular_graph(10, 100)
	>>> type(G)
	<class 'networkdisk.sqlite.graph.SQLiteGraph'>

"""
