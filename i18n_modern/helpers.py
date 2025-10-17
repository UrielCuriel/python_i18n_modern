"""Helper functions for i18n_modern."""

from __future__ import annotations

import ast
import functools
import logging
import operator
import re
from collections.abc import Generator, Mapping
from typing import Callable, cast

from .types import FormatParam, FormatValue, LocaleDict, LocaleValue

# Precompiled regex patterns for performance
_FORMAT_VALUE_PATTERN: re.Pattern[str] = re.compile(r"\[(.*?)\]")
_IS_SAFE_STRING_PATTERN: re.Pattern[str] = re.compile(
    r"^(?:\[?(\d+|\w+)\]?)(?:(?:(?:\s?)(?:[\>\=\!\<\|\&]|and|or){1,3}(?:\s?)(?:\[?(\d+|\w+)\]?))*)?$"
)

_STRING_COMPARATORS: dict[type[ast.cmpop], Callable[[str, str], bool]] = {
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
}

_NUMERIC_COMPARATORS: dict[type[ast.cmpop], Callable[[float, float], bool]] = {
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
}


class TreePathVisitor:
    """Visitor for traversing nested mapping structures using path segments."""

    segments: list[str]
    segment_index: int

    def __init__(self, segments: list[str]) -> None:
        """
        Initialize visitor with path segments.

        Args:
            segments: Path segments to traverse (e.g., ["user", "profile", "name"])
        """
        self.segments = segments
        self.segment_index = 0

    def visit(self, node: LocaleValue | None) -> LocaleValue | None:
        """
        Visit a node in the tree structure.

        Args:
            node: Current node to visit

        Returns:
            The value at the path or None if not found
        """
        if self.segment_index >= len(self.segments) or node is None:
            return node if self.segment_index >= len(self.segments) else None

        if not isinstance(node, Mapping):
            return None

        current_key = self.segments[self.segment_index]
        next_node = node.get(current_key)

        if next_node is None:
            return None

        self.segment_index += 1
        return self.visit(next_node)


def _walk_segments_generator(
    current: LocaleValue | None, segments: list[str]
) -> Generator[tuple[int, LocaleValue | None], None, None]:
    """
    Generate values at each segment of a path using lazy evaluation.

    Args:
        current: Starting value
        segments: Path segments to walk

    Yields:
        Tuples of (segment_index, value)
    """
    for index, segment in enumerate(segments):
        if current is None or not isinstance(current, Mapping):
            yield index, None
            return

        current = current.get(segment)
        yield index, current


def get_deep_value(obj: LocaleValue | None, path: str) -> LocaleValue | None:
    """
    Get value from deep object using dot notation.

    Args:
        obj: Object to get value from
        path: Path to object (e.g., "user.profile.name")

    Returns:
        The value at the specified path or None
    """
    if not path:
        return None

    segments: list[str] = path.split(".")
    visitor = TreePathVisitor(segments)
    return visitor.visit(obj)


def _get_from_segments(current: LocaleValue | None, segments: list[str]) -> LocaleValue | None:
    """Recursive helper to walk nested mappings using the provided path segments."""

    if not segments:
        return current

    if not isinstance(current, Mapping):
        return None

    next_value: object | None = current.get(segments[0])
    if next_value is None:
        return None

    return _get_from_segments(next_value, segments[1:])


def eval_key(key: str, values: FormatParam | None = None) -> bool:
    """
    Evaluate a key object string against values.

    Args:
        key: Key to evaluate
        values: Object to eval key against

    Returns:
        Boolean result of evaluation
    """
    if not is_safe_string(key):
        logging.warning("evalKey: key '%s' is not a safe string", key)
        return False

    logical_tokens = ("==", "!=", ">=", "<=", ">", "<", " and ", " or ")

    # Replace && with 'and' and || with 'or' for Python
    key_formatted = key.replace("&&", " and ").replace("||", " or ")
    key_formatted = format_value(key_formatted, values)

    if any(token in key_formatted for token in logical_tokens):
        return _evaluate_expression(key_formatted)

    if not values:
        return False

    search_value = key_formatted.strip()
    return search_value in values or search_value in {str(v) for v in values.values()}


def format_value(string: str, values: FormatParam | None = None) -> str:
    """
    Replace [value] in string with actual values.

    Args:
        string: String with placeholders like [key]
        values: Dictionary with replacement values

    Returns:
        Formatted string
    """
    if values is None or not values:
        return string

    replacements = values

    def replacer(match: re.Match[str]) -> str:
        key = match.group(1)
        if key in replacements:
            return str(replacements[key])
        return match.group(0)

    return _FORMAT_VALUE_PATTERN.sub(replacer, string)


def is_safe_string(string: str) -> bool:
    """
    Validate that the string does not include Python reserved words.

    Args:
        string: String to validate

    Returns:
        True if string is safe to evaluate
    """
    reserved_words = [
        "break",
        "case",
        "catch",
        "class",
        "const",
        "continue",
        "debugger",
        "delete",
        "do",
        "enum",
        "export",
        "extends",
        "false",
        "finally",
        "for",
        "function",
        "if",
        "import",
        "isinstance",
        "interface",
        "let",
        "new",
        "null",
        "package",
        "private",
        "protected",
        "public",
        "return",
        "static",
        "super",
        "switch",
        "this",
        "throw",
        "true",
        "try",
        "typeof",
        "var",
        "void",
        "while",
        "with",
        "alert",
        "console",
        "script",
        "eval",
        "exec",
        "__import__",
        "open",
        "compile",
    ]

    # Replace && and || for validation
    test_string = string.replace("&&", "and").replace("||", "or")

    # Regex to validate expression format - updated to allow 'and', 'or'
    return _IS_SAFE_STRING_PATTERN.match(test_string) is not None and all(
        word not in test_string for word in reserved_words
    )


def merge_deep(obj1: Mapping[str, LocaleValue] | None, obj2: Mapping[str, LocaleValue]) -> LocaleDict:
    """
    Merge deep objects recursively.

    Args:
        obj1: First object to merge
        obj2: Second object to merge

    Returns:
        Merged object
    """
    merged: LocaleDict = {}

    if obj1:
        merged.update(obj1)

    for key, value in obj2.items():
        existing = merged.get(key)

        if isinstance(value, Mapping):
            value_mapping = cast(Mapping[str, LocaleValue], value)
            existing_mapping = (
                cast(Mapping[str, LocaleValue] | None, existing) if isinstance(existing, Mapping) else None
            )
            merged[key] = merge_deep(existing_mapping, value_mapping)
        else:
            merged[key] = value

    return merged


class DictMergeVisitor:
    """Visitor pattern for merging nested dictionaries efficiently."""

    merged: LocaleDict

    def __init__(self) -> None:
        """Initialize the merge visitor."""
        self.merged = {}

    def visit(self, obj1: Mapping[str, LocaleValue] | None, obj2: Mapping[str, LocaleValue]) -> LocaleDict:
        """
        Visit and merge two dictionaries.

        Args:
            obj1: First dictionary to merge
            obj2: Second dictionary to merge

        Returns:
            Merged dictionary
        """
        if obj1:
            self.merged.update(obj1)

        for key, value in obj2.items():
            existing = self.merged.get(key)
            self.merged[key] = self._merge_value(existing, value)

        return self.merged

    def _merge_value(self, existing: LocaleValue | None, new_value: LocaleValue) -> LocaleValue:
        """
        Merge a single value, recursing for nested dictionaries.

        Args:
            existing: Existing value
            new_value: New value to merge

        Returns:
            Merged value
        """
        if isinstance(new_value, Mapping):
            value_mapping = cast(Mapping[str, LocaleValue], new_value)
            existing_mapping = cast(Mapping[str, LocaleValue], existing) if isinstance(existing, Mapping) else None
            visitor = DictMergeVisitor()
            return visitor.visit(existing_mapping, value_mapping)

        return new_value


@functools.lru_cache(maxsize=128)
def _evaluate_expression(expression: str) -> bool:
    """Safely evaluate a boolean expression constructed from locale keys."""

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        return False

    try:
        return _evaluate_condition(tree.body)
    except ValueError:
        return False


def _evaluate_condition(node: ast.expr) -> bool:
    """Evaluate a parsed AST node that represents a conditional expression."""

    if isinstance(node, ast.BoolOp):
        results = [_evaluate_condition(value) for value in node.values]
        if isinstance(node.op, ast.And):
            return all(results)
        if isinstance(node.op, ast.Or):
            return any(results)
        raise ValueError

    if isinstance(node, ast.Compare):
        left = _evaluate_operand(node.left)
        for operator, comparator in zip(node.ops, node.comparators):
            right = _evaluate_operand(comparator)
            if not _apply_comparator(operator, left, right):
                return False
            left = right
        return True

    if isinstance(node, ast.Constant) and isinstance(node.value, bool):
        return node.value

    raise ValueError


def _evaluate_operand(node: ast.expr) -> FormatValue:
    """Evaluate an operand within a conditional expression."""

    if isinstance(node, ast.Constant) and isinstance(node.value, (bool, int, float, str)):
        return node.value

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        operand = _evaluate_operand(node.operand)
        if isinstance(operand, (int, float)):
            return operand if isinstance(node.op, ast.UAdd) else -operand
        raise ValueError

    raise ValueError


def _apply_comparator(operator: ast.cmpop, left: FormatValue, right: FormatValue) -> bool:
    """Apply a comparator node between two evaluated operands."""

    try:
        if isinstance(operator, ast.Eq):
            return left == right
        if isinstance(operator, ast.NotEq):
            return left != right
        if isinstance(operator, (ast.Gt, ast.GtE, ast.Lt, ast.LtE)):
            return _compare_ordered(operator, left, right)
    except TypeError as error:  # pragma: no cover - defensive guard
        raise ValueError from error

    raise ValueError


def _compare_ordered(operator: ast.cmpop, left: FormatValue, right: FormatValue) -> bool:
    """Compare two values using an ordering-aware comparator."""

    comparator_str = _STRING_COMPARATORS.get(type(operator))
    if comparator_str and isinstance(left, str) and isinstance(right, str):
        return comparator_str(left, right)

    comparator_num = _NUMERIC_COMPARATORS.get(type(operator))
    if comparator_num and isinstance(left, (int, float, bool)) and isinstance(right, (int, float, bool)):
        return comparator_num(float(left), float(right))

    raise ValueError
