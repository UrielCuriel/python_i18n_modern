"""
Backwards-compatible entry point for the benchmark suite.

The real benchmarks now live under `benchmarks/` and are powered by
pytest-benchmark, which provides warmup, GC control, calibration and
proper statistics (min/mean/median/stddev/ops). This wrapper just
forwards to it so existing workflows keep working.

Examples:
    python benchmark_comparison.py
    python benchmark_comparison.py -k simple
    python benchmark_comparison.py --benchmark-save=baseline
    python benchmark_comparison.py --benchmark-compare=baseline

See `benchmarks/README.md` for full documentation.
"""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    try:
        import pytest  # noqa: F401
    except ImportError:
        print(
            "ERROR: pytest / pytest-benchmark are not installed.\n"
            "Install the benchmark extras:\n"
            '    pip install -e ".[benchmark]"\n'
            "or:\n"
            "    uv sync --extra benchmark",
            file=sys.stderr,
        )
        return 1

    import pytest

    bench_dir = Path(__file__).parent / "benchmarks"
    args = [str(bench_dir), "--benchmark-only", *sys.argv[1:]]
    return int(pytest.main(args))


if __name__ == "__main__":
    raise SystemExit(main())
