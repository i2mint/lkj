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


from typing import Union, Callable, Dict, Any

# A match is represented as a dictionary (keys like "start", "end", etc.)
# and the replacement is either a static string or a callable that takes that
# dictionary and returns a string.
Replacement = Union[str, Callable[[Dict[str, Any]], str]]


class FindReplaceTool:
    r"""
    A general-purpose find-and-replace tool that can treat the input text
    as a continuous sequence of characters, even if operations such as viewing
    context are performed line by line. The tool can analyze matches based on
    a user-supplied regular expression, navigate through the matches with context,
    and perform replacements either interactively or in bulk. Replacements can be
    provided as either a static string or via a callback function that receives details
    of the match.

    Instead of keeping a single modified text, this version maintains a history of
    text versions in self._text_versions, where self._text_versions[0] is the original
    text and self._text_versions[-1] is the current text. Each edit is performed on the
    current version and appended to the history. Additional methods allow reverting changes.

    1: Basic usage
    -----------------------------------------------------
    >>> FindReplaceTool("apple banana apple").find_and_print_matches(r'apple')
    Match 0 (around line 1):
    apple banana apple
    ^^^^^
    ----------------------------------------
    Match 1 (around line 1):
    apple banana apple
                 ^^^^^
    ----------------------------------------
    >>> FindReplaceTool("apple banana apple").find_and_replace(r'apple', "orange")
    'orange banana orange'


    2: Using line_mode=True with a static replacement.
    --------------------------------------------------------
    >>> text1 = "apple\nbanana apple\ncherry"
    >>> tool = FindReplaceTool(text1, line_mode=True)
    >>> import re
    >>> # Find all occurrences of "apple" (two in total).
    >>> _ = tool.analyze(r'apple', flags=re.MULTILINE)
    >>> len(tool._matches)
    2
    >>> # Replace the first occurrence ("apple" on the first line) with "orange".
    >>> tool.replace_one(0, "orange").get_modified_text()
    'orange\nbanana apple\ncherry'

    3: Using line_mode=False with a callback replacement.
    -----------------------------------------------------------
    >>> text2 = "apple banana apple"
    >>> tool2 = FindReplaceTool(text2, line_mode=False)
    >>> # Find all occurrences of "apple" in the continuous text.
    >>> len(tool2.analyze(r'apple')._matches)
    2
    >>> # Define a callback that converts each matched text to uppercase.
    >>> def to_upper(match):
    ...     return match["matched_text"].upper()
    >>> tool2.replace_all(to_upper).get_modified_text()
    'APPLE banana APPLE'

    4: Reverting changes.
    ---------------------------
    >>> text3 = "one two three"
    >>> tool3 = FindReplaceTool(text3)
    >>> import re
    >>> # Analyze to match the first word "one" (at the start of the text).
    >>> tool3.analyze(r'^one').replace_one(0, "ONE").get_modified_text()
    'ONE two three'
    >>> # Revert the edit.
    >>> tool3.revert()
    'one two three'
    """

    def __init__(
        self,
        text: str,
        *,
        line_mode: bool = False,
        show_line_numbers: bool = True,
        context_size: int = 2,
        highlight_char: str = "^",
    ):
        # Maintain a list of text versions; the first element is the original text.
        self._text_versions = [text]
        self.line_mode = line_mode
        self.show_line_numbers = show_line_numbers
        self.context_size = context_size
        self.highlight_char = highlight_char

        # Internal storage for matches; each entry is a dict with:
        #   "start": start offset in the current text,
        #   "end": end offset in the current text,
        #   "matched_text": the text that was matched,
        #   "groups": any named groups from the regex,
        #   "line_number": the line number where the match occurs.
        self._matches = []

    # ----------------------------------------------------------------------------------
    # Main methods

    # TODO: Would like to have these functions be stateless
    def find_and_print_matches(self, pattern: str, *, flags: int = 0) -> None:
        """
        Searches the current text (the last version) for occurrences matching the given
        regular expression. Any match data (including group captures) is stored internally.
        """
        return self.analyze(pattern, flags).view_matches()

    def find_and_replace(
        self, pattern: str, replacement: Replacement, *, flags: int = 0
    ) -> None:
        """
        Searches the current text (the last version) for occurrences matching the given
        regular expression. Any match data (including group captures) is stored internally.
        """
        return self.analyze(pattern, flags).replace_all(replacement).get_modified_text()

    # ----------------------------------------------------------------------------------
    # Advanced methods

    def analyze(self, pattern: str, flags: int = 0) -> None:
        """
        Searches the current text (the last version) for occurrences matching the given
        regular expression. Any match data (including group captures) is stored internally.
        """
        import re

        self._matches.clear()
        current_text = self._text_versions[-1]
        for match in re.finditer(pattern, current_text, flags):
            match_data = {
                "start": match.start(),
                "end": match.end(),
                "matched_text": match.group(0),
                "groups": match.groupdict(),
                "line_number": current_text.count("\n", 0, match.start()),
            }
            self._matches.append(match_data)

        return self

    def view_matches(self) -> None:
        """
        Displays all stored matches along with surrounding context. When line_mode
        is enabled, the context is provided in full lines with (optionally) line numbers,
        and a line is added below the matched line to indicate the matched portion.
        In non-line mode, a snippet of characters around the match is shown.
        """
        current_text = self._text_versions[-1]
        if not self._matches:
            print("No matches found.")
            return

        if self.line_mode:
            lines = current_text.splitlines()
            for idx, m in enumerate(self._matches):
                line_num = m["line_number"]
                start_pos = m["start"]
                end_pos = m["end"]
                start_context = max(0, line_num - self.context_size)
                end_context = min(len(lines), line_num + self.context_size + 1)
                print(f"Match {idx} at line {line_num+1}:")
                for ln in range(start_context, end_context):
                    prefix = f"{ln+1:>4}  " if self.show_line_numbers else ""
                    print(prefix + lines[ln])
                    # For the match line, mark the position of the match.
                    if ln == line_num:
                        pos_in_line = start_pos - (
                            len("\n".join(lines[:ln])) + (1 if ln > 0 else 0)
                        )
                        highlight = " " * (
                            len(prefix) + pos_in_line
                        ) + self.highlight_char * (end_pos - start_pos)
                        print(highlight)
                print("-" * 40)
        else:
            snippet_radius = 20
            for idx, m in enumerate(self._matches):
                start, end = m["start"], m["end"]
                snippet_start = max(0, start - snippet_radius)
                snippet_end = min(len(current_text), end + snippet_radius)
                snippet = current_text[snippet_start:snippet_end]
                print(f"Match {idx} (around line {m['line_number']+1}):")
                print(snippet)
                highlight = " " * (start - snippet_start) + self.highlight_char * (
                    end - start
                )
                print(highlight)
                print("-" * 40)

    def replace_one(self, match_index: int, replacement: Replacement) -> None:
        """
        Replaces a single match, identified by match_index, with a new string.
        The 'replacement' argument may be either a static string or a callable.
        When it is a callable, it is called with a dictionary containing the match data
        (including any captured groups) and should return the replacement string.
        The replacement is performed on the current text version, and the new text is
        appended as a new version in the history.
        """

        if match_index < 0 or match_index >= len(self._matches):
            print(f"Invalid match index: {match_index}")
            return

        m = self._matches[match_index]
        start, end = m["start"], m["end"]
        current_text = self._text_versions[-1]

        # Determine the replacement string.
        if callable(replacement):
            new_replacement = replacement(m)
        else:
            new_replacement = replacement

        # Create the new text version.
        new_text = current_text[:start] + new_replacement + current_text[end:]
        self._text_versions.append(new_text)
        offset_diff = len(new_replacement) - (end - start)

        # Update offsets for subsequent matches (so they refer to the new text version).
        for i in range(match_index + 1, len(self._matches)):
            self._matches[i]["start"] += offset_diff
            self._matches[i]["end"] += offset_diff

        # Update the current match record.
        m["end"] = start + len(new_replacement)
        m["matched_text"] = new_replacement

        return self

    def replace_all(self, replacement: Replacement) -> None:
        """
        Replaces all stored matches in the current text version. The 'replacement' argument may
        be a static string or a callable (see replace_one for details). Replacements are performed
        from the last match to the first, so that earlier offsets are not affected.
        """
        for idx in reversed(range(len(self._matches))):
            self.replace_one(idx, replacement)

        return self

    def get_original_text(self) -> str:
        """Returns the original text (first version)."""
        return self._text_versions[0]

    def get_modified_text(self) -> str:
        """Returns the current (latest) text version."""
        return self._text_versions[-1]

    def revert(self, steps: int = 1):
        """
        Reverts the current text version by removing the last 'steps' versions
        from the history. The original text (version 0) is never removed.
        Returns the new current text.

        >>> text = "one two three"
        >>> tool = FindReplaceTool(text)
        >>> import re
        >>> tool.analyze(r'^one').replace_one(0, "ONE").get_modified_text()
        'ONE two three'
        >>> tool.revert()
        'one two three'
        """
        if steps < 1:
            return self.get_modified_text()
        while steps > 0 and len(self._text_versions) > 1:
            self._text_versions.pop()
            steps -= 1
        return self.get_modified_text()
