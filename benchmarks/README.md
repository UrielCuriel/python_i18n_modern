# Benchmark suite

Este directorio contiene benchmarks formales basados en
[`pytest-benchmark`](https://pytest-benchmark.readthedocs.io/) que reemplazan
al script ad-hoc `benchmark_comparison.py`.

## ¿Por qué pytest-benchmark?

El script anterior medía cada caso con un único `time.perf_counter()` sobre
N iteraciones. Eso causaba mucha varianza entre corridas porque:

- No hacía warmup → la primera corrida pagaba caches fríos.
- No deshabilitaba el GC → pausas aleatorias entre rondas.
- No calibraba el número de iteraciones → llamadas muy rápidas se medían con
  muy baja resolución.
- Reportaba una sola muestra → sin stddev, sin mediana, sin min.

`pytest-benchmark` resuelve todo eso: calibración automática, múltiples
rondas, warmup, GC desactivado, estadísticas (min/mean/median/stddev/ops),
y comparación entre runs guardadas.

## Instalación

```sh
pip install -e ".[benchmark]"
# o con uv:
uv sync --extra benchmark
```

## Ejecutar

```sh
# Correr todo el suite con la configuración por defecto del pyproject.
pytest benchmarks/ --benchmark-only

# Solo un grupo (simple / nested / params / conditional / parallel_load):
pytest benchmarks/ --benchmark-only -k simple

# Solo una librería:
pytest benchmarks/test_bench_i18n_modern.py --benchmark-only
```

## Comparar runs (detección de regresiones)

```sh
# Guardar baseline.
pytest benchmarks/ --benchmark-only --benchmark-save=baseline

# Después de un cambio, comparar.
pytest benchmarks/ --benchmark-only --benchmark-compare=baseline \
    --benchmark-compare-fail=mean:10%
```

`--benchmark-compare-fail=mean:10%` hace que la corrida falle si la media
empeoró más de 10% respecto al baseline. Útil en CI.

## Output JSON y reporte Markdown

```sh
# Opción A: explícita — un solo JSON
pytest benchmarks/ --benchmark-only --benchmark-json=bench.json
python scripts/bench_json_to_md.py bench.json -o BENCHMARK_REPORT.md

# Opción B: auto-discovery desde .benchmarks/ (recomendada)
# Toma el archivo más reciente por cada (máquina, save-name) y los
# concatena en un solo reporte. Por defecto filtra por la versión
# actual del proyecto leída de pyproject.toml.
pytest benchmarks/ --benchmark-only --benchmark-save=v0.2.3
python scripts/bench_json_to_md.py -o BENCHMARK_REPORT.md

# Variantes:
python scripts/bench_json_to_md.py --all-versions -o BENCHMARK_REPORT.md
python scripts/bench_json_to_md.py --save baseline -o BENCHMARK_REPORT.md
```

Convención sugerida: nombrar los saves con la versión del proyecto
(`--benchmark-save=v0.2.3`) para que el script los agrupe automáticamente
por versión.

## CI (GitHub Actions)

El workflow `.github/workflows/benchmarks.yml`:

- Corre el suite en cada push a `main` y en cada PR.
- En `main` guarda el run como artifact `benchmark-baseline`.
- En PRs descarga ese baseline y compara con
  `--benchmark-compare-fail=median:15%` (falla si la mediana empeora >15%).
- Renderiza `BENCHMARK_REPORT.md` y lo publica como artifact + en el
  `GITHUB_STEP_SUMMARY` del job.

## Tips para reducir varianza aún más

- Cierra apps pesadas (Chrome, Docker, etc.) antes de medir.
- En Linux: `taskset -c 0 pytest benchmarks/ --benchmark-only` para fijar CPU.
- Usa el mismo perfil de energía (no batería en laptops).
- Sube `--benchmark-min-rounds` (ej. `100`) si quieres más estabilidad a
  costa de tiempo total.
