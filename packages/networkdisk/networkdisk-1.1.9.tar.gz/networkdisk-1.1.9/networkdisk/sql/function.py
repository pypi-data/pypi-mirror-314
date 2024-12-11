import functools, copy
import networkx as nx


@functools.wraps(nx.freeze)
def freeze(G):
    object.__setattr__(G, "_node", G._node.to_readonly())
    object.__setattr__(G, "_adj", G._adj.to_readonly())
    object.__setattr__(G, "_edgestore", G.edgestore.to_readonly())
    if G.is_directed():
        object.__setattr__(G, "_pred", G._pred.to_readonly())
        object.__setattr__(G, "_succ", G._adj)
    return nx.freeze(G)


def frozen_copy(G):
    H = copy.copy(G)
    return freeze(H)
