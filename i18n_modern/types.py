"""Type definitions for :mod:`i18n_modern`."""

from typing import TypeAlias  # ty:ignore[unresolved-import]

LocaleValue: TypeAlias = "str | LocaleDict"
LocaleDict: TypeAlias = dict[str, LocaleValue]  # ty:ignore[invalid-type-form]
Locales: TypeAlias = dict[str, LocaleDict]

FormatValue: TypeAlias = bool | float | int | str  # ty:ignore[unsupported-operator]
FormatParam: TypeAlias = dict[str, FormatValue]

__all__ = [
    "FormatParam",
    "FormatValue",
    "LocaleDict",
    "LocaleValue",
    "Locales",
]
