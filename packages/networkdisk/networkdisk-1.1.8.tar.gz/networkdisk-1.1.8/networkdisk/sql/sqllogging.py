import re, sys, collections, functools
from termcolor import colored
import networkdisk.utils as ndutls


class SQL_logger:
    buffer = collections.deque(maxlen=5)
    comment_prefix = "--- "
    _max_length = 84

    def __init__(
        self, active=True, end="\n", flush=True, file=None, color=None, prefix=None
    ):
        self.active = active
        self.oncontext_active = None
        self.contexts = []
        self.flush = flush
        self.end = end
        self.file = file
        self.querycount = 0
        self.color = file is None if color is None else color
        self.prefix = ("<SQL>:" if file is None else "") if prefix is None else prefix

    @staticmethod
    def bulk_print(k):
        return (k < 10) or (k % 100 == 0)

    def format_args(self, args, color=None, prepadd="\t\t\t"):
        color = self.color if color is None else color
        s = f"{self.prefix} {self.comment_prefix}{prepadd}↖ {', '.join(map(str, args))}"
        if len(s) > self._max_length:
            s = s[: self._max_length - 2] + " …"
        if color:
            s = colored(s, "blue")
        return s

    def format_range_args(
        self,
        first,
        current,
        previous_length,
        color=None,
        prepadd="\t\t\t",
        postpadd=" ",
    ):
        color = self.color if color is None else color
        first = ",".join(map(str, first))
        current = ",".join(map(str, current))
        new_length = len(current)
        if previous_length:
            postpadd = postpadd * (previous_length - new_length)
        else:
            postpadd = postpadd
        s = f"{self.prefix} {self.comment_prefix}{prepadd}↖ {first} … {current}{postpadd}"
        if len(s) > self._max_length:
            s = s[: self._max_length - 1] + "…"
        if color:
            s = colored(s, "blue")
        return s, new_length

    def format_query(self, q, prefix=None, color=None):
        # TODO: use pygments!
        color = self.color if color is None else color
        prefix = self.prefix if prefix is None else prefix
        s = getattr(q, "pretty_qformat", q.qformat)()
        s = re.sub("\s+", " ", s)
        if color:
            prefix = colored(prefix, "yellow")
            s = re.sub(
                r"([0-9]+)([^}]*)({|$)", colored(r"\1", "red") + r"\2" + r"\3", s
            )
            s = re.sub(r"([A-Z]+)", colored(r"\1", attrs=["bold"]), s)
            s = re.sub(r"(\.)", colored(r"\1", "blue"), s)
        s = (
            prefix + " " + re.sub("\s+", " ", s.strip())
        )  # does not clean all white spaces because of colors…
        return s

    def __call__(self, q, args=None, end=None, file=None):
        self.querycount += 1
        if q in (True, False) and {args, end, file} == {None}:
            self.oncontext_active = q
            return self
        file = self.file if file is None else file
        end = self.end if end is None else end
        self.buffer.append(q)
        if not hasattr(q, "qformat"):
            if self.active:
                with ndutls.tools.OutFile(file) as file:
                    print(
                        f"{self.comment_prefix}{q}{f' -- {args}' if args else ''}",
                        end=end,
                        file=file,
                        flush=self.flush,
                    )
            return
        args = args or q.get_args()
        if not self.active:
            return
        if args:
            fargs = self.format_args(args)
            fargs = "\n" + fargs
        else:
            fargs = ""
        q = f"{self.format_query(q)}{fargs}"
        with ndutls.tools.OutFile(file) as file:
            print(q, end=end, file=file, flush=self.flush)

    def call_iter(self, q, I=(), end=None, file=None, **kwargs):
        if not hasattr(q, "qformat"):
            raise TypeError(f"Query expected, got {type(q)}")
        self.buffer.append(q)
        if not self.active:
            return
        file = self.file if file is None else file
        end = self.end if end is None else end
        with ndutls.tools.OutFile(file) as file:
            print(self.format_query(q), file=file, flush=self.flush)
            rangeprt = None
            lastlen = 0
            for k, current in enumerate(I):
                if not k:
                    first = current
                if self.bulk_print(k):
                    rangeprt, lastlen = self.format_range_args(first, current, lastlen)
                    print(rangeprt, file=file, end="\r", flush=True)
                yield current
            if rangeprt is not None:
                rangeprt, _ = self.format_range_args(first, current, lastlen)
                print(rangeprt, file=file, flush=self.flush)

    def nocall_iter(self, q, I=(), end=None, file=None, **kwargs):
        return iter(I)

    @property
    def __call_many__(self):
        self.querycount += 1
        if self.active:
            return self.call_iter
        return self.nocall_iter

    def __enter__(self):
        self.contexts.append(self.active)
        self.active = self.oncontext_active
        return self

    def __exit__(self, exc, args, tb):
        self.active = self.contexts.pop()


qpretty_breaks = {
    "LEFT JOIN": "\nLEFT JOIN",
    "FROM": "\nFROM",
    "(": "(\n",
    ")": "\n)",
    "GROUP BY": "\nGROUP BY",
    "LIMIT": "\nLIMIT",
}


def qpretty(q, tab=0):
    if hasattr(q, "qformat"):
        q = q.qformat()
    for l, r in qpretty_breaks.items():
        q = q.replace(l, r)
    for line in q.split("\n"):
        if ")" in line:
            tab -= 1
        print("\t" * tab, line, sep="")
        if "(" in line:
            tab += 1
