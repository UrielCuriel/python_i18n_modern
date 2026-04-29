# Benchmark Report

_Generated: 2026-04-29T22:42:57+00:00_

Project version: `0.2.3`

Including **2** run(s): `Linux-CPython-3.12-64bit/v0.2.3`, `Windows-CPython-3.12-64bit/v0.2.3`

## Run: `Linux-CPython-3.12-64bit` — save `v0.2.3`

- Source: `.benchmarks/Linux-CPython-3.12-64bit/0001_v0.2.3.json` (save `v0.2.3`, run #0001)
- Python: `CPython 3.12.1`
- System: `Linux 6.8.0-1044-azure (x86_64)`
- CPU: `AMD EPYC 7763 64-Core Processor`
- Commit: `1e9a3a65a615` on branch `master`

### Group: `conditional`

| Rank | Library | Min | Median | Mean | StdDev | Ops/s | Rounds | vs Fastest |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **i18n_modern** | 681.2 ns | 703.3 ns | 793.1 ns | 1.593 µs | 1.26 Mops/s | 139607 | **1.00x (fastest)** |

### Group: `nested`

| Rank | Library | Min | Median | Mean | StdDev | Ops/s | Rounds | vs Fastest |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **i18n_modern** | 268.3 ns | 277.2 ns | 306.1 ns | 343.7 ns | 3.27 Mops/s | 192679 | **1.00x (fastest)** |
| 2 | pyi18n-v2 | 787.5 ns | 809.5 ns | 945.2 ns | 2.423 µs | 1.06 Mops/s | 66770 | 2.92x slower |
| 3 | i18nice | 1.406 µs | 1.442 µs | 1.708 µs | 1.931 µs | 585.32 Kops/s | 69267 | 5.20x slower |
| 4 | toml-i18n | 2.277 µs | 2.326 µs | 2.967 µs | 8.365 µs | 337.04 Kops/s | 42152 | 8.39x slower |
| 5 | python-i18n | 11.70 µs | 11.93 µs | 12.54 µs | 4.424 µs | 79.73 Kops/s | 83809 | 43.05x slower |

### Group: `parallel_load`

| Rank | Library | Min | Median | Mean | StdDev | Ops/s | Rounds | vs Fastest |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **i18n_modern** | 1.483 ms | 1.646 ms | 1.668 ms | 189.6 µs | 599.39 ops/s | 10 | **1.00x (fastest)** |

### Group: `params`

| Rank | Library | Min | Median | Mean | StdDev | Ops/s | Rounds | vs Fastest |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **i18n_modern** | 679.3 ns | 697.3 ns | 766.2 ns | 2.744 µs | 1.31 Mops/s | 141764 | **1.00x (fastest)** |
| 2 | pyi18n-v2 | 1.337 µs | 1.361 µs | 1.418 µs | 277.9 ns | 705.09 Kops/s | 73282 | 1.95x slower |
| 3 | i18nice | 1.519 µs | 1.549 µs | 1.730 µs | 2.462 µs | 578.19 Kops/s | 63739 | 2.22x slower |
| 4 | toml-i18n | 2.559 µs | 2.634 µs | 3.177 µs | 8.829 µs | 314.73 Kops/s | 184163 | 3.78x slower |
| 5 | python-i18n | 7.324 µs | 7.534 µs | 8.730 µs | 31.09 µs | 114.55 Kops/s | 92765 | 10.80x slower |

### Group: `simple`

| Rank | Library | Min | Median | Mean | StdDev | Ops/s | Rounds | vs Fastest |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **i18n_modern** | 270.5 ns | 282.7 ns | 349.1 ns | 1.116 µs | 2.86 Mops/s | 198847 | **1.00x (fastest)** |
| 2 | pyi18n-v2 | 739.4 ns | 776.5 ns | 865.1 ns | 915.9 ns | 1.16 Mops/s | 128783 | 2.75x slower |
| 3 | i18nice | 1.402 µs | 1.437 µs | 1.799 µs | 2.865 µs | 555.76 Kops/s | 68367 | 5.08x slower |
| 4 | toml-i18n | 2.215 µs | 2.259 µs | 2.406 µs | 2.597 µs | 415.67 Kops/s | 43549 | 7.99x slower |
| 5 | python-i18n | 7.223 µs | 7.434 µs | 9.118 µs | 26.32 µs | 109.68 Kops/s | 134899 | 26.29x slower |

## Run: `Windows-CPython-3.12-64bit` — save `v0.2.3`

- Source: `.benchmarks/Windows-CPython-3.12-64bit/0001_v0.2.3.json` (save `v0.2.3`, run #0001)
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

Generated from `pytest-benchmark` JSON via `scripts/generate_benchmark_report.py`. See `benchmarks/README.md` for how to reproduce.
