"""UnionFind."""

import abc
import functools
import json
from dataclasses import dataclass
from typing import Callable, Generic, Optional, TypeVar

from typing_extensions import Self

A = TypeVar("A")


class UnionFindOperations(abc.ABC, Generic[A]):
    """Union-find data structure operations."""

    @abc.abstractmethod
    def find(self, x: A) -> A:
        """Answers what group `x` belongs to."""

    @abc.abstractmethod
    def union(self, x: A, y: A) -> A:
        """Make these belong to the same group."""

    @abc.abstractmethod
    def unions(self, xs: list[A]) -> None:
        """Make these belong to the same group."""


class UnionFind(UnionFindOperations[int]):  # noqa: D101
    def __init__(self, *, rev: Optional[list[Optional[int]]] = None) -> None:  # noqa: D107
        self._rev: list[Optional[int]] = rev or []

    def find(self, x: int) -> int:  # noqa: D102
        while x >= len(self._rev):
            self._rev.append(None)  # type: ignore [arg-type]
        if self._rev[x] is None:
            self._rev[x] = x
        elif self._rev[x] != x:
            self._rev[x] = self.find(self._rev[x])  # type: ignore [arg-type]
        return self._rev[x]  # type: ignore [return-value]

    def union(self, x: int, y: int) -> int:  # noqa: D102
        find_x = self.find(x)
        find_y = self.find(y)
        if find_x != find_y:
            self._rev[find_y] = find_x
        return find_x

    def unions(self, xs: list[int]) -> None:  # noqa: D102
        functools.reduce(self.union, xs, xs[0])


@dataclass
class Renumber(Generic[A]):  # noqa: D101
    bw: dict[str, int]
    fw: dict[int, A]
    i = 0
    serialize: Callable[[A], str]

    def num(self, a: A) -> int:  # noqa: D102
        s = self.serialize(a)
        if s not in self.bw:
            self.fw[self.i] = a
            self.bw[s] = self.i
            self.i += 1
        return self.bw[s]

    def un(self, n: int) -> Optional[A]:  # noqa: D102
        return self.fw.get(n)

    @classmethod
    def init(cls, serialize: Callable[[A], str] = json.dumps) -> Self:  # noqa: D102
        return cls(bw={}, fw={}, serialize=serialize)


def renumber(
    serialize: Callable[[A], str] = json.dumps,
) -> tuple[Callable[[int], Optional[A]], Callable[[A], int]]:
    """Assign unique numbers to each distinct element.

    const {un, num} = Renumber()
    num('foo') // => 0
    num('bar') // => 1
    num('foo') // => 0
    un(0) // => 'foo'
    un(1) // => 'bar'
    un(2) // => undefined

    const {un, num} = Renumber<string>(a => a.toLowerCase())
    num('foo') // => 0
    num('FOO') // => 0
    un(0) // => 'foo'
    """
    renum: Renumber[A] = Renumber(bw={}, fw={}, serialize=serialize)

    return renum.un, renum.num


@dataclass
class PolyUnionFind(Generic[A]):  # noqa: D101
    _uf: UnionFind
    _renum: Renumber[A]

    def repr(self, x: A) -> int:  # noqa: D102
        return self._uf.find(self._renum.num(x))

    def find(self, x: A) -> Optional[A]:  # noqa: D102
        return self._renum.un(self._uf.find(self._renum.num(x)))

    def union(self, x: A, y: A) -> Optional[A]:  # noqa: D102
        return self._renum.un(self._uf.union(self._renum.num(x), self._renum.num(y)))

    def unions(self, xs: list[A]) -> None:  # noqa: D102
        num_xs_0 = self._renum.num(xs[0])
        for x in xs[1:]:
            self._uf.union(num_xs_0, self._renum.num(x))


def poly_union_find(serialize: Callable[[str], str]) -> PolyUnionFind[str]:  # noqa: D103
    renum = Renumber.init(serialize)
    uf = UnionFind()
    return PolyUnionFind(_uf=uf, _renum=renum)
