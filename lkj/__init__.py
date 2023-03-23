"""
Lightweight Kit Jumpstart
"""


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


def get_app_data_folder():
    """
    Returns the full path of a directory suitable for storing application-specific data.

    On Windows, this is typically %APPDATA%.
    On macOS, this is typically ~/.config.
    On Linux, this is typically ~/.config.

    Returns:
        str: The full path of the app data folder.

    See https://github.com/i2mint/i2mint/issues/1.

    >>> import os
    >>> app_data_folder = get_app_data_folder()
    >>> if os.name == 'nt': # Windows
    ...     assert app_data_folder == os.getenv('APPDATA')
    ... else: # macOS or linux/unix
    ...     assert app_data_folder == os.path.expanduser('~/.config')

    """
    import os

    if os.name == "nt":
        # Windows
        app_data_folder = os.getenv("APPDATA")
    elif os.name == "darwin":
        # macOS
        app_data_folder = os.path.expanduser("~/.config")
    else:
        # Linux/Unix
        app_data_folder = os.path.expanduser("~/.config")

    return app_data_folder
