# pyright: basic
"""
Comprehensive benchmark comparing i18n_modern with other i18n libraries.

Compares:
- i18n_modern (our library)
- python-i18n
- pyi18n-v2
"""

import json
import time
from pathlib import Path
from typing import Callable

import i18n
import pyi18n

from i18n_modern import I18nModern


class BenchmarkRunner:
    """Runs performance benchmarks on different i18n libraries."""

    def __init__(self):
        """Initialize the benchmark runner."""
        self.results = {}

    def measure_time(self, func: Callable, iterations: int = 10000) -> tuple[float, float]:
        """
        Measure execution time of a function.

        Args:
            func: Function to measure
            iterations: Number of iterations

        Returns:
            Tuple of (total_time, time_per_iteration)
        """
        start = time.perf_counter()
        for _ in range(iterations):
            func()
        end = time.perf_counter()
        total_time = end - start
        return total_time, total_time / iterations

    def setup_i18n_modern(self) -> I18nModern:
        """Setup i18n_modern with test data."""
        locales_path = Path(__file__).parent / "examples" / "locales" / "en.json"
        with open(locales_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        i18n_obj = I18nModern("en", data)
        return i18n_obj

    def setup_python_i18n(self) -> dict:
        """Setup python-i18n with test data."""
        locales_path = Path(__file__).parent / "examples" / "locales" / "en.json"
        i18n.set("locale", "en")
        i18n.set("filename_format", "{namespace}.{locale}.json")
        i18n.set("file_format", "json")
        i18n.set("default_locale", "en")

        # Load from file
        locale_dir = Path(__file__).parent / "examples" / "locales"
        i18n.load_path.clear()
        i18n.load_path.append(str(locale_dir))

        # Load the file
        with open(locales_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return {"i18n": i18n, "data": data}

    def setup_pyi18n(self) -> dict:
        """Setup pyi18n-v2 with test data."""
        locales_path = Path(__file__).parent / "examples" / "locales" / "en.json"
        with open(locales_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        pyi18n_obj = pyi18n.PyI18n("en", data)
        return {"i18n": pyi18n_obj, "data": data}

    def benchmark_i18n_modern(self):
        """Benchmark i18n_modern library."""
        print("\n" + "=" * 70)
        print("BENCHMARKING: i18n_modern")
        print("=" * 70)

        i18n_obj = self.setup_i18n_modern()

        # Test 1: Simple key access
        print("\n1. Simple Key Access (welcome)")
        total, per_iter = self.measure_time(lambda: i18n_obj.get("welcome"), iterations=10000)
        print(f"   Total: {total:.4f}s | Per iteration: {per_iter * 1e6:.2f}µs")
        self.results["i18n_modern_simple"] = {"total": total, "per_iter": per_iter}

        # Test 2: Nested key access
        print("\n2. Nested Key Access (messages.success)")
        total, per_iter = self.measure_time(lambda: i18n_obj.get("messages.success"), iterations=10000)
        print(f"   Total: {total:.4f}s | Per iteration: {per_iter * 1e6:.2f}µs")
        self.results["i18n_modern_nested"] = {"total": total, "per_iter": per_iter}

        # Test 3: With parameter substitution
        print("\n3. Parameter Substitution (greeting)")
        total, per_iter = self.measure_time(
            lambda: i18n_obj.get("greeting", values={"name": "Alice"}),
            iterations=10000,
        )
        print(f"   Total: {total:.4f}s | Per iteration: {per_iter * 1e6:.2f}µs")
        self.results["i18n_modern_params"] = {"total": total, "per_iter": per_iter}

        # Test 4: With conditional logic
        print("\n4. Conditional Logic (age_group with adult)")
        total, per_iter = self.measure_time(
            lambda: i18n_obj.get("age_group", values={"age": 25}),
            iterations=5000,
        )
        print(f"   Total: {total:.4f}s | Per iteration: {per_iter * 1e6:.2f}µs")
        self.results["i18n_modern_conditional"] = {"total": total, "per_iter": per_iter}

        # Test 5: Cache effectiveness (repeated calls)
        print("\n5. Cache Effectiveness (100 repeated calls)")
        cache_test = lambda: i18n_obj.get("greeting", values={"name": "Alice"})
        total, per_iter = self.measure_time(cache_test, iterations=10000)
        print(f"   Total: {total:.4f}s | Per iteration: {per_iter * 1e6:.2f}µs")
        self.results["i18n_modern_cache"] = {"total": total, "per_iter": per_iter}

    def benchmark_python_i18n(self):
        """Benchmark python-i18n library."""
        print("\n" + "=" * 70)
        print("BENCHMARKING: python-i18n")
        print("=" * 70)

        try:
            setup = self.setup_python_i18n()
            i18n_lib = setup["i18n"]

            # Test 1: Simple key access
            print("\n1. Simple Key Access (welcome)")
            try:
                total, per_iter = self.measure_time(lambda: i18n_lib.t("welcome"), iterations=10000)
                print(f"   Total: {total:.4f}s | Per iteration: {per_iter * 1e6:.2f}µs")
                self.results["python_i18n_simple"] = {
                    "total": total,
                    "per_iter": per_iter,
                }
            except Exception as e:
                print(f"   Error: {e}")
                self.results["python_i18n_simple"] = {"error": str(e)}

            # Test 2: Nested key access
            print("\n2. Nested Key Access (messages.success)")
            try:
                total, per_iter = self.measure_time(lambda: i18n_lib.t("messages.success"), iterations=10000)
                print(f"   Total: {total:.4f}s | Per iteration: {per_iter * 1e6:.2f}µs")
                self.results["python_i18n_nested"] = {
                    "total": total,
                    "per_iter": per_iter,
                }
            except Exception as e:
                print(f"   Error: {e}")
                self.results["python_i18n_nested"] = {"error": str(e)}

            # Test 3: With parameter substitution
            print("\n3. Parameter Substitution (greeting)")
            try:
                total, per_iter = self.measure_time(lambda: i18n_lib.t("greeting", name="Alice"), iterations=10000)
                print(f"   Total: {total:.4f}s | Per iteration: {per_iter * 1e6:.2f}µs")
                self.results["python_i18n_params"] = {
                    "total": total,
                    "per_iter": per_iter,
                }
            except Exception as e:
                print(f"   Error: {e}")
                self.results["python_i18n_params"] = {"error": str(e)}

        except Exception as e:
            print(f"\nError setting up python-i18n: {e}")

    def benchmark_pyi18n(self):
        """Benchmark pyi18n-v2 library."""
        print("\n" + "=" * 70)
        print("BENCHMARKING: pyi18n-v2")
        print("=" * 70)

        try:
            setup = self.setup_pyi18n()
            pyi18n_obj = setup["i18n"]

            # Test 1: Simple key access
            print("\n1. Simple Key Access (welcome)")
            try:
                total, per_iter = self.measure_time(lambda: pyi18n_obj.get("welcome"), iterations=10000)
                print(f"   Total: {total:.4f}s | Per iteration: {per_iter * 1e6:.2f}µs")
                self.results["pyi18n_simple"] = {"total": total, "per_iter": per_iter}
            except Exception as e:
                print(f"   Error: {e}")
                self.results["pyi18n_simple"] = {"error": str(e)}

            # Test 2: Nested key access
            print("\n2. Nested Key Access (messages.success)")
            try:
                total, per_iter = self.measure_time(lambda: pyi18n_obj.get("messages.success"), iterations=10000)
                print(f"   Total: {total:.4f}s | Per iteration: {per_iter * 1e6:.2f}µs")
                self.results["pyi18n_nested"] = {"total": total, "per_iter": per_iter}
            except Exception as e:
                print(f"   Error: {e}")
                self.results["pyi18n_nested"] = {"error": str(e)}

            # Test 3: With parameter substitution
            print("\n3. Parameter Substitution (greeting)")
            try:
                total, per_iter = self.measure_time(
                    lambda: pyi18n_obj.get("greeting", name="Alice"),
                    iterations=10000,
                )
                print(f"   Total: {total:.4f}s | Per iteration: {per_iter * 1e6:.2f}µs")
                self.results["pyi18n_params"] = {"total": total, "per_iter": per_iter}
            except Exception as e:
                print(f"   Error: {e}")
                self.results["pyi18n_params"] = {"error": str(e)}

        except Exception as e:
            print(f"\nError setting up pyi18n-v2: {e}")

    def print_comparison_summary(self):
        """Print a summary comparison of all libraries."""
        print("\n" + "=" * 70)
        print("COMPARISON SUMMARY")
        print("=" * 70)

        # Extract times for each test
        tests = {
            "Simple Access": ("i18n_modern_simple", "python_i18n_simple", "pyi18n_simple"),
            "Nested Access": (
                "i18n_modern_nested",
                "python_i18n_nested",
                "pyi18n_nested",
            ),
            "Parameter Substitution": (
                "i18n_modern_params",
                "python_i18n_params",
                "pyi18n_params",
            ),
        }

        for test_name, keys in tests.items():
            print(f"\n{test_name}:")
            print("-" * 70)

            times = {}
            for key in keys:
                if key in self.results:
                    result = self.results[key]
                    if "error" not in result:
                        times[key] = result["per_iter"] * 1e6
                    else:
                        times[key] = float("inf")

            if times:
                fastest_key = min(times.keys(), key=lambda k: times[k])
                fastest_time = times[fastest_key]

                for key, time_us in times.items():
                    library = key.split("_")[0]
                    if time_us == float("inf"):
                        print(f"  {library:15} - Error")
                    else:
                        ratio = time_us / fastest_time
                        bar = "█" * int(ratio * 20)
                        print(f"  {library:15} - {time_us:8.2f}µs {bar} ({ratio:.1f}x)")

    def run_all_benchmarks(self):
        """Run all benchmarks."""
        print("\n" + "█" * 70)
        print("█ I18N LIBRARIES PERFORMANCE BENCHMARK".ljust(70) + "█")
        print("█" * 70)

        self.benchmark_i18n_modern()
        self.benchmark_python_i18n()
        self.benchmark_pyi18n()
        self.print_comparison_summary()

        print("\n" + "█" * 70)
        print("█ BENCHMARK COMPLETE".ljust(70) + "█")
        print("█" * 70 + "\n")


if __name__ == "__main__":
    runner = BenchmarkRunner()
    runner.run_all_benchmarks()
