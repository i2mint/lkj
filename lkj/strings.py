"""
String Utilities Module

This module provides a comprehensive set of utility functions and classes for working with strings in Python.
It includes tools for string manipulation, formatting, pretty-printing, and find/replace operations.

Core Components:

- StringAppender: A helper class for collecting strings, useful for capturing output that would otherwise be printed.
- indent_lines: Indents each line of a string by a specified prefix.
- most_common_indent: Determines the most common indentation used in a multi-line string.
- FindReplaceTool: A class for advanced find-and-replace operations on strings, supporting regular expressions, match history, and undo functionality.

Pretty-Printing Functions:

- print_list: Prints lists in various human-friendly formats (wrapped, columns, numbered, bullet, table, compact), with options for width, separators, and custom print functions.
- print_list.as_table: Formats and prints a list (or list of lists) as a table, with optional headers and alignment.
- print_list.summary: Prints a summary of a list, showing first few and last few items if the list is long.
- print_list.compact, print_list.wrapped, print_list.columns, print_list.numbered, print_list.bullets: Convenience methods using print_list's partial functionality for common display styles.

These utilities are designed to make it easier to display, format, and manipulate strings and collections of strings in a readable and flexible way.
"""

import re
from typing import Iterable, Sequence, Callable, Optional, Any, Literal
from functools import partial


class StringAppender:
    """Helper class to collect strings instead of printing them directly."""

    def __init__(self, separator="\n"):
        self.lines = []
        self.separator = separator

    def __call__(self, text):
        """Append text to the internal list."""
        self.lines.append(str(text))

    def __str__(self):
        """Return the collected string."""
        return self.separator.join(self.lines)

    def get_string(self):
        """Alternative way to get the string."""
        return str(self)


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
    >>> tool = FindReplaceTool(text1, line_mode=True, flags=re.MULTILINE)
    >>> import re
    >>> # Find all occurrences of "apple" (two in total).
    >>> _ = tool.analyze(r'apple')
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
        flags: int = 0,
        show_line_numbers: bool = True,
        context_size: int = 2,
        highlight_char: str = "^",
    ):
        # Maintain a list of text versions; the first element is the original text.
        self._text_versions = [text]
        self.line_mode = line_mode
        self.flags = flags
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
    def find_and_print_matches(self, pattern: str) -> None:
        """
        Searches the current text (the last version) for occurrences matching the given
        regular expression. Any match data (including group captures) is stored internally.
        """
        return self.analyze(pattern).view_matches()

    def find_and_replace(self, pattern: str, replacement: Replacement) -> None:
        """
        Searches the current text (the last version) for occurrences matching the given
        regular expression. Any match data (including group captures) is stored internally.
        """
        return self.analyze(pattern).replace_all(replacement).get_modified_text()

    # ----------------------------------------------------------------------------------
    # Advanced methods

    def analyze(self, pattern: str) -> None:
        """
        Searches the current text (the last version) for occurrences matching the given
        regular expression. Any match data (including group captures) is stored internally.
        """
        import re

        self._matches.clear()
        current_text = self._text_versions[-1]
        for match in re.finditer(pattern, current_text, self.flags):
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
            # In non-line mode, a naive snippet (characters around the match) can
            # include newlines. If we simply print that snippet and then print the
            # highlight line relative to the snippet start, the visual caret
            # markers may appear under a different printed line. To avoid this,
            # find the full line that contains the match and print the context as
            # lines: preceding context lines, the matched line, then the highlight
            # directly under the matched line, then the following context lines.
            snippet_radius = 20
            for idx, m in enumerate(self._matches):
                start, end = m["start"], m["end"]
                # Find the boundaries of the line containing the match
                line_start = current_text.rfind("\n", 0, start) + 1
                line_end = current_text.find("\n", end)
                if line_end == -1:
                    line_end = len(current_text)

                # Context window (characters) around the matched line
                context_start = max(0, line_start - snippet_radius)
                context_end = min(len(current_text), line_end + snippet_radius)
                context_text = current_text[context_start:context_end]

                # Split into lines while preserving newlines so output looks natural
                context_lines = context_text.splitlines(True)

                # Determine which line in context_lines contains the match
                acc = 0
                match_line_idx = 0
                rel_pos_in_context = line_start - context_start
                for i, line in enumerate(context_lines):
                    if acc + len(line) > rel_pos_in_context:
                        match_line_idx = i
                        break
                    acc += len(line)

                print(f"Match {idx} (around line {m['line_number']+1}):")
                # Print each context line. For the match line, print a highlight
                # line immediately after it so the caret markers line up under
                # the matched text.
                for i, line in enumerate(context_lines):
                    # Print the context line as-is (it may or may not contain a newline)
                    print(line, end="")
                    if i == match_line_idx:
                        # If the printed line did not end with a newline, ensure the
                        # caret highlight appears on the next line so it lines up
                        # visually beneath the matched characters.
                        if not line.endswith("\n"):
                            print()
                        # position of match within the printed line
                        pos_in_line = start - line_start
                        highlight = " " * pos_in_line + self.highlight_char * (
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


def print_list(
    items: Optional[Iterable[Any]] = None,
    *,
    style: Literal[
        "wrapped", "columns", "numbered", "bullet", "table", "compact"
    ] = "wrapped",
    max_width: int = 80,
    sep: str = ", ",
    line_prefix: str = "",
    items_per_line=None,
    show_count: Union[bool, Callable[[int], str]] = False,
    title=None,
    print_func=print,
):
    """
    Print a list in a nice, readable format with multiple style options.

    Args:
        items: The list or iterable to print. If None, returns a partial function.
        style: One of "wrapped", "columns", "numbered", "bullet", "table", "compact"
        max_width: Maximum width for wrapped style
        sep: Separator for items
        line_prefix: Prefix for each line
        items_per_line: For columns style, how many items per line
        show_count: Whether to prefix with the count of items
        title: Optional title to display before the list
        print_func: Function to use for printing. Defaults to print.
                   If None, returns the string instead of printing.

    Examples:
        >>> items = ["apple", "banana", "cherry", "date", "elderberry", "fig"]

        # Wrapped style (default)
        >>> print_list(items, max_width=30)
        apple, banana, cherry, date,
        elderberry, fig

        # Columns style
        >>> print_list(items, style="columns", items_per_line=3)
        apple banana     cherry
        date  elderberry fig

        # Numbered style
        >>> print_list(items, style="numbered")
        1. apple
        2. banana
        3. cherry
        4. date
        5. elderberry
        6. fig

        # Bullet style
        >>> print_list(items, style="bullet")
        • apple
        • banana
        • cherry
        • date
        • elderberry
        • fig

        # Return string instead of printing
        >>> result = print_list(items, style="numbered", print_func=None, show_count=True)
        >>> print(result)
        List (6 items):
        1. apple
        2. banana
        3. cherry
        4. date
        5. elderberry
        6. fig

        Partial function functionality: If you don't specify the items (or items=None),
        the function returns a partial function that can be called with the items later.
        That is, the print_list acts as a factory function for different
        printing styles.

        >>> numbered_printer = print_list(style="numbered", show_count=False)
        >>> numbered_printer(items)
        1. apple
        2. banana
        3. cherry
        4. date
        5. elderberry
        6. fig

        >>> compact_printer = print_list(style="compact", max_width=60, show_count=False)
        >>> compact_printer(items)
        apple, banana, cherry, date, elderberry, fig

        >>> bullet_printer = print_list(style="bullet", print_func=None, show_count=False)
        >>> result = bullet_printer(items)
        >>> print(result)
        • apple
        • banana
        • cherry
        • date
        • elderberry
        • fig
    """
    if items is None:
        return partial(
            print_list,
            style=style,
            max_width=max_width,
            sep=sep,
            line_prefix=line_prefix,
            items_per_line=items_per_line,
            show_count=show_count,
            title=title,
            print_func=print_func,
        )
    items = list(items)  # Convert to list if it's an iterable
    if show_count is True:
        show_count = lambda n_items: f"List ({n_items} items):"

    # Handle print_func=None by using StringAppender
    if print_func is None:
        string_appender = StringAppender()
        print_func = string_appender
        return_string = True
    else:
        return_string = False

    # Show title and count
    if title:
        print_func(title)
    elif show_count:
        print_func(show_count(len(items)))

    if not items:
        print_func(f"{line_prefix}(empty list)")
        return str(string_appender) if return_string else None

    if style == "wrapped":
        # Use the existing wrapped_print function with a safe fallback for doctest context
        try:
            from .loggers import wrapped_print  # type: ignore
        except Exception:  # pragma: no cover - fallback when relative import fails
            import textwrap

            def wrapped_print(
                items, sep=", ", max_width=80, line_prefix="", print_func=print
            ):
                text = sep.join(map(str, items))
                return print_func(
                    line_prefix
                    + textwrap.fill(
                        text, width=max_width, subsequent_indent=line_prefix
                    )
                )

        wrapped_print(
            items,
            sep=sep,
            max_width=max_width,
            line_prefix=line_prefix,
            print_func=print_func,
        )

    elif style == "columns":
        if items_per_line is None:
            # Auto-calculate based on max_width and average item length
            avg_length = sum(len(str(item)) for item in items) / len(items)
            items_per_line = max(1, int(max_width / (avg_length + len(sep))))

        for i in range(0, len(items), items_per_line):
            line_items = items[i : i + items_per_line]
            # Calculate column widths across all rows for each column position
            col_widths = []
            for col in range(items_per_line):
                col_items = items[col::items_per_line]
                if col_items:
                    col_widths.append(max(len(str(item)) for item in col_items))
                else:
                    col_widths.append(0)

            # Print the line; pad all but the last column to avoid trailing spaces
            parts = []
            for j, item in enumerate(line_items):
                text = str(item)
                if j < len(line_items) - 1:
                    parts.append(text.ljust(col_widths[j]))
                else:
                    parts.append(text)
            print_func(f"{line_prefix}{' '.join(parts)}")

    elif style == "numbered":
        max_num_width = len(str(len(items)))
        for i, item in enumerate(items, 1):
            print_func(f"{line_prefix}{i:>{max_num_width}}. {item}")

    elif style == "bullet":
        for item in items:
            print_func(f"{line_prefix}• {item}")

    elif style == "table":
        # Simple table format
        if items and hasattr(items[0], "__iter__") and not isinstance(items[0], str):
            # List of lists/tuples - treat as table data
            if not items:
                return str(string_appender) if return_string else None

            # Find column widths
            num_cols = len(items[0])
            col_widths = [0] * num_cols
            for row in items:
                for j, cell in enumerate(row):
                    col_widths[j] = max(col_widths[j], len(str(cell)))

            # Print table
            for row in items:
                formatted_row = []
                for j, cell in enumerate(row):
                    formatted_row.append(str(cell).ljust(col_widths[j]))
                print_func(f"{line_prefix}{' | '.join(formatted_row)}")
        else:
            # Single column table
            max_width = max(len(str(item)) for item in items)
            for item in items:
                print_func(f"{line_prefix}{str(item).ljust(max_width)}")

    elif style == "compact":
        # Most compact form - all on one line if possible
        items_str = sep.join(str(item) for item in items)
        if len(items_str) <= max_width:
            print_func(f"{line_prefix}{items_str}")
        else:
            # Fall back to wrapped style
            try:
                from .loggers import wrapped_print  # type: ignore
            except Exception:  # pragma: no cover - fallback when relative import fails
                import textwrap

                def wrapped_print(
                    items, sep=", ", max_width=80, line_prefix="", print_func=print
                ):
                    text = sep.join(map(str, items))
                    return print_func(
                        line_prefix
                        + textwrap.fill(
                            text, width=max_width, subsequent_indent=line_prefix
                        )
                    )

            wrapped_print(
                items,
                sep=sep,
                max_width=max_width,
                line_prefix=line_prefix,
                print_func=print_func,
            )

    else:
        raise ValueError(
            f"Unknown style: {style}. Use one of: wrapped, columns, numbered, bullet, table, compact"
        )

    return str(string_appender) if return_string else None


def print_list_as_table(
    items, headers=None, *, max_width=80, align="left", print_func=print
):
    """
    Print a list as a nicely formatted table.

    Args:
        items: List of items (strings, numbers, or objects with __str__)
        headers: Optional list of column headers
        max_width: Maximum width of the table
        align: Alignment for columns ("left", "right", "center")
        print_func: Function to use for printing. Defaults to print.
                   If None, returns the string instead of printing.

    Examples:
        >>> data = [["Name", "Age", "City"], ["Alice", 25, "NYC"], ["Bob", 30, "LA"]]
        >>> print_list_as_table(data)
        Name  | Age | City
        -----|---|----
        Alice | 25  | NYC
        Bob   | 30  | LA

        # Return string instead of printing
        >>> result = print_list_as_table(data, print_func=None)
        >>> print(result)
        Name  | Age | City
        -----|---|----
        Alice | 25  | NYC
        Bob   | 30  | LA
    """
    # Handle print_func=None by using StringAppender
    if print_func is None:
        string_appender = StringAppender()
        print_func = string_appender
        return_string = True
    else:
        return_string = False

    if not items:
        print_func("(empty table)")
        return str(string_appender) if return_string else None

    # Convert items to list of lists if needed
    if not hasattr(items[0], "__iter__") or isinstance(items[0], str):
        # Single column
        table_data = [[str(item)] for item in items]
        if headers:
            headers = [headers] if isinstance(headers, str) else headers
        else:
            headers = ["Value"]
    else:
        # Multi-column
        table_data = [[str(cell) for cell in row] for row in items]

    if headers:
        table_data.insert(0, headers)

    # Calculate column widths
    num_cols = len(table_data[0])
    col_widths = [0] * num_cols

    for row in table_data:
        for j, cell in enumerate(row):
            col_widths[j] = max(col_widths[j], len(cell))

    # Adjust column widths to fit max_width
    total_width = sum(col_widths) + (num_cols - 1) * 3  # 3 for " | "
    if total_width > max_width:
        # Reduce column widths proportionally
        excess = total_width - max_width
        for j in range(num_cols):
            reduction = min(excess // num_cols, col_widths[j] // 2)
            col_widths[j] -= reduction
            excess -= reduction

    # Determine if the first row should be treated as header
    header_present = bool(headers) or all(isinstance(c, str) for c in table_data[0])

    # Helper to format a row without padding the last column
    def format_row(row):
        formatted = []
        for j, cell in enumerate(row):
            if j < num_cols - 1:
                formatted.append(cell.ljust(col_widths[j]))
            else:
                formatted.append(cell)
        return " | ".join(formatted)

    for i, row in enumerate(table_data):
        print_func(format_row(row))
        if header_present and i == 0:
            # Print separator line without spaces around the pipes
            print_func("|".join("-" * w for w in col_widths))

    return str(string_appender) if return_string else None


def print_list_summary(
    items, *, max_items=10, show_total=True, title=None, print_func=print
):
    """
    Print a summary of a list, showing first few and last few items if the list is long.

    Args:
        items: The list to summarize
        max_items: Maximum number of items to show (first + last)
        show_total: Whether to show the total count
        title: Optional title
        print_func: Function to use for printing. Defaults to print.
                   If None, returns the string instead of printing.

    Examples:
        >>> long_list = list(range(100))
        >>> print_list_summary(long_list, max_items=6)
        List (100 items):
        [0, 1, 2, ..., 97, 98, 99]

        >>> print_list_summary(long_list, max_items=10)
        List (100 items):
        [0, 1, 2, 3, 4, ..., 95, 96, 97, 98, 99]

        # Return string instead of printing
        >>> result = print_list_summary(long_list, max_items=6, print_func=None)
        >>> print(result)
        List (100 items):
        [0, 1, 2, ..., 97, 98, 99]
    """
    items = list(items)

    # Handle print_func=None by using StringAppender
    if print_func is None:
        string_appender = StringAppender()
        print_func = string_appender
        return_string = True
    else:
        return_string = False

    if title:
        print_func(title)
    elif show_total:
        print_func(f"List ({len(items)} items):")

    if not items:
        print_func("(empty list)")
        return str(string_appender) if return_string else None

    if len(items) <= max_items:
        print_func(items)
    else:
        # Show first and last items with ellipsis
        first_count = max_items // 2
        last_count = max_items - first_count

        first_items = items[:first_count]
        last_items = items[-last_count:]

        print_func(
            f"[{', '.join(map(str, first_items))}, ..., {', '.join(map(str, last_items))}]"
        )

    return str(string_appender) if return_string else None


# Convenience functions are now available as attributes of print_list
# using the partial functionality:
# - print_list.compact
# - print_list.wrapped
# - print_list.columns
# - print_list.numbered
# - print_list.bullets


print_list.as_table = print_list_as_table
print_list.summary = print_list_summary
print_list.compact = print_list(style="compact", show_count=False)
print_list.wrapped = print_list(style="wrapped", show_count=False)
print_list.columns = print_list(style="columns", show_count=False)
print_list.numbered = print_list(style="numbered", show_count=False)
print_list.bullets = print_list(style="bullet", show_count=False)
