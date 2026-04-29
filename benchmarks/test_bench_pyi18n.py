"""Benchmarks for pyi18n-v2."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.benchmark


def test_pyi18n_simple(benchmark, pyi18n_instance):
    benchmark.group = "simple"
    benchmark.extra_info["library"] = "pyi18n"
    benchmark(pyi18n_instance.gettext, "en", "welcome")


def test_pyi18n_nested(benchmark, pyi18n_instance):
    benchmark.group = "nested"
    benchmark.extra_info["library"] = "pyi18n"
    benchmark(pyi18n_instance.gettext, "en", "messages.success")


def test_pyi18n_params(benchmark, pyi18n_instance):
    benchmark.group = "params"
    benchmark.extra_info["library"] = "pyi18n"
    benchmark(lambda: pyi18n_instance.gettext("en", "greeting", name="Alice"))
