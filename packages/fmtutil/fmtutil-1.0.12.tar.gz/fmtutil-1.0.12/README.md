# Formatter

[![test](https://github.com/korawica/fmtutil/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/korawica/fmtutil/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/korawica/fmtutil/branch/main/graph/badge.svg?token=J2MN63IFT0)](https://codecov.io/gh/korawica/fmtutil)
[![pypi version](https://img.shields.io/pypi/v/fmtutil?logo=pypi&logoColor=white&label=pypi)](https://pypi.org/project/fmtutil/)
[![python support version](https://img.shields.io/pypi/pyversions/fmtutil?logo=pypi&logoColor=white)](https://pypi.org/project/fmtutil/)
[![size](https://img.shields.io/github/languages/code-size/korawica/fmtutil?logo=webpack&logoColor=white)](https://github.com/korawica/fmtutil)
[![gh license](https://img.shields.io/github/license/ddeutils/ddeutil-workflow)](https://github.com/ddeutils/ddeutil-workflow/blob/main/LICENSE)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![type check: mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

Lightweight formatter objects, this fmtutil package was created for `parse`
and `format` any string values that match a format pattern which created base on
Python regular expression.

:dart: First objective of this project is include necessary formatter objects for
any data components package which mean we can `parse` any complicate names on
data source and ingest the right names to in-house or data target.

## :round_pushpin: Installation

```shell
pip install -U fmtutil[all]
```

**Python version supported**:

| Python Version | Installation                        | Support Fixed Bug  |
|----------------|-------------------------------------|--------------------|
| `== 3.8`       | `pip install "fmtutil>=0.4,<0.5.0"` | :x:                |
| `>=3.9,<3.14`  | `pip install -U fmtutil`            | :heavy_check_mark: |

> [!NOTE]
> This package has one dependency package, `python-dateutil`, this package use
> for support add and sub datetime value on the Datetime formatter only.
> If you do not want to install this package, you can use `pip install -U fmtutil`.

## :beers: Introduction

For example, we want to get filename with the format like, `filename_20220101.csv`,
on the file system storage, and we want to incremental ingest the latest file with
date **2022-03-25** date. So we will implement `Datetime` object and parse
that filename to it,

```python
assert (
    Datetime.parse('filename_20220101.csv', 'filename_%Y%m%d.csv').value
    == datetime.datetime(2022, 1, 1, 0)
)
```

The above example is :yawning_face: **NOT SURPRISE!!!** for you right?
Because the Python already provide the build-in `datetime` to parse by `datetime.strptime`
and format by `{dt}.strftime` :banana:.

This package will be the special thing when we group more than one format-able
objects together as `Naming`, `Version`, and `Datetime`.
For a complex filename format like :triumph:;

```text
{filename:%s}_{datetime:%Y_%m_%d}.{version:%m.%n.%c}.csv
```

> [!WARNING]
> **Disclaimer**: The above filename format, the `datetime` package that already
> build-in in Python does not enough for this scenario :snake: but you can handle by your
> code function or create the better package than this project :dash:.

> [!NOTE]
> Any formatter object was implemented the `self.valid` method for help us validate
> format string value like the above the example scenario,
> ```python
> this_date = Datetime.parse('20220101', '%Y%m%d')
> assert this_date.valid('any_files_20220101.csv', 'any_files_%Y%m%d.csv')
> ```

## :tada: Usage

If you have multi-format filenames on the data source directory, and you want to
dynamic getting max datetime on these filenames to your app, you can use a
formatter group.

```python
from fmtutil import (
  make_group, Naming, Datetime, FormatterGroup, FormatterGroupType, FormatterArgumentError,
)

name: Naming = Naming.parse('Google Map', fmt='%t')

fmt_group: FormatterGroupType = make_group({
    "naming": name.to_const(),
    "timestamp": Datetime,
})

rs: list[FormatterGroup] = []
for file in (
    'googleMap_20230101.json',
    'googleMap_20230103.json',
    'googleMap_20230103_bk.json',
    'googleMap_with_usage_20230105.json',
    'googleDrive_with_usage_20230105.json',
):
    try:
        rs.append(
            fmt_group.parse(file, fmt=r'{naming:c}_{timestamp:%Y%m%d}\.json')
        )
    except FormatterArgumentError:
        continue

repr(max(rs).groups['timestamp'])
```

```text
>>> <Datetime.parse('2023-01-03 00:00:00.000000', '%Y-%m-%d %H:%M:%S.%f')>
```

> [!TIP]
> The above **Example** will convert the `name`, **Naming** instance, to **Constant**
> instance before passing to the **Formatter Group** because it does not want
> to dynamic parsing this format when find any matching filenames at destination
> path.

## :dart: Next Step

I will change formatter object construction from changing with inside method to
assert design. The code already implement and testing stage at file `__assets.py`.

That mean, you can create any formatter object by dynamic asset changed strategy.

```python
class Datetime(Formatter, asset=DATETIME_ASSET, config=DATETIME_CONF, level=10):
    """Datetime Formatter object."""
    ...
```

## :speech_balloon: Contribute

I do not think this project will go around the world because it has specific propose
and you can create by your coding without this project dependency for long term
solution. So, on this time, you can open [the GitHub issue on this project :raised_hands:](https://github.com/korawica/fmtutil/issues)
for fix bug or request new feature if you want it.
