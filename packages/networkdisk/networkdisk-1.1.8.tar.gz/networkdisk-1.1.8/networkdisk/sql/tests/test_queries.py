import itertools, abc, pytest, networkdisk as nd
from networkdisk.sql import sqldialect
from networkdisk.sql.scope import InternalColumns
from networkdisk.exception import NetworkDiskSQLError


class TestColumn:
    dialect = sqldialect

    def setup_method(self):
        SchemaTable = self.dialect.schema.SchemaTable
        columns = self.dialect.columns

        self.T1 = T1 = SchemaTable("name_tbl")
        T1.add_column("id", sqltype="INT", primarykey=True)
        T1.add_column("name", sqltype="JSON")
        self.T2 = T2 = SchemaTable("data_tbl")
        T2.add_column("id", sqltype="INT", primarykey=True)
        T2.add_column("fnameId", references=T1["id"])
        T2.add_column("key", sqltype="TEXT")
        T2.add_column("value", sqltype="JSON")
        self.T3 = T3 = SchemaTable("conflict")
        T3.add_column("id", sqltype="INT", primarykey=True)
        T3.add_column("name", sqltype="JSON")
        T3.add_column("fnameId", sqltype=T3["id"])
        T3.add_column("key", sqltype="TEXT")
        T3.add_column("value", sqltype="JSON")
        self.V = V = dict(
            str=columns.ValueColumn("string"),
            int=columns.ValueColumn(3),
            bool=columns.ValueColumn(True),
            list=columns.ValueColumn(list(range(3))),
            dict=columns.ValueColumn({"key": "value"}),
            set=columns.ValueColumn({"item"}),
            tuple=columns.ValueColumn((3, 4, 8)),
        )

    def test_column(self):
        Ph = self.dialect.constants.Placeholder
        for tbl in [self.T1, self.T2]:
            for name, c in tbl.children.items():
                orig = InternalColumns(tbl)
                origConflict = InternalColumns(tbl, self.T3)
                assert name == c.name
                assert name == c.qformat(context=None)
                assert name == c.qformat(context=None, alias=name)
                assert c.qformat(context=None, alias="alias") == f"{name} AS alias"
                assert c.qformat(context=orig) == f"{name}"
                assert c.qformat(context=origConflict) == f"{tbl.name}.{name}"
                assert c.qformat(context=orig, alias=c.name) == f"{name}"
                assert (
                    c.qformat(context=origConflict, alias=c.name)
                    == f"{tbl.name}.{name}"
                )
                assert c.qformat(context=orig, alias="alias") == f"{name} AS alias"
                assert (
                    c.qformat(context=origConflict, alias="alias")
                    == f"{tbl.name}.{name} AS alias"
                )
                assert c.qformat() == f"{name}"
                assert c.qformat(alias=c.name) == f"{name}"
                assert c.qformat(alias="alias") == f"{name} AS alias"
        origConflict = InternalColumns(self.T3)
        for c in self.V.values():
            assert c.qformat() == Ph.sqlize()
            assert c.qformat(context=origConflict) == Ph.sqlize()
            assert c.qformat(context=None) == Ph.sqlize()
            assert c.qformat(alias="alias") == f"{Ph.sqlize()} AS alias"
            assert (
                c.qformat(context=origConflict, alias="alias")
                == f"{Ph.sqlize()} AS alias"
            )
            assert c.qformat(context=None, alias="alias") == f"{Ph.sqlize()} AS alias"
            assert len(c.get_subargs()) == 1
            assert (c,) == tuple(c.get_subargs())

    def test_transform(self):
        columns = self.dialect.columns
        prev = columns.ValueColumn("any")
        for tbl in (self.T1, self.T2):
            for c in tbl.children.values():
                orig = InternalColumns(tbl)
                origConflict = InternalColumns(tbl, self.T3)
                _kwargs = [
                    {},
                    {"context": orig},
                    {"context": origConflict},
                    {"context": None},
                ]
                #
                t1 = columns.TransformColumn("max", c)
                for kwargs in _kwargs:
                    kwargs = dict(kwargs)
                    assert (
                        t1.qformat(**kwargs).lower()
                        == f"max({c.qformat(**kwargs)})".lower()
                    )
                    assert (
                        t1.qformat(alias="alias", **kwargs).lower()
                        == f"max({c.qformat(**kwargs)}) AS alias".lower()
                    )
                #
                t2 = columns.TransformColumn("min", c, prev)
                for kwargs in _kwargs:
                    kwargs = dict(kwargs)
                    assert (
                        t2.qformat(**kwargs).lower()
                        == f"min({c.qformat(**kwargs)}, {prev.qformat(**kwargs)})".lower()
                    )
                    assert (
                        t2.qformat(alias="alias", **kwargs).lower()
                        == f"min({c.qformat(**kwargs)}, {prev.qformat(**kwargs)}) AS alias".lower()
                    )
                #
                t3 = columns.TransformColumn("sum", c, prev, t2)
                for kwargs in _kwargs:
                    kwargs = dict(kwargs)
                    assert (
                        t3.qformat(**kwargs).lower()
                        == f"sum({c.qformat(**kwargs)}, {prev.qformat(**kwargs)}, {t2.qformat(**kwargs)})".lower()
                    )
                    assert (
                        t3.qformat(alias="alias", **kwargs).lower()
                        == f"sum({c.qformat(**kwargs)}, {prev.qformat(**kwargs)}, {t2.qformat(**kwargs)}) AS alias".lower()
                    )


class TestQuery:
    dialect = sqldialect

    def setup_method(self):
        SchemaTable = self.dialect.schema.SchemaTable
        self.T1 = T1 = SchemaTable("name_tbl")
        T1.add_column("id", sqltype="INT", primarykey=True)
        T1.add_column("name", sqltype="JSON")
        self.T2 = T2 = SchemaTable("data_tbl")
        T2.add_column("id", sqltype="INT", primarykey=True)
        T2.add_column("fnameId", references=T1["id"])
        T2.add_column("key", sqltype="TEXT")
        T2.add_column("value", sqltype="JSON")

    def test_SelectQuery(self):
        SelectQuery = self.dialect.queries.SelectQuery
        T1, T2 = self.T1, self.T2
        Q1 = SelectQuery(T1)
        A1 = "SELECT id, name FROM name_tbl"
        assert Q1.qformat() == A1
        Q2 = SelectQuery(T2)
        A2 = "SELECT id, fnameId, key, value FROM data_tbl"
        assert Q2.qformat() == A2
        Q3 = SelectQuery(T2, columns=("key", "value"))
        A3 = "SELECT key, value FROM data_tbl"
        assert Q3.qformat() == A3
        Q4 = SelectQuery(T2, columns=(T2["key"], "value"))
        A4 = "SELECT key, value FROM data_tbl"
        assert Q4.qformat() == A4

        # Alias
        Q5 = SelectQuery(T2, columns=("key", "value"), aliases={"key": "other_key"})
        A5 = "SELECT key AS other_key, value FROM data_tbl"
        assert Q5.qformat() == A5

        # Nesting
        Q6 = SelectQuery(Q5)
        A6 = f"SELECT other_key, value FROM ({A5})"
        assert Q6.qformat() == A6

        Q7 = SelectQuery(
            Q6, columns=("other_key",), aliases={"other_key": "another_key"}
        )
        A7 = f"SELECT other_key AS another_key FROM ({A6})"
        assert Q6.qformat() == A6

        Q8 = SelectQuery(Q7)
        A8 = f"SELECT another_key FROM ({A7})"
        assert Q7.qformat() == A7

    def test_ValuesQuery(self):
        SelectQuery = self.dialect.queries.SelectQuery
        ValuesQuery = self.dialect.queries.ValuesQuery
        columns = self.dialect.columns
        Q0 = ValuesQuery(3)
        A0 = "VALUES (?)"
        assert Q0.qformat() == A0
        assert tuple(c.value for c in Q0.get_args()) == (3,)
        Q1 = ValuesQuery(2, columns.ValueColumn(4))
        A1 = "VALUES (?), (?)"
        assert Q1.qformat() == A1
        assert tuple(c.value for c in Q1.get_args()) == (2, 4)
        Q2 = SelectQuery(Q1, columns=(columns.StarColumn(),))
        A2 = f"SELECT * FROM ({A1})"
        assert Q2.qformat() == A2
        assert tuple(c.value for c in Q2.get_args()) == (2, 4)

    def test_JoinQuery(self):
        SelectQuery = self.dialect.queries.SelectQuery
        LeftJoinQuery = self.dialect.queries.LeftJoinQuery
        JoinQuery = self.dialect.queries.JoinQuery
        InnerJoinQuery = self.dialect.queries.InnerJoinQuery
        NamedQuery = self.dialect.queries.NamedQuery
        T1, T2 = self.T1, self.T2
        l1 = LeftJoinQuery(T1, T2, ("id", "fnameId"))
        A1 = "name_tbl LEFT JOIN data_tbl ON name_tbl.id = fnameId"
        assert l1.qformat() == A1
        with pytest.raises(NetworkDiskSQLError):
            l2 = LeftJoinQuery(T1, T2, ("id", "fid"))
        l3 = LeftJoinQuery(T1, T2)
        A2 = "name_tbl LEFT JOIN data_tbl"
        assert l3.qformat() == A2
        l4 = LeftJoinQuery(T1, T2, ("id", "fnameId"))
        S5 = SelectQuery(l4, columns=(T2["id"], "name", "key", "value"))
        A5 = "SELECT data_tbl.id, name, key, value FROM name_tbl LEFT JOIN data_tbl ON name_tbl.id = fnameId"
        assert S5.qformat() == A5
        N5 = NamedQuery(S5, "C")
        l6 = JoinQuery(N5, T2, joinpairs=[("id", "id")])
        S6 = SelectQuery(l6, columns=("name", N5["key"]))
        A6 = f"SELECT name, C.key FROM ({A5}) AS C JOIN data_tbl ON C.id = data_tbl.id"
        assert S6.qformat() == A6
        l7 = LeftJoinQuery(T1, T2, ("id", "fnameId"), ("name", "key"))
        A7 = "name_tbl LEFT JOIN data_tbl ON name_tbl.id = fnameId AND name = key"
        assert l7.qformat() == A7
        N8 = NamedQuery(T2, "D")
        l8 = InnerJoinQuery(l1, N8, (T1["id"], "id"))
        A8 = "name_tbl LEFT JOIN data_tbl ON name_tbl.id = data_tbl.fnameId"
        A8 += " INNER JOIN data_tbl AS D ON name_tbl.id = D.id"
        assert l8.qformat() == A8

    def test_WithQuery(self):
        SelectQuery = self.dialect.queries.SelectQuery
        WithQuery = self.dialect.queries.WithQuery
        T1 = self.T1
        Q1 = SelectQuery(T1, columns=("id", "name"))
        W1 = WithQuery(Q1, "w1")
        S = SelectQuery(W1)
        A = "WITH w1 AS (SELECT id, name FROM name_tbl) SELECT id, name FROM w1"
        assert S.qformat() == A
        S = SelectQuery(W1, columns=(W1["id"],))
        A = "WITH w1 AS (SELECT id, name FROM name_tbl) SELECT id FROM w1"
        assert S.qformat() == A

        T2 = self.T2
        Q2 = SelectQuery(T2, columns=("fnameId", "key"))
        W2 = WithQuery(Q2, "w2")
        S = SelectQuery(W2, columns=(W2["key"],))
        A = "WITH w2 AS (SELECT fnameId, key FROM data_tbl) SELECT key FROM w2"
        assert S.qformat() == A
        Q2 = SelectQuery(T2, columns=("fnameId", "key"), aliases={"fnameId": "fid"})
        W2 = WithQuery(Q2, "w2")
        S = SelectQuery(W2, columns=("fid",))
        A = "WITH w2 AS (SELECT fnameId AS fid, key FROM data_tbl) SELECT fid FROM w2"
        assert S.qformat() == A

        S = SelectQuery(W1, W2, columns=("fid", "id", "name"))
        A = "WITH w1 AS (SELECT id, name FROM name_tbl), w2 AS (SELECT fnameId AS fid, key FROM data_tbl) SELECT fid, id, name FROM w1, w2"
        assert S.qformat() == A
