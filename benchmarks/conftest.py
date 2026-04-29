"""
Shared fixtures and configuration for the i18n benchmark suite.

Run with:
    pytest benchmarks/ --benchmark-only

Useful flags:
    --benchmark-min-rounds=20         Force at least N rounds per benchmark.
    --benchmark-warmup=on             Run warmup iterations (recommended).
    --benchmark-warmup-iterations=1000
    --benchmark-disable-gc            (default) Disable GC during measurement.
    --benchmark-sort=mean             Sort results by mean time.
    --benchmark-group-by=group        Group results by `group` arg in @mark.
    --benchmark-save=NAME             Save run as a baseline.
    --benchmark-compare=NAME          Compare against a saved baseline.
    --benchmark-json=out.json         Write machine-readable results.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

LOCALES_DIR = Path(__file__).parent.parent / "examples" / "locales"
EN_JSON = LOCALES_DIR / "en.json"


# ---------------------------------------------------------------------------
# Raw data
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def locales_dir() -> Path:
    return LOCALES_DIR


@pytest.fixture(scope="session")
def en_data() -> dict[str, Any]:
    with open(EN_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# i18n_modern
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def i18n_modern_instance(en_data: dict[str, Any]):
    from i18n_modern import I18nModern

    return I18nModern("en", en_data)


# ---------------------------------------------------------------------------
# python-i18n
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def python_i18n_module(locales_dir: Path):
    import i18n as py_i18n

    py_i18n.set("locale", "en")
    py_i18n.set("filename_format", "{namespace}.{locale}.json")
    py_i18n.set("file_format", "json")
    # Compatibility across i18n variants: some use `default_locale`, others `fallback`.
    try:
        py_i18n.set("default_locale", "en")
    except KeyError:
        py_i18n.set("fallback", "en")
    py_i18n.load_path.clear()  # type: ignore[attr-defined]
    py_i18n.load_path.append(str(locales_dir))  # type: ignore[attr-defined]
    return py_i18n


# ---------------------------------------------------------------------------
# pyi18n-v2
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def pyi18n_instance(locales_dir: Path):
    import pyi18n
    from pyi18n.loaders import PyI18nJsonLoader

    loader = PyI18nJsonLoader(str(locales_dir))
    return pyi18n.PyI18n(available_locales=("en",), loader=loader)


# ---------------------------------------------------------------------------
# i18nice
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def i18nice_module(locales_dir: Path):
    try:
        import i18n as i18nice_lib
    except ImportError:  # pragma: no cover
        pytest.skip("i18nice not installed")

    i18nice_lib.set("locale", "en")  # type: ignore[attr-defined]
    i18nice_lib.set("file_format", "json")  # type: ignore[attr-defined]
    i18nice_lib.set("filename_format", "{namespace}.{locale}.{format}")  # type: ignore[attr-defined]
    i18nice_lib.set("enable_memoization", True)  # type: ignore[attr-defined]
    i18nice_lib.load_path.clear()  # type: ignore[union-attr]
    i18nice_lib.load_path.append(str(locales_dir))  # type: ignore[union-attr]

    try:
        i18nice_lib.load_everything()  # type: ignore[attr-defined]
    except (AttributeError, TypeError):
        pass

    return i18nice_lib


# ---------------------------------------------------------------------------
# toml-i18n
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def toml_i18n_translate(locales_dir: Path):
    try:
        from toml_i18n import TomlI18n
        from toml_i18n import i18n as toml_i18n_translate
    except ImportError:  # pragma: no cover
        pytest.skip("toml-i18n not installed")

    try:
        TomlI18n.initialize(
            locale="en", fallback_locale="en", directory=str(locales_dir)
        )
    except Exception:
        pass

    return toml_i18n_translate
