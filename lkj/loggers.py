"""Utils for logging."""

from typing import Callable, Tuple, Any, Optional, Union, Iterable
from functools import partial, wraps
from operator import attrgetter


# TODO: Verify and add test for line_prefix
# TODO: Merge with wrap_text_with_exact_spacing
# TODO: Add doctests for string
def wrapped_print(
    items: Union[str, Iterable],
    sep=", ",
    max_width=80,
    *,
    print_func=print,
    line_prefix: str = "",
):
    r"""
    Prints a string or list ensuring the total line width does not exceed `max_width`.

    If adding a new item would exceed this width, it starts a new line.

    Args:
        items (str or list): String or list of items to print.
        sep (str): The separator to use between items.
        max_width (int): The maximum width of each line. Default is 80.

    Example:

    >>> items = [
    ...     "item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8",
    ...     "item9", "item10"
    ... ]
    >>> sep = ", "
    >>> wrapped_print(items, sep, max_width=30)
    item1, item2, item3, item4,
    item5, item6, item7, item8,
    item9, item10

    >>> items = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    >>> sep = " - "
    >>> wrapped_print(items, sep, max_width=10)
    a - b - c
    - d - e -
    f - g - h
    - i - j

    Note that you have control over the `print_func`.
    This, for example, allows you to just return the string instead of printing it.

    >>> wrapped_print(items, sep, max_width=10, print_func=lambda x: x)
    'a - b - c\n- d - e -\nf - g - h\n- i - j'

    """

    if isinstance(items, str):
        return wrap_text_with_exact_spacing(
            items, max_width=max_width, print_func=print_func, line_prefix=line_prefix
        )
    else:
        import textwrap

        return print_func(
            line_prefix
            + textwrap.fill(
                sep.join(items), width=max_width, subsequent_indent=line_prefix
            )
        )


# TODO: Merge with wrapped_print
def wrap_text_with_exact_spacing(
    text, *, max_width=80, print_func=print, line_prefix: str = ""
):
    """
    Prints a string with word-wrapping to a maximum line length, while preserving all existing newlines
    exactly as they appear.

    Args:
    - text (str): The text to wrap and print.
    - max_width (int): The maximum width of each line (default is 88).
    """
    import textwrap

    # Split the text into lines, preserving the existing newlines
    lines = text.splitlines(keepends=True)

    # Wrap each line individually, preserving existing newlines and only adding new ones for wrapping
    wrapped_lines = [
        (
            textwrap.fill(
                line, width=max_width, replace_whitespace=False, drop_whitespace=False
            )
            if line.strip()
            else line_prefix + line
        )
        for line in lines
    ]

    # Join the wrapped lines back into a single text
    wrapped_text = "".join(wrapped_lines)

    return print_func(wrapped_text)


def print_with_timestamp(msg, *, refresh=None, display_time=True, print_func=print):
    """Prints with a timestamp and optional refresh.

    input: message, and possibly args (to be placed in the message string, sprintf-style

    output: Displays the time (HH:MM:SS), and the message

    use: To be able to track processes (and the time they take)

    """
    from datetime import datetime

    def hms_message(msg=""):
        t = datetime.now()
        return "({:02.0f}){:02.0f}:{:02.0f}:{:02.0f} - {}".format(
            t.day, t.hour, t.minute, t.second, msg
        )

    if display_time:
        msg = hms_message(msg)
    if refresh:
        print_func(msg, end="\r")
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


def _calling_name(func_name: str, args: Tuple, kwargs: dict) -> str:
    return f"Calling {func_name}..."


def _done_calling_name(func_name: str, args: Tuple, kwargs: dict, result: Any) -> str:
    return f".... Done calling {func_name}"


def _always_log(func: Callable, args: Tuple, kwargs: dict) -> bool:
    """Return True no matter what"""
    return True


def log_calls(
    func: Callable = None,
    *,
    logger: Callable[[str], None] = print,
    ingress_msg: Callable[[str, Tuple, dict], str] = _calling_name,
    egress_msg: Callable[[str, Tuple, dict, Any], str] = _done_calling_name,
    func_name: Callable[[Callable], str] = attrgetter("__name__"),
    log_condition: Callable[[Callable, Tuple, dict], bool] = _always_log,
) -> Callable:
    """
    Decorator that adds logging before and after the function's call.

    Args:
        logger (callable): The logger function to use. Default is print.
        ingress_msg (callable): The message to log before calling the function.
            If it returns None, no message is logged.
            Default is "Calling {name}..." where name is the name of the function.
        egress_msg (callable): The message to log after the function call.
            If it returns None, no message is logged.
            Default is ".... Done".
        func_name (callable): The function to use to get the function's name.
        log_condition (callable): The condition for logging.
            Should be a callable that takes a function, args, and kwargs,
            and return a bool. If log_condition returns False, no logging is done.
            Default is _always_log.

    Tips:
        Use `logger=print_with_timestamp` to get timestamps in your logs.
        Use `lambda *args: None` as the ingress_msg or egress_msg to suppress logging.
        Use `logger=lambda x: None` to suppress all logging.

    Returns:
        The decorated function.

    Example:

    >>> @log_calls
    ... def add(a, b):
    ...     return a + b
    ...
    >>> add(2, 3)
    Calling add...
    .... Done calling add
    5

    >>> @log_calls(
    ...     logger=lambda x: print(f"LOG: {x}"),
    ...     ingress_msg=lambda name, *args: f"Start {name}!",
    ...     egress_msg=lambda *args: "End"
    ... )
    ... def multiply(a, b):
    ...     return a * b
    ...
    >>> multiply(2, 3)
    LOG: Start multiply!
    LOG: End
    6

    Sometimes, you want to dynamically control whether to log or not.
    This is what the `log_condition` parameter is for.
    One common use case is to log only if a flag is set in an instance.
    Since this is a common use case, we provide the `log_calls.instance_flag_is_set`
    helper function for this. You can use partial to set the flag attribute:

    >>> import functools
    >>> log_if_verbose_set_to_true = functools.partial(
    ...     log_calls.instance_flag_is_set, flag_attr='verbose'
    ... )

    Now if you have a class with a `verbose` attribute, you can use this helper function
    to log only if `verbose` is set:

    >>> class MyClass:
    ...     def __init__(self, verbose=False):
    ...         self.verbose = verbose
    ...
    ...     @log_calls(log_condition=log_if_verbose_set_to_true)
    ...     def foo(self):
    ...         print("Executing foo")
    ...
    >>> # Example usage
    >>> obj = MyClass(verbose=True)
    >>> obj.foo()  # This will log
    Calling foo...
    Executing foo
    .... Done calling foo

    But if verbose is set to `False`, no logging will be done:
    >>> obj = MyClass(verbose=False)
    >>> obj.foo()  # This will not log
    Executing foo

    """
    if func is None:
        return partial(
            log_calls,
            logger=logger,
            ingress_msg=ingress_msg,
            egress_msg=egress_msg,
            func_name=func_name,
            log_condition=log_condition,
        )

    @wraps(func)
    def wrapper(*args, **kwargs):
        if log_condition(func, args, kwargs):
            if ingress_msg:
                logger(ingress_msg(func_name(func), args, kwargs))
            result = func(*args, **kwargs)
            if egress_msg:
                logger(egress_msg(func_name(func), args, kwargs, result))
            return result
        else:
            return func(*args, **kwargs)

    return wrapper


def instance_flag_is_set(func, args, kwargs, flag_attr: str = "verbose"):
    """Check if the log flag is set to True in the instance."""
    # get the first argument if any, assuming it's the instance
    if flag_attr:
        instance = next(iter(args), None)
        if instance:  # assume it's the instance
            if getattr(instance, flag_attr, False):
                return True
    return False


log_calls.instance_flag_is_set = instance_flag_is_set

# if func is None:
#     return partial(
#         log_calls,
#         logger=logger,
#         ingress_msg=ingress_msg,
#         egress_msg=egress_msg,
#         func_name=func_name,
#     )
# else:

#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         _func_name = func_name(func)
#         if (_in_msg := ingress_msg(_func_name, args, kwargs)) is not None:
#             logger(_in_msg)
#         result = func(*args, **kwargs)
#         if (_out_msg := egress_msg(_func_name, args, kwargs, result)) is not None:
#             logger(_out_msg)
#         return result

#     return wrapper


# --------------------------------------------------------------------------------------
# Error handling


from typing import Callable, Tuple, Any
from dataclasses import dataclass
import traceback
from typing import Callable, Any, Tuple
from functools import partial, wraps
from operator import attrgetter


@dataclass
class ErrorInfo:
    func: Callable
    error: Exception
    traceback: str
    locals: dict


def _dflt_msg_func(error_info: ErrorInfo) -> str:
    func_name = getattr(error_info.func, "__name__", "unknown")
    error_obj = error_info.error
    return f"Exiting from {func_name} with error: {error_obj}"


def dflt_error_info_processor(
    error_info: ErrorInfo,
    *,
    log_func=print,
    msg_func: Callable[[ErrorInfo], str] = _dflt_msg_func,
):
    return log_func(msg_func(error_info))


def return_error_info_on_error(
    func,
    *,
    caught_error_types: Tuple[Exception] = (Exception,),
    error_info_processor: Callable[[ErrorInfo], Any] = dflt_error_info_processor,
):
    """Decorator that returns traceback and local variables on error.

    This decorator is useful for debugging. It will catch any exceptions that occur
    in the decorated function, and return an ErrorInfo object with the traceback and
    local variables at the time of the error.

    :param func: The function to decorate.
    :param caught_error_types: The types of errors to catch.
    :param error_info_processor: A function that processes the ErrorInfo object.

    Tip: To parametrize this decorator, you can use a functools.partial function.

    Tip: You can have your error_info_processor persist the error info to a file or
    database, or send it to a logging service.

    >>> @return_error_info_on_error
    ... def foo(x, y=2):
    ...     return x / y
    ...
    >>> t = foo(1, 2)
    >>> assert t == 0.5
    >>> t = foo(1, y=0)
    Exiting from foo with error: division by zero
    >>> if isinstance(t, ErrorInfo):
    ...     assert isinstance(t.error, ZeroDivisionError)
    ...     hasattr(t, 'traceback')
    ...     assert t.locals['args'] == (1,)
    ...     assert t.locals['kwargs'] == {'y': 0}

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except caught_error_types as error_obj:
            error_info = ErrorInfo(func, error_obj, traceback.format_exc(), locals())
            return error_info_processor(error_info)

    return wrapper


from contextlib import suppress


class CallOnError(suppress):
    """
    An extension of the suppress context manager that enables the user to issue a warning
    message when an import error occurs.

    >>> warn_about_import_errors = CallOnError(ImportError, on_error=lambda err: print(f"Warning: {err}"))
    >>> with warn_about_import_errors:
    ...     import this_package_surely_does_not_exist
    Warning: No module named 'this_package_surely_does_not_exist'
    >>> with warn_about_import_errors:
    ...     from os.this_module_does_not_exist import this_function_does_not_exist
    Warning: No module named 'os.this_module_does_not_exist'; 'os' is not a package
    """

    def __init__(
        self,
        *exceptions,
        on_error: Callable = print,
    ):
        self.on_error = on_error
        super().__init__(*exceptions)

    def __exit__(self, exctype, excinst, exctb):
        if exctype is not None:
            self.on_error(excinst)
        return super().__exit__(exctype, excinst, exctb)
