# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import re
from collections.abc import Iterable
from decimal import Decimal
from typing import Any, Callable, get_args

try:
    from .__type import String
except ImportError:
    from __type import String


FMT_STR_MAP: dict[str, str] = {
    "-": "minus",
    "+": "plus",
    "!": "exclamation",
    "*": "asterisk",
}

FMT_STR_OTAN_MAP: dict[str, str] = {
    "A": "alpha",
    "B": "bravo",
    "C": "charlie",
    "D": "delta",
    "E": "echo",
    "F": "foxtrot",
    "G": "golf",
    "H": "hotel",
    "I": "india",
    "J": "juliet",
    "K": "kilo",
    "L": "lima",
    "M": "mike",
    "N": "november",
    "O": "oscar",
    "P": "papa",
    "Q": "quebec",
    "R": "romeo",
    "S": "sierra",
    "T": "tango",
    "U": "uniform",
    "V": "victor",
    "W": "whiskey",
    "X": "xray",
    "Y": "yankee",
    "Z": "zulu",
}

concat: Callable[[list[str] | Iterable[str]], str] = "".join


def itself(x: Any = None) -> Any:  # pragma: no cover.
    """Return itself value"""
    return x


def default(value: Any) -> Callable[[], Any]:  # pragma: no cover.
    """Return wrapper function of value"""
    return lambda: value


def caller(func: Callable[[], Any] | Any) -> Any:
    """Call function if it was callable

    Examples:
        >>> some_func = lambda: 100
        >>> caller(some_func)
        100
    """
    return func() if callable(func) else func


def convert_fmt_str(fmt: str) -> str:
    """Convert format string to format string name

    Examples:
        >>> convert_fmt_str('%a')
        'alpha'
        >>> convert_fmt_str('%!b')
        'bravo_exclamation'
        >>> convert_fmt_str('%S')
        'sierra_upper'
        >>> convert_fmt_str('%-N')
        'november_upper_minus'
        >>> convert_fmt_str('G')
        'G'
        >>> convert_fmt_str('%H')
        'hotel_upper'
    """
    _fmt_re: str = fmt
    if search := re.search(r"^%(?P<prefix>[-+!*]?)(?P<format>[a-zA-Z])$", fmt):
        search_dict = search.groupdict()
        _fmt: str
        if (_fmt := search_dict["format"]).isupper():
            _fmt_re = f"{FMT_STR_OTAN_MAP[_fmt]}upper"
        else:
            _fmt = _fmt.upper()
            _fmt_re = FMT_STR_OTAN_MAP[_fmt]

        if prefix := search_dict["prefix"]:
            _fmt_re = f"{_fmt_re}{FMT_STR_MAP[prefix]}"
    return _fmt_re


def can_int(value: Any) -> bool:
    """Check value that able cast to integer.

    Example:
        >>> can_int('0.0')
        True
        >>> can_int('-1.0')
        True
    """
    try:
        return float(str(value)).is_integer()
    except (TypeError, ValueError):
        return False


def can_float(value: Any) -> bool:
    """Check value that able cast to float.

    Example:
        >>> can_float('0.01')
        True
        >>> can_float('0.1a')
        False
    """
    if value is None:
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False


def remove_pad(value: str) -> str:
    """Remove zero padding of string

    Examples:
        >>> remove_pad('000')
        '0'
        >>> remove_pad('0123')
        '123'
    """
    return _last_char if (_last_char := value[-1]) == "0" else value.lstrip("0")


def bytes2str(value: String) -> str:
    """Convert byte to string

    Example:
        >>> bytes2str(b'foo')
        'foo'
        >>> bytes2str('foo')
        'foo'
    """
    if isinstance(value, bytes):
        value = str(value, "utf-8", "strict")
    elif not isinstance(value, get_args(String)):
        raise TypeError(f"not expecting type '{type(value)}'")
    return value


def float2decimal(value: float, precision: int = 15) -> Decimal:
    """Convert a float type value to decimal value with default precision that
    construct with ``Decimal`` object.

    :rtype: Decimal
    """
    return Decimal(value).quantize(Decimal(10) ** -precision)


def scache(cache_num: int) -> str:
    """Return cache suffix string

    Examples:
        >>> scache(1)
        '__1'
        >>> scache(-1)
        ''
        >>> scache(0)
        '__0'
    """
    if not isinstance(cache_num, int):
        raise TypeError(f"Can not cache with type: {type(cache_num)}")
    return f"__{cache_num}" if cache_num > 0 else ""


def escape_fmt_group(value: str) -> str:
    """Escape regex string value of format group before format

    Note for example, I replace \\ to ? because doc-string issue!

    Examples:
        >>> escape_fmt_group(
        ...     "+file_{datetime:%Y-%m-%d %H:%M:%S}_{naming:%n_%e}.json"
        ... ).replace('\\\\', '?')
        '?+file_{datetime:%Y-%m-%d %H:%M:%S}_{naming:%n_%e}?.json'
        >>> escape_fmt_group(
        ...     "+file_{datetime:%Y-%m-%d %H:%M:%S}_{naming:%n_%e}\\.json"
        ... ).replace('\\\\', '?')
        '?+file_{datetime:%Y-%m-%d %H:%M:%S}_{naming:%n_%e}???.json'
    """
    rs: str = value
    revert: dict[str, str] = {}
    for i, s in enumerate(
        re.finditer(r"(?P<found>{\w+:?([^{}]+)?})", value), start=1
    ):
        found: str = s.group("found")
        rs = rs.replace(found, f"<ESCAPE{i:03d}>")
        revert[f"<ESCAPE{i:03d}>"] = found
    rs = re.escape(rs)
    for rv in revert:
        rs = rs.replace(rv, revert[rv])
    return rs


def unescape(value: str) -> str:
    """Unescape regular expression string value with the special escape value.

    :param value: A value that want to un-escape.
    :rtype: str
    """
    return (
        value.replace("\\\\", "<ESCAPE>")
        .replace("\\", "")
        .replace("<ESCAPE>", "\\")
    )
