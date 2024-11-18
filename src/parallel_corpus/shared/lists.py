"""list."""

import copy
from typing import TypeVar

A = TypeVar("A")


def rearrange(xs: list[A], begin: int, end: int, dest: int) -> list[A]:
    """Move a slice of the items and puts back them at some destination.

    rearrange([0, 1, 2, 3], 1, 2, 0) // => [1, 2, 0, 3]
    rearrange([0, 1, 2, 3], 1, 2, 3) // => [0, 3, 1, 2]

    rearrange([0, 1, 2, 3], 1, 2, 1) // => [0, 1, 2, 3]
    rearrange([0, 1, 2, 3], 1, 2, 2) // => [0, 1, 2, 3]
    """
    a, mid, z = split_at_3(xs, begin, end + 1)
    w = end - begin
    if dest > begin:
        dest -= w
    pre, post = split_at(a + z, dest)
    return pre + mid + post


def splice(xs: list[A], start: int, count: int, *insert) -> tuple[list[A], list[A]]:  # noqa: ANN002, D103
    ys = copy.deepcopy(xs)
    zs = ys[start : (start + count)]
    ys[start : (start + count)] = insert
    return ys, zs


def split_at_3(xs: list[A], start: int, end: int) -> tuple[list[A], list[A], list[A]]:
    """Split an array into three pieces.

    splitAt3('0123456'.split(''), 2, 4).map(xs => xs.join('')) // => ['01', '23', '456']
    splitAt3('0123456'.split(''), 2, 2).map(xs => xs.join('')) // => ['01', '', '23456']
    splitAt3('0123456'.split(''), 2, 9).map(xs => xs.join('')) // => ['01', '23456', '']
    splitAt3('0123456'.split(''), 0, 2).map(xs => xs.join('')) // => ['', '01', '23456']
    """
    ab, c = split_at(xs, end)
    a, b = split_at(ab, start)
    return a, b, c


def split_at(xs: list[A], index: int) -> tuple[list[A], list[A]]:  # noqa: D103
    return xs[:index], xs[index:]
