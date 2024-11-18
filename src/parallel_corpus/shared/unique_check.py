"""UniqueCheck."""

from typing import Generic, TypeVar

S = TypeVar("S")


class UniqueCheck(Generic[S]):
    """Check if values are unique.

    >>> u = UniqueCheck()
    >>> u(1)
    True
    >>> u(1)
    False
    >>> u(1)
    False
    >>> u(2)
    True
    >>> u(3)
    True
    >>> u(2)
    False
    """

    def __init__(self) -> None:  # noqa: D107
        self.c: Count[S] = Count()

    def __call__(self, s: S) -> bool:  # noqa: D102
        return self.c.inc(s) == 1


class Count(Generic[S]):
    """Counter that can be increased and queried.

    >>> u = Count()
    >>> u.inc(1)
    1
    >>> u.inc(1)
    2
    >>> u.inc(1)
    3
    >>> u.inc(2)
    1
    >>> u.inc(3)
    1
    >>> u.inc(2)
    2
    >>> u.get(1)
    3
    >>> u.get(2)
    2
    >>> u.get(3)
    1
    """

    def __init__(self) -> None:  # noqa: D107
        self.m: dict[S, int] = {}

    def get(self, s: S) -> int:  # noqa: D102
        return self.m.get(s) or 0

    def inc(self, s: S) -> int:  # noqa: D102
        self.m[s] = self.get(s) + 1
        return self.get(s)
