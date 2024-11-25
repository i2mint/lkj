"""Tools for working with functions."""

from functools import partial

mk_factory = partial(partial, partial)
mk_factory.__doc__ = """
Create a factory for functions by partially applying the first argument.

This higher-order function allows you to fix the first argument of a given function, creating a new
function that requires fewer arguments. It's particularly useful for creating customized functions
on the fly without using lambdas.

Example:

>>> from operator import mul
>>> double = mk_factory(mul)(2)
>>> double(5)
10
"""

# --------------------------------------------------------------------------------------
# operator: Fixing an operand
#
# You can use our trick to fix the (first) operand of an operation. This is useful,
# when, for example, you want to avoid using a `lambda` function in some situation
# (say, because [lambda functions are not pickle-serializable](https://realpython.com/python-pickle-module/)).

import operator

greater_than = mk_factory(operator.lt)
greater_than.__doc__ = """
Create a factory for a function that returns True if the argument is greater than the fixed value.

So, for instance, instead of using a lambda x: 10 < x you can do:

>>> greater_than_10 = greater_than(10)
>>> greater_than_10(11)
True
>>> greater_than_10(9)
False

This is even more useful when you need to define a bunch of greater_than functions, or do so dynamically!
"""

# Other examples:
less_than = mk_factory(operator.gt)
less_than.__doc__ = """
Create a factory for a function that returns True if the argument is less than the fixed value.

Example:

>>> less_than_10 = less_than(10)
>>> less_than_10(9)
True
>>> less_than_10(11)
False
"""

greater_or_equal_to = mk_factory(operator.le)
greater_or_equal_to.__doc__ = """
Create a factory for a function that returns True if the argument is greater than or equal to the fixed value.

Example:

>>> ge_10 = greater_or_equal_to(10)
>>> ge_10(10)
True
>>> ge_10(9)
False
"""

less_or_equal_to = mk_factory(operator.ge)
less_or_equal_to.__doc__ = """
Create a factory for a function that returns True if the argument is less than or equal to the fixed value.

Example:

>>> le_10 = less_or_equal_to(10)
>>> le_10(10)
True
>>> le_10(11)
False
"""

# --------------------------------------------------------------------------------------
# os.path.join: A Path Generator for Files
#
# Imagine working with a large project where you frequently need to generate file paths.
# With mk_factory, creating a path generator becomes effortless.

import os

mk_abs_path_maker = mk_factory(os.path.join)
mk_abs_path_maker.__doc__ = """
Create a factory for functions that join paths with a fixed root.

Example:

>>> abs_path = mk_abs_path_maker('/my/root')
>>> abs_path('a', 'b')
'/my/root/a/b'

Now abs_path behaves like os.path.join but with the root path '/my/root' fixed.
"""

# --------------------------------------------------------------------------------------
# map: Transforming Functions for Iterables: The "Iterizer"
#
# The "iterizer" pattern allows us to take any function and apply it across each element of an iterable.

iterizer = mk_factory(map)
iterizer.__doc__ = """
Create a factory that returns a function applying a given function to each element of an iterable.

Example:

>>> times_two = iterizer(lambda x: x * 2)
>>> list(times_two([1, 2, 3]))
[2, 4, 6]

This is useful when processing collections of data where each item must undergo the same transformation.
"""

# --------------------------------------------------------------------------------------
# filter: Filtering Collections: The "Filterizer"
#
# Create a factory to transform any function into a filter for iterables.

filterizer = mk_factory(filter)
filterizer.__doc__ = """
Create a factory that returns a function filtering elements of an iterable based on a predicate function.

Example:

>>> only_evens = filterizer(lambda x: x % 2 == 0)
>>> list(only_evens(range(10)))
[0, 2, 4, 6, 8]

Such "filterized" functions are powerful for handling datasets where specific criteria need to be applied.
"""

# --------------------------------------------------------------------------------------
# zip: Custom Zippers for Pairing Data
#
# With zipper, we can create functions that zip multiple iterables with predefined keys or labels.

zipper = mk_factory(zip)
zipper.__doc__ = """
Create a factory that returns a function zipping iterables with a fixed first iterable.

Example:

>>> my_zipper = zipper(['the', 'first', 'three'])
>>> dict(my_zipper([1, 2]))
{'the': 1, 'first': 2}
>>> dict(my_zipper([10, 20, 30]))
{'the': 10, 'first': 20, 'three': 30}

This approach is particularly useful for converting data into dictionaries with meaningful keys for easier access and readability.
"""

# --------------------------------------------------------------------------------------
# zip: Zipping with an Infinite Iterator for Unique Key Generation
#
# Use zipper with an infinite iterator to provide a continuous stream of unique keys to pair with values dynamically.

from itertools import count


def zip_with_filenames(start_idx=1):
    """
    Create a function that zips an iterable with file names like 'file_001', 'file_002', etc.

    Example:

    >>> zip_files = zip_with_filenames()
    >>> dict(zip_files([1, 2]))
    {'file_001': 1, 'file_002': 2}
    >>> dict(zip_files(['never', 'say', 'never']))
    {'file_004': 'never', 'file_005': 'say', 'file_006': 'never'}

    Using count ensures that each label is unique and ordered sequentially.
    """
    filenames = map("file_{:03.0f}".format, count(start_idx))
    return zipper(filenames)


# --------------------------------------------------------------------------------------
# regex: Regex Matchers and Extractors
#
# For tasks involving regular expressions, mk_factory can simplify creating matchers and extractors.

import re

matcher = mk_factory(re.match)
matcher.__doc__ = """
Create a factory that returns a function to match a pattern at the beginning of a string.

Example:

>>> is_email = matcher(r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$')
>>> bool(is_email('example@example.com'))
True
>>> is_email('not an email') is None
True

With is_email, you have a quick function for checking email format.
"""

extractor = mk_factory(re.findall)
extractor.__doc__ = """
Create a factory that returns a function to find all non-overlapping matches of a pattern in a string.

Example:

>>> extract_numbers = extractor(r'[\\d\\.]+')
>>> extract_numbers('7 times 6 is 42.0')
['7', '6', '42.0']

These functions streamline text processing workflows, making pattern matching and extraction highly reusable and easy to set up.
"""

# --------------------------------------------------------------------------------------
# reduce: Reduction Functions for Aggregation
#
# Reduction functions allow aggregation of elements, useful for calculating products, sums, or even concatenating strings.

from functools import reduce
from operator import mul, add

reducer = mk_factory(reduce)
reducer.__doc__ = """
Create a factory that returns a function to reduce an iterable using a given binary function.

Example:

>>> product = reducer(mul)
>>> product([2, 3, 4])
24

>>> concatinator = reducer(add)
>>> concatinator(['a', 'b', 'c'])
'abc'

This approach lets you create highly readable, purpose-specific aggregation functions with minimal code.
"""

# --------------------------------------------------------------------------------------
# Creating a Function Composer for Pipelines
#
# Build a function composer that lets you apply a sequence of transformations or operations on data.

composer = reducer(lambda f, g: lambda *args, **kwargs: f(g(*args, **kwargs)))
composer.__doc__ = """
Create a function composer that composes a sequence of functions into a single function.

Example:

>>> exclaimed_title = composer([lambda x: x + '!', str.title])
>>> exclaimed_title('hello world')
'Hello World!'

This is especially useful in data pipelines, where data needs to pass through a series of transformations.
"""

# --------------------------------------------------------------------------------------
# Additional Examples


# Example using map with os.path.join to create full file paths
def full_path_maker(base_directory):
    """
    Create a function that generates full file paths given filenames.

    Example:

    >>> full_path = full_path_maker('/base/directory')
    >>> list(full_path(['file1', 'file2']))
    ['/base/directory/file1', '/base/directory/file2']
    """
    abs_path = mk_abs_path_maker(base_directory)
    return iterizer(abs_path)


# Example of using greater_than in a filter
def filter_greater_than(threshold, data):
    """
    Filter elements in data that are greater than the threshold.

    Example:

    >>> filter_greater_than_5 = filter_greater_than(5, range(10))
    >>> list(filter_greater_than_5)
    [6, 7, 8, 9]
    """
    gt = greater_than(threshold)
    return filter(gt, data)
