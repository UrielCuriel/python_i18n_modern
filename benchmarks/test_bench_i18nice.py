"""Benchmarks for i18nice."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.benchmark


def test_i18nice_simple(benchmark, i18nice_module):
    benchmark.group = "simple"
    benchmark.extra_info["library"] = "i18nice"
    benchmark(i18nice_module.t, "translations.welcome")


def test_i18nice_nested(benchmark, i18nice_module):
    benchmark.group = "nested"
    benchmark.extra_info["library"] = "i18nice"
    benchmark(i18nice_module.t, "translations.messages.success")


def test_i18nice_params(benchmark, i18nice_module):
    benchmark.group = "params"
    benchmark.extra_info["library"] = "i18nice"
    benchmark(lambda: i18nice_module.t("translations.greeting", name="Alice"))
