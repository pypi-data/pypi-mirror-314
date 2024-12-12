# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
# mypy: disable-error-code="attr-defined,unreachable,misc"
"""
This is the Main of the Formatter Objects that able to format every string
value that you want by less config and abstract override methods when inherit
from the Base Formatter class.
"""
from __future__ import annotations

import inspect
import math
import re
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from decimal import Decimal
from functools import lru_cache, partial, total_ordering, wraps
from itertools import tee, zip_longest
from typing import (
    Any,
    Callable,
    ClassVar,
    NoReturn,
    TypedDict,
    Union,
    final,  # docs: https://github.com/python/mypy/issues/9953
)

from typing_extensions import Self, TypeAlias

try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    relativedelta = None

from .__type import (
    DictStr,
    String,
    TupleInt,
)
from .__version import (
    VersionPackage as VerPackage,
)
from .exceptions import (
    FormatterArgumentError,
    FormatterGroupArgumentError,
    FormatterGroupValueError,
    FormatterKeyError,
    FormatterValueError,
)
from .utils import (
    bytes2str,
    caller,
    can_float,
    can_int,
    convert_fmt_str,
    default,
    itself,
    remove_pad,
    scache,
)

FormatterType = type["Formatter"]
FormatterGroupType = type["FormatterGroup"]
ConstantType = type["Constant"]

PriorityCallable: TypeAlias = Union[
    Callable[[Any], Any],
    Callable[[], Any],
    partial[Any],
]
FormatterCallable: TypeAlias = Union[Callable[[], Any], partial[Any]]


class PriorityValue(TypedDict):
    """Type Dictionary for value of mapping of ``cls.priorities``"""

    value: PriorityCallable
    level: int | TupleInt | None


@final
class CRegexValue(TypedDict):
    """Type Dictionary for value of mapping of ``cls.formatter``"""

    value: Union[FormatterCallable, str]
    cregex: str


@final
class RegexValue(TypedDict):
    """Type Dictionary for value of mapping of ``cls.formatter``"""

    value: Union[FormatterCallable, str]
    regex: str


ReturnPrioritiesType: TypeAlias = dict[str, PriorityValue]
ReturnFormattersType: TypeAlias = dict[str, Union[CRegexValue, RegexValue]]


@total_ordering
class SlotLevel:
    """Slot level object for order priority values. This was mean if
    you implement this slot level object to attribute on your class
    and update level to an instance when it has some action, it will
    be make the level more than another instance.

    :param level: a level number of this slot instance.
    :type level: int

    Attributes:
        * level: int
            A number of level that represent n-layer of this instance.
        * slot: List[bool]
            A list of boolean that have index equal the level attribute.
        * count: int
            A counting number of True value in the slot.
        * value: int
            A sum of weighted value from a True value in any slot position.

    Methods:
        * update: int | TupleInt | None -> SlotLevel
            Self that was updated level
        * checker: [Union[int, TupleInt]] -> bool
            A True if all values in ``self.slot`` that match with index numbers
            are True.

    Static-methods:
        * make_tuple: [Union[int, TupleInt]] -> TupleInt
            A tuple of integer value that was created from input.
    """

    __slots__ = (
        "level",
        "slot",
    )

    def __init__(self, level: int) -> None:
        """Main initialize of the slot object that define a slot list
        with level input value length of False.
        """
        self.level = level
        self.slot: list[bool] = [False] * level

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(level={self.level})>"

    def __str__(self) -> str:
        return str(self.level)

    def __hash__(self) -> int:
        return hash(tuple(self.slot))

    def __eq__(self, other: Union[SlotLevel, Any]) -> bool:
        return isinstance(other, self.__class__) and self.value == other.value

    def __lt__(self, other: SlotLevel) -> bool:
        return self.value < other.value

    @property
    def count(self) -> int:
        """Return a counting number of True value in the slot.

        :rtype: int
        :returns: A counting number of True value in the slot.
        """
        return len(list(filter(lambda x: x is True, self.slot)))

    @property
    def value(self) -> int:
        """Return a sum of weighted value from a True value in any slot
        position.

        :rtype: int
        :returns: A sum of weighted value from a True value in any slot
            position.
        """
        return sum(index * int(i) for index, i in enumerate(self.slot, start=1))

    def update(
        self,
        numbers: int | TupleInt | None = None,
        strict: bool = True,
    ) -> Self:
        """Update boolean value in ``self.slot`` from False to True.

        :param numbers: updated numbers of this SlotLevel object.
        :type numbers: Union[int, TupleInt]
        :param strict: a strict flag for raise error when pass out of
            range numbers.
        :type strict: bool(=True)

        :raises FormatterValueError: if updated number does not exist in range.

        :rtype: Self
        :returns: Self that was updated level
        """
        _numbers: Union[int, TupleInt] = numbers or (0,)
        for num in self.make_tuple(_numbers):
            if num == 0:
                continue
            elif 0 <= (_num := (num - 1)) <= (self.level - 1):
                self.slot[_num] = True
                continue
            if strict:
                raise FormatterValueError(
                    f"number for update the slot level object does not "
                    f"in range of 0 and {self.level}."
                )
        return self

    def checker(
        self,
        numbers: int | TupleInt,
    ) -> bool:
        """Return True if boolean value in ``self.slot`` is all True.

        :param numbers: An index number values that want to check in slot.
        :type numbers: Union[int, TupleInt]

        :rtype: bool
        :returns: A True if all values in ``self.slot`` that match with
            index numbers are True.
        """
        _numbers: TupleInt = self.make_tuple(numbers)
        return all(
            (
                self.slot[_n]
                if (0 <= (_n := (n - 1)) <= (self.level - 1))
                else False
            )
            for n in filter(lambda x: x != 0, _numbers)
        )

    @staticmethod
    def make_tuple(value: int | TupleInt) -> TupleInt:
        """Return tuple of integer value that was created from input value
        parameter if it is not tuple.

        :param value: a tuple of integers or any integer
        :type value: Union[int, TupleInt]

        :rtype: TupleInt
        :returns: A tuple of integer value that was created from input.
        """
        return (value,) if isinstance(value, int) else value


@dataclass(frozen=True)
class PriorityData:
    """Priority Data class.

    .. dataclass attributes::

        - value: PriorityCallable
        - level: int | TupleInt | None
    """

    value: PriorityCallable = field(default=itself, repr=False)
    level: int | TupleInt | None = field(default=(0,))


class BaseFormatter(ABC):
    """Base-class Formatter object that implement `__slots__` attribute for any
    instance classes.

    .. metaclass attributes::
        * __slots__: Tuple[str, ...]
            A tuple of necessary attribute for any subclass of Formatter class.
    """

    __slots__: tuple[str, ...] = ()

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError(
            "Please implement ``__str__`` build-in method for this "
            "sub-formatter class"
        )


@total_ordering
class Formatter(BaseFormatter):
    """Formatter object for inherit to any formatter subclass that define
    format and parse method. The base class will implement necessary
    properties and method for subclass that should implement or enhance such
    as `the cls.formatter()` method or the `cls.priorities` property.

    :param formats: A mapping value of priority attribute data.
    :type formats: dict[str, Any] | None(=None)
    :param set_strict_mode: A flag to allow checking duplicate attribute value.
    :type set_strict_mode: bool(=False)
    :param set_std_value: A flag to allow for set standard value form string,
        `self.class-name.lower()` if it True.
    :type set_std_value: bool(=True)

    .. class attributes::
        * base_fmt: str
            The base default format string value for this object.
        * base_level: int
            The maximum level of slot level of this instance.
        * Config: object
            A Configuration object that use for group and keep any config for
            this sub-formatter object.

    .. class-methods::
        * from_value: Self
            An instance of formatter that was use ``cls.parse`` method from any
            correct string value with the ``cls.base_fmt`` value.
        * parse: Self
            An instance of formatter that parse from a bytes or string value by
            a format string or base format string if it None.
        * gen_format: str
            A format string value that was changed to the regular expression
            string value for comply with the `re` module to any string value.
        * regex: DictStr
            A dict of format string, and it's regular expression string
            value that was generated from values of ``cls.formatter``.

    .. attributes::
        * value: Any
            A value that define by property of this formatter object.
        * string: str
            A standard string value that define by property of this formatter
            object.
        * level: SlotLevel
            A SlotLevel instance that have level with ``cls.base_level``.
        * priorities: ReturnPrioritiesType
            A priorities value that define by property of this formatter object.

    .. methods::
        * _setter_std_value: [bool] -> NoReturn
            Setting standard value that have an argument name be the class name
            with lower case if input flag is True.
        * values: Any | None -> DictStr
            A dict of format string, and it's string value that was passed an
            input value to `cls.formatter` method.
        * format: [str] -> str
            A string value that was formatted from format string pattern.
        * validate: [] -> bool
            A Validate method that will call after setup all attributes in
            initialize layer.
        * valid: [] -> Any
            A True value if the value from ``cls.parse`` of a string value,
            and a format string pattern is valid with ``self.value``.
        * to_const: [] -> ConstantType
            A Constant object that create from constant of ``self.values`` and
            has class name with ``f'{self.__class__.__name__}Const'`` with
            ``self.values()``.

    .. static-methods::
        * __validate_format: Dict[str, Any] | None -> Dict[str, Any]
            A formats value that validate with duplicate format string values.
        * formatter: Any | None -> ReturnFormattersType
            A formatter value that define by property of this formatter object.
        * prepare_value: [Any] -> Any
            A prepared value with defined logic.

    .. seealso::

        This class is abstract class for any formatter class. It will raise
    `NotImplementedError` when the necessary attributes and methods does not
    implement from subclass.
    """

    # This value must reassign from child class
    base_fmt: ClassVar[str] = ""

    # This value must reassign from child class
    base_level: ClassVar[int] = 1

    class Config:
        """A Configuration object that use for group and keep any config for
        this sub-formatter object.
        """

        base_config_value: ClassVar[Any | None] = None

    def __init_subclass__(
        cls: type[Self],
        /,
        level: int | None = None,
        fmt: str | None = None,
        **kwargs: Any,
    ) -> NoReturn:
        """Subclass Initialize method that will declare class variables if it
        set from class creation or direct override with that variables.

        :param level: The max level that this formatter class will limit.
        :type level: int | None(=1)
        :param fmt: The default format string value that use on the parsing.
        :type fmt: str | None(=None)
        """
        cls.base_level: int = level or cls.base_level
        cls.base_fmt: str = fmt or cls.base_fmt
        super().__init_subclass__(**kwargs)

        if not cls.base_fmt:
            raise NotImplementedError(
                "Please implement base_fmt class property for this "
                "sub-formatter class."
            )
        if not cls.__slots__:
            raise NotImplementedError(
                "Please implement `__slots__` class property for this "
                "sub-formatter class."
            )

    @classmethod
    def from_value(
        cls,
        value: Any,
    ) -> Self:
        """Passer the value to this formatter that will pass this value to
        ``cls.formatter`` method and map with the base format string value
        before parse by ``cls.parse``.

        :param value: An any value that able to pass to `cls.formatter` method.
        :type value: Any

        :rtype: Self
        :returns: An instance of formatter that was use ``cls.parse`` method
            from any correct string value with the ``cls.base_fmt`` value.
        """
        fmt_filter = [
            (k, caller(v["value"]))
            for k, v in cls.formatter(value).items()
            if k in re.findall("(%[-+!*]?[A-Za-z])", cls.base_fmt)
        ]
        fmts, values = zip(*fmt_filter)
        return cls.parse(value="_".join(values), fmt="_".join(fmts))

    @classmethod
    def parse(
        cls,
        value: String,
        fmt: str | None = None,
        *,
        strict: bool = False,
    ) -> Self:
        """Parse bytes or string value with its format to this formatter object.
        This method generates the value for itself data that can be formatted
        to another format string values.

        :param value: A bytes or string value that match with fmt.
        :type value: String
        :param fmt: a format value will use `cls.base_fmt` if it does not pass
            from input argument.
        :type fmt: str | None(=None)
        :param strict: A flag strict validate that pass to ``set_strict_mode``.
        :type strict: bool(=False)

        :raises NotImplementedError: if fmt value parameter does not pass form
            input, or `cls.base_fmt` does not implement.
        :raises FormatterValueError: if value does not match with regular
            expression format string.

        :rtype: Self
        :returns: An instance of formatter that parse from a bytes or string
            value by a format string or base format string if it None.
        """
        _fmt: str = fmt or cls.base_fmt
        _value: str = bytes2str(value)

        if not _fmt:
            raise NotImplementedError(
                "This Formatter class does not set default format string "
                "value."
            )

        _fmt = cls.gen_format(_fmt)
        if _search := re.search(rf"^{_fmt}$", _value):
            return cls(_search.groupdict(), set_strict_mode=strict)

        raise FormatterValueError(
            f"value {_value!r} does not match with format {_fmt!r}"
        )

    @classmethod
    def gen_format(
        cls,
        fmt: str,
        *,
        prefix: str | None = None,
        suffix: str | None = None,
        alias: bool = True,
    ) -> str:
        """Generate format string value that combine from any matching of
        format name with format regular expression value that able to search.

        :param fmt: a format string value pass from input argument.
        :type fmt: str
        :param prefix: a prefix string value that will add to alias format
            string value.
        :type prefix: str | None(=None)
        :param suffix: a suffix string value that will add to alias format
            string value.
        :type suffix: str | None(=None)
        :param alias: an alias boolean flag that will pass alias name if it
            true to the format string value.
        :type alias: bool

        :rtype: str
        :returns: A format string value that was changed to the regular
            expression string value for comply with the `re` module to any
            string value.
        """
        _cache: dict[str, int] = defaultdict(int)
        _prefix: str = prefix or ""
        _suffix: str = suffix or ""
        regexes = cls.regex()
        for fmt_match in re.finditer(r"(%?%[-+!*]?[A-Za-z])", fmt):
            fmt_str: str = fmt_match.group()
            if fmt_str.startswith("%%"):
                fmt = fmt.replace(fmt_str, fmt_str[1:], 1)
                continue
            if fmt_str not in regexes:
                raise FormatterArgumentError(
                    "fmt",
                    (
                        f"The format string, {fmt_str!r}, does not exists in "
                        f"``cls.regex``."
                    ),
                )
            regex: str = regexes[fmt_str]
            insided: bool = False
            for fmt_inside in re.finditer(
                r"\(\?P<(?P<alias>\w+)>(?P<fmt>(?:(?!\(\?P<\w+>).)*)\)",
                regex,
            ):
                _sr_re: str = fmt_inside.group("alias")
                regex = re.sub(
                    rf"\(\?P<{_sr_re}>",
                    (
                        (
                            f"(?P<{_prefix}{_sr_re}{scache(_cache[_sr_re])}"
                            f"{_suffix}>"
                        )
                        if alias
                        else "("
                    ),
                    regex,
                    count=1,
                )
                _cache[_sr_re] += 1
                insided = True
            if not insided:
                raise FormatterValueError(
                    "Regex format string does not set group name for "
                    "parsing value to its class."
                )
            fmt = fmt.replace(fmt_str, regex, 1)
        return fmt

    @classmethod
    @lru_cache(maxsize=None)
    def regex(cls) -> DictStr:
        """Return a dict of format string, and it's regular expression value
        that was generated from values of ``cls.formatter``. This class-method
        was wrapped with ``lru_cache`` function for more frequency getting this
        ``cls.regex()`` value because the value does not change depend on the
        formatter class.

        :raises FormatterValueError: if any key of value in formatter mapping
            does not contain `regex` nor `cregex`.

        :rtype: DictStr
        :returns: A dict of format string, and it's regular expression string
            value that was generated from values of ``cls.formatter``.

            Examples:
                {
                    "%n": "(?P<normal>...)",
                    "%N": "(?P<normal_upper>...)",
                    ...
                }
        """
        results: DictStr = {}
        pre_results: DictStr = {}
        for f, props in cls.formatter().items():
            if "regex" in props:
                results[f] = props["regex"]
            elif "cregex" in props:
                pre_results[f] = props["cregex"]
            else:
                raise FormatterValueError(
                    "formatter does not contain `regex` or `cregex` "
                    "in dict value"
                )
        for f, cr in pre_results.items():
            cr = cr.replace("%%", "[ESCAPE]")
            for cm in re.finditer(r"(%[-+!*]?[A-Za-z])", cr):
                cs: str = cm.group()
                if cs in results:
                    cr = cr.replace(cs, results[cs], 1)
                else:
                    raise FormatterArgumentError(
                        "format",
                        (
                            f"format cregex string that contain {cs} regex "
                            f"does not found."
                        ),
                    )
            results[f] = cr.replace("[ESCAPE]", "%%")
        return results

    def values(self, value: Any | None = None) -> DictStr:
        """Return a dict of format string, and it's string value that was passed
        an input value to `cls.formatter` method.

        :rtype: DictStr
        :returns: A dict of format string, and it's string value that was passed
            an input value to `cls.formatter` method.

            Example:
                {
                    "%n": "normal-value",
                    "%N": "NORMAL-UPPER-VALUE",
                    ...
                }
        """
        return {
            f: caller(props["value"])
            for f, props in self.formatter(value or self.value).items()
        }

    def format(self, fmt: str) -> str:
        """Return a string value that was formatted and filled by an input
        format string pattern.

        :param fmt: A format string value for mapping with formatter.
        :type fmt: str

        :raises KeyError: if it has any format pattern does not found in
            `cls.formatter`.

        :rtype: str
        :returns: A string value that was formatted from format string pattern.
        """
        _fmts: ReturnFormattersType = self.formatter(self.value)
        fmt = fmt.replace("%%", "[ESCAPE]")
        for _fmt_match in re.finditer(r"(%[-+!*]?[A-Za-z])", fmt):
            _fmt_str: str = _fmt_match.group()
            try:
                _value: Union[FormatterCallable, str] = _fmts[_fmt_str]["value"]
                fmt = fmt.replace(_fmt_str, caller(_value))
            except KeyError as err:
                raise FormatterKeyError(
                    f"the format: {_fmt_str!r} does not support for "
                    f"{self.__class__.__name__!r}"
                ) from err
        return fmt.replace("[ESCAPE]", "%")

    def __init__(
        self,
        formats: dict[str, Any] | None = None,
        *,
        set_strict_mode: bool = False,
        set_std_value: bool = True,
    ) -> None:
        """Main initialization get the format mapping from input argument
        and generate the necessary attributes for define the value of this
        base formatter object.

            The setter of attribute does not do anything to __slot__ variable.
        """
        _formats: dict[str, Any] = self.__validate_format(formats)
        # Set level of SlotLevel object that set from `base_level` and pass this
        # value to _level variable for update process in priorities loop.
        self.level = SlotLevel(level=self.base_level)

        # Set None default of any set up value in `cls.__slots__`
        for attr in getattr(self, "__slots__", ()):
            if attr != (self.__class__.__name__.lower()):
                setattr(self, attr, None)

        for name, values in self.priorities.items():
            # Split name of key of priorities property value.
            # From: <prefix>_<body> -> TO: [<prefix>, <body>]
            attr = name.split("_", maxsplit=1)[0]

            # Prepare values from priorities to PriorityData object.
            props = PriorityData(**values)

            # Set attr condition
            if getter := getattr(self, attr):
                if not set_strict_mode:
                    continue
                elif (name in _formats) and getter != (
                    p := props.value(
                        _formats[name],  # type: ignore[call-arg]
                    )
                ):
                    raise FormatterValueError(
                        f"Parsing duplicate values do not equal, {getter} and "
                        f"{p}, in ``self.{attr}`` with strict mode."
                    )

            elif any(name.endswith(i) for i in {"_default", "_fix"}):
                # Set default value
                setattr(self, attr, caller(props.value))

                # Update level by default it will update at first level
                self.level.update(props.level)
            elif name in _formats:
                setattr(
                    self,
                    attr,
                    props.value(_formats[name]),  # type: ignore[call-arg]
                )

                # Update level by default it will update at first level
                self.level.update(props.level)

        # Run validate method before setting standard value.
        if not self.validate():
            raise FormatterValueError(
                "Parsing value does not valid from validator"
            )

        # Set standard property by default is string value or `self.string`
        self._setter_std_value(flag=set_std_value)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __hash__(self) -> int:
        return hash(self.string)

    def __str__(self) -> str:
        return self.string

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}"
            f".parse('{self.string}', "
            f"'{self.base_fmt}')>"
        )

    def __eq__(self, other: Union[Formatter, Any]) -> bool:
        return isinstance(other, self.__class__) and self.value == other.value

    def __lt__(self, other: Formatter) -> bool:
        return self.value.__lt__(other.value)  # type: ignore[no-any-return]

    def _setter_std_value(self, flag: bool = True) -> None:
        """Setting standard value that have an argument name be the class name
        with lower case if input flag is True.

        :param flag: A boolean flag that want to set standard value or not.
        :type flag: bool(=True)
        """
        if flag:
            setattr(
                self,
                self.__class__.__name__.lower(),
                str(self.string),
            )

    @property
    @abstractmethod
    def value(self) -> Any:  # pragma: no cover
        """Return a value that define by property of this formatter object.

        :rtype: Any
        """
        raise NotImplementedError(
            "Please implement ``value`` property for this sub-formatter class"
        )

    @property
    @abstractmethod
    def string(self) -> str:  # pragma: no cover
        """Return a standard string value that define by property of this
        formatter object.

        :rtype: str
        """
        raise NotImplementedError(
            "Please implement ``string`` property for this sub-formatter class"
        )

    def validate(self) -> bool:
        """Validate method that will call after setup all attributes in
        initialize layer. This method should return with True. If it has some
        rule of validation fail, it will raise the ``FormatterValueError``.

        :rtype: bool
        :returns: True
        """
        return True

    def valid(self, value: str, fmt: str) -> bool:
        """Return a True value if the value from ``cls.parse`` of a string
        value, and a format string pattern is valid with ``self.value``.

        :param value: A string value that want to parse with a format string.
        :type value: str
        :param fmt: A format string pattern.
        :type fmt: str
        """
        return self.value.__eq__(  # type: ignore[no-any-return]
            self.__class__.parse(value, fmt).value,
        )

    def _sub_validate(self, level: int, checker: bool, error: str) -> bool:
        """Return True if validate condition does not raise the Error.

        :param level: A level number that check for slot exists.
        :type level: int
        :param checker: A validate result.
        :type checker: bool
        :param error: An error statement that raise from FormatterValueError
        :type error: str

        :raises FormatterValueError: If a slot of ``self.level`` with an input
            level and checker condition are Ture together.

        :rtype: bool
        :returns: A boolean value from slot of ``self.level`` with an input
            level integer.
        """
        if (sl := self.level.slot[(level - 1)]) and checker:
            raise FormatterValueError(
                f"Parsing value does not valid with {error}."
            )
        return not sl

    @staticmethod
    def __validate_format(
        formats: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a formats value that validate with duplicate format string
        values, and it will raise error if any duplication format name do not
        all equal.

        :param formats:
        :type formats: dict[str, Any] | None(=None)

        :rtype: Dict[str, Any]
        :returns: A formats value that validate with duplicate format string
            values.
        """
        results: dict[str, Any] = {}
        _formats: dict[str, Any] = formats or {}
        for fmt in _formats:
            _fmt: str = fmt.split("__", maxsplit=1)[0]
            if _fmt not in results:
                results[_fmt] = _formats[fmt]
                continue
            if results[_fmt] != _formats[fmt]:
                raise FormatterValueError(
                    "Parsing with some duplicate format name that have "
                    "value do not all equal."
                )
        return results

    @property
    @abstractmethod
    def priorities(self) -> ReturnPrioritiesType:
        """Return a priorities value that define by property of this formatter
        object.

        :rtype: ReturnPrioritiesType
        :returns: a priorities value that define by property of this formatter
            object.
        """
        raise NotImplementedError(
            "Please implement ``priorities`` property for this sub-formatter "
            "class"
        )

    @staticmethod
    @abstractmethod
    def formatter(value: Any | None = None) -> ReturnFormattersType:
        """Return a formatter value that define by property of this formatter
        object.

        :param value: An any value that want to generate with formatter.
        :type value: Any | None(=None)

        :rtype: ReturnFormattersType
        :returns: a formatter value that define by property of this formatter
            object.
        """
        raise NotImplementedError(
            "Please implement ``formatter`` static method for this "
            "sub-formatter class"
        )

    def to_const(self) -> ConstantType:
        """Convert this formatter instance to Constant object that have class
        name with ``f'{self.__class__.__name__}Const'`` with ``self.values()``.

        :rtype: ConstantType
        :returns: A Constant object that create from constant of ``self.values``
            and has class name with ``f'{self.__class__.__name__}Const'`` with
            ``self.values()``.
        """
        return dict2const(
            self.values(),
            name=f"{self.__class__.__name__}Const",
            base_fmt=self.base_fmt,
        )

    @staticmethod
    @abstractmethod
    def prepare_value(value: Any) -> Any:
        """Prepare value before passing to convert logic in the formatter
        method that define by property of this formatter object.

        :param value: A value that want to prepare before passing to formatter.
        :type value: Any

        :rtype: Any
        :returns: A prepared value with defined logic.
        """
        raise NotImplementedError(
            "Please implement ``prepare_value`` static method for this "
            "sub-formatter class."
        )

    def __add__(self, other: Union[Formatter, Any]) -> Formatter:
        if not isinstance(other, Formatter):
            try:
                return self.__class__.from_value(value=self.value + other)
            except FormatterValueError:
                return NotImplemented
        return self.__class__.from_value(value=self.value + other.value)

    def __radd__(self, other: Union[Formatter, Any]) -> Formatter:
        return self.__add__(other)

    def __sub__(self, other: Union[Formatter, Any]) -> Formatter:
        try:
            if not isinstance(other, Formatter):
                return self.__class__.from_value(value=(self.value - other))
            return self.__class__.from_value(value=(self.value - other.value))
        except FormatterValueError:
            return NotImplemented

    def __rsub__(self, other: Union[Formatter, Any]) -> Any:
        try:
            return other - self.value
        except (TypeError, FormatterValueError):
            return NotImplemented

    def __format__(self, fmt_spec: str) -> str:
        """Format a formatter object with any formatter setting value."""
        return self.format(fmt_spec)


class Serial(Formatter, fmt="%n"):
    """Serial formatter object that parse and format any serial (positive
    integer) value.
    """

    class Config(Formatter.Config):
        serial_max_padding: int = 3
        serial_max_binary: int = 8

    __slots__ = (
        "number",
        "serial",
    )

    @property
    def value(self) -> int:
        """Return a serial value (positive int)."""
        return int(self.string)

    @property
    def string(self) -> str:
        """Return a string number value (positive integer)."""
        return self.number  # type: ignore[no-any-return]

    @property
    def priorities(
        self,
    ) -> ReturnPrioritiesType:
        """Return a priorities value that define by property of this formatter
        object.

        :priority: A priority mapping.
            [
                0: default
                1: number
            ]

        :rtype: ReturnPrioritiesType
        :returns: A properties of the serial formatter object.
        """
        return {
            "number": {
                "value": lambda x: x,
                "level": 1,
            },
            "number_pad": {
                "value": lambda x: remove_pad(x),
                "level": 1,
            },
            "number_binary": {
                "value": lambda x: str(int(x, 2)),
                "level": 1,
            },
            "number_comma": {
                "value": lambda x: x.replace(",", ""),
                "level": 1,
            },
            "number_underscore": {
                "value": lambda x: x.replace("_", ""),
                "level": 1,
            },
            "number_default": {
                "value": default("0"),
                "level": 0,
            },
        }

    @classmethod
    def formatter(
        cls,
        serial: int | str | float | None = None,
    ) -> ReturnFormattersType:
        """Return a formatter value that define by property of this formatter
        object. Generate formatter that support mapping formatter,

            %n  : Normal serial number
            %p  : Padding serial number
            %b  : Binary number
            %c  : Normal with comma separate number
            %u  : Normal with underscore separate number

        :param serial: A serial value that pass to generate all format.
        :type serial: int | str | float | None(=None)

        :rtype: ReturnFormattersType
        :returns: A generated mapping values of all format string pattern of
            this serial formatter object.
        """
        _value: int = cls.prepare_value(serial)
        return {
            "%n": {
                # "value": lambda: str(_value),
                "value": partial(itself, str(_value)),
                "regex": r"(?P<number>[0-9]*)",
            },
            "%p": {
                "value": partial(cls.to_padding, str(_value)),
                "regex": (
                    r"(?P<number_pad>"
                    rf"[0-9]{{{str(cls.Config.serial_max_padding)}}})"
                ),
            },
            "%b": {
                "value": partial(cls.to_binary, str(_value)),
                "regex": r"(?P<number_binary>[0-1]*)",
            },
            "%c": {
                "value": partial(itself, f"{_value:,}"),
                "regex": r"(?P<number_comma>\d{1,3}(?:,\d{3})*)",
            },
            "%u": {
                "value": partial(itself, f"{_value:_}"),
                "regex": r"(?P<number_underscore>\d{1,3}(?:_\d{3})*)",
            },
        }

    @staticmethod
    def prepare_value(value: int | str | float | None) -> int:
        """Prepare value before passing to convert logic in the formatter
        method that define by property of this formatter object. Return 0 if an
        input value does not pass.

        :param value: A value that want to prepare before passing to this
            serial formatter.
        :type value: int | str | float | None

        :raises FormatterValueError: If an input value does not able cast to
            integer, or it's value less than 0.

        :rtype: int
        :returns: A prepared positive integer value.
        """
        if value is None:
            return 0
        if not can_int(value) or ((prepare := int(float(value))) < 0):
            raise FormatterValueError(
                f"Serial formatter does not support for value, {value!r}."
            )
        return prepare

    @classmethod
    def to_padding(cls, value: str) -> str:
        """Return a padding string value with zero by setting config
        ``Serial.Config.serial_max_padding`` value.

        :param value: A string value that want to pad with zero.
        :type value: str

        :rtype: str
        :returns: A padding string value with zero by setting config
            ``Serial.Config.serial_max_padding`` value.
        """
        return value.rjust(cls.Config.serial_max_padding, "0") if value else ""

    @classmethod
    def to_binary(cls, value: str) -> str:
        """Return a binary number string value with limit of max zero padding
        by setting config ``Serial.Config.serial_max_binary`` value.

        :param value: A string value that want to convert to binary.
        :type value: str

        :rtype: str
        :returns: A binary number string value with limit of max zero padding
            by setting config ``Serial.Config.serial_max_binary`` value.
        """
        return (
            f"{int(value):0{str(cls.Config.serial_max_binary)}b}"
            if value
            else ""
        )


MONTHS: DictStr = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
}

WEEKS: DictStr = {
    "Sun": "0",
    "Mon": "1",
    "Thu": "2",
    "Wed": "3",
    "Tue": "4",
    "Fri": "5",
    "Sat": "6",
}

WEEKS_FULL: DictStr = {
    "0": "Sunday",
    "1": "Monday",
    "2": "Thursday",
    "3": "Wednesday",
    "4": "Tuesday",
    "5": "Friday",
    "6": "Saturday",
}


class Datetime(Formatter, level=10, fmt="%Y-%m-%d %H:%M:%S.%f"):
    """Datetime formatter object that parse and format any datetime value."""

    __slots__ = (
        "year",
        "month",
        "week",
        "weeks",
        "day",
        "hour",
        "minute",
        "second",
        "microsecond",
        "locale",
        "datetime",
    )

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}"
            f".parse('{self.string}', "
            f"'{self.base_fmt}')>"
        )

    @property
    def value(self) -> datetime:
        """Return a ``datetime.datetime`` instance value."""
        return datetime.fromisoformat(self.string)

    @property
    def string(self) -> str:
        """Return a string datetime with ISO format."""
        return (
            f"{self.year}-{self.month}-{self.day} "
            f"{self.hour}:{self.minute}:{self.second}."
            f"{self.microsecond}"
        )

    @property
    def iso_date(self) -> datetime:
        """Return Datetime that parsing from string of date with ISO format.

        :rtype: datetime
        :returns: A datetime that parsing from string of date with ISO format.
        """
        return datetime.strptime(
            f"{self.year}-{self.month}-{self.day}", "%Y-%m-%d"
        )

    def validate(self) -> bool:
        """Validate method that validate all Datetime attributes in initialize
        layer.

        :raises FormatterValueError: If one of these rules was failed,
            * attribute ``self.week`` does not equal with value.
            * attribute ``self.locale`` does not equal with value.

        :rtype: bool
        :returns: True if all validation rules was passed.
        """
        if self.week != (w := self.value.strftime("%w")):
            raise FormatterValueError(
                f"Week that was parsed does not equal with standard datetime, "
                f"this weekday should be {WEEKS_FULL[w]}."
            )
        if self.locale != (p := self.value.strftime("%p")):
            raise FormatterValueError(
                f"Locale that was parsed does not equal with standard "
                f"datetime, this locale should be {p}."
            )
        return True

    @property
    def priorities(
        self,
    ) -> ReturnPrioritiesType:
        """Return a priorities value that define by property of this formatter
        object.

        Level Priority:
            [
                0: default
                1: locale
                2: week
                3: microsecond
                4: second
                5: minute
                6: hour, hour_12
                7: hour
                8: day, day_year
                9: month, day_year, week_year
                10: year
            ]

        :rtype: ReturnPrioritiesType
        :returns: A properties of the datetime formatter object.
        """
        return {
            "locale": {
                "value": lambda x: x,
                "level": 1,
            },
            "year": {
                "value": lambda x: x,
                "level": 10,
            },
            "year_cut_pad": {
                "value": lambda x: f"19{x}",
                "level": 10,
            },
            "year_cut": {
                "value": lambda x: f"19{x}",
                "level": 10,
            },
            "year_default": {
                "value": default("1900"),
                "level": 0,
            },
            "month": {
                "value": lambda x: x.rjust(2, "0"),
                "level": 9,
            },
            "month_pad": {
                "value": lambda x: x,
                "level": 9,
            },
            "month_short": {
                "value": lambda x: MONTHS[x],
                "level": 9,
            },
            "month_full": {
                "value": lambda x: MONTHS[x[:3]],
                "level": 9,
            },
            "month_default": {
                "value": default("01"),
                "level": 0,
            },
            "day": {
                "value": lambda x: x.rjust(2, "0"),
                "level": 8,
            },
            "day_pad": {
                "value": lambda x: x,
                "level": 8,
            },
            "day_year": {
                "value": self._from_day_year,
                "level": (
                    8,
                    9,
                ),
            },
            "day_year_pad": {
                "value": self._from_day_year,
                "level": (
                    8,
                    9,
                ),
            },
            "day_default": {
                "value": default("01"),
                "level": 0,
            },
            "week": {
                "value": lambda x: x,
                "level": 2,
            },
            "week_mon": {
                "value": lambda x: str(int(x) % 7),
                "level": 2,
            },
            "week_short": {
                "value": lambda x: WEEKS[x],
                "level": 2,
            },
            "week_full": {
                "value": lambda x: WEEKS[x[:3]],
                "level": 2,
            },
            "week_default": {
                "value": lambda: self.iso_date.strftime("%w"),
                "level": 0,
            },
            "weeks_year_mon_pad": {
                "value": self._from_week_year_mon,
                "level": 9,
            },
            "weeks_year_sun_pad": {
                "value": self._from_week_year_sun,
                "level": 9,
            },
            "hour": {
                "value": lambda x: x.rjust(2, "0"),
                "level": (
                    5,
                    6,
                ),
            },
            "hour_pad": {
                "value": lambda x: x,
                "level": (
                    5,
                    6,
                ),
            },
            "hour_12": {
                "value": self._from_hour_12,
                "level": 5,
            },
            "hour_12_pad": {
                "value": self._from_hour_12,
                "level": 5,
            },
            "hour_default": {
                "value": default("00"),
                "level": 0,
            },
            "locale_default": {
                "value": self._default_locale,
                "level": 0,
            },
            "minute": {
                "value": lambda x: x.rjust(2, "0"),
                "level": 4,
            },
            "minute_pad": {
                "value": lambda x: x,
                "level": 4,
            },
            "minute_default": {
                "value": default("00"),
                "level": 0,
            },
            "second": {
                "value": lambda x: x.rjust(2, "0"),
                "level": 3,
            },
            "second_pad": {
                "value": lambda x: x,
                "level": 3,
            },
            "second_default": {
                "value": default("00"),
                "level": 0,
            },
            "microsecond_pad": {
                "value": lambda x: x,
                "level": 2,
            },
            "microsecond_default": {
                "value": default("000000"),
                "level": 0,
            },
        }

    @classmethod
    def formatter(
        cls,
        dt: str | datetime | date | None = None,
    ) -> ReturnFormattersType:
        """Return a formatter value that define by property of this formatter
        object. Generate formatter that support mapping formatter,

            %n  : Normal format with `%Y%m%d_%H%M%S`
        **  %G  : ISO 8601 year
        **  %C  : Century
            %Y  : Year with century as a decimal number.
            %y  : Year without century as a zero-padded decimal number.
            %-y : Year without century as a decimal number.
            %m  : Month as a zero-padded decimal number.
            %-m : Month as a decimal number.
            %b  : Abbreviated month name.
            %B  : Full month name.
            %a  : the abbreviated weekday name
            %A  : the full weekday name
            %w  : weekday as a decimal number, 0 as Sunday and 6 as Saturday.
            %u  : weekday as a decimal number, 1 as Monday and 7 as Sunday.
                  ISO 8601 weekday (1-7)
            %d  : Day of the month as a zero-padded decimal.
            %-d : Day of the month as a decimal number.
            %H  : Hour (24-hour clock) as a zero-padded decimal number.
            %-H : Hour (24-hour clock) as a decimal number.
            %I  : Hour (12-hour clock) as a zero-padded decimal number.
            %-I : Hour (12-hour clock) as a decimal number.
            %M  : minute as a zero-padded decimal number
            %-M : minute as a decimal number
            %S  : second as a zero-padded decimal number
            %-S : second as a decimal number
            %j  : day of the year as a zero-padded decimal number
            %-j : day of the year as a decimal number
            %U  : Week number of the year (Sunday as the first day of the
                week). All days in a new year preceding the first Sunday are
                considered to be in week 0.
            %W  : Week number of the year (Monday as the first day of the week
                ). All days in a new year preceding the first Monday are
                considered
                to be in week 0.
        **  %V  : ISO 8601 week-number (01-53)
            %p  : Locale’s AM or PM.
            %f  : Microsecond as a decimal number, zero-padded on the left.
        **  %x  : Local version of date (%Y/%m/%d)
        **  %X  : Local version of time (%H:%M:%S)

        :param dt: A datetime value that pass to generate all format.
        :type dt: str | datetime | date | None(=None)

        :rtype: ReturnFormattersType
        :returns: A generated mapping values of all format string pattern of
            this datetime formatter object.
        """
        _dt: datetime = cls.prepare_value(dt)
        return {
            "%n": {
                "value": partial(_dt.strftime, "%Y%m%d_%H%M%S"),
                "cregex": "%Y%m%d_%H%M%S",
            },
            "%Y": {
                "value": partial(_dt.strftime, "%Y"),
                "regex": r"(?P<year>\d{4})",
            },
            "%y": {
                "value": partial(_dt.strftime, "%y"),
                "regex": r"(?P<year_cut_pad>\d{2})",
            },
            "%-y": {
                "value": partial(cls.remove_pad_dt, _dt, "%y"),
                "regex": r"(?P<year_cut>\d{1,2})",
            },
            "%m": {
                "value": partial(_dt.strftime, "%m"),
                "regex": r"(?P<month_pad>01|02|03|04|05|06|07|08|09|10|11|12)",
            },
            "%-m": {
                "value": partial(cls.remove_pad_dt, _dt, "%m"),
                "regex": r"(?P<month>1|2|3|4|5|6|7|8|9|10|11|12)",
            },
            "%b": {
                "value": partial(_dt.strftime, "%b"),
                "regex": (
                    r"(?P<month_short>"
                    r"Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
                ),
            },
            "%B": {
                "value": partial(_dt.strftime, "%B"),
                "regex": (
                    r"(?P<month_full>"
                    r"January|February|March|April|May|June|July|"
                    r"August|September|October|November|December)"
                ),
            },
            "%a": {
                "value": partial(_dt.strftime, "%a"),
                "regex": r"(?P<week_short>Mon|Thu|Wed|Tue|Fri|Sat|Sun)",
            },
            "%A": {
                "value": partial(_dt.strftime, "%A"),
                "regex": (
                    r"(?P<week_full>"
                    r"Monday|Thursday|Wednesday|Tuesday|Friday|"
                    r"Saturday|Sunday)"
                ),
            },
            "%w": {
                "value": partial(_dt.strftime, "%w"),
                "regex": r"(?P<week>[0-6])",
            },
            "%u": {
                "value": partial(_dt.strftime, "%u"),
                "regex": r"(?P<week_mon>[1-7])",
            },
            "%d": {
                "value": partial(_dt.strftime, "%d"),
                "regex": r"(?P<day_pad>[0-3][0-9])",
            },
            "%-d": {
                "value": partial(cls.remove_pad_dt, _dt, "%d"),
                "regex": r"(?P<day>\d{1,2})",
            },
            "%H": {
                "value": partial(_dt.strftime, "%H"),
                "regex": r"(?P<hour_pad>[0-2][0-9])",
            },
            "%-H": {
                "value": partial(cls.remove_pad_dt, _dt, "%H"),
                "regex": r"(?P<hour>\d{2})",
            },
            "%I": {
                "value": partial(_dt.strftime, "%I"),
                "regex": (
                    r"(?P<hour_12_pad>"
                    r"00|01|02|03|04|05|06|07|08|09|10|11|12)"
                ),
            },
            "%-I": {
                "value": partial(cls.remove_pad_dt, _dt, "%I"),
                "regex": r"(?P<hour_12>0|1|2|3|4|5|6|7|8|9|10|11|12)",
            },
            "%M": {
                "value": partial(_dt.strftime, "%M"),
                "regex": r"(?P<minute_pad>[0-6][0-9])",
            },
            "%-M": {
                "value": partial(cls.remove_pad_dt, _dt, "%M"),
                "regex": r"(?P<minute>\d{1,2})",
            },
            "%S": {
                "value": partial(_dt.strftime, "%S"),
                "regex": r"(?P<second_pad>[0-6][0-9])",
            },
            "%-S": {
                "value": partial(cls.remove_pad_dt, _dt, "%S"),
                "regex": r"(?P<second>\d{1,2})",
            },
            "%j": {
                "value": partial(_dt.strftime, "%j"),
                "regex": r"(?P<day_year_pad>[0-3][0-9][0-9])",
            },
            "%-j": {
                "value": partial(cls.remove_pad_dt, _dt, "%j"),
                "regex": r"(?P<day_year>\d{1,3})",
            },
            "%U": {
                "value": partial(_dt.strftime, "%U"),
                "regex": r"(?P<weeks_year_sun_pad>[0-5][0-9])",
            },
            "%W": {
                "value": partial(_dt.strftime, "%W"),
                "regex": r"(?P<weeks_year_mon_pad>[0-5][0-9])",
            },
            "%p": {
                "value": partial(_dt.strftime, "%p"),
                "regex": r"(?P<locale>PM|AM)",
            },
            "%f": {
                "value": partial(_dt.strftime, "%f"),
                "regex": r"(?P<microsecond_pad>\d{6})",
            },
        }

    @staticmethod
    def prepare_value(value: str | datetime | date | None) -> datetime:
        """Prepare value before passing to convert logic in the formatter
        method that define by property of this formatter object. Return
        ``datetime.now()`` if an input value does not pass.

        :param value: A value that want to prepare before passing to this
            datetime formatter.
        :type value: str | datetime | date | None

        :raises FormatterValueError: If an input value does be
            ``datetime.datetime`` or ``datetime.date``.

        :rtype: datetime
        :returns: A prepared datetime value.
        """

        if value is None:
            return datetime.now()
        if not isinstance(
            value,
            (
                str,
                datetime,
                date,
            ),
        ):
            raise FormatterValueError(
                f"Datetime formatter does not support for value, {value!r}."
            )
        elif isinstance(value, str):
            return datetime.fromisoformat(value)
        return (
            value
            if isinstance(value, datetime)
            else datetime(value.year, value.month, value.day)
        )

    def _from_day_year(self, value: str) -> str:
        """Return a validated day string value from date of year string value.

        :param value: A format string value that pass from initialize.
        :type value: str

        :rtype: str
        :returns: A validated day string value from date of year string value.
        """
        _this_year: datetime = datetime.strptime(self.year, "%Y") + timedelta(
            days=(int(value) - 1)
        )
        _month: str = _this_year.strftime("%m")
        if self._sub_validate(
            level=9,
            checker=(self.month != _month),
            error=f"month: {self.month} and day-year: {value}",
        ):
            self.month = _month
        return _this_year.strftime("%d")

    def _from_week_year_mon(self, value: str) -> str:
        """Return a validated week string value from week year number with
        Monday string value.

        :param value: A format string value that pass from initialize.
        :type value: str

        :rtype: str
        :returns: A validated week string value from week year number with
            Monday string value.
        """
        _this_year: datetime = datetime.strptime(
            f"{self.year}-W{value}-{self.week}", "%Y-W%W-%w"
        )
        _month: str = _this_year.strftime("%m")
        if self._sub_validate(
            level=9,
            checker=(self.month != _month),
            error=f"month: {self.month} and week-year-monday: {value}",
        ):
            self.month = _month

        _day: str = _this_year.strftime("%d")
        if self._sub_validate(
            level=8,
            checker=(self.day != _day),
            error=f"day: {self.day} and week-year-monday: {value}",
        ):
            self.day = _day
        return _this_year.strftime("%w")

    def _from_week_year_sun(self, value: str) -> str:
        """Return a validated week string value from week year number with
        Sunday string value.

        :param value: A format string value that pass from initialize.
        :type value: str

        :rtype: str
        :returns: A validated week string value from week year number with
            Sunday string value.
        """
        _this_year: datetime = datetime.strptime(
            f"{self.year}-W{value}-{self.week}", "%Y-W%U-%w"
        )
        _month: str = _this_year.strftime("%m")
        if self._sub_validate(
            level=9,
            checker=(self.month != _month),
            error=f"month: {self.month} and week-year-sunday: {value}",
        ):
            self.month = _month

        _day: str = _this_year.strftime("%d")
        if self._sub_validate(
            level=8,
            checker=(self.day != _day),
            error=f"day: {self.day} and week-year-sunday: {value}",
        ):
            self.day = _day
        return _this_year.strftime("%w")

    def _from_hour_12(self, value: str) -> str:
        """Return a validated hour string value that map with ``self.locale``
        attribute value.

        :param value: The hour string value.
        :type value: str

        :rtype: str
        :returns: A validated hour string value that map with ``self.locale``
            attribute value.
        """
        if self.level.slot[0] and self.locale and self.locale == "PM":
            return str(int(value) + 12).rjust(2, "0")
        return value.rjust(2, "0")

    def _default_locale(self) -> str:
        """Return a default string locale value that generate depend on
        ``self.hour`` attribute value.

        :rtype: str
        :returns: A default string locale value that generate depend on
            ``self.hour`` attribute value.
        """
        return "PM" if int(self.hour) >= 12 else "AM"

    @staticmethod
    def remove_pad_dt(_dt: datetime, fmt: str) -> str:
        """Return a padded datetime string value that was formatted.

        :param _dt: A datetime instance that want to convert to string format.
        :type _dt: datetime
        :param fmt: A format string value of datetime package.
        :type: str

        :rtype: str
        :returns: A padded datetime string value that was formatted.
        """
        return str(remove_pad(_dt.strftime(fmt)))

    @staticmethod
    def week_year_mon_to_isoweek(year: int, week: int) -> datetime:
        """Return a converted week numbers with ISO week number that was passed
        with Monday format.

        :param year: A year number.
        :type year: int
        :param week: A week number that count by monday.
        :type week: int

        :rtype: datetime
        :returns: A converted datetime value
        """
        dt: datetime = datetime.strptime(f"{year}-{week}-1", "%Y-%W-%w")
        if date(year, 1, 4).isoweekday() > 4:
            dt -= timedelta(days=7)
        return dt

    def __add__(self, other: Any) -> Formatter:
        if isinstance(
            other,
            (
                timedelta
                if relativedelta is None
                else (relativedelta, timedelta)
            ),
        ):
            return self.__class__.from_value(self.value + other)
        return NotImplemented

    def __sub__(  # type: ignore[override]
        self,
        other: Any,
    ) -> Union[Formatter, timedelta]:
        if isinstance(
            other,
            (
                timedelta
                if relativedelta is None
                else (relativedelta, timedelta)
            ),
        ):
            return self.__class__.from_value(self.value - other)
        elif isinstance(other, self.__class__):
            return self.value - other.value
        return NotImplemented

    def __rsub__(self, other: Any) -> Any:
        return NotImplemented


class Version(Formatter, level=4, fmt="%m_%n_%c"):
    """Version formatter object that parse and format any version
    (``packaging.version.Version``) value.

    .. patterns::

        Version segments reference from ``packaging.version``:
        - epoch             1!1.0.0
        - release           1.0.0
        - a/alpha           1.0.0a0
        - b/beta            1.0.0b0
        - c/rc/pre/preview	1.0.0rc0
        - r/rev/post	    1.0.0.post0
        - dev	            1.0.0.dev1
        - local             1.0.0+ubuntu.1

        Version segments reference from Hatch:
        - release           1.0.0
        - major	            2.0.0
        - minor	            1.1.0
        - micro/patch/fix   1.0.1
        - a/alpha           1.0.0a0
        - b/beta            1.0.0b0
        - c/rc/pre/preview	1.0.0rc0
        - r/rev/post	    1.0.0.post0
        - dev	            1.0.0.dev0

        Version segments reference from Semantic Versioning
        - release           1.2.3
        - pre-release       1.2.3-pre.2
        - build             1.2.3+build.4
                            1.2.3-pre.2+build.4

    .. ref::
        - The standard of versioning will align with the PEP0440
        (https://peps.python.org/pep-0440/)

        - Enhance the version object from the packaging library
        (https://packaging.pypa.io/en/latest/version.html)
    """

    __slots__ = (
        "version",
        "epoch",
        "major",
        "minor",
        "micro",
        "pre",
        "post",
        "dev",
        "local",
    )

    def __repr__(self) -> str:
        _fmt: str = "v%m.%n.%c"
        if self.epoch != "0":
            _fmt = f"%e{_fmt[1:]}"
        if self.pre:
            _fmt = f"{_fmt}%q"
        if self.post:
            _fmt = f"{_fmt}%p"
        if self.dev:
            _fmt = f"{_fmt}%d"
        if self.local:
            _fmt = f"{_fmt}%l"
        return f"<{self.__class__.__name__}.parse('{self.string}', '{_fmt}')>"

    @property
    def value(self) -> VerPackage:
        """Return a ``__version.VersionPackage`` instance value."""
        return VerPackage.parse(self.string)

    @property
    def string(self) -> str:
        """Return a string version value with full format version."""
        _release: str = f"v{self.major}.{self.minor}.{self.micro}"
        if self.epoch != "0":
            _release = f"{self.epoch}!{_release[1:]}"
        if self.pre:
            _release = f"{_release}{self.pre}"
        if self.post:
            _release = f"{_release}{self.post}"
        if self.dev:
            _release = f"{_release}.{self.dev}"
        if self.local:
            _release = f"{_release}+{self.local}"
        return _release

    @property
    def priorities(
        self,
    ) -> ReturnPrioritiesType:
        """Return a priorities value that define by property of this formatter
        object.

        Level Priority:
            [
                0: default, pre, post, dev, local
                1: micro
                2: minor
                3: major
                4: epoch
            ]

        :rtype: ReturnPrioritiesType
        :returns: A properties of the version formatter object.
        """
        return {
            "epoch": {
                "value": lambda x: x.removesuffix("!"),
                "level": 4,
            },
            "epoch_num": {
                "value": lambda x: x,
                "level": 4,
            },
            "epoch_default": {
                "value": default("0"),
                "level": 0,
            },
            "major": {
                "value": lambda x: x,
                "level": 3,
            },
            "major_default": {
                "value": default("0"),
                "level": 0,
            },
            "minor": {
                "value": lambda x: x,
                "level": 2,
            },
            "minor_default": {
                "value": default("0"),
                "level": 0,
            },
            "micro": {
                "value": lambda x: x,
                "level": 1,
            },
            "micro_default": {
                "value": default("0"),
                "level": 0,
            },
            "pre": {
                "value": lambda x: self.__from_prefix(x),
                "level": 0,
            },
            "post": {
                "value": lambda x: self.__from_prefix(x),
                "level": 0,
            },
            "post_num": {
                "value": lambda x: x,
                "level": 0,
            },
            "dev": {
                "value": lambda x: x,
                "level": 0,
            },
            "local": {
                "value": lambda x: x.removeprefix("+"),
                "level": 0,
            },
            "local_str": {
                "value": lambda x: x,
                "level": 0,
            },
        }

    @classmethod
    def formatter(
        cls,
        version: str | VerPackage | None = None,
    ) -> ReturnFormattersType:
        """Return a formatter value that define by property of this formatter
        object. Generate formatter that support mapping formatter,

            %f  : full version format with `%m_%n_%c`
            %-f : full version format with `%m-%n-%c`
        **  %r  : release version format `%m.%n.%c`
            %e  : epoch release
            %m  : major number
            %n  : minor number
            %c  : micro number
            %q  : pre-release
            %p  : post release
            %-p : post release number
            %d  : dev release
            %l  : local release
            %-l : local release number

        :param version: A version value that pass to generate all format.
        :type version: str | __version.VerPackage | None(=None)

        :rtype: ReturnFormattersType
        :returns: A generated mapping values of all format string pattern of
            this version formatter object.
        """
        _version: VerPackage = cls.prepare_value(version)
        return {
            "%f": {
                "value": partial(
                    itself,
                    f"{_version.major}_{_version.minor}_{_version.patch}",
                ),
                "cregex": "%m_%n_%c",
            },
            "%-f": {
                "value": partial(
                    itself,
                    f"{_version.major}_{_version.minor}_{_version.patch}",
                ),
                "cregex": "%m-%n-%c",
            },
            "%m": {
                "value": partial(str, _version.major),
                "regex": r"(?P<major>\d{1,3})",
            },
            "%n": {
                "value": partial(str, _version.minor),
                "regex": r"(?P<minor>\d{1,3})",
            },
            "%c": {
                "value": partial(str, _version.patch),
                "regex": r"(?P<micro>\d{1,3})",
            },
            "%e": {
                "value": partial(itself, f"{_version.epoch}!"),
                "regex": r"(?P<epoch>[0-9]+!)",
            },
            "%-e": {
                "value": partial(itself, str(_version.epoch)),
                "regex": r"(?P<epoch_num>[0-9]+)",
            },
            "%q": {
                "value": partial(itself, str(_version.v_pre or "")),
                "regex": (
                    r"(?P<pre>(a|b|c|rc|alpha|beta|pre|preview)[-_\.]?[0-9]+)"
                ),
            },
            "%p": {
                "value": partial(itself, str(_version.v_post or "")),
                "regex": (
                    r"(?P<post>(?:(post|rev|r)[-_\.]?[0-9]+)|(?:-[0-9]+))"
                ),
            },
            "%-p": {
                "value": partial(itself, str(_version.v_post or "")),
                "regex": r"(?P<post_num>[0-9]+)",
            },
            "%d": {
                "value": partial(itself, str(_version.v_dev or "")),
                "regex": r"(?P<dev>dev[-_\.]?[0-9]+)",
            },
            "%l": {
                "value": partial(itself, _version.local),
                "regex": r"(?P<local>\+[a-z0-9]+(?:[-_\.][a-z0-9]+)*)",
            },
            "%-l": {
                "value": partial(itself, f"+{_version.local}"),
                "regex": r"(?P<local_str>[a-z0-9]+(?:[-_\.][a-z0-9]+)*)",
            },
        }

    @staticmethod
    def prepare_value(
        value: str | VerPackage | None,
    ) -> VerPackage:
        """Prepare value before passing to convert logic in the formatter
        method that define by property of this formatter object. Return
        ``__version.VersionPackage.parse("0.0.1")`` if an input value does not
        pass.

        :param value: A value that want to prepare before passing to this
            version formatter.
        :type value: str |  __version.VersionPackage | None

        :raises FormatterValueError: If an input value does be
            ``__version.VersionPackage``

        :rtype: __version.VersionPackage
        :returns: A prepared version value.
        """
        if value is None:
            return VerPackage.parse("0.0.1")
        if not isinstance(
            value,
            (
                str,
                VerPackage,
            ),
        ):
            raise FormatterValueError(
                f"Version formatter does not support for value, {value!r}."
            )
        elif isinstance(value, str):
            return VerPackage.parse(value)
        return value

    @staticmethod
    def __from_prefix(value: str) -> str:
        """Return a replaced string value to standard prefix of pre- and post-
        format version string.

        :param value: A pre- or post- format version string.
        :type value: str

        :rtype: str
        :returns: A replaced string value to standard prefix of pre- and post-
            format version string.
        """
        for rep, matches in (
            (
                "a",
                [
                    "alpha",
                ],
            ),
            (
                "b",
                [
                    "beta",
                ],
            ),
            (
                "rc",
                [
                    "c",
                    "pre",
                    "preview",
                ],
            ),
            (
                "post",
                [
                    "rev",
                    "r",
                    "post",
                ],
            ),
        ):
            for letter in matches:
                if re.match(rf"{letter}[-_.]?[0-9]+", value):
                    return value.replace(letter, rep)
            if re.match(rf"{rep}[-_.]?[0-9]+", value):
                return value
        raise FormatterValueError(
            f"Convert prefix dose not valid for value `{value}`."
        )

    def __add__(  # type: ignore
        self,
        other: Union[tuple[int, int, int], Any],
    ):  # no cov
        if isinstance(other, tuple) and len(other) == 3:
            old = self.value
            old = old.replace(
                **{
                    part: getattr(old, part) + value
                    for part, value in zip(("major", "minor", "patch"), other)
                    if isinstance(value, int) and value > 0
                }
            )
            return self.__class__.from_value(old)
        return NotImplemented

    def __sub__(self, other: Any):  # type: ignore # no cov
        return NotImplemented

    def __rsub__(self, other: Any):  # type: ignore # no cov
        return NotImplemented


class Naming(Formatter, level=5, fmt="%n"):
    """Naming formatter object that parse and format any name value.

    .. note::

        A name value that parsing to this class should not contain any
    special characters, this will keep only.
    """

    __slots__ = (
        "naming",
        "strings",
        "flats",
        "shorts",
        "vowels",
    )

    @property
    def value(self) -> list[str]:
        """Return a list of word of naming value."""
        return self.string.split()

    @property
    def string(self) -> str:
        """Return a string naming with \\s sep if it is possible."""
        if self.strings:
            return " ".join(self.strings)
        elif self.flats:
            return self.flats[0]  # type: ignore[no-any-return]
        elif self.shorts:
            return " ".join(self.shorts)
        elif self.vowels:
            return self.vowels[0]  # type: ignore[no-any-return]
        return ""

    def validate(self) -> bool:
        """Validate method that validate all Naming attributes in initialize
        layer.

        :raises FormatterValueError: If one of these rules was failed,
            * attribute ``self.flats`` does not equal with ``self.shorts``.
            * attribute ``self.flats`` does not equal with ``self.vowels``.
            * attribute ``self.vowels`` does not equal with ``self.shorts``.

        :rtype: bool
        :returns: True if all validation rules was passed.
        """
        # Validate flat and short-name
        if self.level.checker((3, 2)):
            if self.__validate_word_with_short(self.flats[0], self.shorts):
                raise FormatterValueError(
                    f"Flat and Shortname that were parsed are not equal, "
                    f"{self.flats[0]} and {''.join(self.shorts)}."
                )
            elif not self.level.checker(5):
                self.__setattr__(
                    "strings",
                    self.__extract_from_word_with_short(
                        self.flats[0], self.shorts
                    ),
                )

        # Validate flat and vowel
        if (
            self.level.checker((1, 3))
            and [re.sub(r"[aeiou]", "", self.flats[0])] != self.vowels
        ):
            raise FormatterValueError(
                f"Flat and Vowel that were parsed are not equal, "
                f"{self.flats[0]} and {self.vowels[0]}."
            )

        # Validate short and vowel
        if self.level.checker((1, 2)) and self.__validate_word_with_short(
            self.vowels[0],
            list(filter(lambda x: x not in "aeiou", self.shorts)),
        ):
            raise FormatterValueError(
                f"Shortname and Vowel that were parsed are not equal, "
                f"{''.join(self.shorts)} and {self.vowels[0]}."
            )
        return True

    @staticmethod
    def __validate_word_with_short(word: str, shorts: list[str]) -> bool:
        """Validate a word with list of shortname Private static-method.

        :param word: A word string that want to validate.
        :type word: str
        :param shorts: A list of shortname.
        :type shorts: List[str]

        :rtype: bool
        :returns: True if validation process of a word with list of shortname
            Private static-method be correct.
        """
        idx: int = 0
        for s in shorts:
            if s not in word[idx:]:
                return True
            idx += word[idx:].index(s) + 1
        return False

    @staticmethod
    def __extract_from_word_with_short(
        word: str,
        shorts: list[str],
    ) -> list[str]:
        """Return a list of word that was extracted from word by list of
        shortnames.

        :param word: A word string value.
        :type word: str
        :param shorts: A list of first char of naming.
        :type shorts: List[str]

        :rtype: List[str]
        :returns: A list of word that was extracted from word by list of
            shortnames.
        """
        idx: int = 0
        rs: list[int] = []
        for s in shorts:
            idx += word[idx:].index(s)
            rs.append(idx)
        start, end = tee(rs, 2)
        # Move index of end for split with correct end of word index.
        next(end)
        return [word[i:j] for i, j in zip_longest(start, end)]

    @property
    def priorities(
        self,
    ) -> ReturnPrioritiesType:
        """Return a priorities value that define by property of this formatter
        object.

        Level Priority:
            [
                0: default
                1: vowels
                2: shorts
                3: flats
                4: -
                5: strings
            ]

        :rtype: ReturnPrioritiesType
        :returns: A properties of the naming formatter object.
        """
        return {
            "strings": {"value": lambda x: x.split(), "level": 5},
            "strings_upper": {
                "value": lambda x: x.lower().split(),
                "level": 5,
            },
            "strings_title": {
                "value": lambda x: x.lower().split(),
                "level": 5,
            },
            "strings_lower": {"value": lambda x: x.split(), "level": 5},
            "strings_camel": {
                "value": lambda x: self.__split_pascal_case(x),
                "level": 5,
            },
            "strings_pascal": {
                "value": lambda x: self.__split_pascal_case(x),
                "level": 5,
            },
            "strings_kebab": {
                "value": lambda x: x.split("-"),
                "level": 5,
            },
            "strings_kebab_upper": {
                "value": lambda x: x.lower().split("-"),
                "level": 5,
            },
            "strings_train": {
                "value": lambda x: x.lower().split("-"),
                "level": 5,
            },
            "strings_snake": {
                "value": lambda x: x.split("_"),
                "level": 5,
            },
            "strings_snake_upper": {
                "value": lambda x: x.lower().split("_"),
                "level": 5,
            },
            "strings_snake_title": {
                "value": lambda x: x.lower().split("_"),
                "level": 5,
            },
            "strings_default": {
                "value": default([]),
                "level": 0,
            },
            "flats": {
                "value": self._from_flats,
                "level": 3,
            },
            "flats_upper": {
                "value": lambda x: self._from_flats(x.lower()),
                "level": 3,
            },
            "flats_default": {
                "value": self.__default(lambda x: "".join(x)),
                "level": 0,
            },
            "shorts": {
                "value": self._from_shorts,
                "level": 2,
            },
            "shorts_upper": {
                "value": lambda x: self._from_shorts(x.lower()),
                "level": 2,
            },
            "shorts_default": {
                "value": self.__default(lambda x: [i[0] for i in x]),
                "level": 0,
            },
            "vowels": {
                "value": self._from_vowels,
                "level": 1,
            },
            "vowels_upper": {
                "value": lambda x: self._from_vowels(x.lower()),
                "level": 1,
            },
            "vowels_default": {
                "value": self.__default(
                    lambda x: re.sub(r"[aeiou]", "", "".join(x))
                ),
                "level": 0,
            },
        }

    @classmethod
    def formatter(
        cls,
        nm: str | list[str] | None = None,
    ) -> ReturnFormattersType:
        """Return a formatter value that define by property of this formatter
        object. Generate formatter that support mapping formatter,

            %n  : Normal name format
            %N  : Normal name upper case format
            %-N : Normal name title case format
            %u  : Upper case format
            %l  : Lower case format
            %t  : Title case format
            %a  : Shortname format
            %A  : Shortname upper case format
            %f  : Flat case format
            %F  : Flat upper case format
            %c  : Camel case format
            %-c : Upper first Camel case format
            %p  : Pascal case format
            %s  : Snake case format
            %S  : Snake upper case format
            %-S : Snake title case format
            %k  : Kebab case format
            %K  : Kebab upper case format
            %-K : Kebab title case format (Train Case)
            %T  : Train case format
            %v  : normal name removed vowel
            %V  : normal name removed vowel with upper case

        .. refs::
            * https://gist.github.com/SuppieRK/a6fb471cf600271230c8c7e532bdae4b

        :param nm: A naming value that pass to generate all format.
        :type nm: str | list[str] | None(=None)

        :rtype: ReturnFormattersType
        :returns: A generated mapping values of all format string pattern of
            this naming formatter object.
        """
        _value: list[str] = cls.prepare_value(nm)
        return {
            "%n": {
                "value": partial(cls.__join_with, " ", _value),
                "cregex": "%l",
            },
            "%N": {
                "value": partial(
                    cls.__join_with, " ", _value, lambda x: x.upper()
                ),
                "cregex": "%u",
            },
            "%-N": {
                "value": partial(
                    cls.__join_with, " ", _value, lambda x: x.capitalize()
                ),
                "cregex": "%t",
            },
            "%u": {
                "value": partial(
                    cls.__join_with, " ", _value, lambda x: x.upper()
                ),
                "regex": r"(?P<strings_upper>[A-Z0-9]+(?:\s[A-Z0-9]+)*)",
            },
            "%l": {
                "value": partial(cls.__join_with, " ", _value),
                "regex": r"(?P<strings>[a-z0-9]+(?:\s[a-z0-9]+)*)",
            },
            "%t": {
                "value": partial(
                    cls.__join_with, " ", _value, lambda x: x.capitalize()
                ),
                "regex": (
                    r"(?P<strings_title>[A-Z][a-z0-9]+(?:\s[A-Z]+[a-z0-9]*)*)"
                ),
            },
            "%a": {
                "value": partial(
                    cls.__join_with,
                    "",
                    _value,
                    lambda x: (x[0] if x else ""),
                ),
                "regex": r"(?P<shorts>[a-z0-9]+)",
            },
            "%A": {
                "value": partial(
                    cls.__join_with,
                    "",
                    _value,
                    lambda x: (x[0].upper() if x else ""),
                ),
                "regex": r"(?P<shorts_upper>[A-Z0-9]+)",
            },
            "%c": {
                "value": partial(cls.camel_case, "_".join(_value)),
                "regex": (
                    r"(?P<strings_camel>[a-z]+"
                    r"((\d)|([A-Z0-9][a-z0-9]+))*([A-Z])?)"
                    # r"(?P<strings_camel>[a-z]+(?:[A-Z0-9]+[a-z0-9]+[A-Za-z0-9]*)*)"
                ),
            },
            "%-c": {
                "value": partial(cls.pascal_case, "_".join(_value)),
                "cregex": "%p",
            },
            "%p": {
                "value": partial(cls.pascal_case, "_".join(_value)),
                "regex": (
                    r"(?P<strings_pascal>[A-Z]"
                    r"([A-Z0-9]*[a-z][a-z0-9]*[A-Z]|"
                    r"[a-z0-9]*[A-Z][A-Z0-9]*[a-z])["
                    r"A-Za-z0-9]*)"
                    # r"(?P<strings_pascal>(?:[A-Z][a-z0-9]+)(?:[A-Z]+[a-z0-9]*)*)"
                ),
            },
            "%k": {
                "value": partial(cls.__join_with, "-", _value),
                "regex": r"(?P<strings_kebab>[a-z0-9]+(?:-[a-z0-9]+)*)",
            },
            "%K": {
                "value": partial(
                    cls.__join_with, "-", _value, lambda x: x.upper()
                ),
                "regex": r"(?P<strings_kebab_upper>[A-Z0-9]+(?:-[A-Z0-9]+)*)",
            },
            "%-K": {
                "value": partial(
                    cls.__join_with, "-", _value, lambda x: x.capitalize()
                ),
                "cregex": "%T",
            },
            "%f": {
                "value": partial(cls.__join_with, "", _value),
                "regex": r"(?P<flats>[a-z0-9]+)",
            },
            "%F": {
                "value": partial(
                    cls.__join_with, "", _value, lambda x: x.upper()
                ),
                "regex": r"(?P<flats_upper>[A-Z0-9]+)",
            },
            "%s": {
                "value": partial(cls.__join_with, "_", _value),
                "regex": r"(?P<strings_snake>[a-z0-9]+(?:_[a-z0-9]+)*)",
            },
            "%S": {
                "value": partial(
                    cls.__join_with, "_", _value, lambda x: x.upper()
                ),
                "regex": r"(?P<strings_snake_upper>[A-Z0-9]+(?:_[A-Z0-9]+)*)",
            },
            "%-S": {
                "value": partial(
                    cls.__join_with, "_", _value, lambda x: x.capitalize()
                ),
                "regex": (
                    r"(?P<strings_snake_title>"
                    r"[A-Z][a-z0-9]+(?:_[A-Z]+[a-z0-9]*)*)"
                ),
            },
            "%T": {
                "value": partial(
                    cls.__join_with, "-", _value, lambda x: x.capitalize()
                ),
                "regex": (
                    r"(?P<strings_train>"
                    r"[A-Z][a-z0-9]+(?:-[A-Z]+[a-z0-9]*)*)"
                ),
            },
            "%v": {
                "value": partial(re.sub, r"[aeiou]", "", "".join(_value)),
                "regex": r"(?P<vowels>[b-df-hj-np-tv-z]+)",
            },
            "%V": {
                "value": partial(
                    re.sub, r"[AEIOU]", "", "".join(_value).upper()
                ),
                "regex": r"(?P<vowels_upper>[B-DF-HJ-NP-TV-Z]+)",
            },
        }

    @classmethod
    def prepare_value(cls, value: str | list[str] | None) -> list[str]:
        """Prepare value before passing to convert logic in the formatter
        method that define by property of this formatter object. Return
        List of empty string if an input value does not pass.

        :param value: A value that want to prepare before passing to this
            naming formatter.
        :type value: str | list[str] | None

        :raises FormatterValueError: If an input value does be list of str.

        :rtype: List[str]
        :returns: A prepared naming value.
        """
        if value is None:
            return [""]
        if isinstance(value, str):
            return cls.__remove_special_char(value)
        elif not isinstance(value, list) or any(
            not isinstance(v, str) for v in value
        ):
            raise FormatterValueError(
                f"Naming formatter does not support for value, {value!r}."
            )
        return [re.sub(r"[^\-.\w\s]+", "", v) for v in value]

    def _from_flats(self, value: str) -> list[str]:
        """Return a validated flats value.

        :param value: A format string value that pass from initialize.
        :type value: str

        :raises FormatterValueError: If flat string from ``self.strings`` does
            not equal with an input value.

        :rtype: List[str]
        :returns: a validated flats value.
        """
        v: list[str] = [value]
        if self.level.checker(5) and (_s := ["".join(self.strings)]) != v:
            raise FormatterValueError(
                f"Parsing value does not valid with flat from "
                f"strings: {_s} and flats: {v}."
            )
        return v

    def _from_shorts(self, value: str) -> list[str]:
        """Return a validated shorts value.

        :param value: A format string value that pass from initialize.
        :type value: str

        :raises FormatterValueError: If short string from ``self.strings`` does
            not equal with an input value.

        :rtype: List[str]
        :returns: a validated shorts value.
        """
        v: list[str] = list(value)
        if self.level.checker(5) and (_s := [s[0] for s in self.strings]) != v:
            raise FormatterValueError(
                f"Parsing value does not valid with short from "
                f"strings: {_s} and shorts: {v}."
            )
        return v

    def _from_vowels(self, value: str) -> list[str]:
        """Return a validated vowels value.

        :param value: A format string value that pass from initialize.
        :type value: str

        :raises FormatterValueError: If vowel string from ``self.strings`` does
            not equal with an input value.

        :rtype: List[str]
        :returns: A validated vowels value.
        """
        v: list[str] = [value]
        if (
            self.level.checker(5)
            and (_s := [re.sub(r"[aeiou]", "", "".join(self.strings))]) != v
        ):
            raise FormatterValueError(
                f"Parsing value does not valid with vowel from "
                f"strings: {_s} and vowels: {v}."
            )
        return v

    def __default(
        self,
        logic: Callable[[list[str]], str],
    ) -> Callable[[], list[str]]:
        """Return a default function that pass logic to ``self.strings`` if
        it was set from initialization.

        :param logic: A logic function receive a ``self.strings`` list.
        :type logic: Callable[[List[str]], str]

        :rtype: Callable[[], List[str]]
        :returns: A default function that pass logic to ``self.strings`` if
            it was set from initialization.
        """

        def sub_caller() -> list[str]:
            if not self.level.slot[4]:
                return []
            return (
                [*rs] if isinstance((rs := logic(self.strings)), list) else [rs]
            )

        return sub_caller

    @staticmethod
    def pascal_case(snake_case: str) -> str:
        """Return a string value with pascal case that reference by
        `inflection`.

        :param snake_case: A word with the snake case string.
        :type snake_case: str

        :rtype: str
        :returns: A string value with pascal case that reference by
            `inflection`.
        """
        return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), snake_case)

    @classmethod
    def camel_case(cls, snake_case: str) -> str:
        """Return a string value with camel case with lower case first
        letter.

        :param snake_case: A word with the snake case string.
        :type snake_case: str

        :rtype: str
        :returns: A string value with camel case with lower case first
            letter.
        """
        return (
            (snake_case[0].lower() + cls.pascal_case(snake_case)[1:])
            if snake_case
            else ""
        )

    @staticmethod
    def __join_with(
        by: str,
        values: list[str],
        func: Callable[[str], str] | None = None,
    ) -> str:
        """Return a string value that join with any separate string after
        prepare with an input function if it set.

        :param by: A seperator string that want to join.
        :type by: str
        :param values: A list of word that want to join with.
        :type values: List[str]
        :param func: A function that want to prepare before join.
        :type func: Callable[[str], str] | None(=None)

        :rtype: str
        :returns: A string value that join with any separate string after
            prepare with an input function if it set.
        """
        return by.join(map(func, values)) if func else by.join(values)

    @staticmethod
    def __remove_special_char(value: str) -> list[str]:
        """Return a list of word that split from an input value string
        before remove special character.

        :param value: A string value that want to prepare.
        :type value: str

        :rtype: List[str]
        :returns: A list of word that split from an input value string
            before remove special character.
        """
        result: str = re.sub(r"[^\-.\w\s]+", "", value)
        return re.sub(r"[\-._\s]", " ", result).strip().split()

    @staticmethod
    def __split_pascal_case(value: str) -> list[str]:
        """Return a list of word that prepare from the Pascal case.

        :param value: A pascal value string that want to prepare.
        :type value: str

        :rtype: str
        :returns: A list of word that prepare from the Pascal case.
        """
        return (
            "".join([f" {c.lower()}" if c.isupper() else c for c in value])
            .strip()
            .split()
        )

    def __sub__(self, other: Any):  # type: ignore # no cov
        return NotImplemented

    def __rsub__(self, other: Any):  # type: ignore # no cov
        return NotImplemented


SIZE: tuple[str, ...] = (
    "B",
    "KB",
    "MB",
    "GB",
    "TB",
    "PB",
    "EB",
    "ZB",
    "YB",
)


@final
class StorageSearchOrder(TypedDict):
    """Type Dictionary for value of mapping of ``cls.search_order``"""

    value: str
    order: str


class Storage(Formatter, fmt="%b"):
    """Storage formatter object that parse and format any storage value.

    .. note::

        A storage value will use ``decimal.Decimal`` package for wrap up
    standard value for this Storage formatter object.
    """

    class Config(Formatter.Config):
        storage_rounding: int = 0

    __slots__ = (
        "bit",
        "byte",
        "storage",
    )

    @property
    def value(self) -> Decimal:
        """Return a bit integer value."""
        return Decimal(self.string)

    @property
    def string(self) -> str:
        """Return a bit string value."""
        return str(self.bit)  # type: ignore[no-any-return]

    def validate(self) -> bool:
        """Validate method that validate all Storage attributes in initialize
        layer.

        :raises FormatterValueError: If one of these rules was failed,
            * attribute ``self.week`` does not equal with value.
            * attribute ``self.locale`` does not equal with value.

        :rtype: bool
        :returns: True if all validation rules was passed.
        """
        if (b := self.byte2bit(self.byte)) != self.bit:
            raise FormatterValueError(
                f"Byte that was parsed does not equal with bit, receive {b} bit"
                f"(byte to bit) but get "
                f"{self.bit:.{self.Config.storage_rounding:02d}f} bit from "
                f"parsing."
            )
        return True

    @property
    def priorities(self) -> ReturnPrioritiesType:
        """Return a priorities value that define by property of this formatter
        object.

        Level Priority:
            [
                0: default
                1: bit, byte
            ]

        :rtype: ReturnPrioritiesType
        :returns: A properties of the storage formatter object.
        """
        return {
            "bit": {
                "value": lambda x: Decimal(x),
                "level": 1,
            },
            "byte": {
                "value": lambda x: self.str2byte(x, "B"),
                "level": 1,
            },
            "byte_kilo": {
                "value": lambda x: self.str2byte(x, "KB"),
                "level": 1,
            },
            "byte_mega": {
                "value": lambda x: self.str2byte(x, "MB"),
                "level": 1,
            },
            "byte_giga": {
                "value": lambda x: self.str2byte(x, "GB"),
                "level": 1,
            },
            "byte_tera": {
                "value": lambda x: self.str2byte(x, "TB"),
                "level": 1,
            },
            "byte_peta": {
                "value": lambda x: self.str2byte(x, "PB"),
                "level": 1,
            },
            "byte_exa": {
                "value": lambda x: self.str2byte(x, "EB"),
                "level": 1,
            },
            "byte_zetta": {
                "value": lambda x: self.str2byte(x, "ZB"),
                "level": 1,
            },
            "byte_yotta": {
                "value": lambda x: self.str2byte(x, "YB"),
                "level": 1,
            },
            "bit_default": {
                "value": self.__default_from_byte,
                "level": 0,
            },
            "byte_default": {
                "value": self.__default_from_bit,
                "level": 0,
            },
        }

    @staticmethod
    def formatter(storage: int | None = None) -> ReturnFormattersType:
        """Return a formatter value that define by property of this formatter
        object. Generate formatter that support mapping formatter,

            %b  : Bit format
            %B  : Byte format
            %K  : Kilo-Byte format
            %M  : Mega-Byte format
            %G  : Giga-Byte format
            %T  : Tera-Byte format
            %P  : Peta-Byte format
            %E  : Exa-Byte format
            %Z  : Zetta-Byte format
            %Y  : Yotta-Byte format

        :param storage: A storage value that pass to generate all format.
        :type storage: int | None

        :rtype: ReturnFormattersType
        :returns: A generated mapping values of all format string pattern of
            this storage formatter object.
        """
        size: Decimal = Storage.prepare_value(storage)
        return {
            "%b": {
                "value": partial(itself, str(size)),
                "regex": r"(?P<bit>[0-9]*.?[0-9]*)",
            },
            "%B": {
                "value": partial(itself, f"{round(size / 8)}B"),
                "regex": r"(?P<byte>[0-9]*B)",
            },
            "%K": {
                "value": partial(Storage.bit2byte, size, "KB"),
                "regex": r"(?P<byte_kilo>[0-9]*KB)",
            },
            "%M": {
                "value": partial(Storage.bit2byte, size, "MB"),
                "regex": r"(?P<byte_mega>[0-9]*MB)",
            },
            "%G": {
                "value": partial(Storage.bit2byte, size, "GB"),
                "regex": r"(?P<byte_giga>[0-9]*GB)",
            },
            "%T": {
                "value": partial(Storage.bit2byte, size, "TB"),
                "regex": r"(?P<byte_tera>[0-9]*TB)",
            },
            "%P": {
                "value": partial(Storage.bit2byte, size, "PB"),
                "regex": r"(?P<byte_peta>[0-9]*PB)",
            },
            "%E": {
                "value": partial(Storage.bit2byte, size, "EB"),
                "regex": r"(?P<byte_exa>[0-9]*EB)",
            },
            "%Z": {
                "value": partial(Storage.bit2byte, size, "ZB"),
                "regex": r"(?P<byte_zetta>[0-9]*ZB)",
            },
            "%Y": {
                "value": partial(Storage.bit2byte, size, "YB"),
                "regex": r"(?P<byte_yotta>[0-9]*YB)",
            },
        }

    @classmethod
    def prepare_value(
        cls,
        value: int | float | Decimal | str | None,
    ) -> Decimal:
        """Prepare value before passing to convert logic in the formatter
        method that define by property of this formatter object. Return 0 if an
        input value does not pass.

        :param value: A value that want to prepare before passing to this
            storage formatter.
        :type value: int | float | Decimal | str | None

        :raises FormatterValueError: If an input value does not able cast to
            integer, or it's value less than 0.

        :rtype: decimal.Decimal
        :returns: A prepared positive decimal value.
        """
        if value is None:
            return Decimal("0")
        if not can_float(value) or (Decimal(value) < 0):
            raise FormatterValueError(
                f"Storage formatter does not support for value, {value!r}."
            )
        # Wrap the value to string after pass to decimal value.
        return cls.round_up(Decimal(str(value)))

    @classmethod
    def round_up(cls, value: Decimal) -> Decimal:
        """Return a rounded value that use ``cls.Config.storage_rounding``.

        :param value: A decimal value that want to round up.
        :type value: decimal.Decimal

        :rtype: decimal.Decimal
        :returns: A rounded value that use ``cls.Config.storage_rounding``.
        """
        return round(value, cls.Config.storage_rounding)

    def __default_from_byte(self) -> Decimal:
        """Return default value that calculate from the byte value."""
        return Decimal(self.byte or "0") * 8

    def __default_from_bit(self) -> Decimal:
        """Return default value that calculate from the bit value."""
        return Decimal(self.bit or "0") / 8

    @classmethod
    def bit2byte(
        cls,
        value: Decimal,
        order: str,
        *,
        suffix: bool = True,
    ) -> str:
        """Convert the bit value to byte value with string type that depend on
        an input order value.

        :param value: A decimal value that want to convert to the byte string.
        :type value: str
        :param order: The order value that want to power with 1024.
        :type order: str
        :param suffix: A suffix flag that will add order string to return value
        :type suffix: bool

        Examples:

            >>> Storage.bit2byte('150', 'B')
            19B
            >>> Storage.bit2byte('150', 'B', suffix=False)
            19

        :rtype: str
        :returns: The bit to byte value with string type that depend on an input
            order value.
        """
        p: Decimal = Decimal(math.pow(1024, SIZE.index(order)))
        return f"{(cls.round_up((value / 8) / p))}{order if suffix else ''}"

    @classmethod
    def search_order(cls, value: str) -> StorageSearchOrder:
        """Searching order suffix

        :rtype: StorageSearchOrder
        """
        _decimal: str = (
            rf"(?:\.\d{{0,{st_round}}})?"
            if (st_round := cls.Config.storage_rounding) > 0
            else ""
        )
        return (
            s.groupdict()
            if (
                s := re.search(
                    rf"(?P<value>\d+{_decimal})(?P<order>[KMGTPEZY]?B)?",
                    value,
                )
            )
            else {"value": value, "order": "B"}
        )

    @classmethod
    def str2byte(cls, value: str, order: str | None = None) -> Decimal:
        """Convert to byte value that depend on an input order value.

        :param value: A string value that want to convert to the byte value.
        :type value: str
        :param order: The order value that want to power with 1024.
        :type order: str | None(=None)

        Examples:

            >>> Storage.str2byte('12MB', 'MB')

        :rtype: decimal.Decimal
        :returns: A converted byte value that depend on an input order value.
        """
        if order is None:
            searching: StorageSearchOrder = cls.search_order(value)
            value = searching["value"]
            order = searching["order"]
        p: Decimal = Decimal(math.pow(1024, SIZE.index(order)))
        return cls.round_up(Decimal(value.replace(order, "")) * p)

    @classmethod
    def byte2bit(cls, value: str | Decimal, order: str = "B") -> Decimal:
        """Convert the byte value to bit value with string type that depend on
        an input order value or default with `B`.

        :param value: A decimal value that want to convert to the byte string.
        :type value: str
        :param order: The order value that want to power with 1024.
        :type order: str(=B)

        Examples:

            >>> Storage.byte2bit(19.000)
            152.000

        :rtype: decimal.Decimal
        :returns: The byte to bit value with string type that depend on an input
            order value.
        """
        p: Decimal = Decimal(math.pow(1024, SIZE.index(order)))
        return cls.round_up(
            (
                Decimal(value.replace(order, ""))
                if isinstance(value, str)
                else value
            )
            * p
            * 8
        )


ConstantComparator: TypeAlias = Callable[["Constant", "Constant"], bool]


def const_comparison(operator: ConstantComparator) -> ConstantComparator:
    """Decorator function for compare operators in the Constant class."""

    @wraps(operator)
    def wrapper(self: Constant, other) -> bool:
        if not issubclass(other.__class__, Constant):
            return NotImplemented
        return operator(self, other)

    return wrapper


class Constant(Formatter, fmt="%%"):
    """Constant object for create Constant class in the constructor function.

    :param formats: A mapping value of priority attribute data.
    :type formats: Dict[str, Any] | None(=None)
    :param set_strict_mode: A flag to allow checking duplicate attribute value.
    :type set_strict_mode: bool(=False)

    .. seealso::

        This class does not implement abstract properties because it does not
    any senses to compare a constant instance such as ``__add__``, or
    ``__sub__`` properties.
    """

    __slots__: tuple[str, ...] = ("_constant",)

    @classmethod
    def from_value(cls, value: Any) -> NoReturn:
        """Passer the value to this formatter that will pass this value to
        ``cls.formatter`` method and map with the base format string value
        before parse by ``cls.parse``.

        :param value: An any value that able to pass to `cls.formatter` method.
        :type value: Any

        :raises NotImplementedError: This class does not implement this class
            method.
        """
        raise NotImplementedError(
            "The Constant class does not support for passing value to this "
            "class initialization."
        )

    @classmethod
    def parse(
        cls,
        value: String,
        fmt: str | None = None,
        *,
        strict: bool = False,
    ) -> Self:
        """Parse bytes or string value with its format to this formatter object.
        This method generates the value for itself data that can be formatted
        to another format string values.

        :param value: A bytes or string value that match with fmt.
        :type value: String
        :param fmt: a format value.
        :type fmt: str | None(=None)
        :param strict: A flag strict validate that pass to ``set_strict_mode``.
        :type strict: bool(=False)

        :raises NotImplementedError: If an input fmt value does not pass.

        :rtype: Self
        :returns: An instance of formatter that parse from a bytes or string
            value by a format string or base format string if it None.
        """
        if fmt is None:
            raise NotImplementedError(
                "The Constant class does not support for default format string "
                "when parsing with this unknown format value."
            )
        return super().parse(value, fmt, strict=strict)

    def __init__(
        self,
        formats: dict[str, Any] | None = None,
        *,
        set_strict_mode: bool = False,
    ) -> None:
        """Main initialization get the format mapping from input argument
        and generate the necessary attributes for define the value of this
        base formatter object. This process will set the standard value after
        set ``self._constant`` value.
        """
        # Raise if formatter does not set
        if not self.formatter():
            raise NotImplementedError(
                "The Constant object should define the ``cls.base_formatter`` "
                "before make a instance."
            )
        super().__init__(
            formats=formats,
            set_strict_mode=set_strict_mode,
            set_std_value=False,
        )

        # Set ``_constant`` property that contain all arguments from
        # ``cls.__slots__``.
        self._constant: list[str] = [
            getter for v in self.__slots__ if (getter := getattr(self, v, None))
        ]

        # Set standard property by default is string value or ``self.string``.
        self._setter_std_value(flag=True)

    @property
    def value(self) -> list[str]:
        """Return a list of string value that list from ``cls.__slots__``
        attributes.

        :rtype: List[str]
        :returns: A list of string value that list from ``cls.__slots__``
            attributes.
        """
        return self._constant

    @property
    def string(self) -> str:
        """Return string value that was joined with ``|`` value from string
        value of ``self._constant``.
        """
        return "|".join(self._constant)

    @property
    def priorities(self) -> ReturnPrioritiesType:
        """Return a priorities value that define by property of this formatter
        object.

        :rtype: ReturnPrioritiesType
        :returns: a priorities value that define by property of this formatter
            object.
        """
        raise NotImplementedError(
            "Please implement ``priorities`` property for this sub-constant "
            "formatter class"
        )

    @staticmethod
    def formatter(value: str | None = None) -> ReturnFormattersType:
        """Return a formatter value that define by property of this formatter
        object.

        :param value: An any value that want to generate with formatter.
        :type value: str | None(=None)

        :rtype: ReturnFormattersType
        :returns: a formatter value that define by property of this formatter
            object.
        """
        raise NotImplementedError(
            "Please implement ``formatter`` staticmethod for this sub-constant "
            "formatter class"
        )

    @staticmethod
    def prepare_value(value: Any) -> Any:
        """Prepare value before passing to convert logic in the formatter
        method that define by property of this formatter object.

        :param value: A value that want to prepare before passing to formatter.
        :type value: Any

        :rtype: Any
        :returns: An itself input value.
        """
        return value

    def __add__(self, other: Any):  # type: ignore # no cov
        return NotImplemented

    def __sub__(self, other: Any):  # type: ignore # no cov
        return NotImplemented

    def __rsub__(self, other: Any):  # type: ignore # no cov
        return NotImplemented

    def __hash__(self) -> int:
        return hash(tuple(self.value))

    @const_comparison
    def __eq__(self, other: Constant) -> bool:
        return self.value.__eq__(other.value)

    @const_comparison
    def __lt__(self, other: Constant) -> bool:
        return self != other

    @const_comparison
    def __gt__(self, other: Constant) -> bool:
        return self < other


def dict2const(
    fmt: DictStr,
    name: str,
    *,
    base_fmt: str | None = None,
) -> ConstantType:
    """Constant function constructor that receive the dict of format string
    value and constant value.

    :param fmt: A mapping of format string and value of its format that want
        to make constant object.
    :type fmt: DictStr
    :param name: A custom class name that want to rename.
    :type name: str
    :param base_fmt: A base format string value.
    :type base_fmt: str | None(=None)

    :rtype: ConstantType
    :returns: A constant object that construct from an input fmt and name
        values.
    """
    _base_fmt: str = base_fmt or "".join(fmt.keys())

    class CustomConstant(Constant):
        """Dynamic Custom Constant object that will change the class name to an
        input name from constructor function.
        """

        base_fmt: ClassVar[str] = _base_fmt

        __qualname__ = name

        __slots__: tuple[str, ...] = (
            name.lower(),
            "_constant",
            *(convert_fmt_str(f) for f in fmt),
        )

        def __repr__(self) -> str:
            return (
                f"<{self.__class__.__name__}"
                f".parse('{self.string}', "
                f"{'|'.join(self.__search_fmt(c) for c in self._constant)!r})>"
            )

        @staticmethod
        def formatter(  # type: ignore[override]
            v: str | None = None,
        ) -> ReturnFormattersType:
            """Return a formatter value that define by property of this
            formatter object. Generate formatter that support mapping formatter
            with an input dict in fmt value.

            :param v: A constant value that pass to generate all format.
            :type v: str | None(=None)

            :rtype: ReturnFormattersType
            :returns: A generated mapping values of all format string pattern of
                this constant formatter object.
            """
            # It does not use an input value.
            _ = CustomConstant.prepare_value(v)
            return {
                f: {
                    "regex": f"(?P<{convert_fmt_str(f)}>{fmt[f]})",
                    "value": fmt[f],
                }
                for f in fmt.copy()
            }

        @property
        def priorities(self) -> ReturnPrioritiesType:
            """Return a priorities value that define by property of this
            formatter object.

            Level Priority:
                [
                    1: all fmt keys
                ]

            :rtype: ReturnPrioritiesType
            :returns: A properties of the constant formatter object.
            """
            return {
                convert_fmt_str(f): {"value": lambda x: x, "level": 1}
                for f in fmt
            }

        def values(self, value: Any | None = None) -> DictStr:
            """Return the constant values"""
            _ = self.prepare_value(value)
            return fmt

        def __search_fmt(self, value: str) -> str:
            """Return the first format that equal to an input string value.

            :param value:
            :type value: str

            :rtype: str
            :returns: The first format that equal to an input string value.
            """
            return [k for k, v in iter(self.values().items()) if v == value][0]

    CustomConstant.__name__ = name
    return CustomConstant


def make_const(
    name: str | None = None,
    formatter: DictStr | Formatter | None = None,
    *,
    fmt: FormatterType | None = None,
    value: Any | None = None,
) -> ConstantType:
    """Helper constant constructor function that will prepare all input values
    before call ``dict2const`` constructor function.

    :param name: A custom class name that want to rename.
    :type name: str | None(=None)
    :param formatter: ...
    :type formatter: DictStr | Formatter | None
    :param fmt: A formatter object.
    :type fmt: FormatterType | None(=None)
    :param value: A value that want to passer to an input fmt value.
    :type value: Any | None(=None)

    :raises FormatterArgumentError: If an input formatter was passed together
        with an input fmt value.
    :raises FormatterArgumentError: If an input name does not set for construct
        a constant object.

    :rtype: ConstantType
    :returns: A constant object that construct from an input fmt and name
        values.
    """
    base_fmt: str | None = None
    _fmt: DictStr
    if formatter is None:
        if fmt is None or not inspect.isclass(fmt):
            raise FormatterArgumentError(
                "formatter",
                "The Constant constructor function must pass formatter nor fmt "
                "arguments.",
            )
        name = f"{fmt.__name__}Const"
        _fmt = fmt().values(value=value)
        base_fmt = fmt.base_fmt
    elif isinstance(formatter, Formatter):
        return formatter.to_const()
    else:
        _fmt = formatter

    if not name:
        raise FormatterArgumentError("name", "The Constant want name arguments")
    return dict2const(_fmt, name=name, base_fmt=base_fmt)


EnvConst: ConstantType = make_const(
    name="EnvConst",
    formatter={
        "%d": "development",
        "%-d": "dev",
        "%D": "DEVELOPMENT",
        "%-D": "DEV",
        "%s": "sit",
        "%-s": "sit",
        "%S": "SIT",
        "%u": "uat",
        "%-u": "uat",
        "%U": "UAT",
        "%p": "production",
        "%-p": "prd",
        "%P": "PRODUCTION",
        "%-P": "PROD",
        "%t": "test",
        "%-t": "test",
        "%T": "TEST",
        "%b": "sandbox",
        "%-b": "box",
        "%B": "SANDBOX",
        "%-B": "BOX",
        "%c": "poc",
        "%C": "POC",
    },
)


@final
class GenFormatValue(TypedDict):
    """Type Dictionary for value of mapping of ``ReturnGroupGenFormatType``."""

    fmt: str


@final
class ParseValue(TypedDict):
    """Type Dictionary for value of mapping of ``ReturnParseType``."""

    fmt: str
    value: str
    props: DictStr


ReturnGroupGenFormatType: TypeAlias = dict[str, GenFormatValue]
ReturnParseType: TypeAlias = dict[str, ParseValue]


BaseGroupsType: TypeAlias = dict[str, FormatterType]
GroupsType: TypeAlias = dict[str, Formatter]
FormatsGroupType: TypeAlias = Union[
    dict[str, DictStr],
    GroupsType,
    dict[str, Any],
]

Comparator: TypeAlias = Callable[["FormatterGroup", "FormatterGroup"], bool]


def comparison(operator: Comparator) -> Comparator:
    @wraps(operator)
    def wrapper(self: FormatterGroup, other: Any) -> bool:
        if not (
            issubclass(other.__class__, FormatterGroup)
            and (self.__class__.__name__ == other.__class__.__name__)
        ):
            return NotImplemented
        return operator(self, other)

    return wrapper


class FormatterGroup:
    """Group of Formatters with dynamic group naming like 'timestamp' for
    Datetime, 'name' for Naming. This class will use for ``make_group``
    constructor function because of different and complicate group of formatter
    instances.

    :param formats: A mapping value of priority attribute data.
    :type formats: FormatsGroupType
    :param ignore_construct: A flag for ignore pass an input formats value to
        validate and construct function.
    :type ignore_construct: bool(=False)

    :raises FormatterGroupValueError: If any group naming from an input formats
        does not exist in ``cls.base_groups`` value.

    .. class-attributes::
        * base_groups: BaseGroupsType
            The base group of naming and Formatter class.

    .. class-method::
        * __parse: ReturnParseType
            A mapping of fmt, value, and props keys that passing from searching
            step with `re` module.
        * parse: Self
            An instance of formatter group that parse from a bytes or string
            value by a format string.
        * gen_format: Tuple[str, ReturnGroupGenFormatType]
            A tuple of group naming and format string value that change format
            string to regular expression string for complied to the `re` module.
        * from_formatter: Self
            An instance of formatter group that was pass formats value directly
            to its formatter object.
        * from_value: Self
            An instance of formatter group that was use ``cls.from_value``
            method from any formatter object and its value.

    .. attributes::
        * groups: GroupsType
            A dict of group naming and Formatter instance.

    .. methods::
        * __construct_groups: [str, Union[DictStr, Formatter, Any]] -> Formatter
            A Formatter instance.
        * format: [str] -> str
            A string value that was formatted and filled by an input format
            string pattern.
        * adjust: [Dict[str, Any]] -> Self
            Adjust any formatter instance in ``self.groups`` of this formatter
            group.
        * to_const: list[str] | None -> FormatterGroupType
            A FormatterGroup object that create from constant of ``self.groups``
            values.

    .. seealso::

        This class is an abstract class for any formatter group that override
    the ``cls.base_groups`` value with mapping for group naming and Formatter
    object.
    """

    # This value must reassign from child class
    base_groups: BaseGroupsType = {}

    def __init_subclass__(cls: FormatterGroupType, **kwargs: Any) -> NoReturn:
        """Subclass Initialize method."""
        super().__init_subclass__(**kwargs)

        if not cls.base_groups:
            raise NotImplementedError(
                "Please implement base_groups class property for this "
                "sub-formatter group class."
            )

    @classmethod
    def from_formats(
        cls,
        formats: dict[str, DictStr],
    ) -> Self:
        """Passer the formats to this formatter group directly to its formatter
        object.

        :param formats: A dict of group naming and formats of its group that
            pass directly to formatter object.
        :type formats: Dict[str, DictStr]

        :raises FormatterGroupValueError: If any group naming from an input
            formats does not exist in ``cls.base_groups`` value.

        :rtype: Self
        :returns: An instance of formatter group that was pass formats value
            directly to its formatter object.
        """
        rs: GroupsType = {}
        for k, v in formats.items():
            if k not in cls.base_groups:
                raise FormatterGroupValueError(
                    f"{cls.__name__} does not support for this group name, "
                    f"{k!r}."
                )
            rs[k] = cls.base_groups[k](v)
        return cls(formats=rs, ignore_construct=True)

    @classmethod
    def from_value(
        cls,
        values: dict[str, Any],
    ) -> Self:
        """Passer the value to this formatter group that will pass this value to
        ``cls.from_value`` method of its formatter.

        :param values: A dict of group naming and value of its group that pass
            to `cls.form_value` of formatter object.
        :type values: Dict[str, Any]

        :raises FormatterGroupValueError: If any group naming from an input
            formats does not exist in ``cls.base_groups`` value.

        :rtype: Self
        :returns: An instance of formatter group that was use ``cls.from_value``
            method from any formatter object and its value.
        """
        rs: GroupsType = {}
        for k, v in values.items():
            if k not in cls.base_groups:
                raise FormatterGroupValueError(
                    f"{cls.__name__} does not support for this group name, "
                    f"{k!r}."
                )
            rs[k] = cls.base_groups[k].from_value(v)
        return cls(formats=rs, ignore_construct=True)

    @classmethod
    def parse(
        cls,
        value: String,
        fmt: str,
    ) -> Self:
        """Parse bytes or string value with its format to this formatter object.
        This method generates the value for itself data that can be formatted
        to another format string values.

        :param value: A bytes or string value that match with fmt.
        :type value: String
        :param fmt: a format string value that must have the formatter group
            pattern like `{group-name:fmt-str}`.
        :type fmt: str

        :rtype: Self
        :returns: An instance of formatter group that parse from a bytes or
            string value by a format string.
        """
        parser_rs: ReturnParseType = cls.__parse(bytes2str(value), fmt)
        rs: dict[str, DictStr] = defaultdict(dict)
        for g in parser_rs:
            rs[g.split("__")[0]] |= parser_rs[g]["props"]
        return cls(formats=rs)

    @classmethod
    def __parse(
        cls,
        value: str,
        fmt: str,
    ) -> ReturnParseType:
        """Private Parse that return a mapping of necessary value for main
        parsing method.

        :param value: A string value that match with fmt.
        :type value: str
        :param fmt: a format string value that must have the formatter group
            pattern like `{group-name:fmt-str}`.
        :type fmt: str

        :raises FormatterGroupArgumentError: If value does not match with format
            pattern value from ``cls.gen_format``.

        :rtype: ReturnParseType
        :returns: A mapping of fmt, value, and props keys that passing
            from searching step with `re` module.
        """
        _fmt, _fmt_getter = cls.gen_format(fmt=fmt)
        if not (_search := re.search(rf"^{_fmt}$", value)):
            raise FormatterGroupArgumentError(
                "format",
                f"{value!r} does not match with the format: '^{_fmt}$'",
            )

        _search_dict: DictStr = _search.groupdict()
        rs: ReturnParseType = {}
        for name in iter(_fmt_getter.copy()):
            rs[name] = {
                "fmt": _fmt_getter[name]["fmt"],
                "value": _search_dict.pop(name),
                "props": {
                    k.replace(f"{name}___", "", 1): _search_dict.pop(k)
                    for k in filter(
                        lambda x: x.startswith(f"{name}___"),
                        _search_dict.copy(),
                    )
                },
            }
        return rs

    @classmethod
    def gen_format(cls, fmt: str) -> tuple[str, ReturnGroupGenFormatType]:
        """Generate format string value that combine from any matching of
        format name to regular expression value that able to search with any
        input value string.

        :param fmt: a format string value pass from input argument.
        :type fmt: str

        :rtype: Tuple[str, ReturnGroupGenFormatType]
        :returns: A tuple of group naming and format string value that change
            format string to regular expression string for complied to the `re`
            module.
        """
        fmt_getter: ReturnGroupGenFormatType = {}
        for group, formatter in cls.base_groups.items():
            for _index, fmt_match in enumerate(
                re.finditer(
                    rf"(?P<found>{{{group}:?(?P<format>[^{{}}]+)?}})",
                    fmt,
                ),
                start=0,
            ):
                # Format Dict Example:
                # {'name': '{timestamp:%Y_%m_%d}', 'format': '%Y_%m_%d'}
                fmt_dict: DictStr = fmt_match.groupdict()
                fmt_str: str
                if not (fmt_str := fmt_dict["format"]):
                    fmt_str = formatter.base_fmt
                group_index: str = f"{group}{scache(_index)}"
                fmt_re = formatter.gen_format(
                    fmt_str,
                    prefix=f"{group_index}___",
                    suffix=scache(_index),
                )
                fmt = fmt.replace(
                    fmt_dict["found"],
                    f"(?P<{group_index}>{fmt_re})",
                    1,
                )
                fmt_getter[group_index] = {"fmt": fmt_str}
        return fmt, fmt_getter

    def format(self, fmt: str) -> str:
        """Return a string value that was formatted and filled by an input
        format string pattern.

        :param fmt: A format string value for mapping with formatter group.
        :type fmt: str

        :raises FormatterGroupValueError: If group naming on format string
            pattern does not exist in ``self.base_groups``.
        :raises FormatterGroupArgumentError: If any group of formatter raise
            FormatterKeyError from ``format`` method.

        :rtype: str
        :returns: A string value that was filled and formatted by an input
            format pattern.
        """
        for fmt_match in re.finditer(
            r"(?P<found>{(?P<group>\w+):?(?P<format>[^{}]+)?})", fmt
        ):
            # Format Dict Example::
            # {
            #   'name': '{timestamp:%Y_%m_%d}',
            #   'group': 'timestamp',
            #   'format': '%Y_%m_%d'
            # }
            fmt_dict: DictStr = fmt_match.groupdict()
            if (group := fmt_dict["group"]) not in self.base_groups:
                raise FormatterGroupValueError(
                    f"This group, {group!r}, does not set on `cls.base_groups`."
                )
            formatter: Formatter = self.groups[group]
            fmt_str: str
            if not (fmt_str := fmt_dict["format"]):
                fmt_str = formatter.base_fmt

            try:
                fmt = fmt.replace(
                    fmt_dict["found"],
                    formatter.format(fmt=fmt_str),
                    1,
                )
            except FormatterKeyError as err:
                raise FormatterGroupArgumentError(
                    "format", f"{err} in {fmt_dict['found']}"
                ) from err
        return fmt

    def __init__(
        self,
        formats: FormatsGroupType,
        *,
        ignore_construct: bool = False,
    ) -> None:
        """Main initialization that get the formats value, a mapping of group
        naming and formatter instance from an input argument and generate the
        ``self.groups`` attributes for define the value of this formatter group
        instance.
        """
        # Make default formatter instance from `cls.base_groups` mapping.
        self.groups: GroupsType = {
            group: fmt() for group, fmt in self.base_groups.items()
        }
        if not ignore_construct:
            for k, v in formats.items():
                if k not in self.base_groups:
                    raise FormatterGroupValueError(
                        f"{self.__class__.__name__} does not support for this "
                        f"group name, {k!r}."
                    )
                self.groups[k] = self.__construct_groups(k, v)
        else:
            self.groups.update(formats)

    def __construct_groups(
        self,
        group: str,
        v: Union[DictStr, Formatter, Any],
    ) -> Formatter:
        """Group attribute constructor function that receive any value that
        able to pass with Formatter object.

        :param group: A group naming value.
        :type group: str
        :param v: A value of this group naming that want to dynamic construct.
        :type v: Union[DictStr, Formatter, Any]

        :rtype: Formatter
        :returns: A Formatter instance.
        """
        if isinstance(v, Formatter):
            return v
        elif isinstance(v, dict):
            return self.base_groups[group](v)
        return self.base_groups[group].from_value(v)

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __repr__(self) -> str:
        values: list[str] = []
        fmts: list[str] = []
        for group in self.base_groups:
            formatter: Formatter = self.groups[group]
            values.append(formatter.string)
            fmts.append(formatter.base_fmt)
        return (
            f"<{self.__class__.__name__}"
            f".parse(value={'_'.join(values)!r}, "
            f"fmt={'_'.join(fmts)!r})>"
        )

    def __str__(self) -> str:
        return ", ".join(v.string for v in self.groups.values())

    @comparison
    def __eq__(self, other: Self) -> bool:
        return all(self.groups[g] == other.groups[g] for g in self.base_groups)

    @comparison
    def __gt__(self, other: Self) -> bool:
        return any(
            self.groups[g].__gt__(other.groups[g]) for g in self.base_groups
        ) and all(
            not self.groups[g].__lt__(other.groups[g]) for g in self.base_groups
        )

    @comparison
    def __lt__(self, other: Self) -> bool:
        return any(
            self.groups[g].__lt__(other.groups[g]) for g in self.base_groups
        ) and all(
            not self.groups[g].__gt__(other.groups[g]) for g in self.base_groups
        )

    def adjust(self, values: dict[str, Any]) -> Self:  # no cov
        """Adjust value to any formatter instance in ``self.groups`` of this
        formatter group.

        :param values: A mapping of group and its value that able to adding
            to origin value.
        :type values: Dict[str, Any]

        :raises FormatterGroupValueError: If any key in an input value does not
            exist in ``self.base_groups``.

        :rtype: FormatterGroup
        :returns: Self that was adjusted the value.
        """
        _keys: list[str] = [
            f"{k!r}" for k in values if k not in self.base_groups
        ]
        if _keys:
            raise FormatterGroupValueError(
                f"Key of values, {', '.join(_keys)}, does not support for this "
                f"{self.__class__}."
            )
        _groups: GroupsType = {
            k: (fmt + values[k]) if k in values else fmt
            for k, fmt in self.groups.items()
        }
        return self.__class__(formats=_groups)

    def to_const(
        self,
        included: list[str] | None = None,
    ) -> FormatterGroupType:  # no cov
        """Convert this formatter group instance to constant group object.

        :rtype: FormatterGroupType
        :returns: A FormatterGroup object that create from constant of
            ``self.groups`` values.
        """
        _inc: list[str] = included or list(self.groups.keys())
        if any(i not in self.base_groups for i in _inc):
            raise FormatterGroupArgumentError(
                "included",
                (
                    f"It must be existing group naming in this {self.__class__}"
                    f" , the naming in {list(self.base_groups.keys())}."
                ),
            )
        return make_group(
            group={
                k: v.to_const() if k in _inc else v.__class__
                for k, v in self.groups.items()
            }
        )


def make_group(group: BaseGroupsType) -> FormatterGroupType:
    """Making Formatter Group constructor function that return a FormatterGroup
    class from an input group value.

    :param group: A dict of group naming and Formatter class.
    :type group: BaseGroupsType

    :raises FormatterGroupValueError: If any value in an input group does not
        be subclassed of Formatter instance.
    :raises FormatterGroupArgumentError: If any value in an input group does not
        be objected that mean this value is any instance.

    :rtype: FormatterGroupType
    :returns: A FormatterGroup class that construct from an input group value.
    """
    # Validate argument group that should contain ``FormatterType``
    for _ in group.values():
        try:
            if not issubclass(_, Formatter):
                raise FormatterGroupValueError(
                    f"Make group constructor function want group with type, "
                    f"Dict[str, FormatterType], not {_.__name__!r}."
                )
        except TypeError as err:
            raise FormatterGroupArgumentError(
                "group",
                (
                    f"Make group constructor function want group with type, "
                    f"Dict[str, FormatterType], not instance of "
                    f"{_.__class__.__name__!r}."
                ),
            ) from err

    name: str = f'{"".join(_.__name__ for _ in group.values())}Group'

    @total_ordering
    class CustomGroup(FormatterGroup):
        """Dynamic Custom Group of Formatter objects that will change the class
        name to an input name from constructor function.
        """

        base_groups: BaseGroupsType = group

        __qualname__ = name

    CustomGroup.__name__ = name
    return CustomGroup


__all__ = (
    "WEEKS",
    "WEEKS_FULL",
    "MONTHS",
    "Formatter",
    "FormatterType",
    "ReturnPrioritiesType",
    "ReturnFormattersType",
    "Serial",
    "Datetime",
    "Version",
    "Naming",
    "SlotLevel",
    "Storage",
    "ConstantType",
    "Constant",
    "EnvConst",
    "dict2const",
    "make_const",
    "FormatterGroup",
    "FormatterGroupType",
    "make_group",
)
