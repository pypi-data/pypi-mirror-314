# ------------------------------------------------------------------------------
# This file license under the BSD-3 License of ``python-semver`` package and
# BSD and Apache-2.0 License of ``packaging`` package.
# ------------------------------------------------------------------------------
# refs:
# * https://github.com/python-semver/python-semver
# * https://github.com/pypa/packaging
# ------------------------------------------------------------------------------
from __future__ import annotations

from typing import Union

from typing_extensions import TypeAlias

String: TypeAlias = Union[str, bytes]
DictStr: TypeAlias = dict[str, str]
TupleInt: TypeAlias = tuple[int, ...]
TupleStr: TypeAlias = tuple[str, ...]


class InfObject:
    def __repr__(self) -> str:
        return "Infinity"

    def __hash__(self) -> int:
        return hash(repr(self))

    def __lt__(self, other: object) -> bool:
        return False

    def __le__(self, other: object) -> bool:
        return False

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __gt__(self, other: object) -> bool:
        return True

    def __ge__(self, other: object) -> bool:
        return True

    def __neg__(self: object) -> NegInfObject:
        return NegInf


Inf = InfObject()


class NegInfObject:
    def __repr__(self) -> str:
        return "-Infinity"

    def __hash__(self) -> int:
        return hash(repr(self))

    def __lt__(self, other: object) -> bool:
        return True

    def __le__(self, other: object) -> bool:
        return True

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __gt__(self, other: object) -> bool:
        return False

    def __ge__(self, other: object) -> bool:
        return False

    def __neg__(self: object) -> InfObject:
        return Inf


NegInf = NegInfObject()
