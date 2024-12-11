from .test_schema import SchemaBase, SchemaHelper
import networkx as nx
from networkdisk.sql import sqldialect as dialect


class TupleDictSchema(SchemaBase):
    def setup_method(self):
        super().setup_method()
        self.tupledict = tupledict = dialect.tupledict
        self.conditions = dialect.conditions
        self.columns = dialect.columns
        T1 = self.T1
        T2 = self.T2
        self.TDS1 = tupledict.ReadWriteTupleDictSchema(
            T1,
            T2,
            columns=("name", "key", "value"),
            joinpairs=[
                (T1["id"], T2["fnameId"]),
            ],
        )

    def test_repr(self):
        _repr = "ReadWriteTupleDictSchema<name_tbl.name, data_tbl.key, data_tbl.value>"
        assert self.TDS1.__repr__() == _repr

    def test_select_row_simple(self):
        TDS = self.TDS1
        Q1 = "SELECT ?"
        assert TDS.select_row_query(()).qformat().strip() == Q1

        Q2 = "SELECT key FROM name_tbl LEFT JOIN data_tbl ON name_tbl.id = fnameId"
        assert TDS.select_row_query((1,)).qformat() == Q2

        Q3 = "SELECT key, value FROM name_tbl LEFT JOIN data_tbl ON name_tbl.id = fnameId"
        assert TDS.select_row_query((1, 2)).qformat() == Q3
        assert TDS.select_row_query((TDS[1], 2)).qformat() == Q3
        assert TDS.select_row_query((1, TDS[2])).qformat() == Q3

        Q4 = (
            "SELECT name, key FROM name_tbl LEFT JOIN data_tbl ON name_tbl.id = fnameId"
        )
        assert TDS.select_row_query((0, 1)).qformat() == Q4

        Q5 = "SELECT name, key, value FROM name_tbl LEFT JOIN data_tbl ON name_tbl.id = fnameId"
        assert TDS.select_row_query((0, 1, 2)).qformat() == Q5

        Q6 = "SELECT value, key, name FROM name_tbl LEFT JOIN data_tbl ON name_tbl.id = fnameId"
        assert TDS.select_row_query((2, 1, 0)).qformat() == Q6

    def test_operations_select(self):
        TDS = self.TDS1
        columns = self.columns
        conditions = self.conditions
        tdsfrom = "FROM name_tbl INNER JOIN data_tbl ON name_tbl.id = fnameId"
        Q1 = f"SELECT name, key, value {tdsfrom} WHERE value IS NOT NULL"
        assert TDS.select_row_query((0, 1, 2), notnull=True).qformat() == Q1
        Q2 = f"SELECT SUM(value) {tdsfrom} WHERE value IS NOT NULL AND key = ?"
        sq = TDS.select_row_query(
            (columns.SumColumn(TDS[2]),),
            notnull=True,
            condition=conditions.CompareCondition(TDS[1], columns.ValueColumn("money")),
        )
        assert sq.qformat() == Q2

    def test_conditions_select(self):
        TDS = self.TDS1
        conditions = self.conditions
        Q1 = TDS.select_row_query(
            (0,),
            condition=conditions.CompareCondition(TDS[1], "first name")
            & conditions.CompareCondition(TDS[2], "John"),
        )
        A1 = "SELECT name FROM name_tbl INNER JOIN data_tbl ON name_tbl.id = fnameId WHERE key = ? AND value = ?"
        assert Q1.qformat() == A1
        assert tuple(c.value for c in Q1.get_args()) == ("first name", "John")

    def test_insert_rows(self):
        TDS = self.TDS1
        PLACEHOLDER = self.dialect.constants.Placeholder
        Qs = (
            TDS.insert_infix_query(("a",)),
            TDS.insert_infix_query(("a", "color", "black")),
        )
        assert Qs[0].qformat() == "INSERT INTO name_tbl(name) VALUES (?)"
        assert str(tuple(Qs[0].get_args())) == "(ValueColumn<name:?:a>,)"
        assert (
            Qs[1].qformat()
            == "INSERT INTO data_tbl(fnameId, key, value) SELECT id, ?, ? FROM name_tbl WHERE name = ?"
        )
        assert (
            str(tuple(Qs[1].get_args()))
            == "(ValueColumn<key:?:color>, ValueColumn<value:?:black>, ValueColumn<name:?:a>)"
        )
        Qs = (
            TDS.insert_infix_query(("a",)),
            TDS.insert_infix_query(("a", PLACEHOLDER, PLACEHOLDER)),
        )
        assert Qs[0].qformat() == "INSERT INTO name_tbl(name) VALUES (?)"
        assert str(tuple(Qs[0].get_args())) == "(ValueColumn<name:?:a>,)"
        assert (
            Qs[1].qformat()
            == "INSERT INTO data_tbl(fnameId, key, value) SELECT id, ?, ? FROM name_tbl WHERE name = ?"
        )
        assert (
            str(tuple(Qs[1].get_args()))
            == "(ValueColumn<key:?:?>, ValueColumn<value:?:?>, ValueColumn<name:?:a>)"
        )
        assert (
            str(tuple(Qs[1].get_placeholder_args()))
            == "(ValueColumn<key:?:?>, ValueColumn<value:?:?>)"
        )


class TupleDict(SchemaHelper):
    def setup_method(self):
        super().setup_method()
        T1, T2, T3 = self.T1, self.T2, self.T3
        tupledict = self.dialect.tupledict
        TDS1 = tupledict.ReadWriteTupleDictSchema(
            T1,
            T2,
            columns=("name", "key", "value"),
            joinpairs=[
                (T1["id"], T2["fnameId"]),
            ],
        )
        TDS2 = tupledict.ReadWriteTupleDictSchema(
            T3,
            columns=("name", "key", "value"),
            joinpairs=[
                (T1["id"], T2["fnameId"]),
            ],
        )
        self.TD = TD1 = self.dialect.tupledict.ReadWriteTupleDict(
            self.M, TDS1, lazy=False
        )
        self.TD_Lazy = TD2 = self.dialect.tupledict.ReadWriteTupleDict(
            self.M, TDS1, lazy=True
        )
        self.TD_one_table = TD3 = self.dialect.tupledict.ReadWriteTupleDict(
            self.M, TDS2, lazy=False
        )
        self.TD_one_table = TD4 = self.dialect.tupledict.ReadWriteTupleDict(
            self.M, TDS2, lazy=True
        )
        self.TDs = [TD1, TD2, TD3, TD4]

    def test_updates(self):
        for T in self.TDs:
            T["foo"] = "bar"
            assert T["foo"] == {"bar": None}
            del T["foo"]
            assert T.fold() == {}
            d = {"key1": (0, 1, 2), "key2": "value"}
            T["foo"] = d
            assert T["foo"] != d
            d["key1"] = list(d["key1"])
            assert T["foo"] == d
            del T["foo"]
            assert T.fold() == {}

    # TODO: write many more tests
