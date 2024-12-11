import abc, functools, threading
from networkdisk.sql.dialect import sqldialect as dialect
from networkdisk.sql import sqllogging as sqllog
from networkdisk.utils import (
    notProvidedArg,
    IgnoreFunction,
    IdentityFunction,
    DataClass,
    Attributes,
)
from networkdisk.tupledict import Permutation
from networkdisk.exception import NetworkDiskBackendError, NetworkDiskSQLError
from networkdisk.sql.dialect import sqldialect

dialect = sqldialect.provide_submodule(__name__)

sql_logger = sqllog.SQL_logger(active=True)
__all__ = ["Helper", "IterableQuery"]


@dialect.register(True)
class Helper(DataClass, abc.ABC):
    """A class to provide a common interface with the DataBase backend

    Parameters
    ----------
    dialect: Dialect
            the SQL dialect used by the BackEnd

    dbpath: str or None
            If not `None`, the DB to which to connect.

    sql_logger: bool or None or str or callable, default=False
            Whether and how to log queries or not.

    autocommit: bool, default=False
            Whether to automatically commit each queries when not within a
            transaction.

    notransaction: bool, default=False
            Whether to forbid context transaction use.

    temporary_table_count: int, default=0
            The number of temporary tables in the current session.

    db: DB-connector or None, default=None
            A DB-connector to use (use same session).  If not provided, a new
            connection is obtained from `dbpath` by the `connect` method.

    Attributes
    ----------
    dialect: Dialect
            the SQL dialect used by the BackEnd

    dbpath: str or None
            If a string, the path to the db file to which the Helper is connected.

    sql_logger: SQLLogger
            An object to log query send to the backend
    """

    __attributes__ = Attributes(
        "dialect",
        "dbpath",
        sql_logger=notProvidedArg,
        autocommit=False,
        notransaction=False,
        temporary_table_count=0,
        db=None,
    )

    def __post_init__(self):
        self.thread_id = threading.get_ident()
        if self.sql_logger is notProvidedArg:
            self.sql_logger = sqllog.SQL_logger(active=False)
        elif not self.sql_logger:
            self.sql_logger = IgnoreFunction
        elif isinstance(self.sql_logger, str):
            self.sql_logger = sqllog.SQL_logger(active=True, file=self.sql_logger)
        elif not callable(self.sql_logger):
            self.sql_logger = sql_logger
        self.transaction = self.dialect.helper.Transaction(self)

    def __repr__(self):
        return f"Helper〈dialect={self.dialect.name}, dbpath={self.dbpath} 〉"

    @abc.abstractmethod
    def connect(self):
        if not self.db:
            self.temporary_table_count = 0

    @property
    @abc.abstractmethod
    def BackendException(self):
        pass

    def __getstate__(self):
        state = super().__getstate__()
        state.pop("temporary_table_count")
        state.pop("db")
        # state['sql_logger'] = notProvidedArg #not serializable
        return state

    def __setstate__(self, state):
        state.setdefault("temporary_table_count", 0)
        state.setdefault("db", None)
        super().__setstate__(state)
        self.__post_init__()
        self.connect()

    def close(self):
        self.db.close()

    def __del__(self):
        if self.thread_id == threading.get_ident():
            self.close()

    def execute(
        self,
        query,
        args=(),
        column_map=(),
        sql_logger=notProvidedArg,
        rekey=None,
        commit=None,
    ):
        """Execute a query

        Parameters
        ----------
        query:  Query
                a Query object to execute.

        sql_logger:
                a SQL Logger object to output the resulting query executed.
                It should be a callable object for printing the query
                Setting it to `None` makes the logging to do nothing,
                namely `lambda e: None`. Default value is `notProvidedArg`
                which is replaced by the `sql_logger` attribute of `self`.

        commit: bool
                A Boolean indication whether to commit or not, after executing the
                query, if not in an explicit transaction.  If its value is `None`
                (default), then it is replaced by the `self.autocommit`.

        args:
                a mapping from ValueColumn specification to non-encoded value
                or iterable of values, to replace Placeholders in order

        column_map: mapping, default={}
                TODO

        keykey:
                TODO

        permutation:
                TODO
        """
        commit = self.autocommit if commit is None else commit
        with self.transaction(oncontext=0) as t:
            res = t.execute(
                query,
                args=args,
                column_map=column_map,
                sql_logger=sql_logger,
                rekey=rekey,
            )
        if not t.active and commit:
            t.commit(implicit=True)
        return res

    def executemany(
        self,
        query,
        I=(),
        column_map=(),
        args=(),
        sql_logger=notProvidedArg,
        rekey=None,
        commit=None,
    ):
        """Similar to execute except can be used with an iterable of arguments instead of simply one argument.

        A method to optimize bulk-insert
        """
        commit = self.autocommit if commit is None else commit
        with self.transaction(oncontext=0) as t:
            res = t.executemany(
                query,
                I=I,
                column_map=column_map,
                args=args,
                sql_logger=sql_logger,
                rekey=rekey,
            )
        if not t.active and commit:
            t.commit(implicit=True)
        return res

    def cursor(self):
        """Returns a database cursor

        The object returned should have the methods `execute`, `executemany`
        and `__iter__`.
        """
        return self.db.cursor()

    def executescript(
        self, queries, sql_logger=notProvidedArg, transaction_control=0, commit=None
    ):
        """
        Same as `execute` method, but uses `self.db.executescript` rather than
        `self.db.execute` for executing the script after having formatted it.
        This forbid the use of arguments.
        """
        commit = self.autocommit if commit is None else commit
        res = ()
        with self.transaction(oncontext=transaction_control) as t:
            for query in queries:
                res = t.execute(query, sql_logger=sql_logger)
        if not t.active and commit:
            t.commit(implicit=True)
        return res

    def generate_temporary_table_name(self, suffix=""):
        name = f"nd_{suffix}{self.temporary_table_count}"
        self.temporary_table_count += 1
        return name


@dialect.register(False)
class Transaction:
    """Transaction manager.  Every Helper should have one.

    Parameters
    ----------
    helper : Helper
            The helper for which to manage transactions.

    autocontext : bool or None, default=None
            Whether to automatically control transaction on contexts.

    Glossary
    --------
    transaction control query
            One of the "BEGIN", "COMMIT", "ROLLBACK", "SAVEPOINT", and "RELEASE
            SAVEPOINT" queries or variants, which allows transaction control.  It
            should be an explicit query, i.e., not, e.g., a commit through the
            backend connector's `commit` method.

    active query
            A query, not being a transaction control query, that has been executed
            but neither committed nor rolled back.

    explicit (active) transaction
            A sequence of active queries that was preceded by a "BEGIN" query.

    implicit (active) transaction
            A sequence of active queries that was not preceded by a "BEGIN" query.

    active savepoint
            A savepoint that has been created and not released, within an explicit
            active transaction.

    transaction segment
            A maximal sequence of active queries, not including transaction control
            queries, delimited by an explicit or implicit transaction start, or the
            creation of an active savepoint.  There always is a (possibly empty)
            transaction segment, which correspond to an implicit transaction.  When
            an explicit transaction is started (by a "BEGIN" query), we consider
            that there are two transactions segments:  a first one for the implicit
            transaction that occurs before the just-started explicit one, and one
            for the explicit transaction, although the start of such an explicit
            transaction implies a commit of the implicit transaction.

    Attributes
    ----------
    active : bool (property)
            Whether there currently is an explicit active transaction.  This is
            equivalent to having the list attribute `query_count` longer than 1.

    dialect: Dialect (property)
            The SQL dialect to use.  It is inherited from `helper`.

    helper : Helper
            The helper for which to manage transactions.

    query_count : list[int]
            Counters of active queries, by transaction segments.  The first item
            always exists and equals the number of queries performed out of the
            current running transaction — it is reset on each transaction start, so
            it might be non zero only if the list has length one.  In particular,
            if there is no active transaction, this item is the only item of the
            list.  If a transaction is active, then there is a second item which
            equals the number of active queries executed after the transaction
            start and before the first active savepoint, if any, or until now,
            otherwise.  The subsequent items indicate the numbers of active queries
            executed between consecutive active savepoints.  In particular, if no
            savepoint has been created but a transaction is active, the list has
            length exactly 2.  An active savepoint is a savepoint within the active
            transaction that has not be released.  Notice that rollbacking to a
            savepoint does not release it, that is, the savepoint remains active
            after this partial rollback.  However, this operation releases every
            active savepoint that have been created within the rolled back
            transaction segment.

    savepoints : list[str]
            The ordered list of active savepoints of the running transaction.  The
            list length always equals the length of `query_count` minus 2, unless
            there currently is no explicit transaction.  Indeed, within an explicit
            transaction, each savepoint starts a new transaction segment, and there
            are two more transaction segments:  the first one (corresponding to an
            implicit transaction out from the explicit transaction), and the second
            one (which has been started by the "BEGIN" query that initialized the
            current explicit transaction).  In absence of explicit transaction, the
            list is empty:  savepoints can exist only in explicit transactions.

    subcontexts : list[int or None]
            For each current context (which can be nested whence the list), the
            specification of the transaction segment start that occur at context
            entrance or just before.  The value `-1` indicates that the transaction
            segment that was started at context entrance is the current transaction
            beginning.  Other integer value indicate the index in `savepoints` of
            the active savepoint that has been created by the context management
            (i.e., within `__enter__` method) for the context.  Finally, the value
            `None` indicates that no transaction segment is under control for the
            context.

    mode : str or None
            The SQL transaction mode with which the active transaction has been
            started, if there is an active transaction, or with which to start the
            next transaction, otherwise.  (After ending the next transaction, the
            mode is reset to `None`.)

    oncontext : int or None or str
            Specifies how transaction is controlled when entering a context.  If
            `0` then no transaction control is performed.  If `1` then a minimal
            transaction control is performed, namely, nothing more than starting a
            transaction if none is active is performed.  If `2` then a intermediate
            transaction control is performed:  a transaction is started if none is
            active, a savepoint is created otherwise, unless no queries has been
            executed in the transaction segment.  In which case, there is indeed no
            need to create a savepoint, as rolling back to the preceding savepoint
            if any, or the transaction start, otherwise, does the rollback job.
            Finally, if `3` or more, then a full transaction control is performed,
            each context entering produces a transaction start or a savepoint
            creation, according to whether no transaction is active.  Alternatively
            the attribute may have a string value, implying level `3` behavior, but
            with a specific savepoint name given.  If left unspecified, then the
            default value is taken from the `autocontext` attribute — see below.
            The `oncontext` mode applies to the next context to enter only.  After
            use, it is set to the default `autocontext` value.

    autocontext : int
            Default value for `oncontext` attribute, when missing.

    deferred : list[int]
            The ordered list of deferred transaction segment starts.  If `-1`, the
            deferred transaction segment start is a transaction begin.  Otherwise,
            it is the savepoint creation at corresponding index in `savepoints`.

    deferrable : bool
            Whether transaction start and savepoint creations are deferred to avoid
            empty transactions or transaction segments, or not.

    NOTES
    -----
    Invariants:
            `len(query_count) == len(savepoints)+2 or (len(query_count) == 1 and len(savepoints) == 0)`
            `len(deferred) < len(savepoints)+1 < len(query_count)`

    """

    def _invariant_check(self):
        if self.active:
            assert len(self.query_count) == len(self.savepoints) + 2
            assert len(self.deferred) <= len(self.savepoints) + 1
            assert all(
                ctxt is None or -1 <= ctxt < len(self.savepoints)
                for ctxt in self.subcontexts
            )
            assert all(-1 <= dfrd < len(self.savepoints) for dfrd in self.deferred)
            assert not self.deferred or not self.query_count[-1]
        else:
            assert not self.savepoints
            assert not self.deferred
            assert len(self.query_count) == 1
            assert all(ctxt is None for ctxt in self.subcontexts)

    @property
    def dialect(self):
        return self.helper.dialect

    @property
    def active(self):
        return len(self.query_count) > 1

    def __init__(self, helper: Helper, autocontext: int = 1, deferrable: bool = True):
        self.helper = helper
        self.autocontext = autocontext
        self.subcontexts = []
        self.deferrable = deferrable
        self.chainwithnext = False
        self.chainwithprevious = False
        self.reset()

    def reset(self):
        self.mode = None
        self.deferred = []
        self.oncontext = self.autocontext
        self.savepoints = []
        self.query_count = [0]
        self._invariant_check()

    def __call__(
        self,
        mode=notProvidedArg,
        chainwithnext=None,
        oncontext=None,
        autocontext=None,
        deferrable=None,
    ):
        """
        Parameters
        ----------
        mode : notProvidedArg or None or str
                Set the mode of the next transaction.  This is possible only if no
                transaction is active.

        chainwithnext : None or bool
                Whether to chain the current transaction (or the next one, if none
                is active) with its successor one.  If `None` the current instance
                value is kept unchanged.

        oncontext : None or int or str
                Set the oncontext attribute, for controlling how the next context to
                enter should manage transaction.  If `None`, the value defaults to
                `autocontext`.  Otherwise, it is interpreted with the following
                meaning, applied to the next context:
                · `0`: no transaction control is performed;
                · `1`: a transaction is started if none is active, otherwise as `0`;
                · `2`: if a transaction is active, a savepoint is created if there
                        have been some queries executed since the last transaction segment
                        start, otherwise as `1`;
                · `3` (or more): a transaction start is always ensured, which might
                        be a transaction beginning if no transaction is already active, or
                        a savepoint creation otherwise…
                Alternatively, the parameter may take a string value, interpreted as
                level `3`, but with the created savepoint name given explicitly.

        autocontext : None or int
                Set the default `oncontext` value, which is will be applied for every
                contexts following the next one, unless specified differently.  If
                `None`, then the current default value is unchanged.  Otherwise, an
                integer with the meaning as described when documenting `oncontext`
                above is expected.

        deferrable : None or bool
                Whether transaction start should be deferred or not.  If deferred,
                their corresponding TCL query is executed only if needed, namely,
                only if a query is executed in the transaction segment or if an inner
                transaction segment.  If `None` the instance value is kept unchanged.
        """
        self._invariant_check()
        if mode is not notProvidedArg:
            if self.active:
                raise NetworkDiskSQLError(
                    f"Cannot change mode of active transaction to {mode}"
                )
            self.mode = mode
        if chainwithnext is not None:
            self.chainwithnext = chainwithnext
        if autocontext is not None:
            self.autocontext = autocontext
        if oncontext is not None:
            self.oncontext = oncontext
        else:
            self.oncontext = self.autocontext
        if deferrable is not None:
            self.deferrable = deferrable
        self._invariant_check()
        return self

    def __enter__(self):
        self._invariant_check()
        prv_ctxt = None  # get previous transaction segment start for context if any, None otherwise
        for k in self.subcontexts:
            if k is not None:
                prv_ctxt = k
        if isinstance(self.oncontext, str):
            ctxt = len(self.savepoints)
            self.savepoint(
                ctxt.format(index=len(self.subcontexts)), deferred=self.deferrable
            )
        elif self.oncontext <= 0:
            ctxt = None
        elif not self.active:
            self.begin(mode=self.mode, implicit=True, deferred=self.deferrable)
            ctxt = -1
        elif self.oncontext < 2:
            ctxt = None
        elif (
            self.oncontext == 2
            and prv_ctxt == len(self.savepoints) - 1
            and not self.query_count[-1]
        ):
            ctxt = prv_ctxt
        else:
            ctxt = len(self.savepoints)
            self.savepoint(
                f"_context_{len(self.subcontexts)}", deferred=self.deferrable
            )
        self.subcontexts.append(ctxt)
        self.oncontext = self.autocontext
        self._invariant_check()
        return self

    def __exit__(self, exc, arg, tb):
        if not isinstance(exc, AssertionError):
            self._invariant_check()
        ctxt = self.subcontexts.pop()
        if ctxt is None:
            return
        if exc:
            keep = [i for i, c in enumerate(self.subcontexts) if c == ctxt]
            if ctxt == -1:
                self.rollback(implicit=True)
                if keep:
                    # restart the transaction segment, deferred, for outer-contexts…
                    self.begin(mode=self.mode, deferred=True, implicit=True)
                    for i in keep:
                        self.subcontexts[i] = ctxt
            else:
                self._rollback_to_savepoint(ctxt, release=not keep)
        else:
            if ctxt in self.subcontexts:
                pass
            elif ctxt == -1:
                try:
                    self.commit(implicit=True)
                except Exception as e:
                    self.rollback(implicit=True)
                    raise
            else:
                self._release_savepoint(ctxt)
        self._invariant_check()

    def apply_deferred(self):
        while self.deferred:
            trans = self.deferred.pop(0)
            if trans == -1:
                q = self.dialect.queries.BeginTransactionQuery(mode=self.mode)
            else:
                sp = self.savepoints[trans]
                q = self.dialect.queries.SavepointQuery(sp)
            self._execute(q)
        self._invariant_check()

    def start_segment(self, name="savepoint", *, implicit=False, deferred=None):
        # TODO: drop this method?
        deferred = self.deferred if deferred is None else deferred
        if not self.active:
            self.begin(mode=self.mode, implicit=implicit, deferred=deferred)
        else:
            self.savepoint(name, deferred=deferred)

    def begin(self, mode=notProvidedArg, *, implicit=True, deferred=False):
        self._invariant_check()
        mode = self.mode if mode is notProvidedArg else mode
        if self.active:
            if self.chainwithprevious:
                self.chainwithprevious = False
                return
            raise NetworkDiskSQLError(
                "Cannot start an explicit transaction within an already-existing explicit transaction"
            )
        if self.query_count[0]:
            if not implicit:
                raise NetworkDiskSQLError(
                    "Cannot start an explicit transaction since an implicit one is running"
                )
            self.query_count[0] = 0
        self.helper.db.commit()
        self.mode = mode
        self.query_count.append(0)
        if deferred:
            self.deferred.append(-1)
        else:
            q = self.dialect.queries.BeginTransactionQuery(mode=mode)
            self.apply_deferred()
            self._execute(q)
        self._invariant_check()

    def commit(self, *, implicit=False):
        self._invariant_check()
        if not self.active:
            if not implicit:
                self.reset()
                raise NetworkDiskSQLError("No transaction to commit")
            self.helper.db.commit()
        elif self.chainwithnext:
            self.chainwithnext = False
            self.chainwithprevious = True
        elif not self.deferred or self.deferred[0] != -1:
            q = self.dialect.queries.CommitTransactionQuery()
            self._execute(q)
            self.helper.db.commit()
        self.subcontexts = [None] * len(self.subcontexts)
        self.reset()
        self._invariant_check()

    def _rollback_to_savepoint(self, idx, release=False):
        self._invariant_check()
        name = self.savepoints[idx]
        for i in range(len(self.savepoints) - 1, idx, -1):
            if self.savepoints[i] == name:
                self._rollback_to_unique_savepoint(idx, release=True)
        self._rollback_to_unique_savepoint(idx, release=release)
        self._invariant_check()

    def _rollback_to_unique_savepoint(self, idx, release=False):
        # assumed: no savepoints in self.savepoints[idx+1:] have name self.savepoints[idx]
        self._invariant_check()
        name = self.savepoints[idx]
        # several savepoints might be implicitly released
        self.savepoints = self.savepoints[: idx + 1]
        self.query_count = self.query_count[: idx + 2] + [0]
        for i, ctxt in enumerate(self.subcontexts):
            if ctxt is not None and ctxt > idx:
                self.subcontexts[i] = None
        if idx in self.deferred:
            n = len(self.deferred)
            j = self.deferred.index(idx)
            self.deferred = self.deferred[: -(n - j) - (not release)]
            if release:
                self.savepoints.pop()
                self.query_count.pop()
        else:
            q = self.dialect.queries.RollbackTransactionQuery(to_savepoint=name)
            self._execute(q)
            if release:
                self._release_unique_savepoint(idx)
        self._invariant_check()

    def rollback(self, to_savepoint=None, release=False, *, implicit=False):
        self._invariant_check()
        if to_savepoint is True:
            to_savepoint = len(self.savepoints) - 1 if self.savepoints else None
        if not self.active:
            if not implicit:
                self.reset()
                raise NetworkDiskSQLError("No transaction to rollback")
            self.query_count[0] = 0
            self.helper.db.rollback()
        elif to_savepoint is not None:
            if isinstance(to_savepoint, int):
                idx = to_savepoint
            elif to_savepoint not in self.savepoints:
                raise NetworkDiskSQLError("No savepoint {to_savepoint} is known")
            else:
                revsavepoints = list(reversed(self.savepoints))
                idx = len(revsavepoints) - 1 - revsavepoints.index(to_savepoint)
            self._rollback_to_unique_savepoint(idx, release=release)
        else:
            if not self.deferred or self.deferred[0] != -1:
                q = self.dialect.queries.RollbackTransactionQuery()
                self._execute(q)
                self.helper.db.rollback()
            self.subcontexts = [None] * len(self.subcontexts)
            self.reset()
        self._invariant_check()

    def get_new_indexed_savepoint(self, name="savepoint"):
        savepoints = set(self.savepoints)
        i = 0
        while f"{name}{i}" in savepoints:
            i += 1
        name = f"{name}{i}"
        return name

    def savepoint(self, name, autoindex=False, *, deferred=False):
        """
        +	name
                a string, being a savepoint name or basename (c.f. index).
        +	index
                a Boolean. If `True`, then the smallest integer index `i`
                such that `f"{name}{i}"` is not an existing savepoint name
                is append to `name`. This happen even if `name` is not an
                existing savepoint name (whence, the first indexed
                savepoint name of root `name` is `f"{name}0"`). If `False`
                {name} is used unchanged, whence an error is raised if the
                name is already used by some existing savepoint. In every
                case, the method returns the created savepoint name, so
                that the indexed version can be saved by the caller.
        """
        self._invariant_check()
        if not self.active:
            raise NetworkDiskSQLError(
                f"No transaction within which to create savepoint {name}{'N' if index else ''}"
            )
        if autoindex:
            name = self.get_new_indexed_savepoint(name=name)
        self.savepoints.append(name)
        self.query_count.append(0)
        q = self.dialect.queries.SavepointQuery(name)
        if deferred:
            self.deferred.append(len(self.savepoints) - 1)
        else:
            self.apply_deferred()
            self._execute(q)
        return name
        self._invariant_check()

    def _release_unique_savepoint(self, idx):
        """Release active savepoint specified by index, assuming its name is not shadowed."""
        self._invariant_check()
        name = self.savepoints[idx]
        # assumed: idx is the rightmost occurrence index of name in self.savepoints
        self.savepoints = self.savepoints[:idx]
        for i, ctxt in enumerate(self.subcontexts):
            if ctxt is None or ctxt < 0:
                continue
            elif ctxt >= idx:
                self.subcontexts[i] = None
        if idx in self.deferred:
            n = len(self.deferred)
            i = self.deferred.index(idx)
            self.query_count = self.query_count[: -(n - i)]
            self.deferred = self.deferred[: -(n - i)]
        else:
            qbefore = self.query_count[: idx + 1]
            qafter = [sum(self.query_count[idx + 1 :])]
            self.query_count = qbefore + qafter
            self.deferred = []
            q = self.dialect.queries.ReleaseSavepointQuery(name)
            self._execute(q)
        self._invariant_check()

    def _release_savepoint(self, idx):
        """Release active savepoint specified by index.

        If the name of the savepoint specified by `idx` is shared by other
        active after-created savepoints, then they are released as well.

        Parameters
        ----------
        idx : int
                The index of the active savepoint to release in `self.savepoints`.
        """
        self._invariant_check()
        name = self.savepoints[idx]
        n = len(self.savepoints)
        for i in range(n - 1, idx - 1, -1):
            if self.savepoints[i] == name:
                self._release_unique_savepoint(i)
        self._invariant_check()

    def release_savepoint(self, name=True):
        """Release active savepoint by name.

        Notice that several active savepoints may have same name, the newest
        shadowing the oldest.  Thus, only the newest active savepoint of name
        `name` is released.

        Parameters
        ----------
        name : str or bool
                The name of the active savepoint to release.  If `True`, then the
                newest active savepoint name is taken.  If `False`, no savepoint is
                released (thus nothing is done).

        Raises
        ------
        NetworkDiskSQLError
                If the specified savepoint does not exists.  This includes cases in
                which `name` is `True` but there is no active savepoint, or in which
                there is no active transaction at all.
        """
        self._invariant_check()
        if name is True:
            if not self.savepoints:
                raise NetworkDiskSQLError("No savepoint in current transaction")
            idx = len(self.savepoints) - 1
        elif name is False:
            return
        elif not self.active:
            raise NetworkDiskSQLError(
                f"Cannot release savepoint {name} in ended transaction"
            )
        elif name not in self.savepoints:
            raise NetworkDiskSQLError(
                f"No savepoint named {name} known in the current transaction"
            )
        else:
            revsavepoints = list(reversed(self.savepoints))
            idx = len(revsavepoints) - 1 - revsavepoints.index(name)
        self._release_unique_savepoint(idx)
        self._invariant_check()

    def execute(
        self, query, args=(), column_map=(), sql_logger=notProvidedArg, rekey=None
    ):
        self._invariant_check()
        self.apply_deferred()
        self.query_count[-1] += 1
        res = self._execute(
            query, args=args, column_map=column_map, sql_logger=sql_logger, rekey=rekey
        )
        self._invariant_check()
        return res

    def _execute(
        self, query, args=(), column_map=(), sql_logger=notProvidedArg, rekey=None
    ):
        self._invariant_check()
        sql_logger = (
            self.helper.sql_logger if sql_logger is notProvidedArg else sql_logger
        )
        permut = query.get_args_permutation(column_map)
        args = query.encode_args(permut, args, reorder_post_encoding=rekey)
        q = query.qformat()
        if sql_logger is not None:
            sql_logger(query, args=args)
        cursor = self.helper.cursor()
        cursor.execute(q, args)
        res = iter(cursor)
        decode = getattr(query, "decode", None)
        self._invariant_check()
        if decode:
            return map(decode, res)
        return res

    def executemany(
        self, query, I=(), column_map=(), args=(), sql_logger=notProvidedArg, rekey=None
    ):
        self._invariant_check()
        self.apply_deferred()
        self.query_count[-1] += 1
        res = self._executemany(
            query,
            I=I,
            column_map=column_map,
            args=args,
            sql_logger=sql_logger,
            rekey=rekey,
        )
        self._invariant_check()
        return res

    def _executemany(
        self, query, I=(), column_map=(), args=(), sql_logger=notProvidedArg, rekey=None
    ):
        self._invariant_check()
        sql_logger = (
            self.helper.sql_logger if sql_logger is notProvidedArg else sql_logger
        )
        permut = query.get_args_permutation(column_map)
        if args:
            I = map(lambda t: args + t, I)
        I = query.encode_many_args(permut, I, reorder_post_encoding=rekey)
        q = query.qformat()
        __call_many__ = getattr(sql_logger, "__call_many__", None)
        if __call_many__:
            # __call_many__ is a generator that yields elements from I in addition to print them within formatted query
            I = __call_many__(query, I=I)
        elif sql_logger is not None:
            sql_logger(query, args="…many…")
        cursor = self.helper.cursor()
        cursor.executemany(q, I)
        res = iter(cursor)
        decode = getattr(query, "decode", None)
        self._invariant_check()
        if decode:
            return map(decode, res)
        return res


@dialect.register(False)
class IterableQuery:
    """A object for considering the results of a query as a reiterable.

    Parameters
    ----------
    helper : Helper
            The helper that describes the DB to connect.

    query : SelectQuery
            The query that produces the results of the iterable.

    index : int or None, default=None
            Whether to project the result on a single column, specified by the
            integer `index`, or not (if `None`, the default).

    apply:	iterable function or None, default=None
            Whether to modify the results of a query applying a function on Python side.

    Notes
    -----
    The length of the iterable is available through the method `len`.  Since
    it is not a free operation, we do not override the dunder `__len__` that
    is automatically called by some constructors, such as `list`.

    `apply` and `index` parameters are carried away when using composition of iterable
    query, by taking the one at left.
    """

    __repr_limit = 4

    def __init__(self, helper, query, index=None, apply=None):
        self.helper = helper
        self.query = query
        self.index = index
        self.__itr = None
        self._apply = apply

    @property
    def dialect(self):
        return self.helper.dialect

    def len(self):
        # defining `len` instead of `__len__` to avoid automatic call (e.g., by `list` builder) to this nonfree computation
        return next(iter(self.helper.execute(self.query.count())))[0]

    def __repr__(self):
        if hasattr(self.query, "set_limit"):
            res = self.query.set_limit(self.__repr_limit)
        else:
            res = self.query.select_query(limit=self.__repr_limit)
        res = self.helper.execute(res)
        if self.index is not None:
            res = map(lambda t: t[self.index], res)
        res = list(res)
        if len(res) >= self.__repr_limit:
            return f"{type(self).__name__}<{', '.join(map(str, res[:self.__repr_limit]))},…>"
        return f"{type(self).__name__}<{', '.join(map(str, res))}>"

    def __str__(self):
        return f"{type(self).__name__}<{self.query.qformat()}>"

    def __iter__(self):
        res = self.helper.execute(self.query)
        if self.index is not None:
            res = map(lambda t: t[self.index], res)
        if self._apply is not None:
            res = self._apply(res)
        return res

    def intersection(self, *others):
        iq = self.dialect.queries.IntersectQuery(
            self.query, *(getattr(o, "query", o) for o in others)
        )
        return type(self)(self.helper, iq, self.index, self._apply)

    def union(self, *others):
        iq = self.dialect.queries.UnionQuery(
            self.query, *(getattr(o, "query", o) for o in others)
        )
        return type(self)(self.helper, iq, self.index, self._apply)

    def difference(self, other):
        iq = self.dialect.queries.ExceptQuery(
            self.query, getattr(other, "query", other)
        )
        return type(self)(self.helper, iq, self.index, self._apply)

    def unionall(self, *others):
        iq = self.dialect.queries.UnionAllQuery(
            self.query, *(getattr(o, "query", o) for o in others)
        )
        return type(self)(self.helper, iq, self.index, self._apply)

    def project(self, index=None, project_query=True):
        if self.index is not None and self.index != index:
            raise ValueError(
                f"Cannot project on different index already projected iterable query, {self.index}≠{index}"
            )
        if project_query:
            extcols = self.query.external_columns
            col = extcols.sources[extcols.unambiguous_get(index)]
            return type(self)(self.helper, self.query.set_columns(col), index=0)
        return type(self)(self.helper, self.query, index=index, apply=self._apply)

    def limit(self, limit, offset=None):
        return type(self)(
            self.helper,
            self.query.set_limit(limit, offset),
            index=self.index,
            apply=self._apply,
        )

    def apply(self, func):
        if self._apply is not None:
            orig_func = func

            def func(res):
                res = self._apply(res)
                res = orig_func(res)
                return res

        return type(self)(self.helper, self.query, self.index, func)

    def map(self, f):
        def func(res):
            return map(f, res)

        return self.apply(func)
