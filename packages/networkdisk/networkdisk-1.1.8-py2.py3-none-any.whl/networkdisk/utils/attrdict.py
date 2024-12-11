import functools
from collections.abc import MutableMapping


class AttrDict(MutableMapping):
    @functools.wraps(dict.__init__)
    def __init__(self, *args, **kwargs):
        self.proxy_dict = dict(*args, **kwargs)

    def __getattr__(self, attr):
        # getattr: only called when attr is not find with usual method
        if attr in self.proxy_dict:
            return self.proxy_dict[attr]
        raise AttributeError(attr)

    def __setattr__(self, attr, v):
        if attr not in ("proxy_dict",):
            self.proxy_dict[attr] = v
        else:
            super().__setattr__(attr, v)

    def __dir__(self):
        return self.proxy_dict.keys()

    # MutableMapping method
    def __getitem__(self, k):
        return self.proxy_dict[k]

    def __setitem__(self, k, v):
        self.proxy_dict[k] = v

    def __delitem__(self, k):
        del self.proxy_dict[k]

    def __iter__(self):
        return iter(self.proxy_dict)

    def __len__(self):
        return len(self.proxy_dict)

    def __getstate__(self):
        return self.proxy_dict

    def __setstate__(self, state):
        self.proxy_dict = state
