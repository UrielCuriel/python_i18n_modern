"""Benchmarks for python-i18n."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.benchmark


def test_python_i18n_simple(benchmark, python_i18n_module):
    benchmark.group = "simple"
    benchmark.extra_info["library"] = "python_i18n"
    benchmark(python_i18n_module.t, "welcome")


def test_python_i18n_nested(benchmark, python_i18n_module):
    benchmark.group = "nested"
    benchmark.extra_info["library"] = "python_i18n"
    benchmark(python_i18n_module.t, "messages.success")


def test_python_i18n_params(benchmark, python_i18n_module):
    benchmark.group = "params"
    benchmark.extra_info["library"] = "python_i18n"
    benchmark(lambda: python_i18n_module.t("greeting", name="Alice"))
