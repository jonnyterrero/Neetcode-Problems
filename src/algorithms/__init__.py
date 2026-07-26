"""Reusable algorithm primitives used across notebooks and tests.

Keep this module small — it is not a general-purpose algorithms library.
Only add functions that are shared by multiple problems, notebooks, or
tests. Anything problem-specific belongs in that problem's folder.
"""

from src.algorithms.search import binary_search_first
from src.algorithms.two_pointers import (
    max_container_area,
    valid_palindrome_alphanumeric,
)

__all__ = [
    "binary_search_first",
    "max_container_area",
    "valid_palindrome_alphanumeric",
]
