import json, pickle, sys


def identity(o):
    return o


def decodeFromJson(t):
    if t is None:
        return None
    elif isinstance(t, (int, float)):
        return t
    return json.loads(t)


def encodeToJson(o):
    return json.dumps(o)


def decodeFromText(t):
    return t  # convert list to tuple, useful for tupledict hashable keys, but not for values


def encodeToText(o):
    return str(o)


def decodeFromBlob(b):
    return None if b is None else pickle.loads(b)


def encodeToBlob(o):
    return pickle.dumps(o)


def decodeDate(d):
    return d


def encodeDate(d):
    return "date('{}')".format(d)


def encodeToInt(o):
    if isinstance(o, int):
        return o
    raise TypeError(o)


def encodeToFloat(o):
    if isinstance(o, float):
        return o
    raise TypeError(o)


# BY SQL TYPES
encoderFunctions = dict(
    IDENTITY=(identity, identity),
    INT=(encodeToInt, identity),
    INTEGER=(encodeToInt, identity),
    NUMERIC=(encodeToFloat, identity),
    TEXT=(encodeToText, decodeFromText),
    JSON=(encodeToJson, decodeFromJson),
    DATE=(encodeDate, decodeDate),
    BLOB=(encodeToBlob, decodeFromBlob),
    BOOL=(lambda f: "ON" if f else "OFF", bool),
)

# BY ALIAS
encoderFunctions.update(
    [(None, encoderFunctions["IDENTITY"])],
    jsonify=encoderFunctions["JSON"],
    textify=encoderFunctions["TEXT"],
    blobify=encoderFunctions["BLOB"],
)


# COMPLEX STRUCTURE SERIALIZING
def dictify(obj, context=None):
    try:
        h = hash(obj)
    except TypeError:
        h = id(obj)
    if context is None:
        context = {}
    if h in context:
        return h, context
    if isinstance(obj, (str, int, float, dict, type(None))):
        d = obj
    elif hasattr(obj, "__getstate__"):
        d = obj.__getstate__()
    elif hasattr(obj, "_asdict"):
        d = dict(obj._asdict())
    elif hasattr(obj, "__iter__"):
        d = [dictify(v, context=context)[0] for v in obj]
    else:
        raise TypeError(f"Undictifable type {obj}")
    if type(d) is dict:
        d = {k: dictify(v, context=context)[0] for k, v in d.items()}
    context[h] = [obj.__class__.__module__, obj.__class__.__name__, d]
    return h, context


def dedictify(h, context, rebuilt=None):
    rebuilt = rebuilt or {}
    if h in rebuilt:
        return rebuilt[h]
    modname, clsname, dump = context[h]
    cls = getattr(sys.modules[modname], clsname, type(None))
    if type(dump) is dict:
        dump = {k: dedictify(v, context, rebuilt=rebuilt) for k, v in dump.items()}
    if issubclass(cls, (int, str, float, dict, type(None))):
        rebuilt[h] = dump
    elif hasattr(cls, "__getstate__"):
        new = object.__new__(cls)
        new.__setstate__(dump)
        rebuilt[h] = new
    elif hasattr(cls, "_asdict"):
        rebuilt[h] = cls(**dump)
    elif isinstance(dump, list):
        dump = (dedictify(v, context, rebuilt=rebuilt) for v in dump)
        rebuilt[h] = cls(dump)
    else:
        raise TypeError(f"Invalid context {dump}")
    return rebuilt[h]
