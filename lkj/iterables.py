"""Tools with iterables (dicts, lists, tuples, sets, etc.)."""

from typing import Sequence, Mapping, KT, VT, Iterable


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
