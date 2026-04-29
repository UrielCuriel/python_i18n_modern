"""Benchmarks for i18n_modern."""

from __future__ import annotations

from pathlib import Path

import pytest

from i18n_modern import I18nModern

pytestmark = pytest.mark.benchmark


# --- group: simple ---------------------------------------------------------


def test_modern_simple(benchmark, i18n_modern_instance):
    benchmark.group = "simple"
    benchmark.extra_info["library"] = "i18n_modern"
    benchmark(i18n_modern_instance.get, "welcome")


# --- group: nested ---------------------------------------------------------


def test_modern_nested(benchmark, i18n_modern_instance):
    benchmark.group = "nested"
    benchmark.extra_info["library"] = "i18n_modern"
    benchmark(i18n_modern_instance.get, "messages.success")


# --- group: params ---------------------------------------------------------


def test_modern_params(benchmark, i18n_modern_instance):
    benchmark.group = "params"
    benchmark.extra_info["library"] = "i18n_modern"
    values = {"name": "Alice"}
    benchmark(lambda: i18n_modern_instance.get("greeting", values=values))


# --- group: conditional ----------------------------------------------------


def test_modern_conditional(benchmark, i18n_modern_instance):
    benchmark.group = "conditional"
    benchmark.extra_info["library"] = "i18n_modern"
    values = {"age": 25}
    benchmark(lambda: i18n_modern_instance.get("age_group", values=values))


# --- group: parallel_load --------------------------------------------------


def test_modern_parallel_load(benchmark, locales_dir: Path):
    """Loads the same file 4 times in parallel via load_many."""
    benchmark.group = "parallel_load"
    benchmark.extra_info["library"] = "i18n_modern"
    en_path = str(locales_dir / "en.json")
    files = [(en_path, f"en{i}") for i in range(4)]

    def do_load() -> None:
        I18nModern("en").load_many(files)

    # parallel_load is heavy; few rounds, no per-round iterations
    benchmark.pedantic(do_load, rounds=10, iterations=1, warmup_rounds=1)
