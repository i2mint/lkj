"""
Lightweight Kit Jumpstart
"""

from lkj.dicts import truncate_dict_values
from lkj.filesys import get_app_data_dir, get_watermarked_dir
from lkj.strings import regex_based_substitution, truncate_string_with_marker
from lkj.loggers import (
    print_with_timestamp,
    print_progress,
    log_calls,
    clog,
    ErrorInfo,
    return_error_info_on_error,
    wrapped_print,
)
from lkj.importing import import_object, register_namespace_forwarding
from lkj.misc import identity, value_in_interval

ddir = lambda obj: list(filter(lambda x: not x.startswith('_'), dir(obj)))


def chunker(a, chk_size, *, include_tail=True):
    """Chunks an iterable into non-overlapping chunks of size chk_size.

    >>> list(chunker(range(8), 3))
    [(0, 1, 2), (3, 4, 5), (6, 7)]
    >>> list(chunker(range(8), 3, include_tail=False))
    [(0, 1, 2), (3, 4, 5)]
    """
    from itertools import zip_longest

    it = iter(a)
    if include_tail:
        sentinel = object()
        for chunk in zip_longest(*([it] * chk_size), fillvalue=sentinel):
            yield tuple(item for item in chunk if item is not sentinel)
    else:
        yield from zip(*([it] * chk_size))


def user_machine_id():
    """Get an ID for the current computer/user that calls this function."""
    return __import__('platform').node()


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
        if not name and attrname.startswith('_'):
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
        return inspect.getmodule(caller_frame).__name__.split('.')[0]
    except Exception as error:
        return default
