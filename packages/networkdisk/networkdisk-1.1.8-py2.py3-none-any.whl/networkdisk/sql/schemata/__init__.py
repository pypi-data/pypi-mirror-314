from .ungraph import ungraph, ungraph_unsplitted, load_ungraph
from .digraph import digraph, digraph_one_table, digraph_splitted, load_digraph
from networkdisk.sql.dialect import sqldialect as dialect

dialect = dialect.provide_submodule("schemata")

__all__ = ["ungraph", "digraph", "load_graph", "load_ungraph", "load_digraph"]


@dialect.register(True)
def load_graph(dialect, directed, state):
    if directed:
        return dialect.schemata.load_digraph(**state)
    else:
        return dialect.schemata.load_ungraph(**state)
