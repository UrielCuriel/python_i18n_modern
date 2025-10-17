"""
Module to get translation from locales.

Author: Uriel Curiel <urielcurrel@outlook.com>
"""

import json
import logging
from pathlib import Path
from typing import cast

from i18n_modern.helpers import eval_key, format_value, get_deep_value, merge_deep
from i18n_modern.types import FormatParam, LocaleDict, Locales, LocaleValue

yaml_available = False
try:
    import yaml

    yaml_available = True
except ImportError:
    yaml = None

toml_available = False
try:
    import tomli

    toml_available = True
except ImportError:
    tomli = None


class I18nModern:
    """
    Gets the translation from a locales variable.

    Args:
        default_locale: The default locale
        locales: The locales variable (dict) or path to locale file
    """

    def __init__(self, default_locale: str, locales: LocaleDict | str | None = None):
        self._locales: Locales = {}
        self._default_locale: str = default_locale
        self._previous_translations: dict[tuple[object, ...], str] = {}

        if locales:
            if isinstance(locales, str):
                self.load_from_file(locales, default_locale)
            else:
                self.load_from_value(locales, default_locale)

    @property
    def default_locale(self) -> str:
        """Get the default locale."""
        return self._default_locale

    @default_locale.setter
    def default_locale(self, value: str):
        """Set the default locale."""
        self._default_locale = value

    def load_from_file(self, file_path: str, locale_identify: str):
        """
        Load locales from a file (JSON, YAML, or TOML).

        Args:
            file_path: Path to the locale file
            locale_identify: Locale identifier
        """
        path: Path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Locale file not found: {file_path}")

        suffix: str = path.suffix.lower()

        if suffix == ".json":
            with open(path, "r", encoding="utf-8") as f:
                data: LocaleDict = cast(LocaleDict, json.load(f))
        elif suffix in [".yaml", ".yml"]:
            if not yaml_available or yaml is None:
                raise ImportError("PyYAML is required for YAML support. Install with: pip install pyyaml")
            with open(path, "r", encoding="utf-8") as f:
                data = cast(LocaleDict, yaml.safe_load(f))  # type: ignore
        elif suffix == ".toml":
            if not toml_available or tomli is None:
                raise ImportError("tomli is required for TOML support. Install with: pip install tomli")
            with open(path, "rb") as f:
                data = cast(LocaleDict, tomli.load(f))  # type: ignore
        else:
            raise ValueError(f"Unsupported file format: {suffix}. Supported formats: .json, .yaml, .yml, .toml")

        self._locales[locale_identify] = merge_deep(self._locales.get(self._default_locale), data)

    def load_from_value(self, locales: LocaleDict, locale_identify: str):
        """
        Load locales from a dictionary value.

        Args:
            locales: The locales dictionary
            locale_identify: Locale identifier
        """
        self._locales[locale_identify] = merge_deep(self._locales.get(self._default_locale), locales)

    def get(self, key: str, locale: str | None = None, values: FormatParam | None = None) -> str:
        """
        Get a translation with memoization from a key and format params.

        Args:
            key: Translation key (supports dot notation)
            locale: Optional locale override
            values: Optional values for placeholder replacement

        Returns:
            Translated string
        """
        try:
            locale = locale or self._default_locale
            values_tuple = tuple(sorted(values.items())) if values else None
            cache_key = (key, locale, values_tuple)

            if cache_key in self._previous_translations:
                return self._previous_translations[cache_key]

            if locale not in self._locales:
                raise KeyError(f"Locale '{locale}' not found in locales")

            translation: LocaleValue | None = get_deep_value(self._locales[locale], key)

            if translation is None:
                raise KeyError(f"Translation key '{key}' not found in locale '{locale}'")

            result = self._get_translation(translation, values)
            self._previous_translations[cache_key] = result
            return result

        except Exception as error:
            logging.warning("Error: the key '%s' is not defined in locales - %s", key, error)
            return key

    def _get_translation(
        self, translation: LocaleValue, values: FormatParam | None = None, default_translation: str | None = None
    ) -> str:
        """
        Get a translation from object and format it.

        Args:
            translation: Translation value (string or dict)
            values: Optional values for placeholder replacement
            default_translation: Optional default translation

        Returns:
            Formatted translation string
        """
        if isinstance(translation, dict) and "default" in translation:
            default_translation = str(translation["default"])

        if not isinstance(translation, str):
            # Find matching key based on condition
            for key in translation.keys():  # type: ignore
                if eval_key(key, values):  # type: ignore
                    return self._get_translation(
                        translation[key],
                        values,
                        default_translation,  # type: ignore
                    )

            # Return default if no key matches
            if default_translation:
                return self._get_translation(default_translation, values, default_translation)  # type: ignore
            return ""

        return format_value(translation, values)
