"""Tools for chunking (segumentation, batching, slicing, etc.)"""

from itertools import zip_longest, chain, islice

from typing import (
    Iterable,
    Union,
    Dict,
    List,
    Tuple,
    Mapping,
    TypeVar,
    Iterator,
    Callable,
    Optional,
    T,
)

KT = TypeVar("KT")  # there's a typing.KT, but pylance won't allow me to use it!
VT = TypeVar("VT")  # there's a typing.VT, but pylance won't allow me to use it!


def chunk_iterable(
    iterable: Union[Iterable[T], Mapping[KT, VT]],
    chk_size: int,
    *,
    chunk_type: Optional[Callable[..., Union[Iterable[T], Mapping[KT, VT]]]] = None,
) -> Iterator[Union[List[T], Tuple[T, ...], Dict[KT, VT]]]:
    """
    Divide an iterable into chunks/batches of a specific size.

    Handles both mappings (e.g. dicts) and non-mappings (lists, tuples, sets...)
    as you probably expect it to (if you give a dict input, it will chunk on the
    (key, value) items and return dicts of these).
    Thought note that you always can control the type of the chunks with the
    `chunk_type` argument.

    Args:
        iterable: The iterable or mapping to divide.
        chk_size: The size of each chunk.
        chunk_type: The type of the chunks (list, tuple, set, dict...).

    Returns:
        An iterator of dicts if the input is a Mapping, otherwise an iterator
        of collections (list, tuple, set...).

    Examples:
        >>> list(chunk_iterable([1, 2, 3, 4, 5], 2))
        [[1, 2], [3, 4], [5]]

        >>> list(chunk_iterable((1, 2, 3, 4, 5), 3, chunk_type=tuple))
        [(1, 2, 3), (4, 5)]

        >>> list(chunk_iterable({"a": 1, "b": 2, "c": 3}, 2))
        [{'a': 1, 'b': 2}, {'c': 3}]

        >>> list(chunk_iterable({"x": 1, "y": 2, "z": 3}, 1, chunk_type=dict))
        [{'x': 1}, {'y': 2}, {'z': 3}]
    """
    if isinstance(iterable, Mapping):
        if chunk_type is None:
            chunk_type = dict
        it = iter(iterable.items())
        for first in it:
            yield {
                key: value for key, value in chain([first], islice(it, chk_size - 1))
            }
    else:
        if chunk_type is None:
            if isinstance(iterable, (list, tuple, set)):
                chunk_type = type(iterable)
            else:
                chunk_type = list
        it = iter(iterable)
        for first in it:
            yield chunk_type(chain([first], islice(it, chk_size - 1)))


def chunker(
    a: Iterable[T], chk_size: int, *, include_tail: bool = True
) -> Iterator[Tuple[T, ...]]:
    """
    Chunks an iterable into non-overlapping chunks of size `chk_size`.

    Note: This chunker is simpler, but also less efficient than `chunk_iterable`.
    It does have the extra `include_tail` argument, though.
    Though note that you can get the effect of `include_tail=False` in `chunk_iterable`
    by using `filter(lambda x: len(x) == chk_size, chunk_iterable(...))`.

    Args:
        a: The iterable to be chunked.
        chk_size: The size of each chunk.
        include_tail: If True, includes the remaining elements as the last chunk
                      even if they are fewer than `chk_size`. Defaults to True.

    Returns:
        An iterator of tuples, where each tuple is a chunk of size `chk_size`
        (or fewer elements if `include_tail` is True).

    Examples:
        >>> list(chunker(range(8), 3))
        [(0, 1, 2), (3, 4, 5), (6, 7)]
        >>> list(chunker(range(8), 3, include_tail=False))
        [(0, 1, 2), (3, 4, 5)]
    """
    it = iter(a)
    if include_tail:
        sentinel = object()
        for chunk in zip_longest(*([it] * chk_size), fillvalue=sentinel):
            yield tuple(item for item in chunk if item is not sentinel)
    else:
        yield from zip(*([it] * chk_size))
