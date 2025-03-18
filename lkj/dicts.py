"""
Tools for working with dictionaries (and other Mappings).

If you are looking for more, check out the `lkj.iterables` module too
(after all, dicts are iterables).

"""

from typing import Optional


def inclusive_subdict(d, include):
    """
    Returns a new dictionary with only the keys in `include`.

    Parameters:
    d (dict): The input dictionary.
    include (set): The set of keys to include in the new dictionary.

    Example:

    >>> assert inclusive_subdict({'a': 1, 'b': 2, 'c': 3}, {'a', 'c'}) == {'a': 1, 'c': 3}

    """
    return {k: d[k] for k in d.keys() & include}


def exclusive_subdict(d, exclude):
    """
    Returns a new dictionary with only the keys not in `exclude`.

    Parameters:
    d (dict): The input dictionary.
    exclude (set): The set of keys to exclude from the new dictionary.

    Example:
    >>> exclusive_subdict({'a': 1, 'b': 2, 'c': 3}, {'a', 'c'})
    {'b': 2}

    """
    return {k: d[k] for k in d.keys() - exclude}


# Note: There is a copy of truncate_dict_values in the ju package.
def truncate_dict_values(
    d: dict,
    *,
    max_list_size: Optional[int] = 2,
    max_string_size: Optional[int] = 66,
    middle_marker: str = "...",
) -> dict:
    """
    Returns a new dictionary with the same nested keys structure, where:
    - List values are reduced to a maximum size of max_list_size.
    - String values longer than max_string_size are truncated in the middle.

    Parameters:
    d (dict): The input dictionary.
    max_list_size (int, optional): Maximum size for lists. Defaults to 2.
    max_string_size (int, optional): Maximum length for strings. Defaults to None (no truncation).
    middle_marker (str, optional): String to insert in the middle of truncated strings. Defaults to '...'.

    Returns:
    dict: A new dictionary with truncated lists and strings.

    This can be useful when you have a large dictionary that you want to investigate,
    but printing/logging it takes too much space.

    Example:

    >>> large_dict = {'a': [1, 2, 3, 4, 5], 'b': {'c': [6, 7, 8, 9], 'd': 'A string like this that is too long'}, 'e': [10, 11]}
    >>> truncate_dict_values(large_dict, max_list_size=3, max_string_size=20)
    {'a': [1, 2, 3], 'b': {'c': [6, 7, 8], 'd': 'A string...too long'}, 'e': [10, 11]}

    You can use `None` to indicate "no max":

    >>> assert (
    ...     truncate_dict_values(large_dict, max_list_size=None, max_string_size=None)
    ...     == large_dict
    ... )

    """

    def truncate_string(value, max_len, marker):
        if max_len is None or len(value) <= max_len:
            return value
        half_len = (max_len - len(marker)) // 2
        return value[:half_len] + marker + value[-half_len:]

    kwargs = dict(
        max_list_size=max_list_size,
        max_string_size=max_string_size,
        middle_marker=middle_marker,
    )
    if isinstance(d, dict):
        return {k: truncate_dict_values(v, **kwargs) for k, v in d.items()}
    elif isinstance(d, list):
        return (
            [truncate_dict_values(v, **kwargs) for v in d[:max_list_size]]
            if max_list_size is not None
            else d
        )
    elif isinstance(d, str):
        return truncate_string(d, max_string_size, middle_marker)
    else:
        return d


from typing import Mapping, Callable, TypeVar, Iterable, Tuple

KT = TypeVar("KT")  # Key type
VT = TypeVar("VT")  # Value type


# Note: Could have all function parameters (recursive_condition, etc.) also take the
#       enumerated index of the mapping as an argument. That would give us even more
#       flexibility, but it might be overkill and make the interface more complex.
def merge_dicts(
    *mappings: Mapping[KT, VT],
    recursive_condition: Callable[[VT], bool] = lambda v: isinstance(v, Mapping),
    conflict_resolver: Callable[[VT, VT], VT] = lambda x, y: y,
    mapping_constructor: Callable[[Iterable[Tuple[KT, VT]]], Mapping[KT, VT]] = dict,
) -> Mapping[KT, VT]:
    """
    Merge multiple mappings into a single mapping, recursively if needed,
    with customizable conflict resolution for non-mapping values.

    This function generalizes the normal `dict.update()` method, which takes the union
    of the keys and resolves conflicting values by overriding them with the last value.
    While `dict.update()` performs a single-level merge, `merge_dicts` provides additional
    flexibility to handle nested mappings. With `merge_dicts`, you can:
    - Control when to recurse (e.g., based on whether a value is a `Mapping`).
    - Specify how to resolve value conflicts (e.g., override, add, or accumulate in a list).
    - Choose the type of mapping (e.g., `dict`, `defaultdict`) to use as the container.

    Args:
        mappings: The mappings to merge.
        recursive_condition: A callable to determine if values should be merged recursively.
                             By default, checks if the value is a `Mapping`.
        conflict_resolver: A callable that resolves conflicts between two values.
                           By default, overrides with the last seen value (`lambda x, y: y`).
        mapping_constructor: A callable to construct the resulting mapping.
                             Defaults to the standard `dict` constructor.

    Returns:
        A merged mapping that combines all the input mappings.

    Examples:
        Basic usage with single-level merge (override behavior):
        >>> dict1 = {"a": 1}
        >>> dict2 = {"a": 2, "b": 3}
        >>> merge_dicts(dict1, dict2)
        {'a': 2, 'b': 3}

        Handling nested mappings with default behavior (override conflicts):
        >>> dict1 = {"a": 1, "b": {"x": 10, "y": 20}}
        >>> dict2 = {"b": {"y": 30, "z": 40}, "c": 3}
        >>> dict3 = {"b": {"x": 50}, "d": 4}
        >>> merge_dicts(dict1, dict2, dict3)
        {'a': 1, 'b': {'x': 50, 'y': 30, 'z': 40}, 'c': 3, 'd': 4}

        Resolving conflicts by summing values:
        >>> dict1 = {"a": 1}
        >>> dict2 = {"a": 2}
        >>> merge_dicts(dict1, dict2, conflict_resolver=lambda x, y: x + y)
        {'a': 3}

        Accumulating conflicting values into a list:
        >>> dict1 = {"a": 1, "b": [1, 2]}
        >>> dict2 = {"b": [3, 4]}
        >>> merge_dicts(dict1, dict2, conflict_resolver=lambda x, y: x + y if isinstance(x, list) else [x, y])
        {'a': 1, 'b': [1, 2, 3, 4]}

        Recursing only on specific conditions:
        >>> dict1 = {"a": {"nested": 1}}
        >>> dict2 = {"a": {"nested": 2, "new": 3}}
        >>> merge_dicts(dict1, dict2)
        {'a': {'nested': 2, 'new': 3}}

        >>> dict1 = {"a": {"nested": [1, 2]}}
        >>> dict2 = {"a": {"nested": [3, 4]}}
        >>> merge_dicts(dict1, dict2, recursive_condition=lambda v: isinstance(v, dict))
        {'a': {'nested': [3, 4]}}

        Using a custom mapping type (`defaultdict`):
        >>> from collections import defaultdict
        >>> merge_dicts(
        ...     dict1, dict2, mapping_constructor=lambda items: defaultdict(int, items)
        ... )
        defaultdict(<class 'int'>, {'a': defaultdict(<class 'int'>, {'nested': [3, 4]})})
    """
    # Initialize merged mapping with an empty iterable for constructors requiring input
    merged = mapping_constructor([])

    for mapping in mappings:
        for key, value in mapping.items():
            if (
                key in merged
                and recursive_condition(value)
                and recursive_condition(merged[key])
            ):
                # Recursively merge nested mappings
                merged[key] = merge_dicts(
                    merged[key],
                    value,
                    recursive_condition=recursive_condition,
                    conflict_resolver=conflict_resolver,
                    mapping_constructor=mapping_constructor,
                )
            elif key in merged:
                # Resolve conflict using the provided resolver
                merged[key] = conflict_resolver(merged[key], value)
            else:
                # Otherwise, add the value
                merged[key] = value

    return merged


import operator
from typing import Callable, Dict, Any

Comparison = Any
Comparator = Callable[[dict, dict], Comparison]


def _common_keys_list(dict1, dict2):
    return [k for k in dict1.keys() if k in dict2.keys()]


def compare_field_values(
    dict1,
    dict2,
    *,
    field_comparators: Dict[KT, Comparator] = {},
    default_comparator: Comparator = operator.eq,
    aggregator: Callable[
        [Dict[KT, Comparison]], Any
    ] = lambda d: d,  # lambda d: np.mean(list(d.values())),
    get_comparison_fields: Callable[[dict], Iterable[KT]] = _common_keys_list,
):
    """
    Compare two dictionaries' values field by field

    :param dict1: The first dictionary.
    :param dict2: The second dictionary.
    :param field_comparators: A dictionary where keys are field names and values are comparator functions.
    :param default_comparator: A default comparator function to use if no specific comparator is provided for a field.
    :param aggregator: A function to aggregate the comparison results into a final comparison object.
    :return: A final score based on the comparison results.

    >>> dict1 = {"color": "brown", "animal": "dog"}
    >>> dict2 = {"color": "brown", "animal": "cat"}
    >>> dict3 = {"color": "brown", "animal": "bird"}
    >>> field_comparators = {
    ...     "color": lambda x, y: 1 if x == y else 0,
    ...     "animal": lambda x, y: 1 if len(x) == len(y) else 0
    ... }
    >>> compare_field_values(dict1, dict2, field_comparators=field_comparators)
    {'color': 1, 'animal': 1}
    >>> compare_field_values(dict1, dict3, field_comparators=field_comparators)
    {'color': 1, 'animal': 0}
    >>> import functools, statistics
    >>> aggregator = lambda d: statistics.mean(d.values())
    >>> mean_of_values = functools.partial(
    ...     compare_field_values, field_comparators=field_comparators, aggregator=aggregator
    ... )
    >>> mean_of_values(dict1, dict2)
    1
    >>> mean_of_values(dict1, dict3)
    0.5

    """
    common_keys = get_comparison_fields(dict1, dict2)

    comparisons = {}
    for key in common_keys:
        comparator = field_comparators.get(key, default_comparator)
        comparisons[key] = comparator(dict1[key], dict2[key])

    return aggregator(comparisons)
