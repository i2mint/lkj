"""Utils for strings"""

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
