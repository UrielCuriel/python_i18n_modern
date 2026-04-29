# 📊 Benchmark Results Summary

**Updated:** April 2026 (Post-flatten optimization)

## Performance Comparison Matrix

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│           OPERATION            │ i18n_modern │ python-i18n │ pyi18n-v2 │ i18nice │ toml │
├──────────────────────────────────────────────────────────────────────────────────────┤
│ Simple Key Access               │    0.23µs   │   0.79µs    │  0.40µs   │ 1.51µs  │1.23µs│
│ Nested Key Access (CRITICAL) ⭐ │    0.17µs   │  66.90µs    │  0.64µs   │ 1.55µs  │1.39µs│
│ Parameter Substitution          │    0.43µs   │   0.99µs    │  0.83µs   │ 1.91µs  │1.61µs│
│ Conditional Logic               │    0.75µs   │   N/A       │   N/A     │  N/A    │ N/A  │
│ Cache Effectiveness (100x)      │    0.57µs   │   N/A       │   N/A     │  N/A    │ N/A  │
│ Parallel Load (4 files)         │    4.8ms    │   N/A       │   N/A     │  N/A    │ N/A  │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

## Visual Performance Comparison

### Simple Access

```
i18n_modern  ████████████████████ 0.23µs (FASTEST — 1.0x)
pyi18n-v2    ██████████████████████████████████ 0.40µs (1.7x)
python-i18n  ███████████████████████████████████████████████████████████████████ 0.79µs (3.4x)
toml-i18n    ████████████████████████████████████████████████████████████████████████████████████████████████████ 1.23µs (5.2x)
i18nice      ████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████ 1.51µs (6.4x)
```

### Nested Access (Most Important) — 384x faster than python-i18n

```
i18n_modern  ████████████████████ 0.17µs ✅ FASTEST!
pyi18n-v2    █████████████████████████████████████████████████████████████████████████ 0.64µs (3.7x)
i18nice      ██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████ 1.55µs (8.9x)
toml-i18n    █████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████ 1.39µs (8.0x)
python-i18n  ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
             66.90µs (384.4x!) 🚀
```

### Parameter Substitution

```
i18n_modern  ████████████████████ 0.43µs (FASTEST — 1.0x)
pyi18n-v2    ██████████████████████████████████████ 0.83µs (1.9x)
python-i18n  ██████████████████████████████████████████████ 0.99µs (2.3x)
toml-i18n    ███████████████████████████████████████████████████████████████████████ 1.61µs (3.8x)
i18nice      █████████████████████████████████████████████████████████████████████████████████████ 1.91µs (4.5x)
```

---

## Improvement Since Previous Run

| Operation | Before (Oct 2025) | After (Nov 2025) | Δ |
| ----------- | ------------------- | ------------------ | --- |
| Simple Access | 0.38µs | **0.23µs** | **-39%** ⬇️ |
| Nested Access | 0.37µs | **0.17µs** | **-54%** ⬇️ |
| Parameter Substitution | 1.21µs | **0.43µs** | **-64%** ⬇️ |
| Conditional Logic | 1.80µs | **0.75µs** | **-58%** ⬇️ |
| Cache Effectiveness | 1.24µs | **0.57µs** | **-54%** ⬇️ |

**Root cause of improvement:** locale dict flattening at load time — structural nested dicts are collapsed into a single-level dict with dot-notation keys, converting every `get()` lookup from an O(depth) tree traversal into an O(1) direct dict access.

---

## Key Metrics

| Metric | Value | Status |
| -------- | ------- | -------- |
| **Fastest Library** | i18n_modern ✅ | — |
| **Best Nested Access** | i18n_modern (0.17µs) ✅ | **384x faster** than python-i18n |
| **Cache Hit Speed** | 0.57µs average | Optimized |
| **Translation Cache Size** | 2048 entries | Bounded |
| **Visitor Pool Size** | 128 instances | Optimized |
| **Expression Cache Size** | 512 entries | LRU cached |
| **Acceleration Available** | NO | (Python interpreter) |

---

## Optimization Improvements Summary

### Current Performance Status

| Component | Configuration | Performance |
| ----------- | --------------- | ------------- |
| **Locale Flattening** | Structural dicts collapsed at load time | O(1) dict access on every `get()` |
| **Visitor Pool** | 128 instances pre-allocated | Retained for conditional dict traversal |
| **Expression Parsing** | LRU cache (512 entries) | Reduced parsing overhead |
| **Translation Cache** | Bounded to 2048 entries | FIFO eviction, no leaks |
| **Cython Directives** | boundscheck, wraparound, cdivision | Better compiled code |

### Latest Benchmark Results

| Operation | Current | Speedup vs python-i18n |
| ----------- | --------- | ------------------------ |
| Simple Access | 0.23µs | 3.4x faster |
| Nested Access | 0.17µs | **384x faster** ⚡⚡⚡ |
| Parameter Substitution | 0.43µs | 2.3x faster |
| Conditional Logic | 0.75µs | Unique feature |
| Cache Effectiveness (100x) | 0.57µs | Consistent |
| Parallel Load (4 files) | 4.8ms | Async loading support |

---

## Why i18n_modern Wins

### 🏃 Speed

- **Locale flattening** — one-time O(n) cost at load; every `get()` is O(1)
- Tuple-based caching (no JSON serialization)
- Visitor pattern for conditional dict evaluation
- AST caching with LRU (512 entries)
- **384x faster** for nested access operations (vs python-i18n)

### 🎯 Design

- Modern Python patterns (type hints, generators)
- Clean separation of concerns
- Extensible architecture
- Optimized pooling strategies

### 🚀 Features

- Conditional expressions with boolean logic
- Multi-format support (JSON, YAML, TOML)
- Advanced parameter substitution
- Type-safe implementation
- Bounded memory management

### 💾 Caching Strategy

- Smart tuple-based keys
- O(1) lookup times
- No serialization overhead
- Expression compilation cache
- Bounded translation cache (2048 entries)

---

## Detailed Optimization Breakdown

### 1. Locale Flattening ⭐ NEW

**Configuration:** `flatten_locale()` applied after every `merge_deep()` at load time  
**Impact:** Structural nested dicts (`messages.success`, `messages.error`) are inlined
into a single flat dict. Conditional/dynamic dicts (keys containing `[`, `<`, `>`, `=`, `!`,
or spaces) are preserved as-is for runtime evaluation by `eval_key`.

Before: `get("messages.success")` → split key → visitor traversal → `O(depth)`  
After:  `get("messages.success")` → `flat_dict["messages.success"]` → `O(1)`

### 2. Visitor Pool Enhancement

**Configuration:** 128 instances, 32 pre-allocated  
**Impact:** Still used for conditional/dynamic dict traversal inside `_get_translation`

### 3. Expression Compilation Cache

**Configuration:** LRU cache with 512 entries  
**Impact:** Repeated conditions are faster

### 4. Cython Compiler Directives

**Configuration:** `boundscheck=False, wraparound=False, cdivision=True`  
**Impact:** ~5-10% faster compiled code (when using Cython)

### 5. Bounded Translation Cache

**Configuration:** 2048 entry limit with FIFO eviction  
**Impact:** Prevents unbounded memory growth in production

---

## Benchmark Configuration

### Test Parameters

- **Iterations:** 10,000 per test (5,000 for conditional logic)
- **Libraries Compared:** i18n_modern, python-i18n, pyi18n-v2, i18nice, toml-i18n
- **Data:** Realistic locale structures with nested keys
- **Environment:** Python 3.12.8 on Windows x86_64

### Test Scenarios

1. Simple flat key access
2. Nested key access (dot notation)
3. Parameter substitution with [key] syntax
4. Conditional logic evaluation
5. Repeated calls (cache effectiveness)
6. Parallel loading of multiple files

---

## Installation & Usage

### Install with Benchmark Comparison Tools

```bash
uv sync --all-extras
```

### Run Benchmarks

```bash
uv run benchmark_comparison.py
```

---

## Conclusion

The post-flatten benchmark results confirm the most impactful optimization yet:

✅ **All operations improved** — 39–64% faster across the board  
✅ **Nested access: 0.17µs** — O(1) dict lookup, 384x faster than python-i18n  
✅ **Parameter substitution: 0.43µs** — 64% improvement  
✅ **Conditional logic: 0.75µs** — 58% improvement  
✅ **Bounded memory usage** for production reliability  
✅ **Comprehensive caching strategies** at every layer
