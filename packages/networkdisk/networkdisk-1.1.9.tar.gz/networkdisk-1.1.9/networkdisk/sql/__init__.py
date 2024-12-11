"""
A module for generate and manipulate SQL queries.
>>> Users = Table("users")
>>> Users.add_primarykey()
>>> Users.add_column("fName", sqltype="TEXT")
>>> Users.add_column("lName", sqltype="TEXT")
>>> Address = Table("addresses")
>>> Address.add_column("user_id", references=Users["id"])
>>> Address.add_column("street", sqltype="TEXT")
>>> Address.add_column("city", sqltype="TEXT")
>>> data = Table("data")
>>> data.add_column("user_id", references=Users["id"])
>>> data.add_column("key", sqltype="TEXT")
>>> data.add_column("value", sqltype="TEXT")
>>> TDS = tupledict.ReadWriteTupleDictSchema((Users["fName"], Users["lName"], data["key"], data["value"]), (Users["id"], data["user_id"]))
>>> tuple(TDS.insert_infix_query(("A", "B")), TDS.insert_infix_query(("A", "B", "color", "black")))
"""

from . import dialect

sqldialect = dialect.sqldialect

from networkdisk.sql import constraints
from networkdisk.sql import conditions
from networkdisk.sql import columns
from networkdisk.sql import queries
from networkdisk.sql import classes
from networkdisk.sql import tupledict
from networkdisk.sql import graph_schema
from networkdisk.sql import master
from networkdisk.sql import schema
from networkdisk.sql import helper
from networkdisk.sql.graph import Graph
from networkdisk.sql.digraph import DiGraph
from networkdisk.sql.function import freeze
from networkdisk.sql.sqllogging import SQL_logger
from networkdisk.exception import NetworkDiskSQLError


__all__ = [
    "sqldialect",
    "dialect",
    "Graph",
    "DiGraph",
    "NetworkDiskSQLError",
    "freeze",
    "SQL_logger",
]
