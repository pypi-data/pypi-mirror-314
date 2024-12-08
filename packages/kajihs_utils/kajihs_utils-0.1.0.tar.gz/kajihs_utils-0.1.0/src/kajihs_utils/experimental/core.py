"""Core module."""

from collections.abc import Callable
from typing import Any


def make_yamlizable[T](obj: T, /, replace_fn: Callable[[Any], Any] | None = None) -> T:
    """
    Recursively convert non-serializable objects to their names in a copy of a dictionary.

    Args:
        obj: The dictionary to make YAML-serializable.
        replace_fn: A function to replace non-serializable objects. If None,
            replace callable objects with their names.

    Returns:
        A YAML-serializable dictionary.
    """
    # By default, replace callable objects with their names
    if replace_fn is None:
        replace_fn = lambda v: v.__name__ if callable(v) else v

    if isinstance(obj, dict):
        return {k: make_yamlizable(v, replace_fn) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_yamlizable(item, replace_fn) for item in obj]
    if isinstance(obj, tuple):
        return tuple(make_yamlizable(item, replace_fn) for item in obj)
    if isinstance(obj, float) and obj.is_integer():
        return int(obj)
    return replace_fn(obj)
