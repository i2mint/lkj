"""Utils for strings"""


def regex_based_substitution(s: str = None, *, replacements: dict = (), regex=None):
    """
    Construct a substitution function based on an iterable of replacement pairs.

    :param replacements: An iterable of (replace_this, with_that) pairs.
    :type replacements: iterable[tuple[str, str]]
    :return: A function that, when called with a string, will perform all substitutions.
    :rtype: Callable[[str], str]

    >>> replacements = [("apple", "orange"), ("banana", "grape")]
    >>> sub_func = construct_substitution_function(replacements)
    >>> input_str = "I like apple and banana."
    >>> sub_func(input_str)
    'I like orange and grape.'
    """
    import re
    from functools import partial

    if s is None:
        assert regex is not None, f"regex must be provided if s is None"
        replacements = dict(replacements)

        if not replacements:  # if replacements iterable is empty.
            return lambda s: s  # return identity function

        regex = re.compile("|".join(re.escape(src) for src in replacements))

        return partial(
            regex_based_substitution, replacements=replacements, regex=regex
        )
    else:
        return regex.sub(lambda m: replacements[m.group(0)], s)
