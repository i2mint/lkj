"""
Lightweight Kit Jumpstart
"""

from lkj.iterables import (
    compare_sets,  # Compare two iterables and return common, left-only, and right-only elements
    index_of,  # Get the index of an element in an iterable
    get_by_value,  # Get a dictionary from a list of dictionaries by a field value
)
from lkj.funcs import mk_factory
from lkj.dicts import (
    truncate_dict_values,  # Truncate list and string values in a dictionary
    inclusive_subdict,  # new dictionary with only the keys in `include`
    exclusive_subdict,  # new dictionary with only the keys not in `exclude`.
    merge_dicts,  # Merge multiple dictionaries recursively
    compare_field_values,  # Compare two dictionaries' values
)
from lkj.filesys import get_app_data_dir, get_watermarked_dir, enable_sourcing_from_file
from lkj.strings import (
    print_list,  # Print a list in a nice format (or get a string to process yourself)
    FindReplaceTool,  # Tool for finding and replacing substrings in a string
    indent_lines,  # Indent all lines of a string
    most_common_indent,  # Get the most common indent of a multiline string
    regex_based_substitution,
    truncate_string,  # Truncate a string to a maximum length, inserting a marker in the middle.
    truncate_lines,  # Truncate a multiline string to a maximum number of lines
    unique_affixes,  # Get unique prefixes or suffixes of a list of strings
    camel_to_snake,  # Convert CamelCase to snake_case
    snake_to_camel,  # Convert snake_case to CamelCase
    fields_of_string_format,  # Extract field names from a string format
    fields_of_string_formats,  # Extract field names from an iterable of string formats,
    truncate_string_with_marker,  # Deprecated: Backcompatibility alias
)
from lkj.loggers import (
    print_with_timestamp,  # Prints with a timestamp and optional refresh.
    print_progress,  # an alias often used for print_with_timestamp
    log_calls,  # Decorator that adds logging before and after the function's call.
    clog,  # Conditional logger
    ErrorInfo,
    return_error_info_on_error,  # Decorator that returns traceback and local variables on error.
    wrapped_print,  # Prints a string or list ensuring the total line width does not exceed `max_width`.
    CallOnError,  # Context manager that calls a function on error (subclass of suppress)
)
from lkj.importing import (
    parent_dir_of_module,  # Get the parent directory of a module
    import_from_path,  # Import a module from a specified path
    import_object,  # Import an object from a module by its name
    register_namespace_forwarding,  # Register a namespace forwarding for a module
)
from lkj.chunking import chunk_iterable, chunker
from lkj.misc import identity, value_in_interval

ddir = lambda obj: list(filter(lambda x: not x.startswith("_"), dir(obj)))


def user_machine_id():
    """Get an ID for the current computer/user that calls this function."""
    return __import__("platform").node()


def add_attr(attr_name: str, attr_val: str = None, obj=None):
    """Add an attribute to an object.

    If no object is provided, return a partial function that takes an object as its
    argument.
    If no attribute value is provided, return a partial function that takes an
    attribute value as its argument.
    If no object or attribute value is provided, return a partial function that takes
    both an object and an attribute value as its arguments.
    If all arguments are provided, add the attribute to the object and return the
    object.

    :param attr_name: The name of the attribute to add.
    :param attr_val: The value of the attribute to add.
    :param obj: The object to which to add the attribute.
    :return: The object with the attribute added, or a partial function that takes an
    object and/or an attribute value as its argument(s).

    >>> def generic_func(*args, **kwargs):
    ...     return args, kwargs
    ...
    >>> generic_func.__name__
    'generic_func'
    >>>
    >>> _ = add_attr('__name__', 'my_func', generic_func);
    >>> generic_func.__name__
    'my_func'
    >>>
    >>>
    >>> add_name = add_attr('__name__')
    >>> add_doc = add_attr('__doc__')
    >>>
    >>> @add_name('my_func')
    ... @add_doc('This is my function.')
    ... def f(*args, **kwargs):
    ...     return args, kwargs
    ...
    >>> f.__name__
    'my_func'
    >>> f.__doc__
    'This is my function.'

    """
    if obj is None:
        from functools import partial

        if attr_val is None:
            return partial(add_attr, attr_name)
        return partial(add_attr, attr_name, attr_val)
    if attr_val is not None:
        setattr(obj, attr_name, attr_val)
    return obj


def add_as_attribute_of(obj, name=None):
    """Decorator that adds a function as an attribute of a container object ``obj``.

    If no ``name`` is given, the ``__name__`` of the function will be used, with a
    leading underscore removed. This is useful for adding helper functions to main
    "container" functions without polluting the namespace of the module, at least
    from the point of view of imports and tab completion.

    >>> def foo():
    ...    pass
    >>>
    >>> @add_as_attribute_of(foo)
    ... def helper():
    ...    pass
    >>> hasattr(foo, 'helper')
    True
    >>> callable(foo.helper)
    True

    In reality, any object that has a ``__name__`` can be added to the attribute of
    ``obj``, but the intention is to add helper functions to main "container" functions.

    Note that if the name of the function starts with an underscore, it will be removed
    before adding it as an attribute of ``obj``.

    >>> @add_as_attribute_of(foo)
    ... def _helper():
    ...    pass
    >>> hasattr(foo, 'helper')
    True

    This is useful for adding helper functions to main "container" functions without
    polluting the namespace of the module, at least from the point of view of imports
    and tab completion. But if you really want to add a function with a leading
    underscore, you can do so by specifying the name explicitly:

    >>> @add_as_attribute_of(foo, name='_helper')
    ... def _helper():
    ...    pass
    >>> hasattr(foo, '_helper')
    True

    Of course, you can give any name you want to the attribute:

    >>> @add_as_attribute_of(foo, name='bar')
    ... def _helper():
    ...    pass
    >>> hasattr(foo, 'bar')
    True

    :param obj: The object to which the function will be added as an attribute
    :param name: The name of the attribute to add the function to. If not given, the

    """

    def _decorator(f):
        attrname = name or f.__name__
        if not name and attrname.startswith("_"):
            attrname = attrname[1:]  # remove leading underscore
        setattr(obj, attrname, f)
        return f

    return _decorator


def get_caller_package_name(default=None):
    """Return package name of caller

    See: https://github.com/i2mint/i2mint/issues/1#issuecomment-1479416085
    """
    import inspect

    try:
        stack = inspect.stack()
        caller_frame = stack[1][0]
        return inspect.getmodule(caller_frame).__name__.split(".")[0]
    except Exception as error:
        return default
