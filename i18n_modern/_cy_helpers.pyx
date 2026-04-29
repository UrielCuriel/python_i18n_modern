# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True
"""
Cython-accelerated helpers for i18n_modern hot paths.

Provides:
- cy_get_deep_value: fast nested dict traversal by dot path
- cy_format_value: fast placeholder substitution using [key]
"""

# Sentinel for missing keys — avoids confusing a stored None with "not found".
cdef object _MISSING = object()


cpdef object cy_get_deep_value(object obj, str path):
    """Traverse mapping using a dot-delimited path.

    Accepts any object that implements .get(key[, default]).
    Returns None if any intermediate is missing or not a mapping.

    Optimized for partially-flattened locale dicts:
    1. Fast path  — direct O(1) lookup of the full dot-notation key.
       Hits immediately when the dict was produced by flatten_locale().
    2. Slow path  — falls back to segment-by-segment traversal for
       remaining nested structures (e.g. conditional dicts kept as-is
       by flatten_locale, or un-flattened dicts passed at runtime).
    """
    if obj is None:
        return None

    cdef object result
    cdef object current
    cdef list segments
    cdef Py_ssize_t i, n
    cdef str segment
    cdef object next_val

    # ------------------------------------------------------------------
    # Fast path: try the whole dot-path as a single key first.
    # Works in O(1) when the locale was pre-flattened.
    # ------------------------------------------------------------------
    if hasattr(obj, 'get'):
        result = (<object>obj).get(path, _MISSING)
        if result is not _MISSING:
            return result

    # ------------------------------------------------------------------
    # Slow path: walk segment by segment for nested / conditional dicts.
    # ------------------------------------------------------------------
    current = obj
    segments = path.split('.')
    n = len(segments)

    for i in range(n):
        segment = segments[i]
        if not hasattr(current, 'get'):
            return None
        next_val = (<object>current).get(segment, _MISSING)
        if next_val is _MISSING:
            return None
        current = next_val

    return current


cdef str _BRACKET_OPEN = '['
cdef str _BRACKET_CLOSE = ']'


cpdef str cy_format_value(str s, dict values):
    """Replace [key] occurrences in s with values[key] when present.

    Leaves unmatched placeholders intact.

    Highly optimized with Cython compiler directives.
    """
    cdef list out = []
    cdef list key_chars = []
    cdef int i = 0
    cdef int n = len(s)
    cdef int in_bracket = 0
    cdef str c
    cdef str key
    cdef object val

    while i < n:
        c = s[i]
        if in_bracket:
            if c == _BRACKET_CLOSE:
                key = ''.join(key_chars)
                if values is not None and key in values:
                    val = values[key]
                    out.append(str(val))
                else:
                    out.append(_BRACKET_OPEN)
                    out.append(key)
                    out.append(_BRACKET_CLOSE)
                key_chars.clear()
                in_bracket = 0
            else:
                key_chars.append(c)
        else:
            if c == _BRACKET_OPEN:
                in_bracket = 1
                key_chars.clear()
            else:
                out.append(c)
        i += 1

    if in_bracket:
        out.append(_BRACKET_OPEN)
        out.extend(key_chars)

    return ''.join(out)
