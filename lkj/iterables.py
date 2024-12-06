"""Tools with iterables (dicts, lists, tuples, sets, etc.)."""

from typing import Sequence, Mapping, KT, VT, Iterable, Iterable, NamedTuple


class SetsComparisonResult(NamedTuple):
    common: set
    left_only: set
    right_only: set


def compare_sets(left: Iterable, right: Iterable) -> SetsComparisonResult:
    """
    Compares two iterables and returns a named tuple with:
    - Elements in both iterables.
    - Elements only in the left iterable.
    - Elements only in the right iterable.

    Note: When applied to dicts, the comparison is done on the keys.
    If you want a comparison on the values, use `compare_iterables(left.values(), right.values())`.

    Args:
        left (Iterable): The first iterable.
        right (Iterable): The second iterable.

    Returns:
        SetsComparisonResult: A namedtuple with fields `common`,
        `left_only`, and `right_only`.

    Examples:
        >>> left = ['a', 'b', 'c']
        >>> right = ['b', 'c', 'd']
        >>> result = compare_sets(left, right)
        >>> assert result.common == {'b', 'c'}  # asserting because order is not guaranteed
        >>> result.left_only
        {'a'}
        >>> result.right_only
        {'d'}
    """
    left_set = set(left)
    right_set = set(right)

    return SetsComparisonResult(
        common=left_set & right_set,
        left_only=left_set - right_set,
        right_only=right_set - left_set,
    )


def index_of(iterable: Iterable[VT], value: VT) -> int:
    """
    List list.index but for any iterable.

    >>> index_of(iter('abc'), 'b')
    1
    >>> index_of(iter(range(5)), 3)
    3
    >>> index_of(iter('abc'), 'z')  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError: 'z' is not in iterable

    """
    for i, element in enumerate(iterable):
        if element == value:
            return i
    # if not found:
    raise ValueError(f"{value} is not in iterable")


def get_by_value(
    list_of_dicts: Sequence[Mapping[KT, VT]], value: VT, field: KT
) -> Mapping[KT, VT]:
    """
    Get a dictionary from a list of dictionaries by a field value.

    >>> data = [{'id': 1, 'value': 'A'}, {'id': 2, 'value': 'B'}]
    >>> get_by_value(data, 2, 'id')
    {'id': 2, 'value': 'B'}

    This function just WANTS to be `functools.partial`-ized!!

    >>> from functools import partial
    >>> get_by_id = partial(get_by_value, field='id')
    >>> get_by_id(data, 1)
    {'id': 1, 'value': 'A'}
    >>> get_value_of_B = partial(get_by_value, value='B', field='value')
    >>> get_value_of_B(data)
    {'id': 2, 'value': 'B'}

    """
    d = next(filter(lambda d: d[field] == value, list_of_dicts), None)
    if d is not None:
        return d
    else:
        raise ValueError(f"Value {value} not found in list of dicts")
