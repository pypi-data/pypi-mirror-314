from networkx.exception import NetworkXException, NetworkXError


class NetworkDiskException(NetworkXException):
    """Base NetworkDisk Exception"""

    pass


class NetworkDiskError(NetworkDiskException, NetworkXError):
    """A NetworkDisk error raised during Graph Manipulation"""

    pass


class NetworkDiskTupleDictError(NetworkDiskException):
    """A NetworkDiskException raised during the manipulation of TupleDict"""

    pass


class NetworkDiskSQLError(NetworkDiskException):
    """A NetworkDiskException raised during the construction of a SQL query"""


class NetworkDiskMetaError(NetworkDiskException):
    """A NetworkDiskException raised during the jungling of Graphs in a DB"""


class NetworkDiskBackendError(NetworkDiskException):
    """A NetworkDiskException raised to encapsulate a backend error"""


class NetworkDiskBackendTypeError(NetworkDiskBackendError, TypeError):
    """A NetworkDiskException raised to encapsulate an argument type error"""
