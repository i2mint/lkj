"""
Lightweight Kit Jumpstart
"""

from lkj.filesys import get_app_data_dir, get_watermarked_dir
from lkj.strings import regex_based_substitution


def chunker(a, chk_size, *, return_tail=True):
    """Chunks an iterable into non-overlapping chunks of size chk_size.

    >>> list(chunks(range(8), 3))
    [[0, 1, 2], [3, 4, 5], [6, 7]]
    >>> list(chunks(range(8), 3, return_tail=False))
    [[0, 1, 2], [3, 4, 5]]
    """
    from itertools import zip_longest

    it = iter(a)
    if return_tail:
        sentinel = object()
        for chunk in zip_longest(*([it] * chk_size), fillvalue=sentinel):
            yield [item for item in chunk if item is not sentinel]
    else:
        yield from zip(*([it] * chk_size))


def import_object(dot_path: str):
    """Imports and returns an object from a dot string path.

    >>> f = import_object('os.path.join')
    >>> from os.path import join
    >>> f is join
    True

    """
    from importlib import import_module

    module_path, _, object_name = dot_path.rpartition('.')
    if not module_path:
        raise ImportError(f'{dot_path} does not contain a module path')
    module = import_module(module_path)
    try:
        return getattr(module, object_name)
    except AttributeError:
        raise ImportError(f'{object_name} is not found in {module_path}')


def user_machine_id():
    """Get an ID for the current computer/user that calls this function."""
    return __import__('platform').node()


def print_with_timestamp(msg, *, refresh=None, display_time=True, print_func=print):
    """Prints with a timestamp and optional refresh.

    input: message, and possibly args (to be placed in the message string, sprintf-style

    output: Displays the time (HH:MM:SS), and the message

    use: To be able to track processes (and the time they take)

    """
    from datetime import datetime

    def hms_message(msg=''):
        t = datetime.now()
        return '({:02.0f}){:02.0f}:{:02.0f}:{:02.0f} - {}'.format(
            t.day, t.hour, t.minute, t.second, msg
        )

    if display_time:
        msg = hms_message(msg)
    if refresh:
        print_func(msg, end='\r')
    else:
        print_func(msg)


print_progress = print_with_timestamp  # alias often used


def clog(condition, *args, log_func=print, **kwargs):
    """Conditional log

    >>> clog(False, "logging this")
    >>> clog(True, "logging this")
    logging this

    One common usage is when there's a verbose flag that allows the user to specify
    whether they want to log or not. Instead of having to litter your code with
    `if verbose:` statements you can just do this:

    >>> verbose = True  # say versbose is True
    >>> _clog = clog(verbose)  # makes a clog with a fixed condition
    >>> _clog("logging this")
    logging this

    You can also choose a different log function.
    Usually you'd want to use a logger object from the logging module,
    but for this example we'll just use `print` with some modification:

    >>> _clog = clog(verbose, log_func=lambda x: print(f"hello {x}"))
    >>> _clog("logging this")
    hello logging this

    """
    if not args and not kwargs:
        import functools

        return functools.partial(clog, condition, log_func=log_func)
    if condition:
        return log_func(*args, **kwargs)


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
