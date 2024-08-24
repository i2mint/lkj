"""Miscellaneous tools."""

from operator import attrgetter, ge, gt, le, lt
from functools import partial
from typing import Callable, T, Optional, Any


def identity(x):
    return x


def value_in_interval(
    x: Any = None,
    /,
    *,
    get_val: Callable[[Any], T] = identity,
    min_val: Optional[T] = None,
    max_val: Optional[T] = None,
    is_minimum: Callable[[T, T], bool] = ge,
    is_maximum: Callable[[T, T], bool] = lt,
):
    """

    >>> from operator import itemgetter, le
    >>> f = value_in_interval(get_val=itemgetter('date'), min_val=2, max_val=8)
    >>> d = [{'date': 1}, {'date': 2}, {'date': 3, 'x': 7}, {'date': 8}, {'date': 9}]
    >>> list(map(f, d))
    [False, True, True, False, False]

    The default `is_maximum` is `lt` (i.e. lambda x: x < max_val). If you want to
    use `le` (i.e. lambda x: x <= max_val) you can change the is_maximum argument:

    >>> ff = value_in_interval(
    ...     get_val=itemgetter('date'), min_val=2, max_val=8, is_maximum=le
    ... )
    >>> list(map(ff, d))
    [False, True, True, True, False]
    """
    if x is None:
        kwargs = locals()
        kwargs.pop('x')
        return partial(value_in_interval, **kwargs)
    else:
        val = get_val(x)
        if min_val is not None and not is_minimum(val, min_val):
            return False
        if max_val is not None and not is_maximum(val, max_val):
            return False
        return True
