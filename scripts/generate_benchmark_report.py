"""
Convert pytest-benchmark JSON output(s) to a Markdown report.

Two modes:

1. Explicit JSON file:

       python scripts/generate_benchmark_report.py bench.json -o BENCHMARK_REPORT.md

2. Auto-discover from `.benchmarks/` (default when no path is given). For
   every (machine, save-name) pair we pick the latest file (highest NNNN_
   prefix) and concatenate them into a single report:

       pytest benchmarks/ --benchmark-only --benchmark-save=local
       python scripts/generate_benchmark_report.py -o BENCHMARK_REPORT.md

By default only runs whose save-name matches the current project version
(read from `pyproject.toml`) are included. Pass `--all-versions` to keep
every saved run, or `--save NAME` to filter by save name.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

try:  # 3.11+
    import tomllib  # type: ignore[unresolved-import]
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[no-redef]


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BENCH_DIR = PROJECT_ROOT / ".benchmarks"
PYPROJECT = PROJECT_ROOT / "pyproject.toml"

# pytest-benchmark file naming: 0001_<save-name>.json
SAVE_FILE_RE = re.compile(r"^(?P<idx>\d+)_(?P<save>.+)\.json$")


# ---------------------------------------------------------------------------
# Project metadata
# ---------------------------------------------------------------------------


def read_current_version() -> str | None:
    """Read [project].version from pyproject.toml."""
    if not PYPROJECT.exists():
        return None
    try:
        with PYPROJECT.open("rb") as f:
            data = tomllib.load(f)
        return data.get("project", {}).get("version")
    except Exception:  # pragma: no cover
        return None


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

_UNITS = [
    (1e-9, "ns"),
    (1e-6, "µs"),
    (1e-3, "ms"),
    (1.0, "s"),
]


def fmt_time(seconds: float) -> str:
    """Render a duration in the most readable unit."""
    if seconds <= 0:
        return "0 s"
    for scale, unit in _UNITS:
        value = seconds / scale
        if value < 1000:
            if value >= 100:
                return f"{value:.1f} {unit}"
            if value >= 10:
                return f"{value:.2f} {unit}"
            return f"{value:.3f} {unit}"
    return f"{seconds:.3f} s"


def fmt_ops(ops: float) -> str:
    if ops >= 1e6:
        return f"{ops / 1e6:.2f} Mops/s"
    if ops >= 1e3:
        return f"{ops / 1e3:.2f} Kops/s"
    return f"{ops:.2f} ops/s"


def library_from_name(name: str) -> str:
    """Extract a friendly library name from a test id."""
    base = name
    if base.startswith("test_"):
        base = base[len("test_") :]
    for suffix in (
        "_parallel_load",
        "_conditional",
        "_simple",
        "_nested",
        "_params",
    ):
        if base.endswith(suffix):
            base = base[: -len(suffix)]
            break
    mapping = {
        "modern": "i18n_modern",
        "python_i18n": "python-i18n",
        "pyi18n": "pyi18n-v2",
        "i18nice": "i18nice",
        "toml_i18n": "toml-i18n",
    }
    return mapping.get(base, base)


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------


class Run:
    """A single resolved pytest-benchmark JSON run."""

    __slots__ = ("path", "machine", "save_name", "idx", "data")

    def __init__(
        self,
        path: Path,
        machine: str,
        save_name: str,
        idx: int,
        data: dict[str, Any],
    ) -> None:
        self.path = path
        self.machine = machine
        self.save_name = save_name
        self.idx = idx
        self.data = data


def discover_runs(
    bench_dir: Path,
    *,
    save_filter: str | None,
    version_filter: str | None,
) -> list[Run]:
    """
    Find the latest JSON for every (machine_subdir, save_name) under bench_dir.

    Args:
        bench_dir: Root .benchmarks directory.
        save_filter: If set, only keep runs whose save_name == this value.
        version_filter: If set, only keep runs whose save_name contains this
            substring (typical convention: save_name == project version).
    """
    if not bench_dir.exists():
        return []

    # (machine, save_name) -> (idx, path)
    latest: dict[tuple[str, str], tuple[int, Path]] = {}

    for machine_dir in sorted(p for p in bench_dir.iterdir() if p.is_dir()):
        machine = machine_dir.name
        for f in machine_dir.iterdir():
            if not f.is_file() or f.suffix != ".json":
                continue
            m = SAVE_FILE_RE.match(f.name)
            if not m:
                continue
            idx = int(m.group("idx"))
            save = m.group("save")

            if save_filter is not None and save != save_filter:
                continue
            if version_filter is not None and version_filter not in save:
                continue

            key = (machine, save)
            prev = latest.get(key)
            if prev is None or idx > prev[0]:
                latest[key] = (idx, f)

    runs: list[Run] = []
    for (machine, save), (idx, path) in sorted(latest.items()):
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        runs.append(Run(path=path, machine=machine, save_name=save, idx=idx, data=data))
    return runs


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _render_environment(run: Run, out: list[str]) -> None:
    machine = run.data.get("machine_info", {})
    commit = run.data.get("commit_info", {})
    out.append(
        f"- Source: `{run.path.relative_to(PROJECT_ROOT)}` "
        f"(save `{run.save_name}`, run #{run.idx:04d})"
    )
    out.append(
        f"- Python: `{machine.get('python_implementation', '?')} "
        f"{machine.get('python_version', '?')}`"
    )
    out.append(
        f"- System: `{machine.get('system', '?')} "
        f"{machine.get('release', '?')} ({machine.get('machine', '?')})`"
    )
    out.append(f"- CPU: `{machine.get('cpu', {}).get('brand_raw', '?')}`")
    if commit.get("id"):
        out.append(
            f"- Commit: `{commit.get('id', '?')[:12]}` on branch "
            f"`{commit.get('branch', '?')}`"
        )
    out.append("")


def _render_groups(benchmarks: list[dict[str, Any]], out: list[str]) -> None:
    groups: dict[str, list[dict[str, Any]]] = {}
    for b in benchmarks:
        groups.setdefault(b.get("group") or "ungrouped", []).append(b)

    for group_name in sorted(groups):
        rows = sorted(groups[group_name], key=lambda b: b["stats"]["median"])
        fastest_median = rows[0]["stats"]["median"]

        out.append(f"### Group: `{group_name}`")
        out.append("")
        out.append(
            "| Rank | Library | Min | Median | Mean | StdDev | Ops/s | Rounds | vs Fastest |"
        )
        out.append("|---:|---|---:|---:|---:|---:|---:|---:|---:|")
        for i, b in enumerate(rows, start=1):
            s = b["stats"]
            lib = library_from_name(b["name"])
            ratio = s["median"] / fastest_median if fastest_median > 0 else 1.0
            ratio_str = "**1.00x (fastest)**" if i == 1 else f"{ratio:.2f}x slower"
            highlight = "**" if i == 1 else ""
            out.append(
                f"| {i} | {highlight}{lib}{highlight} "
                f"| {fmt_time(s['min'])} "
                f"| {fmt_time(s['median'])} "
                f"| {fmt_time(s['mean'])} "
                f"| {fmt_time(s['stddev'])} "
                f"| {fmt_ops(s['ops'])} "
                f"| {s['rounds']} "
                f"| {ratio_str} |"
            )
        out.append("")


def render(runs: Iterable[Run], *, version: str | None) -> str:
    runs = list(runs)
    out: list[str] = []
    out.append("# Benchmark Report")
    out.append("")
    out.append(
        f"_Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}_"
    )
    if version:
        out.append("")
        out.append(f"Project version: `{version}`")
    out.append("")

    if not runs:
        out.append("> No benchmark runs found.")
        out.append("")
        return "\n".join(out)

    out.append(
        f"Including **{len(runs)}** run(s): "
        + ", ".join(f"`{r.machine}/{r.save_name}`" for r in runs)
    )
    out.append("")

    for run in runs:
        out.append(f"## Run: `{run.machine}` — save `{run.save_name}`")
        out.append("")
        _render_environment(run, out)
        _render_groups(run.data.get("benchmarks", []), out)

    out.append("---")
    out.append("")
    out.append(
        "Generated from `pytest-benchmark` JSON via "
        "`scripts/generate_benchmark_report.py`. See `benchmarks/README.md` for how "
        "to reproduce."
    )
    out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "json_path",
        type=Path,
        nargs="?",
        default=None,
        help=(
            "Path to a single pytest-benchmark JSON file. If omitted, the "
            "script auto-discovers the latest run per (machine, save) under "
            "`.benchmarks/`."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Write the markdown to this file instead of stdout.",
    )
    parser.add_argument(
        "--benchmarks-dir",
        type=Path,
        default=DEFAULT_BENCH_DIR,
        help="Root directory of pytest-benchmark storage (default: .benchmarks).",
    )
    parser.add_argument(
        "--save",
        type=str,
        default=None,
        help="Only include runs with this exact save name.",
    )
    parser.add_argument(
        "--all-versions",
        action="store_true",
        help=(
            "Do not filter discovered runs by the current project version. "
            "By default only runs whose save name contains the project "
            "version are included."
        ),
    )
    args = parser.parse_args(argv)

    version = read_current_version()

    if args.json_path is not None:
        if not args.json_path.exists():
            print(f"ERROR: {args.json_path} not found", file=sys.stderr)
            return 1
        with args.json_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        runs = [
            Run(
                path=args.json_path,
                machine="explicit",
                save_name=args.json_path.stem,
                idx=0,
                data=data,
            )
        ]
    else:
        version_filter = None if args.all_versions else version
        runs = discover_runs(
            args.benchmarks_dir,
            save_filter=args.save,
            version_filter=version_filter,
        )
        if not runs:
            hint = ""
            if version_filter:
                hint = (
                    f" (filtered by version `{version_filter}`; "
                    "use --all-versions to disable)"
                )
            print(
                f"ERROR: no benchmark runs found in {args.benchmarks_dir}{hint}",
                file=sys.stderr,
            )
            return 1

    md = render(runs, version=version)

    if args.output:
        args.output.write_text(md, encoding="utf-8")
        print(f"Wrote {args.output} ({len(md)} chars, {len(runs)} run(s))")
    else:
        sys.stdout.write(md)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
