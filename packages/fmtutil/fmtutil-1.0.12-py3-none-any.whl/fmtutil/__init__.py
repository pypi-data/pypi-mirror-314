# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
import logging

from .__about__ import (
    __version__,
    __version_tuple__,
)
from .__version import (
    BaseVersion as Ver,
)
from .__version import (
    VersionPackage as VerPackage,
)
from .__version import (
    VersionSemver as VerSemver,
)
from .exceptions import (
    FormatterArgumentError,
    FormatterError,
    FormatterGroupArgumentError,
    FormatterGroupValueError,
    FormatterKeyError,
    FormatterValueError,
)
from .formatter import (
    Constant,
    ConstantType,
    Datetime,
    EnvConst,
    Formatter,
    FormatterGroup,
    FormatterGroupType,
    FormatterType,
    Naming,
    ReturnFormattersType,
    ReturnPrioritiesType,
    Serial,
    Storage,
    Version,
    dict2const,
    make_const,
    make_group,
)

logging.getLogger(__name__)

__all__ = (
    "Formatter",
    "FormatterType",
    "Serial",
    "Datetime",
    "Version",
    "Naming",
    "Storage",
    "ConstantType",
    "Constant",
    "EnvConst",
    "dict2const",
    "make_const",
    "FormatterGroup",
    "FormatterGroupType",
    "make_group",
    "FormatterArgumentError",
    "FormatterError",
    "FormatterKeyError",
    "FormatterValueError",
    "FormatterGroupArgumentError",
    "FormatterGroupValueError",
    "ReturnFormattersType",
    "ReturnPrioritiesType",
    "Ver",
    "VerPackage",
    "VerSemver",
    "__version__",
    "__version_tuple__",
)
