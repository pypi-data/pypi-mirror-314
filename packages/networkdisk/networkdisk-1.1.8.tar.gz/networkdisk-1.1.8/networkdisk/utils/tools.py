import sys, codecs, io

try:
    utf8_stdout = open(sys.stdout.fileno(), "w", encoding="UTF-8")
except io.UnsupportedOperation:
    utf8_stdout = sys.stdout


class OutFile:
    def __init__(self, path=None, mode="a", encoding="UTF-8"):
        self.path = path
        self.mode = mode
        self.encoding = encoding

    def __enter__(self):
        if self.path is None:
            self.opened = False
            self.outfile = utf8_stdout
        else:
            self.opened = True
            self.outfile = open(self.path, self.mode, encoding=self.encoding)
        return self.outfile

    def __exit__(self, *args):
        if self.opened:
            self.outfile.close()


def overload_package(
    overloaded_package, overloading_package_name, L=locals(), G=globals()
):
    moddict = {"__module__": overloading_package_name}
    for name, obj in overloaded_package.__dict__.items():
        if not isinstance(obj, type) or name in L:
            # TODO: smart inspection, for the case where obj is a static/class method of a class of overloaded_package (?)
            continue
        mro = obj.mro()
        prev = []
        for k in reversed(mro):
            n = k.__name__
            if n in L:
                k = L[n]
                prev = [p for p in prev if p not in k.mro()]
                prev.append(k)
            elif prev:
                k = type(n, (k, *reversed(prev)), moddict)
                L[n] = k
                G[n] = k
                prev = [k]
    getattr(overloaded_package, "update_globals", lambda g: None)(G)
    return G
