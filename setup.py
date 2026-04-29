"""Build script for Cython extensions.

Usage
-----
Compile in-place (development)::

    python setup.py build_ext --inplace

This produces ``i18n_modern/_cy_helpers*.so`` (Linux/macOS) or
``i18n_modern/_cy_helpers*.pyd`` (Windows) next to the source files.

The Cython transpilation step (.pyx → .c) is run automatically if Cython
is available; otherwise the pre-generated ``_cy_helpers.c`` is used.
"""

from __future__ import annotations

import sys
from pathlib import Path

from setuptools import Extension, setup


def _compile_args() -> list[str]:
    """Return appropriate optimization flags for the active compiler."""
    if sys.platform != "win32":
        return ["-O3", "-ffast-math"]
    # On Windows we may have MSVC or MinGW; defer to no extra flags so that
    # setup.py --compiler=mingw32 works out of the box.  Both compilers
    # apply their own default optimizations at -O / /O2 level.
    return []


PYX = Path("i18n_modern/_cy_helpers.pyx")
C_SRC = Path("i18n_modern/_cy_helpers.c")

try:
    from Cython.Build import cythonize  # type: ignore[import-untyped]

    ext_modules = cythonize(
        [
            Extension(
                name="i18n_modern._cy_helpers",
                sources=[str(PYX)],
                extra_compile_args=_compile_args(),
            )
        ],
        compiler_directives={
            "language_level": 3,
            "boundscheck": False,
            "wraparound": False,
            "cdivision": True,
        },
        # Regenerate the .c file when the .pyx changes.
        force=True,
    )
    print("[setup.py] Using Cython to transpile .pyx → .c")
except ImportError:
    if not C_SRC.exists():
        raise RuntimeError(
            "Cython is not installed and no pre-generated _cy_helpers.c was found.\n"
            "Install Cython with:  pip install cython"
        ) from None
    print(f"[setup.py] Cython not found — using pre-generated {C_SRC}")
    ext_modules = [
        Extension(
            name="i18n_modern._cy_helpers",
            sources=[str(C_SRC)],
            extra_compile_args=_compile_args(),
        )
    ]

setup(
    name="i18n_modern",
    ext_modules=ext_modules,
)
