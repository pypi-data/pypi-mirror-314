import pytest, itertools, pickle
from networkdisk.exception import NetworkDiskSQLError
from networkdisk.sql import sqldialect
from networkdisk.utils.serialize import encoderFunctions
from networkdisk.sql.scope import InternalColumns


class SchemaBase:
    """
    Setup methods for schemas related tests.
    """

    dialect = sqldialect

    def setup_method(self):
        dialect = self.dialect
        self.Table = Table = dialect.schema.SchemaTable
        self.View = dialect.schema.SchemaView
        self.Helper = dialect.helper.Helper
        self.Master = dialect.master.MasterGraphs
        self.Placeholder = dialect.constants.Placeholder
        self.ValueColumn = dialect.columns.ValueColumn
        self.CompareCondition = dialect.conditions.CompareCondition
        self.T1 = T1 = Table("name_tbl")
        T1.add_primarykey()
        T1.add_column("name", sqltype="JSON")
        self.T2 = T2 = Table("data_tbl")
        T2.add_column("id", sqltype="INT", primarykey=True)
        T2.add_column("fnameId", references=T1["id"], on_delete="CASCADE")
        T2.add_column("key", sqltype="TEXT")
        T2.add_column("value", sqltype="JSON")
        self.T3 = T3 = Table("conflict")
        T3.add_column("id", sqltype="INT", primarykey=True)
        T3.add_column("name", sqltype="JSON")
        T3.add_column("fnameId", sqltype=T3["id"])
        T3.add_column("key", sqltype="TEXT")
        T3.add_column("value", sqltype="JSON")


class Schema(SchemaBase):
    def test_primarykeys(self):
        T1, T2 = self.T1, self.T2
        assert list(T1.primarykeys) == [T1["id"]]
        assert list(T2.primarykeys) == [T2["id"]]

    def test_foreignkeys(self):
        T1, T2 = self.T1, self.T2
        assert list(T1.foreignkeys) == []
        assert list(T2.foreignkeys) == [T2["fnameId"]]

    def test_columns(self):
        T = self.Table("fake_table")  # table address
        TableColumn = T.add_column
        # typed columns
        c0 = TableColumn("c0", sqltype="INT")
        assert c0
        c1 = TableColumn("c1", sqltype="INTEGER")
        assert c1
        c2 = TableColumn("c2", sqltype="TEXT")
        assert c2
        c3 = TableColumn("c3", sqltype="BLOB")
        assert c3
        c4 = TableColumn("c4", sqltype="DATE")
        assert c4
        # unknown type columns
        with pytest.raises(KeyError):
            c5 = TableColumn("c5", sqltype="")
        with pytest.raises(AttributeError):
            c6 = TableColumn("c6", sqltype=4)
        c7 = TableColumn("c7", sqltype=4, encoder="INT")
        assert c7
        with pytest.raises(AttributeError):
            c8 = TableColumn("c8", sqltype=True)
        c9 = TableColumn("c9", sqltype=True, encoder="INT")
        assert c9
        with pytest.raises(KeyError):
            c10 = TableColumn("c10", sqltype="UNKNOWN")
        c11 = TableColumn("c11", sqltype="UNKNOWN", encoder="INT")
        assert c11
        # custom type
        encoderFunctions["UNKNOWN"] = pickle.dumps, pickle.loads
        c12 = TableColumn("c12", sqltype="UNKNOWN")
        assert c12
        # references
        c13 = TableColumn("c13", references=c0)
        assert c13
        with pytest.raises(AssertionError):
            c14 = TableColumn("c14", sqltype="TEXT", references=c0)
        c15 = TableColumn("c15", sqltype="INT", references=c0)
        assert c15
        c16 = TableColumn("c16", sqltype=c0, references=c0)
        assert c16
        c17 = TableColumn("c17", sqltype=c0)
        assert c17
        assert not c17.foreignkey
        # primary key
        c18 = TableColumn("c18", sqltype="INTEGER", primarykey=True)
        assert c18
        assert c18.primarykey

    def test_tables(self):
        T1, T2, T3 = self.T1, self.T2, self.T3
        C1 = "CREATE TABLE name_tbl (id INTEGER PRIMARY KEY AUTOINCREMENT, name JSON)"
        assert C1 == T1.create_query().qformat()
        C2 = "CREATE TABLE data_tbl (id INT PRIMARY KEY, fnameId INTEGER REFERENCES name_tbl(id) ON DELETE CASCADE, key TEXT, value JSON)"
        assert C2 == T2.create_query().qformat()
        C3 = "CREATE TABLE conflict (id INT PRIMARY KEY, name JSON, fnameId INT, key TEXT, value JSON)"
        assert C3 == T3.create_query().qformat()

    def test_views(self):
        View = self.View
        JoinQuery = self.dialect.queries.JoinQuery
        SelectQuery = self.dialect.queries.SelectQuery
        T1, T2, T3 = self.T1, self.T2, self.T3
        with pytest.raises(NetworkDiskSQLError):
            V = View("view", JoinQuery(T1, T2))
        with pytest.raises(NetworkDiskSQLError):
            V = View("view", SelectQuery(T1, T2))
        V = View("view", SelectQuery(T1, T2), column_names={2: "tid"})
        C = "CREATE VIEW view(id, name, tid, fnameId, key, value) AS SELECT name_tbl.id, name, data_tbl.id, fnameId, key, value FROM name_tbl, data_tbl"
        assert C == V.create_query().qformat()

    def test_qformat(self):
        T1, T2 = self.T1, self.T2
        assert T1.qformat() == T1.name
        assert T2.qformat() == T2.name
        for tbl in [T1, T2]:
            for col in tbl.external_columns:
                orig = InternalColumns(tbl)
                origConflict = InternalColumns(tbl, self.T3)
                assert col.qformat(context=False) == col.name
                assert col.qformat(context=orig) == f"{col.name}"
                assert col.qformat(context=origConflict) == f"{tbl.name}.{col.name}"
                assert col.qformat() == f"{col.name}"

    def test_tree(self):
        T1, T2 = self.T1, self.T2
        allnodes = self.get_all_schema_nodes(T1, T2)
        for node in allnodes:
            if hasattr(node, "children"):
                for name, child in node.children.items():
                    assert child.name == name

    def test_hash(self):
        s = set()
        for n in self.get_all_schema_nodes():
            assert hasattr(n, "__hash__")
            s.add(n)

    def get_all_schema_nodes(self, *nodes):
        if not nodes:
            nodes = (self.T1, self.T2)
        new = list(nodes)
        seen = new[:]
        while new:
            v = new.pop()
            if hasattr(v, "values"):
                for w in v.values():
                    if w not in seen:
                        new.append(w)
                        seen.append(w)
        return seen


class SchemaHelper(SchemaBase):
    path = None

    def setup_method(self):
        super().setup_method()
        self.M = self.Master(self.path)
        self.H = self.M.helper
        self.H.execute(self.T1.create_query())
        self.H.execute(self.T2.create_query())
        self.H.execute(self.T3.create_query())

    def test_insert(self):
        H = self.H
        Placeholder = self.Placeholder
        ValueColumn = self.ValueColumn
        CompareCondition = self.CompareCondition
        T1, T2, T3 = self.T1, self.T2, self.T3
        H.execute(T1.insert_values("Foo", columns=("name",)))
        H.execute(T1.insert_values(Placeholder, columns=("name",)), args=("Bars",))
        assert sorted(H.execute(T1.select_query(columns=("name",)))) == [
            ("Bars",),
            ("Foo",),
        ]
        H.execute(T1.delete_query())
        assert sorted(H.execute(T1.select_query(columns=("name",)))) == []
        I = tuple((e,) for e in "The quick brown fox jumps over the lazy dog".split())
        H.executemany(T1.insert_many(("name",)), I=I)
        assert sorted(H.execute(T1.select_query(columns=("name",)))) == sorted(I)
        H.execute(T1.delete_query())
        assert sorted(H.execute(T1.select_query())) == []
        H.execute(T1.insert_values((22, "Foo")))
        H.execute(T1.insert_values((44, "Bar")))
        assert sorted(H.execute(T1.select_query())) == [(22, "Foo"), (44, "Bar")]
        selq = T1.select_query(
            columns=("id", ValueColumn("color"), ValueColumn("black")),
            condition=CompareCondition(T1["name"], "Foo"),
        )
        inq = T2.insert_query(selq, columns=("fnameId", "key", "value"))
        H.execute(inq)
        selq = T2.select_query(columns=("fnameId", "key", "value"))
        assert sorted(H.execute(selq)) == [(22, "color", "black")]
        data = {"a": "b", "c": "d"}
        selq = T1.select_query(
            columns=("id", ValueColumn("data"), ValueColumn(Placeholder)),
            condition=CompareCondition(T1["name"], "Foo"),
        )
        inq = T2.insert_query(selq, columns=("fnameId", "key", "value"))
        H.execute(inq, args=(data,))
        selq = T2.select_query(
            columns=("value",), condition=CompareCondition(T2["key"], "data")
        )
        assert sorted(H.execute(selq)) == [(data,)]
