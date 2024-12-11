import itertools, functools


class Permutation(tuple):
    @classmethod
    def strip(cls, t):
        """
        Strip a tuples by dropping off rightmost consecutive
        coordinates whose index equals their value. The inverse of
        this operation is `padd` which requires an argument `size`.
        """
        n = len(t)
        if not n:
            return t
        for i, j in enumerate(reversed(t)):
            if (n - 1 - i) != j:
                if not i:
                    return t
                return cls(t[slice(0, n - i)])
        return cls.identity()

    @classmethod
    def padd(cls, t, size):
        """
        Append the minimal amount of coordinates to tuple `t` so its
        size is a least `size`. Each appended coordinate has index
        equal to value. This method is thus the inverse of `strip`.
        """
        return super().__add__(t, tuple(range(len(t), size)))

    @staticmethod
    def __new__(cls, *args, **kwargs):
        t = cls.strip(tuple(*args, **kwargs))
        self = super().__new__(cls, t)
        if not self.check():
            raise ValueError(
                f"Invalid permutation arguments: {args}{', ' if args and kwargs else ''}{kwargs}"
            )
        return self

    @classmethod
    def identity(cls):
        return cls()

    @classmethod
    def swap(cls, i, j):
        i, j = sorted((i, j))
        return cls(itertools.chain(range(i), (j,), range(i + 1, j), (i,)))

    @classmethod
    def rotation(cls, size, repeat=1, rightward=False):
        return cls.identity().rotate(size=size, repeat=repeat, rightward=rightward)

    @classmethod
    def reversion(cls, size):
        return cls.identity().reverse(size)

    @classmethod
    def concat(cls, *permutations):
        redf = lambda p, t: p + cls.shift(t, len(p))
        return cls(functools.reduce(redf, permutations, ()))

    def __getitem__(self, key):
        res = super().__getitem__(key)
        if isinstance(key, slice):
            res = type(self)(res)
        return res

    def __call__(self, t):
        if hasattr(t, "__getitem__"):
            self = self[: len(t)]
            return type(t)(tuple(t[self(i)] for i in range(len(t))))
        return self[t] if t < len(self) else t

    def __repr__(self):
        return f"{super().__repr__()}ₚ"

    def __hash__(self):
        return hash((self.__class__.__name__, super().__hash__()))

    def __add__(self, other):
        try:
            return type(self)(other(tuple(self) + tuple(range(len(self), len(other)))))
        except TypeError as e:
            raise TypeError(
                f"Can only sum permutations, not {type(other)} to permutation"
            ) from e

    def __neg__(self):
        return type(self)(self.index(i) for i in range(len(self)))

    def __sub__(self, other):
        return self + (-other)

    def rotate(self, size=None, repeat=1, rightward=False):
        """
        Returns the effect of `repeat` left (resp. right) rotations
        on permutation `self` where `repeat` is a positive (resp.
        negative) integer, with default value `1`. If the special
        keyword `rightward` is given with value `True`, then the
        sign of `repeat` is inversed, so that a positive value
        produces a right rotation and vice versa. An additional
        argument `size` allows to specify the size of the rotation.
        That is, when `size` is smaller than `len(self)` then the
        rotation is applied on the `size` first coordinates, while
        others are kept unchanged. If, otherwise, `size` is greater
        than (or equal to) `len(self)` then the permutation is
        completed assuming identity on missing coordinates, before
        applying the rotation. In particular, `size=len(self)` has
        the same effect as the default value `None`. A negative
        `size` '-n' correspond to the size `len(self)-n`.

        Please observe that `len(self)` **successive** applications
        of the method without specifying `size` results in the
        identity (empty) permutation, while the single application
        of the method with `repeat` value equal to `len(self)`
        returns (a copy of) `self`.

        Edge cases:
        +	size = 0 ⇒ always returns `self`
        +	repeat = 0 ⇒ returns (a copy of) `self`
        +	repeat = len(self) ⇒ returns (a copy of) `self`
        +	`len(self)` successive calls without argument ⇒ always returns the identity
        """
        if size is None:
            size = len(self)
        lt = self.padd(tuple(self)[:size], size)
        rt = tuple(self)[size:]
        if rightward:
            repeat *= -1
        return type(self)(lt[repeat:] + lt[:repeat] + rt)

    def reverse(self, size=None):
        """
        Apply a reverse permutation of size `size` if specified or
        of size `len(self)` otherwise.
        """
        if size is None:
            size = len(self)
        lt = self.padd(tuple(self)[:size], size)
        rt = tuple(self)[size:]
        return type(self)(tuple(reversed(lt)) + rt)

    def truncate(self, up_to):
        return self[:up_to]

    def shift(self, n):
        shifted = map(lambda c: c + n, self)
        if n < 0:  # then truncate
            shifted = tuple(shifted)[n - 1 :]
        return type(self)(shifted)

    def check(self):
        return set(self) == set(range(len(self)))

    def support(self):
        return tuple(i for i, j in enumerate(self) if i == j)

    def cosupport(self):
        return tuple(i for i, j in enumerate(self) if i != j)
