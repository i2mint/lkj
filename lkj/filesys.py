"""File system utils"""

import os
from typing import Callable, Any
from pathlib import Path
from functools import wraps, partial


# TODO: General pattern Consider generalizing to different conditions and actions
def enable_sourcing_from_file(func=None, *, write_output=False):
    """
    Decorator for functions enables the decorated function to source from a file.

    It is to be applied to functions that take a string or bytes as their first
    argument. Decorating the function will enable it to detect if the first argument
    is a file path, read the file content, call the function with the file content
    as the first argument. Optionally, the decorated function can write the result
    back to the file, or another file if specified.

    Args:
        write_output (bool or str): If True, write the output back to the file. If a
            string, write the output to the specified file path. Default is False.


    """
    if func is None:
        return partial(enable_sourcing_from_file, write_output=write_output)

    @wraps(func)
    def wrapper(*args, write_output=write_output, **kwargs):
        # Check if the first argument is a string and a valid file path
        if args and isinstance(args[0], str) and os.path.isfile(args[0]):
            file_path = args[0]
            # Read the file content
            with open(file_path, "r") as file:
                file_content = file.read()
            # Call the function with the file content and other arguments
            new_args = (file_content,) + args[1:]
            result = func(*new_args, **kwargs)

            if write_output:
                if write_output is True:
                    write_output = file_path
                else:
                    assert isinstance(
                        write_output, str
                    ), "write_output must be a string"
                # Write the result back to the file
                with open(write_output, "w") as file:
                    file.write(result)
            return result
        else:
            # If the first argument is not a file path, call the function as usual
            return func(*args, **kwargs)

    return wrapper


def do_nothing(*args, **kwargs) -> None:
    """Function that does nothing."""
    pass


def _app_data_rootdir():
    """
    Returns the full path of a directory suitable for storing application-specific data.

    On Windows, this is typically %APPDATA%.
    On macOS, this is typically ~/.config.
    On Linux, this is typically ~/.config.

    Returns:
        str: The full path of the app data folder.

    See https://github.com/i2mint/i2mint/issues/1.
    """
    if os.name == "nt":
        # Windows
        APP_DATA_ROOTDIR = os.getenv("APPDATA")
        if not APP_DATA_ROOTDIR:
            raise RuntimeError("APPDATA environment variable is not set")
    else:
        # macOS and Linux/Unix
        APP_DATA_ROOTDIR = os.path.expanduser("~/.config")

    if not os.path.isdir(APP_DATA_ROOTDIR):
        os.mkdir(APP_DATA_ROOTDIR)

    # Note: Joining to '' to be consistent with get_app_data_dir()
    return os.path.join(APP_DATA_ROOTDIR, "")


APP_DATA_ROOTDIR = _app_data_rootdir()


def get_app_data_dir(
    dirname="",
    *,
    if_exists: Callable[[str], Any] = do_nothing,
    if_does_not_exist: Callable[[str], Any] = os.mkdir,
    rootdir: str = APP_DATA_ROOTDIR,
):
    """
    Returns the full path of a directory suitable for storing application-specific data.

    It's a mini-framework for creating a directories: It allows us to specify what to do
    if the directory already exists, and what to do if it doesn't exist.

    Typical use case: We want to create a directory for storing application-specific
    data, but we don't want to write in a directory whose name is already taken if
    it's not "our" directory. To achieve this, we can specify ``if_exists`` to be a
    function that verifies, through some condition on the content (example, watermark
    or subdirectory structure), that the directory was indeed create by our
    application, and ``if_does_not_exist``to be a function that creates the directory
    and populates it with a watermark or otherwise recognizable content.

    :param dirname: The name of the directory to create.
    :param if_exists: A function to call if the directory already exists.
        By default, it does nothing. The main non-default use case is to validate the
        contents of the directory, and/or populate it.
        If you write a custome ``if_exists`` function, it is your responsibility to
        return the full path of the directory (unless your use case doesn't actually
        need that!)
    :param if_does_not_exist: A function to call if the directory does not exist.
        By default, it creates the directory with ``os.mkdir``. If you need to also
        create subdirectories, you can use ``os.makedirs``. You can also choose to
        raise an error, telling the user to create the directory manually.
    :param rootdir:
    :return:

    If you specify nothing else, you'll just get the system-dependent root directory for
    storing application-specific data:

    >>> app_data_dir = get_app_data_dir()
    >>> app_data_dir == APP_DATA_ROOTDIR
    True

    You can control what happens if the directory already exists, or if it doesn't.
    The callbacks take the full path of the directory as an argument, and usually return
    the path after doing something with it.

    >>> import os
    >>> def notify_user_that_path_does_not_exist(path):
    ...     print(f"The '{os.path.basename(path)}' subdirectory doesn't exist")
    ...     return path
    >>> dirpath = get_app_data_dir(
    ...     'nonexistent_dir',
    ...     if_does_not_exist=notify_user_that_path_does_not_exist
    ... )
    The 'nonexistent_dir' subdirectory doesn't exist

    For an example of how to use this function as a framework to make custom directory
    factories, see :func:`get_watermarked_dir`.

    """
    dirpath = os.path.join(rootdir, dirname)
    if os.path.isdir(dirpath):
        if if_exists is not None:
            if_exists(dirpath)
    else:
        if if_does_not_exist is not None:
            if_does_not_exist(dirpath)
    return dirpath


DFLT_WATERMARK = ".lkj"


def watermark_dir(dirpath: str, watermark: str = DFLT_WATERMARK):
    """Watermark."""
    (Path(dirpath) / watermark).touch()


def has_watermark(dirpath: str, watermark: str = DFLT_WATERMARK):
    """Check if a directory has a watermark."""
    return (Path(dirpath) / watermark).exists()


def _raise_watermark_error(dirpath, watermark):
    raise ValueError(
        f"Directory {dirpath} is not watermarked with {watermark}. "
        f"Perhaps you deleted the watermark file? If so, create the file and all will "
        f"be good. For example, you could do:\n"
        f"    import pathlib; (pathlib.Path('{dirpath}') / '{watermark}').touch()"
    )


def get_watermarked_dir(
    dirname: str,
    watermark: str = DFLT_WATERMARK,
    *,
    if_watermark_validation_fails: Callable[[str, str], Any] = _raise_watermark_error,
    make_dir: Callable[[str], Any] = os.mkdir,
    rootdir: str = APP_DATA_ROOTDIR,
):
    """Get a watermarked directory.

    >>> from functools import partial
    >>> import tempfile, os, shutil
    >>> testdir = os.path.join(tempfile.gettempdir(), 'watermark_testdir')
    >>> shutil.rmtree(testdir, ignore_errors=True)  # delete
    >>> os.makedirs(testdir, exist_ok=True)  # and recreate afresh
    >>> # Make a
    >>> f = partial(get_watermarked_dir, rootdir=testdir)
    >>> mytestdir = f('mytestdir', '.my_watermark')
    >>> os.listdir(testdir)
    ['mytestdir']
    >>> os.listdir(mytestdir)
    ['.my_watermark']
    >>> another_testdir = f('another_testdir')
    >>> os.listdir(another_testdir)
    ['.lkj']

    """

    def create_and_watermark(dirpath):
        make_dir(dirpath)
        watermark_dir(dirpath, watermark=watermark)

    def validate_watermark(dirpath):
        if not has_watermark(dirpath, watermark):
            return if_watermark_validation_fails(dirpath, watermark)

    return get_app_data_dir(
        dirname,
        if_exists=validate_watermark,
        if_does_not_exist=create_and_watermark,
        rootdir=rootdir,
    )


Filepath = str


def rename_file(
    file: Filepath,
    renamer_function: Callable[[str], str],
    *,
    dry_run: bool = True,
    verbose: bool = True,
):
    """
    This function takes a list of files and renames them using the provided renamer function.
    """
    if not isinstance(file, str):
        files = file
        for file in files:
            rename_file(file, renamer_function, dry_run=dry_run, verbose=verbose)

    new_name = renamer_function(file)
    if verbose:
        print(f"Renaming {file} to {new_name}")
    if not dry_run:
        os.rename(file, new_name)
