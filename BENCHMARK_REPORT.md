# Benchmark Report

_Generated: 2026-04-29T22:15:38+00:00_

Project version: `0.2.3`

Including **1** run(s): `Windows-CPython-3.12-64bit/v0.2.3`

## Run: `Windows-CPython-3.12-64bit` — save `v0.2.3`

- Source: `.benchmarks\Windows-CPython-3.12-64bit\0001_v0.2.3.json` (save `v0.2.3`, run #0001)
- Python: `CPython 3.12.8`
- System: `Windows 11 (AMD64)`
- CPU: `Intel(R) Core(TM) Ultra 5 125U`
- Commit: `e8009584c84c` on branch `master`

### Group: `conditional`

| Rank | Library | Min | Median | Mean | StdDev | Ops/s | Rounds | vs Fastest |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **i18n_modern** | 540.0 ns | 780.0 ns | 866.1 ns | 775.8 ns | 1.15 Mops/s | 69445 | **1.00x (fastest)** |

### Group: `nested`

| Rank | Library | Min | Median | Mean | StdDev | Ops/s | Rounds | vs Fastest |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **i18n_modern** | 199.0 ns | 214.0 ns | 243.6 ns | 136.8 ns | 4.10 Mops/s | 47620 | **1.00x (fastest)** |
| 2 | pyi18n-v2 | 570.0 ns | 600.0 ns | 685.4 ns | 645.5 ns | 1.46 Mops/s | 169492 | 2.80x slower |
| 3 | i18nice | 2.250 µs | 2.750 µs | 3.184 µs | 4.720 µs | 314.03 Kops/s | 192308 | 12.85x slower |
| 4 | toml-i18n | 1.840 µs | 3.280 µs | 3.436 µs | 9.760 µs | 291.06 Kops/s | 46297 | 15.33x slower |
| 5 | python-i18n | 90.40 µs | 124.2 µs | 140.1 µs | 59.90 µs | 7.14 Kops/s | 10021 | 580.37x slower |

### Group: `parallel_load`

| Rank | Library | Min | Median | Mean | StdDev | Ops/s | Rounds | vs Fastest |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **i18n_modern** | 3.327 ms | 3.989 ms | 4.176 ms | 810.3 µs | 239.47 ops/s | 10 | **1.00x (fastest)** |

### Group: `params`

| Rank | Library | Min | Median | Mean | StdDev | Ops/s | Rounds | vs Fastest |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **i18n_modern** | 520.0 ns | 560.0 ns | 633.2 ns | 688.2 ns | 1.58 Mops/s | 185186 | **1.00x (fastest)** |
| 2 | pyi18n-v2 | 970.0 ns | 1.020 µs | 1.222 µs | 1.364 µs | 818.40 Kops/s | 100001 | 1.82x slower |
| 3 | python-i18n | 830.0 ns | 1.260 µs | 1.391 µs | 1.102 µs | 718.90 Kops/s | 68966 | 2.25x slower |
| 4 | i18nice | 2.700 µs | 3.450 µs | 3.825 µs | 4.774 µs | 261.46 Kops/s | 163935 | 6.16x slower |
| 5 | toml-i18n | 3.300 µs | 3.750 µs | 4.117 µs | 4.776 µs | 242.91 Kops/s | 147059 | 6.70x slower |

### Group: `simple`

| Rank | Library | Min | Median | Mean | StdDev | Ops/s | Rounds | vs Fastest |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **i18n_modern** | 207.1 ns | 371.4 ns | 363.3 ns | 825.3 ns | 2.75 Mops/s | 188680 | **1.00x (fastest)** |
| 2 | pyi18n-v2 | 530.0 ns | 710.0 ns | 804.4 ns | 762.8 ns | 1.24 Mops/s | 80000 | 1.91x slower |
| 3 | python-i18n | 740.0 ns | 1.330 µs | 1.299 µs | 1.099 µs | 769.69 Kops/s | 128206 | 3.58x slower |
| 4 | toml-i18n | 1.760 µs | 1.950 µs | 2.372 µs | 1.772 µs | 421.52 Kops/s | 50001 | 5.25x slower |
| 5 | i18nice | 1.430 µs | 2.070 µs | 2.328 µs | 2.021 µs | 429.52 Kops/s | 39841 | 5.57x slower |

---

Generated from `pytest-benchmark` JSON via `scripts/bench_json_to_md.py`. See `benchmarks/README.md` for how to reproduce.
