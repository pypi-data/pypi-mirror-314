from networkx.classes import coreviews

"""
Networkx AtlasView __contains__ is incompatible with lazy
TupleDictView's, since the latter do not raise KeyError on
__getitem__, but rather return a view on potentially inexisting
object. This behavior is inherited from the standard class
collections.abc.Mapping.
"""


class AtlasView(coreviews.AtlasView):
    def __contains__(self, key):
        return key in self._atlas


class AdjacencyView(coreviews.AdjacencyView):
    # TODO: why overloading?
    def __getitem__(self, name):
        return AtlasView(self._atlas[name])
