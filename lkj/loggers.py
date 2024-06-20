"""Utils for logging."""

def wrapped_print(items, sep=', ', max_width=80, *, print_func=print):
    r"""
    Prints a list of items with a given separator, ensuring the total line width does not exceed max_width.
    
    If adding a new item would exceed this width, it starts a new line.
    
    Args:
        items (list): The list of items to print.
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
    import textwrap

    return print_func(
        textwrap.fill(sep.join(items), width=max_width, subsequent_indent='')
    )

# Example usage
if __name__ == "__main__":
    items = ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9", "item10"]
    sep = ", "
    wrapped_print(items, sep, max_width=30)


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


# --------------------------------------------------------------------------------------
# Error handling


from typing import Callable, Tuple, Any
from functools import wraps
from dataclasses import dataclass
import traceback


@dataclass
class ErrorInfo:
    func: Callable
    error: Exception
    traceback: str
    locals: dict


def _dflt_msg_func(error_info: ErrorInfo) -> str:
    func_name = getattr(error_info.func, '__name__', 'unknown')
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

