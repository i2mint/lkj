"""Utils for strings"""


# Note: Vendored in i2.multi_objects and dol.util
def truncate_string_with_marker(
    s, *, left_limit=15, right_limit=15, middle_marker='...'
):
    """
    Return a string with a limited length.

    If the string is longer than the sum of the left_limit and right_limit,
    the string is truncated and the middle_marker is inserted in the middle.

    If the string is shorter than the sum of the left_limit and right_limit,
    the string is returned as is.

    >>> truncate_string_with_marker('1234567890')
    '1234567890'

    But if the string is longer than the sum of the limits, it is truncated:

    >>> truncate_string_with_marker('1234567890', left_limit=3, right_limit=3)
    '123...890'
    >>> truncate_string_with_marker('1234567890', left_limit=3, right_limit=0)
    '123...'
    >>> truncate_string_with_marker('1234567890', left_limit=0, right_limit=3)
    '...890'

    If you're using a specific parametrization of the function often, you can
    create a partial function with the desired parameters:

    >>> from functools import partial
    >>> truncate_string = partial(truncate_string_with_marker, left_limit=2, right_limit=2, middle_marker='---')
    >>> truncate_string('1234567890')
    '12---90'
    >>> truncate_string('supercalifragilisticexpialidocious')
    'su---us'

    """
    middle_marker_len = len(middle_marker)
    if len(s) <= left_limit + right_limit:
        return s
    elif right_limit == 0:
        return s[:left_limit] + middle_marker
    elif left_limit == 0:
        return middle_marker + s[-right_limit:]
    else:
        return s[:left_limit] + middle_marker + s[-right_limit:]


# TODO: Generalize so that it can be used with regex keys (not escaped)
def regex_based_substitution(replacements: dict, regex=None, s: str = None):
    """
    Construct a substitution function based on an iterable of replacement pairs.

    :param replacements: An iterable of (replace_this, with_that) pairs.
    :type replacements: iterable[tuple[str, str]]
    :return: A function that, when called with a string, will perform all substitutions.
    :rtype: Callable[[str], str]

    The function is meant to be used with ``replacements`` as its single input,
    returning a ``substitute`` function that will carry out the substitutions
    on an input string.

    >>> replacements = {'apple': 'orange', 'banana': 'grape'}
    >>> substitute = regex_based_substitution(replacements)
    >>> substitute("I like apple and bananas.")
    'I like orange and grapes.'

    You have access to the ``replacements`` and ``regex`` attributes of the
    ``substitute`` function:

    >>> substitute.replacements
    {'apple': 'orange', 'banana': 'grape'}

    """
    import re
    from functools import partial

    if regex is None and s is None:
        replacements = dict(replacements)

        if not replacements:  # if replacements iterable is empty.
            return lambda s: s  # return identity function

        regex = re.compile('|'.join(re.escape(key) for key in replacements.keys()))

        substitute = partial(regex_based_substitution, replacements, regex)
        substitute.replacements = replacements
        substitute.regex = regex
        return substitute
    else:
        return regex.sub(lambda m: replacements[m.group(0)], s)
