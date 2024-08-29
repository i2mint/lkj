"""Tools for working with dictionaries (and other Mappings)."""

from typing import Optional


# Note: There is a copy of truncate_dict_values in the ju package.
def truncate_dict_values(
    d: dict,
    *,
    max_list_size: Optional[int] = 2,
    max_string_size: Optional[int] = 66,
    middle_marker: str = "..."
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
