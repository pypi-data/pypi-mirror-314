"""
A small utility to generate JSON schemas for python functions.
"""

from .core import Annotated, Doc, FunctionSchema, get_function_schema, guess_type

__version__ = "0.4.4"
__all__ = (
    "__version__",
    "get_function_schema",
    "guess_type",
    "Doc",
    "Annotated",
    "FunctionSchema",
)
