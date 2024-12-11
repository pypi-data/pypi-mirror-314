import copy


def identity(*args, **kwargs):
    if len(args) == 1:
        return args[0]
    return args


class copymock:
    """
    Mock deepcopy to do nothing.
    """

    def __enter__(self):
        self.oldcode = copy.deepcopy.__code__
        copy.deepcopy.__code__ = identity.__code__

    def __exit__(self, *args):
        copy.deepcopy.__code__ = self.oldcode
