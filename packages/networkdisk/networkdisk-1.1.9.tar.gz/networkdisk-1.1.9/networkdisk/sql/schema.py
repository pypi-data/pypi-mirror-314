"""Module for DB schema manipulation"""

import abc, collections, functools, itertools, networkx as nx
from networkdisk.sql import queries as ndqueries  # needed for nonscopable decorator
from networkdisk.sql.scope import ExternalColumns
from networkdisk.utils.serialize import encoderFunctions
from networkdisk.utils.constants import IdentityFunction
from networkdisk.exception import NetworkDiskSQLError
from networkdisk.sql.dialect import sqldialect as dialect

subdialect = dialect.provide_submodule(__name__)

__all__ = [
    "SchemaNode",
    "SchemaInnerNode",
    "SchemaObject",
    "SchemaTableColumn",
    "SchemaIndex",
    "SchemaTrigger",
    "SchemaContainer",
    "SchemaTable",
    "SchemaView",
    "Schema",
]


# BASE SCHEMA OBJECT
class SchemaNode(abc.ABC):
    """
    This abstract class has two goals:
    1.	Structure the Schema as a single-chained top-down tree,
    except for leaves, namely `QueryColumn`s, which point to
    their parent table (`SchemaTable`). Top-down links are
    stored by name in the `children` dictionary attribute of
    internal nodes.

    2.	Propose dump and load serialization method for storing the
    schema in file or db.

    Parameters
    ----------
    name: str
            a name to identified the node.

    """

    def __init__(self, dialect, name):
        self.name = name
        self.dialect = dialect

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.name}>"

    def __getstate__(self):
        return dict(name=self.name, dialect=self.dialect.name)

    def __setstate__(self, state):
        for k, v in state.items():
            if k == "dialect":
                v = dialect._dialects[v]
            setattr(self, k, v)

    dumps = __getstate__

    @classmethod
    def loads(cls, state):
        self = object.__new__(cls)
        self.__setstate__(state)
        return self

    def __hash__(self):
        return hash(tuple(sorted(self.__getstate__().items())))


class SchemaInnerNode(SchemaNode):
    def create_script(self, ifnotexists=False):
        for dep in self.get_dependencies():
            yield dep.create_query(ifnotexists=ifnotexists)

    def get_dependency_graph(self):
        dag = nx.DiGraph()
        return dag

    def get_dependencies(self):
        yield from reversed(list(nx.dag.topological_sort(self.get_dependency_graph())))


class SchemaObject(SchemaInnerNode):
    """
    A creatable SQL object: TABLE, VIEW, TRIGGER, or INDEX.
    """

    @abc.abstractmethod
    def create_query(self):
        pass

    def get_dependency_graph(self):
        dag = super().get_dependency_graph()
        dag.add_node(self)
        return dag


# Howto cross heritage with dialect ???
@subdialect.register(True)
class SchemaTableColumn(dialect.columns.QueryColumn.func, SchemaNode):
    """Class to represent table column.

    A column which is both a selectable `QueryColumn` and a leaf
    of the schema tree. Additionally, the object has several
    attributes.

    Parameters
    ----------
    name: str
            the QueryColumn name;

    sqltype: str | SQLType | None, default=None
            either a `string` indicating an SQL type (e.g., "INTEGER",
            "TEXT"), or another instance of `QueryColumn`. In the
            latter case, the column SQL type is set to the value of
            the `sqltype` attribute of the given other column. When a
            reference is given (see `references` parameter), the given
            `sqltype` is expected to be `None` (default), so it can be
            replaced by the referenced column to set the SQL type as
            explained above. In any other case, the parameter should
            be provided; otherwise an `NetworkDiskSQLError` exception
            is raised.

    encoder: str | None, default=None
            a key of the `encoderFunctions` dictionary, that allows to
            set the encoder and decoder functions for the column. When
            not provided, the default encoder for the type is taken.
            The so-determined encoder and decoder function are used to
            initialize the object as `QueryColumn`.

    primarykey: bool, default=False
            Either `False` (default), `True` or a nonempty string to
            be used as `on_conflict` for the corresponding constraint
            (e.g., "IGNORE"), with precedence over the `on_conflict`
            keyworded argument.

    references: None | QueryColumn, default=None
            Either the value `None` (default) or another instance of
            `QueryColumn` to which the instance to initialize
            references as foreign key.

    constraints: iterable, default=()
            An iterable (default is `()`) of constraint specifications
            which are either callable objects returning a
            `SchemaConstraint` when call with `self` as argument, or,
            directly, `SchemaConstraint`.

    on_delete: str | None, default=None
            What to do in case of delete, e.g; "CASCADE", "DO NOTHING"

    on_update: str | None, default=None
            What to do in case of delete, e.g; "CASCADE", "DO NOTHING"

    autoincrement: bool, default=False
            If `True`, then `primarykey` is automatically changed to `True`,
            and the column type (`sqltype` attribute) is expected to be `"INTEGER"`.

    notnull:bool, default=False
            If `True` then the column is set to be `NOT NULL`.

    unique:bool, default=False
            If `True` then the column is set to not accept duplicates values.

    onconflict:
            Default `on_conflict` for `ConflictableConstraint`s (given
            by `primarykey`, `unique`, or `notnull`) if their values
            are `True`.

    check:
            Either a condition or a callable object, which returns a
            condition when call with the column `self` as argument.
            The default value `None` is interpreted as the empty
            condition.

    Notes
    -----

    Once the encoder and decoder functions have been determined
    for the column, it is initialized as `QueryColumn` using its
    name (`name`) and the encoder key (`encoder`).

    """

    def __init__(
        self,
        dialect,
        name,
        container_name,
        index_in_container,
        sqltype=None,
        encoder=None,
        # constraints
        references=None,
        on_delete=None,
        on_update=None,
        deferrable=None,
        initially_deferred=None,
        primarykey=False,
        autoincrement=None,
        notnull=False,
        unique=False,
        on_conflict=None,
        default=None,  # default can be: a value, a Column (e.g., ValueColumn, TransformColumn, TableColumn), a Condition
        check=None,  # either None, a Condition, or a function mapping self to a Condition
        constraints=(),
    ):
        # BASIC ATTRIBUTES
        assert not on_delete or references
        self.references = references
        if references:
            assert (
                (sqltype is None)
                or (sqltype is references)
                or (sqltype == references.sqltype)
            )
            sqltype = references
        elif not sqltype and autoincrement:
            sqltype = "INTEGER"
        assert sqltype is not None
        if isinstance(sqltype, SchemaTableColumn):
            if encoder is None:
                encoder = sqltype.encoder
            sqltype = sqltype.sqltype
        else:
            if encoder is None:
                encoder = sqltype.upper()
        assert encoder is not None
        super().__init__(
            dialect,
            name,
            index_in_container,
            encoder=encoder,
            container_name=container_name,
            sqltype=sqltype,
        )
        self.set_constraints(
            constraints,
            references=references,
            on_delete=on_delete,
            on_update=on_update,
            deferrable=deferrable,
            initially_deferred=initially_deferred,
            primarykey=primarykey,
            autoincrement=autoincrement,
            unique=unique,
            notnull=notnull,
            on_conflict=on_conflict,
            default=default,
            check=check,
        )

    def set_constraints(
        self,
        constraints,
        references=None,
        on_delete=None,
        on_update=None,
        deferrable=None,
        initially_deferred=None,
        primarykey=False,
        autoincrement=None,
        unique=False,
        notnull=False,
        on_conflict=None,
        default=None,
        check=None,
    ):
        """ """
        constraints = [cons(self) if callable(cons) else cons for cons in constraints]
        if references:
            if not any(
                isinstance(c, self.dialect.constraints.ForeignkeyConstraint.func)
                for c in constraints
            ):
                constraints.append(
                    self.dialect.constraints.ForeignkeyConstraint(
                        references,
                        container=references.container_name,
                        on_delete=on_delete,
                        on_update=on_update,
                        deferrable=deferrable,
                        initially_deferred=initially_deferred,
                    )
                )
        primarykey = primarykey or autoincrement
        self.primarykey = bool(primarykey)
        if primarykey:
            if primarykey is True:
                primarykey = on_conflict
            if autoincrement is None and self.sqltype == "INTEGER":
                autoincrement = True
            if not any(
                isinstance(c, self.dialect.constraints.PrimarykeyConstraint.func)
                for c in constraints
            ):
                constraints.append(
                    self.dialect.constraints.PrimarykeyConstraint(
                        autoincrement=autoincrement, on_conflict=primarykey
                    )
                )
        if unique:
            if unique is True:
                unique = on_conflict
            if not any(
                isinstance(c, self.dialect.constraints.UniqueConstraint.func)
                for c in constraints
            ):
                constraints.append(
                    self.dialect.constraints.UniqueConstraint(on_conflict=unique)
                )
        if notnull:
            if notnull is True:
                notnull = on_conflict
            if not any(
                isinstance(c, self.dialect.constraints.NotnullConstraint.func)
                for c in constraints
            ):
                constraints.append(
                    self.dialect.constraints.NotnullConstraint(on_conflict=notnull)
                )
        if default:
            if not isinstance(default, self.dialect.columns.AbstractColumn.func):
                default = self.dialect.columns.ValueColumn(default, for_column=self)
            if not any(
                isinstance(c, self.dialect.constraints.DefaultConstraint.func)
                for c in constraints
            ):
                constraints.append(self.dialect.constraints.DefaultConstraint(default))
        if check:
            if callable(check):
                check = check(self)
            constraints.append(self.dialect.constraints.CheckConstraint(check))
        self.constraints = tuple(constraints)

    @property
    def foreignkey(self):
        return self.references is not None

    def defformat(self):
        q = " ".join(
            itertools.chain(
                (self.name, self.sqltype), (cons.qformat() for cons in self.constraints)
            )
        )
        return q.strip()

    def __getstate__(self):
        state = super().__getstate__()  # super ⟶ ViewColumn
        state.update(
            sqltype=self.sqltype,
            container_name=self.container_name,
            references=self.references,
            constraints=self.constraints,
        )
        return state


@subdialect.register(True)
class SchemaIndex(dialect.queries.CreateIndexQuery.func, SchemaObject):
    def create_query(self, ifnotexists=False):
        return self.set_ifnotexists(ifnotexists)

    def get_dependency_graph(self):
        dag = super().get_dependency_graph()
        dag.add_edge(self, self.container)
        return dag

    def drop_query(self):
        return self.dialect.queries.DropIndexQuery(self.name)


@subdialect.register(True)
class SchemaTrigger(dialect.queries.CreateTriggerQuery.func, SchemaObject):
    @functools.wraps(dialect.queries.CreateTriggerQuery)
    def __init__(self, dialect, *args, **kwargs):
        super().__init__(dialect, *args, **kwargs)

    def create_query(self, ifnotexists=False):
        return self.set_ifnotexists(ifnotexists)

    def get_dependency_graph(self):
        dag = super().get_dependency_graph()
        dag.add_edge(self, self.container)
        return dag

    def drop_query(self):
        return self.dialect.queries.DropTriggerQuery(self.name)


@subdialect.register(True)
class SchemaContainer(SchemaObject, dialect.queries.ReadQuery.func):
    """
    An intermediate abstract class to represent SQL containers,
    namely, VIEWs or TABLEs. Both accept many kinds of queries,
    including creation, selection, insertion and update. Their
    subformat is minimal: it indeed returns the container name.
    """

    @functools.wraps(dialect.queries.SelectQuery)
    def select_query(self, *args, **kwargs):
        return self.dialect.queries.SelectQuery(self, *args, **kwargs)

    @functools.wraps(dialect.queries.InsertQuery)
    def insert_query(self, *args, **kwargs):
        return self.dialect.queries.InsertQuery(self, *args, **kwargs)

    @functools.wraps(dialect.queries.ReplaceQuery)
    def replace_query(self, *args, **kwargs):
        return self.dialect.queries.ReplaceQuery(self, *args, **kwargs)

    @functools.wraps(dialect.queries.UpdateQuery)
    def update_query(self, *args, **kwargs):
        return self.dialect.queries.UpdateQuery(self, *args, **kwargs)

    @functools.wraps(dialect.queries.DeleteQuery)
    def delete_query(self, *args, **kwargs):
        return self.dialect.queries.DeleteQuery(self, *args, **kwargs)

    @functools.wraps(dialect.queries.CreateTriggerQuery)
    def create_trigger_query(self, *args, **kwargs):
        return self.dialect.queries.CreateTriggerQuery(self, *args, **kwargs)

    @ndqueries.nonscopable
    def subformat(self):
        return self.name

    def insert_values(self, *valuetuples, columns=None, replace=False, **kwargs):
        """
        Parameters
        ----------
        valuetuples:
                a tuple of either values or same-length tuples;

        columns:
                the ordered iterable of columns in which values should be
                inserted; If `None` (default), then all columns but those
                specified in `kwargs` are assumed, except when the tuple
                `valuetuples` is empty, in which case no `columns` are
                assumed;

        kwargs:
                a dict keyed by container column names, and whose values
                should be inserted in the corresponding column. The keyed
                columns should be disjoint from `columns`.

        Examples
        --------
        >>> t.insert_values( (3, 4, 5), (6, 7, 8), columns=('id', 1, t[2]), key="value" ) # doctest: +SKIP

        ⇒ inserts the rows `(3, 6, "value")`, `(4, 7, "value")`,
        and `(5, 8, "value")` in the columns `t['id']`, `t[1]`,
        `t[2]`, and `t['key']`.
        """
        if columns is None:
            if valuetuples:
                columns = [c for c in self if c.name not in kwargs]
            else:
                columns = []
        else:
            columns = [self[c] for c in columns]
        assert all(c.name not in kwargs for c in columns)
        appendcolumns = [self[k] for k in kwargs.keys()]
        appendvalues = tuple(kwargs[k.name] for k in appendcolumns)
        if valuetuples:
            valuetuples = (
                (t if isinstance(t, tuple) else (t,)) + appendvalues
                for t in valuetuples
            )
        else:
            valuetuples = (appendvalues,)
        columns.extend(appendcolumns)
        vq = self.dialect.queries.ValuesQuery(*valuetuples, for_columns=columns)
        if replace:
            return self.replace_query(vq, columns=columns)
        else:
            return self.insert_query(vq, columns=columns)

    def insert_many(self, columns=None, replace=False, **kwargs):
        if columns is None:
            values = (self.dialect.constants.Placeholder,) * len(self)
        else:
            values = (self.dialect.constants.Placeholder,) * len(columns)
        return self.insert_values(*values, columns=columns, replace=replace, **kwargs)


@subdialect.register(True)
class SchemaTable(SchemaContainer):
    """The SQL tables"""

    def __init__(self, dialect, name, defquery=None, constraints=(), temporary=False):
        super().__init__(dialect, name)
        self.children = {}
        self.constraints = tuple(constraints)
        self.defquery = defquery
        self.temporary = temporary
        self.rowid = self.SchemaChildClass(
            "rowid",
            sqltype="INTEGER",
            primarykey="REPLACE",
            unique=True,
            autoincrement=True,
            container_name=self.name,
            index_in_container=len(self.children),
        )
        if defquery:
            assert not defquery.get_with_queries()
            assert not constraints
            for c in defquery:
                self.add_column(
                    c.name, sqltype=c.sqltype, encoder=getattr(c, "encoder", None)
                )

    @property
    def external_columns(self):
        # TODO: order of columns from SQLite
        return ExternalColumns(self.children.values())

    @property
    def primarykeys(self):
        return list(filter(lambda c: c.primarykey, self.values()))

    @property
    def foreignkeys(self):
        return list(filter(lambda c: c.foreignkey, self.values()))

    @functools.wraps(
        functools.partial(
            SchemaTableColumn.__init__,
            dialect=None,
            container_name=None,
            index_in_container=None,
        )
    )
    def add_column(self, name, *args, **kwargs):
        if name in self.children:
            raise NetworkDiskSQLError(f"Conflict on table column {name}")
        newcol = self.SchemaChildClass(
            name,
            *args,
            container_name=self.name,
            index_in_container=len(self.children),
            **kwargs,
        )
        self.children[name] = newcol
        return newcol

    def add_primarykey(self, name="id", autoincrement=None, **kwargs):
        autoincrement = autoincrement or (
            autoincrement is None and "sqltype" not in kwargs
        )
        return self.add_column(
            name, primarykey=True, autoincrement=autoincrement, **kwargs
        )

    def add_constraint(self, constraint):
        self.constraints += (constraint,)

    def drop_query(self):
        return self.dialect.queries.DropTableQuery(self.name)

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.name}({', '.join(self.children)})>"

    def __getstate__(self):
        state = super().__getstate__()
        state.update(
            children=self.children,
            constraints=self.constraints,
            defquery=self.defquery,
            temporary=self.temporary,
            rowid=self.rowid,
        )
        return state

    def __hash__(self):
        state = self.__getstate__()
        state["children"] = tuple(self.children.items())
        return hash(tuple(sorted(state.items())))

    @property
    def SchemaChildClass(self):
        return self.dialect.schema.SchemaTableColumn

    @functools.wraps(dialect.queries.CreateTableQuery)
    def create_query(self, *args, ifnotexists=False, **kwargs):
        return self.dialect.queries.CreateTableQuery(
            self,
            *args,
            temporary=kwargs.get("temporary", self.temporary),
            ifnotexists=ifnotexists,
            **kwargs,
        )

    @functools.wraps(dialect.queries.CreateIndexQuery)
    def create_index_query(self, *args, **kwargs):
        return self.dialect.queries.CreateIndexQuery(self, *args, **kwargs)


@subdialect.register(True)
class SchemaView(
    SchemaContainer,
    dialect.queries.FromQueriesReadQuery.func,
    dialect.queries.FromQueryQuery.func,
):
    """Class to define views.

    Parameters
    ----------
    name: str
            Name of the container (here, a VIEW), to be created. This
            argument is passed to the `__init__` method of the class
            `SchemaContainer`.

    defquery: Query
            A query `(str, dict, tuple)` that select the rows to be
            represented by the view. This should be defined before
            creating the view (method `creation_scripts`), but can
            be let to its default `None` (namely, undefined) value
            before. In particular, if the SchemaView points an already
            created Schema VIEW, then this parameter is not required
            (although it is recommended to keep it for tractability).

    column_names:
            A partial mapping from external column specifications of the
            query `defquery` to names. If an external column of `defquery`
            has an associated name (namely, an alias), then the view
            uses this name as external column name.

    contdef:
            A list of additional keyworded arguments to be passed to
            the `__init__` method of the `SchemaContainer` class.
    """

    def __init__(self, dialect, name, defquery, column_names=()):
        super().__init__(dialect, name)
        dialect.queries.FromQueryQuery.func.__init__(self, dialect, defquery)
        if not isinstance(
            defquery,
            (
                self.dialect.queries.SelectQuery.func,
                self.dialect.queries.UnionQuery.func,
            ),
        ):
            raise NetworkDiskSQLError(
                f"Definition query of view should be a SelectQuery, got {type(defquery)}"
            )
        self.dialect.queries.FromQueryQuery.__init__(self, defquery)
        self.set_columns(column_names)

    def set_columns(self, column_names):
        # inspired from SelectQuery.set_columns (where column_names plays the role of aliases)
        aliases = dict(column_names)
        fcolumns = []
        f2bcolumns = {}
        track_values = {}
        seen = set()
        for idx, bcol in enumerate(self.internal_columns):
            alias = None
            if hasattr(bcol, "name"):
                alias = aliases.get(bcol.name, alias)
            alias = aliases.get(idx, alias)
            alias = aliases.get(bcol, alias)
            encoder = bcol.encoder
            sqltype = bcol.sqltype
            if alias is None:
                if not hasattr(bcol, "name"):
                    # TODO: what does SQLite? Postgre?
                    raise NetworkDiskSQLError(f"Cannot create view with unnamed column")
                alias = bcol.name
            if alias in seen:
                raise NetworkDiskSQLError(f"Ambiguous names for view columns {alias}")
            seen.add(alias)
            fcol = self.SchemaChildClass(
                name=alias,
                index_in_container=idx,
                container_name=self.name,
                encoder=encoder,
                sqltype=sqltype,
            )
            fcolumns.append(fcol)
            f2bcolumns[fcol] = bcol
            qbcol = self.internal_columns.origin_query[bcol]
            vbcol = qbcol.external_columns.track_values.right.get(bcol, ())
            track_values.update((vcol, fcol) for vcol in vbcol)
        self._external_columns = ExternalColumns(
            fcolumns, sources=f2bcolumns, track_values=track_values
        )

    def get_dependency_graph(self):
        dag = super().get_dependency_graph()
        for cont in self.subquery.get_schema_containers():
            dag.add_edge(self, cont)
            dag = nx.compose(dag, cont.get_dependency_graph())
        return dag

    @property
    def SchemaChildClass(self):
        return self.dialect.columns.QueryColumn

    @functools.wraps(dialect.queries.CreateViewQuery)
    def create_query(self, *args, ifnotexists=False, **kwargs):
        return self.dialect.queries.CreateViewQuery(
            self, *args, ifnotexists=ifnotexists, **kwargs
        )

    @property
    def external_columns(self):
        return self._external_columns

    def __getstate__(self):
        state = SchemaContainer.__getstate__(self)
        state.update(self.dialect.queries.FromQueriesReadQuery.func.__getstate__(self))
        state.update(_external_columns=self._external_columns)
        return state

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.name}({', '.join(c.name for c in self.external_columns)})>"

    def drop_query(self):
        return self.dialect.queries.DropViewQuery(self.name)


@subdialect.register(True)
class Schema(SchemaInnerNode, collections.abc.Mapping):
    """
    A `Mapping` from names to `SchemaObjects`, whose classes are
    give in the `SchemaChildClasses` class attribute.
    """

    def __init__(self, dialect, name=None):
        super().__init__(dialect, name)
        self.children = {}

    @property
    def SchemaChildClasses(self):
        sqlschema = self.dialect.schema
        return dict(
            table=sqlschema.SchemaTable,
            view=sqlschema.SchemaView,
            trigger=sqlschema.SchemaTrigger,
            index=sqlschema.SchemaIndex,
        )

    def get_dependency_graph(self):
        dag = nx.DiGraph()
        for obj in self.values():
            dag = nx.compose(dag, obj.get_dependency_graph())
        return dag

    def get_dependencies(self):
        yield from reversed(list(nx.dag.topological_sort(self.get_dependency_graph())))

    def create_script(self, ifnotexists=False):
        for dep in self.get_dependencies():
            yield dep.create_query(ifnotexists=ifnotexists)

    def add_table(self, name, *args, **kwargs):
        if name in self.children:
            raise NetworkDiskSQLError(f"Conflict on container {name}")
        newtbl = self.SchemaChildClasses["table"](name, *args, **kwargs)
        self.children[name] = newtbl
        return newtbl

    def add_view(self, name, *args, **kwargs):
        if name in self.children:
            raise NetworkDiskSQLError(f"Conflict on container {name}")
        newvw = self.SchemaChildClasses["view"](name, *args, **kwargs)
        self.children[name] = newvw
        return newvw

    def add_index(self, container, columns, *args, name=None, **kwargs):
        """
        Wrapper of `self.SchemaChildClasses['index']` with default
        improved default naming, based on the names of container
        and indexed columns.
        """
        if container in self:
            container = self[container]
        if not name:
            name = (
                f"index_{container.name}_{'_'.join(container[c].name for c in columns)}"
            )
            i = -1
            stri = ""
            while f"{name}{stri}" in self.children:
                i += 1
                stri = f"_{i}"
        elif name in self.children:
            raise NetworkDiskSQLError(f"Conflict on index {name}")
        newidx = self.SchemaChildClasses["index"](
            container, columns, *args, name=name, **kwargs
        )
        self.children[name] = newidx
        return newidx

    def add_trigger(self, container, when, action, *args, name=None, **kwargs):
        """
        Wrapper of `self.SchemaChildClasses['trigger']` with default
        improved default naming, based on names of the container and
        the event to capture (`when` and `action`).
        """
        if container in self:
            container = self[container]
        if not name:
            name = f"{when.lower().replace(' ', '_')}_{action.lower().replace(' ', '_')}_{container.name}"
            i = -1
            stri = ""
            while name + stri in self.children:
                i += 1
                stri = f"_{i}"
            name = name + stri
        elif name in self.children:
            raise NetworkDiskSQLError(f"Conflict on trigger {name}")
        newtrgg = self.SchemaChildClasses["trigger"](
            container, when, action, *args, name=name, **kwargs
        )
        self.children[name] = newtrgg
        return newtrgg

    def add_existing_container(self, container):
        if container.name in self:
            # if self[container.name] is not container:
            if self[container.name] != container:
                raise NetworkDiskSQLError(f"Conflict on container {container.name}")
        else:
            self.children[container.name] = container

    def __repr__(self):
        name = self.name or ""
        return f"{self.__class__.__name__}<{name}({', '.join(self.children)})>"

    def __getstate__(self):
        d = super().__getstate__()
        d["children"] = self.children
        return d

    def __getitem__(self, key):
        return self.children[key]

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        return iter(self.children)
