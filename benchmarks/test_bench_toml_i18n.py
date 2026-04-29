"""Benchmarks for toml-i18n."""

from __future__ import annotations

import io
import sys

import pytest

pytestmark = pytest.mark.benchmark


class _SuppressStdout:
    """Context manager to silence noisy stdout during benchmark calls."""

    def __enter__(self):
        self._old = sys.stdout
        sys.stdout = io.StringIO()
        return self

    def __exit__(self, exc_type, exc, tb):
        sys.stdout = self._old


def _run(translate, key, **kwargs):
    with _SuppressStdout():
        return translate(key, **kwargs)


def test_toml_i18n_simple(benchmark, toml_i18n_translate):
    benchmark.group = "simple"
    benchmark.extra_info["library"] = "toml_i18n"
    benchmark(_run, toml_i18n_translate, "general.welcome")


def test_toml_i18n_nested(benchmark, toml_i18n_translate):
    benchmark.group = "nested"
    benchmark.extra_info["library"] = "toml_i18n"
    benchmark(_run, toml_i18n_translate, "general.messages.success")


def test_toml_i18n_params(benchmark, toml_i18n_translate):
    benchmark.group = "params"
    benchmark.extra_info["library"] = "toml_i18n"
    # Note: toml-i18n returns the template without substitution.
    benchmark(_run, toml_i18n_translate, "general.greeting")
