"""Core module."""

from collections.abc import Iterable, Iterator, Mapping, Sequence
from typing import Any, Literal, overload


@overload
def get_first[K, V, D](d: Mapping[K, V], /, keys: Iterable[K], default: D = None) -> V | D: ...


@overload
def get_first[K, V, D](
    d: Mapping[K, V], /, keys: Iterable[K], default: Any = None, no_default: Literal[True] = True
) -> V: ...


@overload
def get_first[K, V, D](
    d: Mapping[K, V], /, keys: Iterable[K], default: D = None, no_default: bool = True
) -> V | D: ...


def get_first[K, V, D](
    d: Mapping[K, V], /, keys: Iterable[K], default: D = None, no_default: bool = False
) -> V | D:
    """
    Return the first value for the first key that exists in the mapping.

    Args:
        d: The dictionary to search in.
        keys: The sequence of keys to look for.
        default: The value to return if no key is found.
        no_default: If `True`, raises a `KeyError` if no key is found.

    Returns:
        The value associated with the first found key, or the default value if not found.

    Raises:
        KeyError: If `no_default` is `True` and none of the keys are found.

    Examples:
        >>> d = {"a": 1, "b": 2, "c": 3}
        >>> get_first(d, ["x", "a", "b"])
        1
        >>> get_first(d, ["x", "y"], default=0)
        0
        >>> get_first(d, ["x", "y"], no_default=True)  # Raises: KeyError
        Traceback (most recent call last):
        ...
        KeyError: "None of the keys ['x', 'y'] were found in the mapping."
    """
    for key in keys:
        if key in d:
            return d[key]

    if no_default:
        raise KeyError(f"None of the keys {list(keys)} were found in the mapping.")  # noqa: TRY003

    return default


def batch[S: Sequence[Any]](seq: S, /, size: int) -> Iterator[S]:
    """
    Generate batches of the sequence.

    Args:
        seq: The sequence to batch.
        size: Size of the batches. Last batch may be shorter.

    Returns:
        The batched sequence.

    Examples:
        >>> seq = list(range(10))
        >>> list(batch(seq, 3))
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    l = len(seq)
    for ndx in range(0, l, size):
        yield seq[ndx : min(ndx + size, l)]  # pyright: ignore[reportReturnType]
