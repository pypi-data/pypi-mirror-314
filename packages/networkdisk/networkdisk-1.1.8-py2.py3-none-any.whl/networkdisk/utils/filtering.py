class BooleanFunctions:
    def allow(allowed_list):
        return lambda e: e in allowed_list

    def forbid(forbid_list):
        return lambda e: e not in forbid_list

    def complement(f):
        return lambda e: not f(e)

    def all(*g):
        return lambda e: all(map(lambda f: f(e), g))

    def any(*g):
        return lambda e: any(map(lambda f: f(e), g))

    ALL = lambda e: True
    NONE = lambda e: False
    CAST = lambda e: bool(e)
    ISNOTNONE = forbid([None])
    ISNOTEMPTY = lambda e: isinstance(e, dict) and e
    EXISTSANDISNOTEMPTY = (
        lambda e: (e is not None)
        and (not hasattr(e, "exists") or e.exists())
        and (not hasattr(e, "empty") or e.empty())
        and (not isinstance(e, dict) or e)
    )
