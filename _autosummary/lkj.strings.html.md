# lkj.strings

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
- print_list.compact, print_list.wrapped, print_list.columns, print_list.numbered, print_list.bullets: Convenience methods using print_list’s partial functionality for common display styles.

These utilities are designed to make it easier to display, format, and manipulate strings and collections of strings in a readable and flexible way.

### Functions

| [`camel_to_snake`](#lkj.strings.camel_to_snake)(camel_string)                      | Convert a CamelCase string to snake_case.                                                           |
|----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| `fields_of_string_format`(template)                                                                |                                                                                                     |
| [`fields_of_string_formats`](#lkj.strings.fields_of_string_formats)(templates, \*[, ...])    | Extract all unique field names from the templates in \_github_url_templates using string.Formatter. |
| `identity`(x)                                                                                      |                                                                                                     |
| [`indent_lines`](#lkj.strings.indent_lines)(string, indent, \*[, line_sep])      | Indent each line of a string.                                                                       |
| [`most_common_indent`](#lkj.strings.most_common_indent)(string[, ignore_first_line])   | Find the most common indentation in a string.                                                       |
| [`print_list`](#lkj.strings.print_list)([items, style, max_width, sep, ...])   | Print a list in a nice, readable format with multiple style options.                                |
| [`print_list_as_table`](#lkj.strings.print_list_as_table)(items[, headers, ...])        | Print a list as a nicely formatted table.                                                           |
| [`print_list_summary`](#lkj.strings.print_list_summary)(items, \*[, max_items, ...])   | Print a summary of a list, showing first few and last few items if the list is long.                |
| [`regex_based_substitution`](#lkj.strings.regex_based_substitution)(replacements[, ...])     | Construct a substitution function based on an iterable of replacement pairs.                        |
| [`snake_to_camel`](#lkj.strings.snake_to_camel)(snake_string)                      | Convert a snake_case string to CamelCase.                                                           |
| [`truncate_lines`](#lkj.strings.truncate_lines)(s[, top_limit, bottom_limit, ...]) | Truncates a string by limiting the number of lines from the top and bottom.                         |
| [`truncate_string`](#lkj.strings.truncate_string)(s, \*[, left_limit, ...])         | Truncate a string to a maximum length, inserting a marker in the middle.                            |
| [`truncate_string_with_marker`](#lkj.strings.truncate_string_with_marker)(s, \*[, ...])         | Truncate a string to a maximum length, inserting a marker in the middle.                            |
| [`unique_affixes`](#lkj.strings.unique_affixes)(items[, suffix, egress, ingress])  | Returns a list of unique prefixes (or suffixes) for the given iterable of sequences.                |

### Classes

| [`FindReplaceTool`](#lkj.strings.FindReplaceTool)(text, \*[, line_mode, flags, ...])   | A general-purpose find-and-replace tool that can treat the input text as a continuous sequence of characters, even if operations such as viewing context are performed line by line.   |
|-------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`StringAppender`](#lkj.strings.StringAppender)([separator])                          | Helper class to collect strings instead of printing them directly.                                                                                                                     |
| `TrieNode`()                                                                                          |                                                                                                                                                                                        |

### *class* lkj.strings.FindReplaceTool(text, , line_mode=False, flags=0, show_line_numbers=True, context_size=2, highlight_char='^')

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

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

## 1: Basic usage

```pycon
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
```

## 2: Using line_mode=True with a static replacement.

```pycon
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
```

## 3: Using line_mode=False with a callback replacement.

```pycon
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
```

## 4: Reverting changes.

```pycon
>>> text3 = "one two three"
>>> tool3 = FindReplaceTool(text3)
>>> import re
>>> # Analyze to match the first word "one" (at the start of the text).
>>> tool3.analyze(r'^one').replace_one(0, "ONE").get_modified_text()
'ONE two three'
>>> # Revert the edit.
>>> tool3.revert()
'one two three'
```

#### analyze(pattern)

Searches the current text (the last version) for occurrences matching the given
regular expression. Any match data (including group captures) is stored internally.

* **Return type:**
  [`None`](https://docs.python.org/3/library/constants.html#None)

#### find_and_print_matches(pattern)

Searches the current text (the last version) for occurrences matching the given
regular expression. Any match data (including group captures) is stored internally.

* **Return type:**
  [`None`](https://docs.python.org/3/library/constants.html#None)

#### find_and_replace(pattern, replacement)

Searches the current text (the last version) for occurrences matching the given
regular expression. Any match data (including group captures) is stored internally.

* **Return type:**
  [`None`](https://docs.python.org/3/library/constants.html#None)

#### get_modified_text()

Returns the current (latest) text version.

* **Return type:**
  [`str`](https://docs.python.org/3/library/stdtypes.html#str)

#### get_original_text()

Returns the original text (first version).

* **Return type:**
  [`str`](https://docs.python.org/3/library/stdtypes.html#str)

#### replace_all(replacement)

Replaces all stored matches in the current text version. The ‘replacement’ argument may
be a static string or a callable (see replace_one for details). Replacements are performed
from the last match to the first, so that earlier offsets are not affected.

* **Return type:**
  [`None`](https://docs.python.org/3/library/constants.html#None)

#### replace_one(match_index, replacement)

Replaces a single match, identified by match_index, with a new string.
The ‘replacement’ argument may be either a static string or a callable.
When it is a callable, it is called with a dictionary containing the match data
(including any captured groups) and should return the replacement string.
The replacement is performed on the current text version, and the new text is
appended as a new version in the history.

* **Return type:**
  [`None`](https://docs.python.org/3/library/constants.html#None)

#### revert(steps=1)

Reverts the current text version by removing the last ‘steps’ versions
from the history. The original text (version 0) is never removed.
Returns the new current text.

```pycon
>>> text = "one two three"
>>> tool = FindReplaceTool(text)
>>> import re
>>> tool.analyze(r'^one').replace_one(0, "ONE").get_modified_text()
'ONE two three'
>>> tool.revert()
'one two three'
```

#### view_matches()

Displays all stored matches along with surrounding context. When line_mode
is enabled, the context is provided in full lines with (optionally) line numbers,
and a line is added below the matched line to indicate the matched portion.
In non-line mode, a snippet of characters around the match is shown.

* **Return type:**
  [`None`](https://docs.python.org/3/library/constants.html#None)

### *class* lkj.strings.StringAppender(separator='\\n')

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Helper class to collect strings instead of printing them directly.

#### get_string()

Alternative way to get the string.

### lkj.strings.camel_to_snake(camel_string)

Convert a CamelCase string to snake_case. Useful for converting class
names to variable names.

* **Parameters:**
  **camel_string** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The CamelCase string to convert.
* **Returns:**
  The converted snake_case string.
* **Return type:**
  [*str*](https://docs.python.org/3/library/stdtypes.html#str)

### Examples

```pycon
>>> camel_to_snake('BasicParseTest')
'basic_parse_test'
>>> camel_to_snake('HTMLParser')
'html_parser'
>>> camel_to_snake('CamelCaseExample')
'camel_case_example'
```

Note that acronyms are handled correctly:

```pycon
>>> camel_to_snake('XMLHttpRequestTest')
'xml_http_request_test'
```

### lkj.strings.fields_of_string_formats(templates, \*, aggregator=<class 'set'>)

Extract all unique field names from the templates in \_github_url_templates using string.Formatter.

* **Parameters:**
  **templates** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) – A list of dictionaries containing ‘template’ keys.
* **Returns:**
  A sorted list of unique field names found in the templates.
* **Return type:**
  [*list*](https://docs.python.org/3/library/stdtypes.html#list)

### Example

```pycon
>>> templates = ['{this}/and/{that}', 'and/{that}/is/an/{other}']
>>> sorted(fields_of_string_formats(templates))
['other', 'that', 'this']
```

### lkj.strings.indent_lines(string, indent, , line_sep='\\\\n')

Indent each line of a string.

* **Parameters:**
  * **string** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) – The string to indent.
  * **indent** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) – The string to use for indentation.
* **Return type:**
  [`str`](https://docs.python.org/3/library/stdtypes.html#str)
* **Returns:**
  The indented string.

```pycon
>>> print(indent_lines('This is a test.\nAnother line.', ' ' * 8))
        This is a test.
        Another line.
```

### lkj.strings.most_common_indent(string, ignore_first_line=False)

Find the most common indentation in a string.

* **Parameters:**
  * **string** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) – The string to analyze.
  * **ignore_first_line** – Whether to ignore the first line when determining the
    indentation. Default is False. One case where you want True is when using python
    triple quotes (as in docstrings, for example), since the first line often has
    no indentation (from the point of view of the string, in this case.
* **Return type:**
  [`str`](https://docs.python.org/3/library/stdtypes.html#str)
* **Returns:**
  The most common indentation string.

### Examples

```pycon
>>> most_common_indent('    This is a test.\n    Another line.')
'    '
```

### lkj.strings.print_list(items=None, \*, style='wrapped', max_width=80, sep=', ', line_prefix='', items_per_line=None, show_count=False, title=None, print_func=<built-in function print>)

Print a list in a nice, readable format with multiple style options.

* **Parameters:**
  * **items** ([`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any)] | [`None`](https://docs.python.org/3/library/constants.html#None)) – The list or iterable to print. If None, returns a partial function.
  * **style** ([`Literal`](https://docs.python.org/3/library/typing.html#typing.Literal)[`'wrapped'`, `'columns'`, `'numbered'`, `'bullet'`, `'table'`, `'compact'`]) – One of “wrapped”, “columns”, “numbered”, “bullet”, “table”, “compact”
  * **max_width** ([`int`](https://docs.python.org/3/library/functions.html#int)) – Maximum width for wrapped style
  * **sep** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) – Separator for items
  * **line_prefix** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) – Prefix for each line
  * **items_per_line** – For columns style, how many items per line
  * **show_count** ([`bool`](https://docs.python.org/3/library/functions.html#bool) | [`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`int`](https://docs.python.org/3/library/functions.html#int)], [`str`](https://docs.python.org/3/library/stdtypes.html#str)]) – Whether to prefix with the count of items
  * **title** – Optional title to display before the list
  * **print_func** – Function to use for printing. Defaults to print.
    If None, returns the string instead of printing.

### Examples

```pycon
>>> items = ["apple", "banana", "cherry", "date", "elderberry", "fig"]
```

### Wrapped style (default)

```pycon
>>> print_list(items, max_width=30)
apple, banana, cherry, date,
elderberry, fig
```

### Columns style

```pycon
>>> print_list(items, style="columns", items_per_line=3)
apple banana     cherry
date  elderberry fig
```

### Numbered style

```pycon
>>> print_list(items, style="numbered")
1. apple
2. banana
3. cherry
4. date
5. elderberry
6. fig
```

### Bullet style

```pycon
>>> print_list(items, style="bullet")
• apple
• banana
• cherry
• date
• elderberry
• fig
```

### Return string instead of printing

```pycon
>>> result = print_list(items, style="numbered", print_func=None, show_count=True)
>>> print(result)
List (6 items):
1. apple
2. banana
3. cherry
4. date
5. elderberry
6. fig
```

Partial function functionality: If you don’t specify the items (or items=None),
the function returns a partial function that can be called with the items later.
That is, the print_list acts as a factory function for different
printing styles.

```pycon
>>> numbered_printer = print_list(style="numbered", show_count=False)
>>> numbered_printer(items)
1. apple
2. banana
3. cherry
4. date
5. elderberry
6. fig
```

```pycon
>>> compact_printer = print_list(style="compact", max_width=60, show_count=False)
>>> compact_printer(items)
apple, banana, cherry, date, elderberry, fig
```

```pycon
>>> bullet_printer = print_list(style="bullet", print_func=None, show_count=False)
>>> result = bullet_printer(items)
>>> print(result)
• apple
• banana
• cherry
• date
• elderberry
• fig
```

### lkj.strings.print_list_as_table(items, headers=None, \*, max_width=80, align='left', print_func=<built-in function print>)

Print a list as a nicely formatted table.

* **Parameters:**
  * **items** – List of items (strings, numbers, or objects with \_\_str_\_)
  * **headers** – Optional list of column headers
  * **max_width** – Maximum width of the table
  * **align** – Alignment for columns (“left”, “right”, “center”)
  * **print_func** – Function to use for printing. Defaults to print.
    If None, returns the string instead of printing.

### Examples

```pycon
>>> data = [["Name", "Age", "City"], ["Alice", 25, "NYC"], ["Bob", 30, "LA"]]
>>> print_list_as_table(data)
Name  | Age | City
-----|---|----
Alice | 25  | NYC
Bob   | 30  | LA
```

### Return string instead of printing

```pycon
>>> result = print_list_as_table(data, print_func=None)
>>> print(result)
Name  | Age | City
-----|---|----
Alice | 25  | NYC
Bob   | 30  | LA
```

### lkj.strings.print_list_summary(items, \*, max_items=10, show_total=True, title=None, print_func=<built-in function print>)

Print a summary of a list, showing first few and last few items if the list is long.

* **Parameters:**
  * **items** – The list to summarize
  * **max_items** – Maximum number of items to show (first + last)
  * **show_total** – Whether to show the total count
  * **title** – Optional title
  * **print_func** – Function to use for printing. Defaults to print.
    If None, returns the string instead of printing.

### Examples

```pycon
>>> long_list = list(range(100))
>>> print_list_summary(long_list, max_items=6)
List (100 items):
[0, 1, 2, ..., 97, 98, 99]
```

```pycon
>>> print_list_summary(long_list, max_items=10)
List (100 items):
[0, 1, 2, 3, 4, ..., 95, 96, 97, 98, 99]
```

### Return string instead of printing

```pycon
>>> result = print_list_summary(long_list, max_items=6, print_func=None)
>>> print(result)
List (100 items):
[0, 1, 2, ..., 97, 98, 99]
```

### lkj.strings.regex_based_substitution(replacements, regex=None, s=None)

Construct a substitution function based on an iterable of replacement pairs.

* **Parameters:**
  **replacements** ([`dict`](https://docs.python.org/3/library/stdtypes.html#dict)) – An iterable of (replace_this, with_that) pairs.
* **Returns:**
  A function that, when called with a string, will perform all substitutions.
* **Return type:**
  *Callable*[[[*str*](https://docs.python.org/3/library/stdtypes.html#str)], [*str*](https://docs.python.org/3/library/stdtypes.html#str)]

The function is meant to be used with `replacements` as its single input,
returning a `substitute` function that will carry out the substitutions
on an input string.

```pycon
>>> replacements = {'apple': 'orange', 'banana': 'grape'}
>>> substitute = regex_based_substitution(replacements)
>>> substitute("I like apple and bananas.")
'I like orange and grapes.'
```

You have access to the `replacements` and `regex` attributes of the
`substitute` function. See how the replacements dict has been ordered by
descending length of keys. This is to ensure that longer keys are replaced
before shorter keys, avoiding partial replacements.

```pycon
>>> substitute.replacements
{'banana': 'grape', 'apple': 'orange'}
```

### lkj.strings.snake_to_camel(snake_string)

Convert a snake_case string to CamelCase. Useful for converting variable
names to class names.

* **Parameters:**
  **snake_string** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The snake_case string to convert.
* **Returns:**
  The converted CamelCase string.
* **Return type:**
  [*str*](https://docs.python.org/3/library/stdtypes.html#str)

### Examples

```pycon
>>> snake_to_camel('complex_tokenizer')
'ComplexTokenizer'
>>> snake_to_camel('simple_example_test')
'SimpleExampleTest'
```

Note that acronyms are capitalized correctly:

```pycon
>>> snake_to_camel('xml_http_request_test')
'XmlHttpRequestTest'
```

### lkj.strings.truncate_lines(s, top_limit=None, bottom_limit=None, middle_marker='...')

Truncates a string by limiting the number of lines from the top and bottom.
If the total number of lines is greater than top_limit + bottom_limit,
it keeps the first `top_limit` lines, keeps the last `bottom_limit` lines,
and replaces the omitted middle portion with a single line containing
`middle_marker`.

If top_limit or bottom_limit is None, it is treated as 0.

* **Return type:**
  [`str`](https://docs.python.org/3/library/stdtypes.html#str)

### Example

```pycon
>>> text = '''Line1
... Line2
... Line3
... Line4
... Line5
... Line6'''
```

```pycon
>>> print(truncate_lines(text, top_limit=2, bottom_limit=2))
Line1
Line2
...
Line5
Line6
```

### lkj.strings.truncate_string(s, , left_limit=15, right_limit=15, middle_marker='...')

Truncate a string to a maximum length, inserting a marker in the middle.

If the string is longer than the sum of the left_limit and right_limit,
the string is truncated and the middle_marker is inserted in the middle.

If the string is shorter than the sum of the left_limit and right_limit,
the string is returned as is.

```pycon
>>> truncate_string('1234567890')
'1234567890'
```

But if the string is longer than the sum of the limits, it is truncated:

```pycon
>>> truncate_string('1234567890', left_limit=3, right_limit=3)
'123...890'
>>> truncate_string('1234567890', left_limit=3, right_limit=0)
'123...'
>>> truncate_string('1234567890', left_limit=0, right_limit=3)
'...890'
```

If you’re using a specific parametrization of the function often, you can
create a partial function with the desired parameters:

```pycon
>>> from functools import partial
>>> truncate_string = partial(truncate_string, left_limit=2, right_limit=2, middle_marker='---')
>>> truncate_string('1234567890')
'12---90'
>>> truncate_string('supercalifragilisticexpialidocious')
'su---us'
```

### lkj.strings.truncate_string_with_marker(s, , left_limit=15, right_limit=15, middle_marker='...')

Truncate a string to a maximum length, inserting a marker in the middle.

If the string is longer than the sum of the left_limit and right_limit,
the string is truncated and the middle_marker is inserted in the middle.

If the string is shorter than the sum of the left_limit and right_limit,
the string is returned as is.

```pycon
>>> truncate_string('1234567890')
'1234567890'
```

But if the string is longer than the sum of the limits, it is truncated:

```pycon
>>> truncate_string('1234567890', left_limit=3, right_limit=3)
'123...890'
>>> truncate_string('1234567890', left_limit=3, right_limit=0)
'123...'
>>> truncate_string('1234567890', left_limit=0, right_limit=3)
'...890'
```

If you’re using a specific parametrization of the function often, you can
create a partial function with the desired parameters:

```pycon
>>> from functools import partial
>>> truncate_string = partial(truncate_string, left_limit=2, right_limit=2, middle_marker='---')
>>> truncate_string('1234567890')
'12---90'
>>> truncate_string('supercalifragilisticexpialidocious')
'su---us'
```

### lkj.strings.unique_affixes(items, suffix=False, \*, egress=None, ingress=<function identity>)

Returns a list of unique prefixes (or suffixes) for the given iterable of sequences.
Raises a ValueError if duplicates are found.

* **Return type:**
  [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[[`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)]

### Parameters

- items: Iterable of sequences (e.g., list of strings).
- suffix: If True, finds unique suffixes instead of prefixes.
- ingress: Callable to preprocess each item. Default is identity function.
- egress: Callable to postprocess each affix. Default is appropriate function based on item type.
  Usually, ingress and egress are inverses of each other.

```pycon
>>> unique_affixes(['apple', 'ape', 'apricot', 'banana', 'band', 'bandana'])
['app', 'ape', 'apr', 'bana', 'band', 'banda']
```

```pycon
>>> unique_affixes(['test', 'testing', 'tester'])
['test', 'testi', 'teste']
```

```pycon
>>> unique_affixes(['test', 'test'])
Traceback (most recent call last):
...
ValueError: Duplicate item detected: test
```

```pycon
>>> unique_affixes(['abc', 'abcd', 'abcde'])
['abc', 'abcd', 'abcde']
```

```pycon
>>> unique_affixes(['a', 'b', 'c'])
['a', 'b', 'c']
```

```pycon
>>> unique_affixes(['x', 'xy', 'xyz'])
['x', 'xy', 'xyz']
```

```pycon
>>> unique_affixes(['can', 'candy', 'candle'])
['can', 'candy', 'candl']
```

```pycon
>>> unique_affixes(['flow', 'flower', 'flight'])
['flow', 'flowe', 'fli']
```

```pycon
>>> unique_affixes(['ation', 'termination', 'examination'], suffix=True)
['ation', 'rmination', 'amination']
```

```pycon
>>> import functools
>>> ingress = functools.partial(str.split, sep='.')
>>> egress = '.'.join
>>> items = ['here.and.there', 'here.or.there', 'here']
>>> unique_affixes(items, ingress=ingress, egress=egress)
['here.and', 'here.or', 'here']
```
