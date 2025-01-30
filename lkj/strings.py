"""Utils for strings"""

import re


def indent_lines(string: str, indent: str, *, line_sep="\n") -> str:
    r"""
    Indent each line of a string.

    :param string: The string to indent.
    :param indent: The string to use for indentation.
    :return: The indented string.

    >>> print(indent_lines('This is a test.\nAnother line.', ' ' * 8))
            This is a test.
            Another line.
    """
    return line_sep.join(indent + line for line in string.split(line_sep))


def most_common_indent(string: str, ignore_first_line=False) -> str:
    r"""
    Find the most common indentation in a string.

    :param string: The string to analyze.
    :param ignore_first_line: Whether to ignore the first line when determining the
        indentation. Default is False. One case where you want True is when using python
        triple quotes (as in docstrings, for example), since the first line often has
        no indentation (from the point of view of the string, in this case.
    :return: The most common indentation string.

    Examples:

    >>> most_common_indent('    This is a test.\n    Another line.')
    '    '
    """
    indents = re.findall(r"^( *)\S", string, re.MULTILINE)
    n_lines = len(indents)
    if ignore_first_line and n_lines > 1:
        # if there's more than one line, ignore the indent of the first
        indents = indents[1:]
    return max(indents, key=indents.count)


from string import Formatter

formatter = Formatter()


def fields_of_string_format(template):
    return [
        field_name for _, field_name, _, _ in formatter.parse(template) if field_name
    ]


def fields_of_string_formats(templates, *, aggregator=set):
    """
    Extract all unique field names from the templates in _github_url_templates using string.Formatter.

    Args:
        templates (list): A list of dictionaries containing 'template' keys.

    Returns:
        list: A sorted list of unique field names found in the templates.

    Example:
        >>> templates = ['{this}/and/{that}', 'and/{that}/is/an/{other}']
        >>> sorted(fields_of_string_formats(templates))
        ['other', 'that', 'this']
    """

    def field_names():
        for template in templates:
            yield from fields_of_string_format(template)

    return aggregator(field_names())


import re

# Compiled regex to handle camel case to snake case conversions, including acronyms
_camel_to_snake_re = re.compile(r"((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))")


def camel_to_snake(camel_string):
    """
    Convert a CamelCase string to snake_case. Useful for converting class
    names to variable names.

    Args:
        camel_string (str): The CamelCase string to convert.

    Returns:
        str: The converted snake_case string.

    Examples:
        >>> camel_to_snake('BasicParseTest')
        'basic_parse_test'
        >>> camel_to_snake('HTMLParser')
        'html_parser'
        >>> camel_to_snake('CamelCaseExample')
        'camel_case_example'

        Note that acronyms are handled correctly:

        >>> camel_to_snake('XMLHttpRequestTest')
        'xml_http_request_test'
    """
    return _camel_to_snake_re.sub(r"_\1", camel_string).lower()


def snake_to_camel(snake_string):
    """
    Convert a snake_case string to CamelCase. Useful for converting variable
    names to class names.

    Args:
        snake_string (str): The snake_case string to convert.

    Returns:
        str: The converted CamelCase string.

    Examples:

        >>> snake_to_camel('complex_tokenizer')
        'ComplexTokenizer'
        >>> snake_to_camel('simple_example_test')
        'SimpleExampleTest'

        Note that acronyms are capitalized correctly:

        >>> snake_to_camel('xml_http_request_test')
        'XmlHttpRequestTest'
    """
    return "".join(word.capitalize() or "_" for word in snake_string.split("_"))


# Note: Vendored in i2.multi_objects and dol.util
def truncate_string(s: str, *, left_limit=15, right_limit=15, middle_marker="..."):
    """
    Truncate a string to a maximum length, inserting a marker in the middle.

    If the string is longer than the sum of the left_limit and right_limit,
    the string is truncated and the middle_marker is inserted in the middle.

    If the string is shorter than the sum of the left_limit and right_limit,
    the string is returned as is.

    >>> truncate_string('1234567890')
    '1234567890'

    But if the string is longer than the sum of the limits, it is truncated:

    >>> truncate_string('1234567890', left_limit=3, right_limit=3)
    '123...890'
    >>> truncate_string('1234567890', left_limit=3, right_limit=0)
    '123...'
    >>> truncate_string('1234567890', left_limit=0, right_limit=3)
    '...890'

    If you're using a specific parametrization of the function often, you can
    create a partial function with the desired parameters:

    >>> from functools import partial
    >>> truncate_string = partial(truncate_string, left_limit=2, right_limit=2, middle_marker='---')
    >>> truncate_string('1234567890')
    '12---90'
    >>> truncate_string('supercalifragilisticexpialidocious')
    'su---us'

    """
    if len(s) <= left_limit + right_limit:
        return s
    elif right_limit == 0:
        return s[:left_limit] + middle_marker
    elif left_limit == 0:
        return middle_marker + s[-right_limit:]
    else:
        return s[:left_limit] + middle_marker + s[-right_limit:]


truncate_string_with_marker = truncate_string  # backwards compatibility alias


def truncate_lines(
    s: str, top_limit: int = None, bottom_limit: int = None, middle_marker: str = "..."
) -> str:
    """
    Truncates a string by limiting the number of lines from the top and bottom.
    If the total number of lines is greater than top_limit + bottom_limit,
    it keeps the first `top_limit` lines, keeps the last `bottom_limit` lines,
    and replaces the omitted middle portion with a single line containing
    `middle_marker`.

    If top_limit or bottom_limit is None, it is treated as 0.

    Example:
        >>> text = '''Line1
        ... Line2
        ... Line3
        ... Line4
        ... Line5
        ... Line6'''

        >>> print(truncate_lines(text, top_limit=2, bottom_limit=2))
        Line1
        Line2
        ...
        Line5
        Line6
    """
    # Interpret None as zero for convenience
    top = top_limit if top_limit is not None else 0
    bottom = bottom_limit if bottom_limit is not None else 0

    # Split on line boundaries (retaining any trailing newlines in each piece)
    lines = s.splitlines(True)
    total_lines = len(lines)

    # If no need to truncate, return as is
    if total_lines <= top + bottom:
        return s

    # Otherwise, keep the top lines, keep the bottom lines,
    # and insert a single marker line in the middle
    truncated = lines[:top] + [middle_marker + "\n"] + lines[-bottom:]
    return "".join(truncated)


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
    ``substitute`` function. See how the replacements dict has been ordered by
    descending length of keys. This is to ensure that longer keys are replaced
    before shorter keys, avoiding partial replacements.

    >>> substitute.replacements
    {'banana': 'grape', 'apple': 'orange'}

    """
    import re
    from functools import partial

    if regex is None and s is None:
        # Sort keys by length while maintaining value alignment
        sorted_replacements = sorted(
            replacements.items(), key=lambda x: len(x[0]), reverse=True
        )

        # Create regex pattern from sorted keys (without escaping to allow regex)
        sorted_keys = [pair[0] for pair in sorted_replacements]
        sorted_values = [pair[1] for pair in sorted_replacements]
        regex = re.compile("|".join(sorted_keys))

        # Prepare the substitution function with aligned replacements
        aligned_replacements = dict(zip(sorted_keys, sorted_values))
        substitute = partial(regex_based_substitution, aligned_replacements, regex)
        substitute.replacements = aligned_replacements
        substitute.regex = regex
        return substitute
    elif s is not None:
        # Perform substitution using the compiled regex and aligned replacements
        return regex.sub(lambda m: replacements[m.group(0)], s)
    else:
        raise ValueError(
            "Invalid usage: provide either `s` or let the function construct itself."
        )


from typing import Callable, Iterable, Sequence


class TrieNode:
    def __init__(self):
        self.children = {}
        self.count = 0  # Number of times this node is visited during insertion
        self.is_end = False  # Indicates whether this node represents the end of an item


def identity(x):
    return x


def unique_affixes(
    items: Iterable[Sequence],
    suffix: bool = False,
    *,
    egress: Callable = None,
    ingress: Callable = identity,
) -> Iterable[Sequence]:
    """
    Returns a list of unique prefixes (or suffixes) for the given iterable of sequences.
    Raises a ValueError if duplicates are found.

    Parameters:
    - items: Iterable of sequences (e.g., list of strings).
    - suffix: If True, finds unique suffixes instead of prefixes.
    - ingress: Callable to preprocess each item. Default is identity function.
    - egress: Callable to postprocess each affix. Default is appropriate function based on item type.
      Usually, ingress and egress are inverses of each other.

    >>> unique_affixes(['apple', 'ape', 'apricot', 'banana', 'band', 'bandana'])
    ['app', 'ape', 'apr', 'bana', 'band', 'banda']

    >>> unique_affixes(['test', 'testing', 'tester'])
    ['test', 'testi', 'teste']

    >>> unique_affixes(['test', 'test'])
    Traceback (most recent call last):
    ...
    ValueError: Duplicate item detected: test

    >>> unique_affixes(['abc', 'abcd', 'abcde'])
    ['abc', 'abcd', 'abcde']

    >>> unique_affixes(['a', 'b', 'c'])
    ['a', 'b', 'c']

    >>> unique_affixes(['x', 'xy', 'xyz'])
    ['x', 'xy', 'xyz']

    >>> unique_affixes(['can', 'candy', 'candle'])
    ['can', 'candy', 'candl']

    >>> unique_affixes(['flow', 'flower', 'flight'])
    ['flow', 'flowe', 'fli']

    >>> unique_affixes(['ation', 'termination', 'examination'], suffix=True)
    ['ation', 'rmination', 'amination']

    >>> import functools
    >>> ingress = functools.partial(str.split, sep='.')
    >>> egress = '.'.join
    >>> items = ['here.and.there', 'here.or.there', 'here']
    >>> unique_affixes(items, ingress=ingress, egress=egress)
    ['here.and', 'here.or', 'here']

    """
    items = list(map(ingress, items))

    # Determine the default egress function based on item type
    if egress is None:
        if all(isinstance(item, str) for item in items):
            # Items are strings; affixes are lists of characters
            def egress(affix):
                return "".join(affix)

        else:
            # Items are sequences (e.g., lists); affixes are lists
            def egress(affix):
                return affix

    # If suffix is True, reverse the items
    if suffix:
        items = [item[::-1] for item in items]

    # Build the trie and detect duplicates
    root = TrieNode()
    for item in items:
        node = root
        for element in item:
            if element not in node.children:
                node.children[element] = TrieNode()
            node = node.children[element]
            node.count += 1
        # At the end of the item
        if node.is_end:
            # Duplicate detected
            if suffix:
                original_item = item[::-1]
            else:
                original_item = item
            original_item = egress(original_item)
            raise ValueError(f"Duplicate item detected: {original_item}")
        node.is_end = True

    # Find the minimal unique prefixes/suffixes
    affixes = []
    for item in items:
        node = root
        affix = []
        for element in item:
            node = node.children[element]
            affix.append(element)
            if node.count == 1:
                break
        if suffix:
            affix = affix[::-1]
        affixes.append(affix)

    # Postprocess affixes using egress
    affixes = list(map(egress, affixes))
    return affixes
