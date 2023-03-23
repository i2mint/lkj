"""Lightweight Kit Jumpstart"""


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

